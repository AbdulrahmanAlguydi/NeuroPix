"""Basic checks for the Dashboard and Studio pages."""

import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import app


def test_dashboard_shows_counts_and_recent_image():
    image = {
        "image_id": 42,
        "file_name": "city.png",
        "edit_type": "standard",
        "upload_date": datetime(2026, 10, 10),
        "original_url": "/original.png",
        "modified_url": "/edited.png",
    }
    with app.test_client() as client:
        with client.session_transaction() as session:
            session["user_id"] = 1
            session["username"] = "Student"
        with patch("app.fetch_formatted_user_gallery", return_value=[image]):
            response = client.get("/dashboard.html")

    assert response.status_code == 200
    assert b'id="standardEditCount">1</strong>' in response.data
    assert b'src="/edited.png"' in response.data
    assert b"Student" in response.data


def test_studio_shows_signed_in_username():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session["user_id"] = 1
            session["username"] = "Student"
        response = client.get("/workspace.html")

    assert response.status_code == 200
    assert b'id="sidebarUsername">Student</strong>' in response.data
    assert b'id="fileInput"' in response.data


def test_dashboard_and_studio_require_login():
    with app.test_client() as client:
        for page in ("/dashboard.html", "/workspace.html"):
            response = client.get(page)
            assert response.status_code == 302
            assert response.headers["Location"] == "/login.html"
