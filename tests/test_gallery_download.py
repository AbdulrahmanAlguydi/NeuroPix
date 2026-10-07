"""Basic checks for downloading saved gallery images."""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import app


@pytest.fixture
def client():
    """Create a test client with a logged-in user."""
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "student_test_secret_key"
    with app.test_client() as client:
        with client.session_transaction() as session:
            session["user_id"] = 1
        yield client


def test_download_original(client, tmp_path):
    """The original version downloads with its original filename."""
    image_path = tmp_path / "city.jpg"
    image_path.write_bytes(b"original image")
    saved_image = {
        "path": str(image_path),
        "file_name": "city.jpg",
        "source_key": "inputs/city.jpg",
    }

    with patch("app.stage_gallery_image", return_value=saved_image):
        response = client.get("/api/gallery/42/download?source=original")

    assert response.status_code == 200
    assert response.data == b"original image"
    assert response.headers["Content-Disposition"] == "attachment; filename=city.jpg"


def test_download_edited(client, tmp_path):
    """The edited version downloads with an edited filename."""
    image_path = tmp_path / "result.png"
    image_path.write_bytes(b"edited image")
    saved_image = {
        "path": str(image_path),
        "file_name": "city.jpg",
        "source_key": "outputs/result.png",
    }

    with patch("app.stage_gallery_image", return_value=saved_image):
        response = client.get("/api/gallery/42/download?source=edited")

    assert response.status_code == 200
    assert response.data == b"edited image"
    assert response.headers["Content-Disposition"] == "attachment; filename=city-edited.png"
