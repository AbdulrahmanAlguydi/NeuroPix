import os
import tempfile
import uuid
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, request, send_file, session
from PIL import Image

from database.queries import get_user_by_username, register_user
from services.ai_editor import apply_ai_edits
from services.image_editor import apply_standard_edits
from services.image_service import (
    delete_image_transaction,
    fetch_formatted_user_gallery,
    save_image_transaction,
)
from utils.s3 import get_full_s3_url
from utils.security import hash_password, verify_password

load_dotenv()

# static_folder points Flask at our frontend folder so it can serve the
# HTML/CSS/JS files, and static_url_path="" means we don't need "/static"
# in front of every file (so "login.html" works instead of "/static/login.html").
app = Flask(__name__, static_folder="frontend", static_url_path="")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "neuropix_secret_key_123")

# Folder used to hold uploaded images temporarily, before any edit
# decides whether they need to be saved permanently to S3/MySQL.
UPLOAD_TEMP_DIR = os.path.join(tempfile.gettempdir(), "neuropix_uploads")
os.makedirs(UPLOAD_TEMP_DIR, exist_ok=True)

ALLOWED_UPLOAD_EXTENSIONS = {".jpg", ".jpeg", ".png"}

# The 1080p limit is orientation-aware: a landscape image may be as wide
# as 1920x1080, while a portrait image may be as tall as 1080x1920.
MAX_LANDSCAPE_SIZE = (1920, 1080)
MAX_PORTRAIT_SIZE = (1080, 1920)


def login_required(f):
    """
    Route decorator that blocks access unless the current session
    belongs to a logged-in user.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return {"error": "Authentication required"}, 401
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def home():
    # Show the landing page when someone visits the site.
    return app.send_static_file("index.html")


@app.route("/health")
def health_check():
    return {"status": "ok"}


@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "Username and password are required"}, 400

    if not isinstance(password, str) or len(password) < 8:
        return {"error": "Password must be at least 8 characters long"}, 400

    if get_user_by_username(username):
        return {"error": "Username is already taken"}, 409

    password_hash = hash_password(password)
    was_saved = register_user(username, password_hash)

    if not was_saved:
        return {"error": "Could not save the new account. Please try again."}, 500

    return {"message": "User registered successfully"}, 201


@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "Username and password are required"}, 400

    user = get_user_by_username(username)

    if user and verify_password(password, user["PasswordHash"]):
        session["user_id"] = user["UserID"]
        session["username"] = user["Username"]
        return {"message": "Login successful"}, 200

    # Same generic message whether the username doesn't exist or the
    # password is wrong, so we never reveal which usernames are registered.
    return {"error": "Invalid username or password"}, 401


@app.route("/api/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return {"message": "Logged out successfully"}, 200


@app.route("/api/auth/me")
@login_required
def me():
    return {"user_id": session["user_id"], "username": session["username"]}, 200


@app.route("/api/gallery", methods=["GET"])
@login_required
def gallery():
    images = fetch_formatted_user_gallery(session["user_id"])
    return images, 200


@app.route("/api/gallery/<int:image_id>", methods=["DELETE"])
@login_required
def delete_gallery_image(image_id):
    was_deleted = delete_image_transaction(image_id, session["user_id"])

    if not was_deleted:
        return {"error": "Image could not be found or deleted"}, 404

    return {"message": "Image deleted successfully"}, 200


@app.route("/api/upload", methods=["POST"])
@login_required
def upload():
    if "image" not in request.files:
        return {"error": "No image file provided"}, 400

    file = request.files["image"]
    if not file or not file.filename:
        return {"error": "No image file provided"}, 400

    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_UPLOAD_EXTENSIONS:
        return {
            "error": "Unsupported file format. Only JPG and PNG images are allowed."
        }, 400

    try:
        width, height = Image.open(file.stream).size
    except Exception:
        return {"error": "Invalid or corrupted image file."}, 400

    max_width, max_height = MAX_LANDSCAPE_SIZE if width >= height else MAX_PORTRAIT_SIZE
    if width > max_width or height > max_height:
        return {
            "error": "Image resolution exceeds the 1080p limit (1920x1080 landscape or 1080x1920 portrait)."
        }, 400
    file.seek(0)  # Image.open advanced the stream; rewind before saving the full file

    temp_filename = f"{uuid.uuid4().hex}_{file.filename}"
    temp_path = os.path.join(UPLOAD_TEMP_DIR, temp_filename)
    file.save(temp_path)

    # Just stage the file locally for now. It only gets uploaded to S3 and
    # logged in the database once it has actually been processed, in
    # /api/process, since one Images row is meant to hold the original AND
    # the processed result together.
    session["uploaded_image_path"] = temp_path
    session.pop("processed_image_path", None)
    session.pop("processed_edit_mode", None)

    return {"message": "Image uploaded successfully"}, 200


@app.route("/api/process", methods=["POST"])
@login_required
def process_image():
    raw_image_path = session.get("uploaded_image_path")
    if not raw_image_path or not os.path.exists(raw_image_path):
        return {"error": "No image has been uploaded yet."}, 400

    data = request.get_json(silent=True) or {}
    edit_mode = data.get("editMode", "standard")

    if edit_mode not in {"standard", "ai"}:
        return {"error": "Unknown editing mode"}, 400

    settings = data.get("settings", {})

    try:
        if edit_mode == "standard":
            original_image = Image.open(raw_image_path)
            edited_image = apply_standard_edits(original_image, settings)
            processed_filename = f"{uuid.uuid4().hex}_processed.jpg"
            processed_path = os.path.join(UPLOAD_TEMP_DIR, processed_filename)
            edited_image.save(processed_path, "JPEG")
        else:
            edited_bytes = apply_ai_edits(raw_image_path, settings)
            processed_filename = f"{uuid.uuid4().hex}_processed.png"
            processed_path = os.path.join(UPLOAD_TEMP_DIR, processed_filename)
            with open(processed_path, "wb") as processed_file:
                processed_file.write(edited_bytes)
    except Exception:
        return {"error": "Could not process this image."}, 400

    # Upload both the original and the processed image to S3, and log
    # the edit as one row in the database.
    saved_record = save_image_transaction(
        user_id=session["user_id"],
        local_raw_path=raw_image_path,
        local_edited_path=processed_path,
        edit_type=edit_mode,
    )

    if not saved_record:
        return {"error": "Could not save the processed image. Please try again."}, 500

    session["processed_image_path"] = processed_path
    session["processed_edit_mode"] = edit_mode

    # Turn the S3 keys into full URLs the frontend can put in an <img> tag.
    result = {
        "originalUrl": get_full_s3_url(saved_record["OriginalFilePath"]),
        "processedUrl": get_full_s3_url(saved_record["ModifiedFilePath"]),
        "editType": saved_record["EditType"],
    }

    return {"message": "Image processed successfully", "result": result}, 200


@app.route("/api/download")
@login_required
def download_processed_image():
    processed_path = session.get("processed_image_path")

    if not processed_path or not os.path.exists(processed_path):
        return {"error": "No processed image is available."}, 404

    extension = "png" if session.get("processed_edit_mode") == "ai" else "jpg"

    return send_file(
        processed_path,
        as_attachment=True,
        download_name=f"neuropix-processed.{extension}",
    )


if __name__ == "__main__":
    app.run(debug=True)
