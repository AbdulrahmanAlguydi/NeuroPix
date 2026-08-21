import os
from flask import Flask, request
from dotenv import load_dotenv

from database.queries import register_user
from utils.security import hash_password

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route("/health")
def health_check():
    return {"status": "ok"}


@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    password_hash = hash_password(password)
    register_user(username, password_hash)

    return {"message": "User registered successfully"}, 201


if __name__ == "__main__":
    app.run(debug=True)
