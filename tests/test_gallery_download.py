"""Check that both saved gallery versions can be downloaded."""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import app


@pytest.mark.parametrize(
    "source,filename",
    [("original", "city.jpg"), ("edited", "city-edited.png")],
)
def test_gallery_download(tmp_path, source, filename):
    saved_image = tmp_path / "saved.png"
    saved_image.write_bytes(b"saved image")
    image = {
        "path": str(saved_image),
        "file_name": "city.jpg",
        "source_key": "outputs/saved.png",
    }
    app.config.update(TESTING=True, SECRET_KEY="gallery-test")

    with (
        app.test_client() as client,
        patch("app.stage_gallery_image", return_value=image),
    ):
        with client.session_transaction() as session:
            session["user_id"] = 1
        response = client.get(f"/api/gallery/42/download?source={source}")

    assert response.status_code == 200
    assert response.data == b"saved image"
    assert response.headers["Content-Disposition"] == f"attachment; filename={filename}"
