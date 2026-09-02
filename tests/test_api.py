import io
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from PIL import Image

# Add project root folder to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import app
from utils.security import hash_password, verify_password


@pytest.fixture
def client():
    """
    Creates a Flask test client for testing API routes.
    """
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "student_test_secret_key"
    with app.test_client() as client:
        yield client


def make_test_image(width, height, image_format="JPEG"):
    """
    Helper function to generate image bytes in memory for upload testing.
    """
    img = Image.new("RGB", (width, height), color="blue")
    image_bytes = io.BytesIO()
    img.save(image_bytes, format=image_format)
    image_bytes.seek(0)
    return image_bytes


# =====================================================================
# 1. SERVER STARTUP & HEALTH CHECK TEST
# =====================================================================
def test_server_health(client):
    """Test that the server starts up and responds to /health."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


# =====================================================================
# 2. USER REGISTRATION TESTS
# =====================================================================
@patch("app.get_user_by_username", return_value=None)
@patch("app.register_user", return_value=True)
def test_user_registration_success(mock_register, mock_get_user, client):
    """Test registering a new user with valid username and password."""
    user_data = {"username": "student_user", "password": "password123"}
    response = client.post("/api/auth/register", json=user_data)

    assert response.status_code == 201
    assert response.get_json() == {"message": "User registered successfully"}

    # Verify password was hashed before saving to database (not plain text)
    args, _ = mock_register.call_args
    registered_username, hashed_pass = args
    assert registered_username == "student_user"
    assert hashed_pass != "password123"
    assert verify_password("password123", hashed_pass) is True


def test_user_registration_missing_fields(client):
    """Test registration when username or password is missing."""
    response = client.post("/api/auth/register", json={"username": "only_name"})
    assert response.status_code == 400

    response = client.post("/api/auth/register", json={})
    assert response.status_code == 400


def test_user_registration_short_password(client):
    """Test registration with a short password (< 8 chars)."""
    response = client.post(
        "/api/auth/register", json={"username": "student1", "password": "123"}
    )
    assert response.status_code == 400
    assert "at least 8 characters" in response.get_json()["error"]


@patch(
    "app.get_user_by_username",
    return_value={"UserID": 1, "Username": "existing_student"},
)
def test_user_registration_duplicate_username(mock_get_user, client):
    """Test registration fails if username already exists."""
    user_data = {"username": "existing_student", "password": "password123"}
    response = client.post("/api/auth/register", json=user_data)

    assert response.status_code == 409
    assert "already taken" in response.get_json()["error"]


# =====================================================================
# 3. USER LOGIN TESTS
# =====================================================================
@patch("app.get_user_by_username")
def test_user_login_success(mock_get_user, client):
    """Test login with correct username and password."""
    valid_hash = hash_password("student_pass")
    mock_get_user.return_value = {
        "UserID": 10,
        "Username": "student10",
        "PasswordHash": valid_hash,
    }

    login_payload = {"username": "student10", "password": "student_pass"}
    response = client.post("/api/auth/login", json=login_payload)

    assert response.status_code == 200
    assert response.get_json() == {"message": "Login successful"}

    # Verify user session was saved
    with client.session_transaction() as session_data:
        assert session_data["user_id"] == 10
        assert session_data["username"] == "student10"


@patch("app.get_user_by_username")
def test_user_login_wrong_password(mock_get_user, client):
    """Test login with an incorrect password."""
    valid_hash = hash_password("correct_pass")
    mock_get_user.return_value = {
        "UserID": 10,
        "Username": "student10",
        "PasswordHash": valid_hash,
    }

    response = client.post(
        "/api/auth/login",
        json={"username": "student10", "password": "wrong_pass"},
    )
    assert response.status_code == 401
    assert "Invalid username or password" in response.get_json()["error"]


@patch("app.get_user_by_username", return_value=None)
def test_user_login_nonexistent_user(mock_get_user, client):
    """Test login with a username that does not exist."""
    response = client.post(
        "/api/auth/login",
        json={"username": "unknown_user", "password": "password123"},
    )
    assert response.status_code == 401


def test_user_login_missing_fields(client):
    """Test login with missing input fields."""
    response = client.post("/api/auth/login", json={})
    assert response.status_code == 400


# =====================================================================
# 4. AUTHENTICATION & PROTECTED ROUTE TESTS
# =====================================================================
def test_get_auth_me_logged_in(client):
    """Test /api/auth/me returns user info when logged in."""
    with client.session_transaction() as session_data:
        session_data["user_id"] = 12
        session_data["username"] = "logged_in_student"

    response = client.get("/api/auth/me")
    assert response.status_code == 200
    assert response.get_json() == {
        "user_id": 12,
        "username": "logged_in_student",
    }


def test_get_auth_me_logged_out(client):
    """Test /api/auth/me returns 401 Unauthorized when logged out."""
    response = client.get("/api/auth/me")
    assert response.status_code == 401


# =====================================================================
# 5. LOGOUT TESTS
# =====================================================================
def test_user_logout(client):
    """Test logging out clears the user session."""
    with client.session_transaction() as session_data:
        session_data["user_id"] = 99
        session_data["username"] = "temp_student"

    logout_resp = client.post("/api/auth/logout")
    assert logout_resp.status_code == 200

    # Protected route should now be rejected
    me_resp = client.get("/api/auth/me")
    assert me_resp.status_code == 401


# =====================================================================
# 6. IMAGE UPLOAD TESTS
# =====================================================================
@pytest.fixture
def logged_in_client(client):
    """A test client with a fake logged-in user, since /api/upload now requires login."""
    with client.session_transaction() as session_data:
        session_data["user_id"] = 1
        session_data["username"] = "student_uploader"
    return client


# Fake return value standing in for a real S3 + database save during tests.
FAKE_SAVED_IMAGE = {
    "OriginalFilePath": "inputs/fake_test_image.jpg",
    "ModifiedFilePath": None,
    "EditType": None,
}


@patch("app.save_image_transaction", return_value=FAKE_SAVED_IMAGE)
def test_image_upload_valid_jpg(mock_save, logged_in_client):
    """Test uploading a valid JPG image."""
    img_data = make_test_image(800, 600, "JPEG")
    response = logged_in_client.post(
        "/api/upload",
        content_type="multipart/form-data",
        data={"image": (img_data, "test.jpg")},
    )
    assert response.status_code == 200
    assert response.get_json() == {"message": "Image uploaded successfully"}


@patch("app.save_image_transaction", return_value=FAKE_SAVED_IMAGE)
def test_image_upload_valid_png(mock_save, logged_in_client):
    """Test uploading a valid PNG image."""
    img_data = make_test_image(1000, 1000, "PNG")
    response = logged_in_client.post(
        "/api/upload",
        content_type="multipart/form-data",
        data={"image": (img_data, "test.png")},
    )
    assert response.status_code == 200


def test_image_upload_unsupported_format(logged_in_client):
    """Test rejecting unsupported file extensions like .txt or .gif."""
    file_bytes = io.BytesIO(b"not an image")
    response = logged_in_client.post(
        "/api/upload",
        content_type="multipart/form-data",
        data={"image": (file_bytes, "notes.txt")},
    )
    assert response.status_code == 400
    assert "Unsupported file format" in response.get_json()["error"]


def test_image_upload_missing_file(logged_in_client):
    """Test upload endpoint with no file attached."""
    response = logged_in_client.post("/api/upload", content_type="multipart/form-data")
    assert response.status_code == 400


def test_image_upload_requires_login(client):
    """Test that uploading without being logged in is rejected."""
    img_data = make_test_image(800, 600, "JPEG")
    response = client.post(
        "/api/upload",
        content_type="multipart/form-data",
        data={"image": (img_data, "test.jpg")},
    )
    assert response.status_code == 401


@patch("app.save_image_transaction", return_value=FAKE_SAVED_IMAGE)
def test_image_upload_resolution_validation(mock_save, logged_in_client):
    """Test 1080p resolution limits for landscape and portrait images."""
    # Landscape 1920x1080 -> Allowed
    ok_landscape = make_test_image(1920, 1080, "JPEG")
    r1 = logged_in_client.post(
        "/api/upload",
        content_type="multipart/form-data",
        data={"image": (ok_landscape, "ls_ok.jpg")},
    )
    assert r1.status_code == 200

    # Landscape 1921x1080 -> Rejected
    bad_landscape = make_test_image(1921, 1080, "JPEG")
    r2 = logged_in_client.post(
        "/api/upload",
        content_type="multipart/form-data",
        data={"image": (bad_landscape, "ls_bad.jpg")},
    )
    assert r2.status_code == 400

    # Portrait 1080x1920 -> Allowed
    ok_portrait = make_test_image(1080, 1920, "JPEG")
    r3 = logged_in_client.post(
        "/api/upload",
        content_type="multipart/form-data",
        data={"image": (ok_portrait, "pt_ok.jpg")},
    )
    assert r3.status_code == 200

    # Portrait 1080x1921 -> Rejected
    bad_portrait = make_test_image(1080, 1921, "JPEG")
    r4 = logged_in_client.post(
        "/api/upload",
        content_type="multipart/form-data",
        data={"image": (bad_portrait, "pt_bad.jpg")},
    )
    assert r4.status_code == 400


# =====================================================================
# 7. DATABASE AND S3 SERVICE MOCKS
# =====================================================================
@patch("services.image_service.upload_original_image", return_value="inputs/raw123.jpg")
@patch("services.image_service.upload_processed_image", return_value="outputs/edit123.jpg")
@patch("services.image_service.log_image_edit", return_value=True)
def test_image_service_pipeline_mock(mock_log, mock_up_proc, mock_up_raw):
    """Test image storage service coordinates S3 and DB safely."""
    from services.image_service import save_image_transaction

    result = save_image_transaction(
        user_id=5,
        local_raw_path="/tmp/raw.jpg",
        local_edited_path="/tmp/edit.jpg",
        edit_type="ai",
    )

    assert result == {
        "OriginalFilePath": "inputs/raw123.jpg",
        "ModifiedFilePath": "outputs/edit123.jpg",
        "EditType": "ai",
    }
    mock_up_raw.assert_called_once_with("/tmp/raw.jpg")
    mock_up_proc.assert_called_once_with("/tmp/edit.jpg")
    mock_log.assert_called_once_with(
        user_id=5,
        original_path="inputs/raw123.jpg",
        modified_path="outputs/edit123.jpg",
        edit_type="ai",
    )


if __name__ == "__main__":
    pytest.main(["-v", __file__])
