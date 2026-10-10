"""Basic checks for the server-rendered gallery."""

import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import app


def test_gallery_renders_saved_image():
    image = {
        "image_id": 42,
        "file_name": "city.png",
        "edit_type": "ai",
        "upload_date": datetime(2026, 9, 18),
        "original_url": "/original.png",
        "modified_url": "/edited.png",
    }
    with app.test_client() as client:
        with client.session_transaction() as session:
            session["user_id"] = 1
        with patch("app.fetch_formatted_user_gallery", return_value=[image]):
            response = client.get("/gallery.html")

    assert response.status_code == 200
    assert b'data-image-id="42"' in response.data
    assert b'src="/edited.png"' in response.data
    assert b"AI Edited" in response.data


def test_gallery_requires_login():
    with app.test_client() as client:
        response = client.get("/gallery.html")

    assert response.status_code == 302
    assert response.headers["Location"] == "/login.html"
