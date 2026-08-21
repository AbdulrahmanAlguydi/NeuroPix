import os
import uuid
import tempfile
from functools import wraps
from flask import Flask, request, session
from dotenv import load_dotenv

from database.queries import register_user, get_user_by_username
from utils.security import hash_password, verify_password

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Folder used to hold uploaded images temporarily, before any edit
# decides whether they need to be saved permanently to S3/MySQL.
UPLOAD_TEMP_DIR = os.path.join(tempfile.gettempdir(), "neuropix_uploads")
os.makedirs(UPLOAD_TEMP_DIR, exist_ok=True)

ALLOWED_UPLOAD_EXTENSIONS = {".jpg", ".jpeg", ".png"}


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

    if len(password) < 8:
        return {"error": "Password must be at least 8 characters long"}, 400

    if get_user_by_username(username):
        return {"error": "Username is already taken"}, 409

    password_hash = hash_password(password)
    register_user(username, password_hash)

    return {"message": "User registered successfully"}, 201


@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

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


@app.route("/api/upload", methods=["POST"])
def upload():
    file = request.files["image"]

    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_UPLOAD_EXTENSIONS:
        return {"error": "Unsupported file format. Only JPG and PNG images are allowed."}, 400

    temp_filename = f"{uuid.uuid4().hex}_{file.filename}"
    temp_path = os.path.join(UPLOAD_TEMP_DIR, temp_filename)
    file.save(temp_path)

    session["uploaded_image_path"] = temp_path

    return {"message": "Image uploaded successfully"}, 200


if __name__ == "__main__":
    app.run(debug=True)
