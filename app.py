import os
from flask import Flask, request
from dotenv import load_dotenv

from database.queries import register_user, get_user_by_username
from utils.security import hash_password

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


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


if __name__ == "__main__":
    app.run(debug=True)
