import os
import uuid

from database.queries import (
    delete_image_record,
    get_gallery_image,
    get_user_gallery,
    log_image_edit,
)
from utils.s3 import (
    delete_s3_object,
    download_s3_object,
    get_full_s3_url,
    upload_original_image,
    upload_processed_image,
)


def save_image_transaction(
    user_id,
    local_raw_path,
    local_edited_path=None,
    edit_type=None,
    original_filename=None,
):
    """Upload the image files and record their paths in the database."""
    # Upload the original first because every gallery record needs it.
    original_filename = original_filename or os.path.basename(local_raw_path)
    original_filename = os.path.basename(original_filename)
    original_stem, original_extension = os.path.splitext(original_filename)
    unique_original_name = (
        f"{original_stem}-{uuid.uuid4().hex}{original_extension}"
    )
    original_key = upload_original_image(
        local_raw_path, object_name=unique_original_name
    )
    if not original_key:
        print("[SERVICE ERROR] Original image upload failed.")
        return None

    modified_key = None
    if local_edited_path:
        modified_key = upload_processed_image(local_edited_path)
        if not modified_key:
            print("[SERVICE ERROR] Processed image upload failed.")
            return None

    if not log_image_edit(
        user_id=user_id,
        original_path=original_key,
        modified_path=modified_key,
        edit_type=edit_type,
    ):
        print("[SERVICE ERROR] Image record could not be saved.")
        return None

    return {
        "OriginalFilePath": original_key,
        "ModifiedFilePath": modified_key,
        "EditType": edit_type,
    }


def delete_image_transaction(image_id, user_id):
    """Delete an image record and its S3 files."""
    # The query checks ownership before returning the paths to delete.
    paths = delete_image_record(image_id, user_id)
    if not paths:
        return False

    # Remove the database row first, then remove its two optional S3 objects.
    for key in (paths.get("OriginalFilePath"), paths.get("ModifiedFilePath")):
        if key:
            delete_s3_object(key)
    return True


def is_uuid_hex(value):
    """Check the UUID format used in older object keys."""
    return len(value) == 32 and all(
        character in "0123456789abcdef" for character in value.lower()
    )


def get_original_filename(path):
    """Remove the UUID added to an uploaded filename."""
    # New uploads use "name-uuid.ext"; the second pattern supports older records.
    filename = os.path.basename(path)
    stem, extension = os.path.splitext(filename)

    parts = stem.rsplit("-", 1)
    if len(parts) == 2 and is_uuid_hex(parts[1]):
        return parts[0] + extension

    parts = filename.split("_", 1)
    if len(parts) == 2 and is_uuid_hex(parts[0]):
        return parts[1]

    return filename


def fetch_formatted_user_gallery(user_id):
    """Return gallery records with browser-ready image URLs."""
    # Convert database column names into the smaller object expected by JavaScript.
    records = get_user_gallery(user_id)
    gallery = []

    for record in records:
        original_filename = get_original_filename(record["OriginalFilePath"])
        modified_url = None
        if record["ModifiedFilePath"]:
            modified_url = get_full_s3_url(record["ModifiedFilePath"])

        gallery.append(
            {
                "image_id": record["ImageID"],
                "file_name": original_filename,
                "edit_type": record["EditType"],
                "upload_date": record["UploadDate"],
                "original_url": get_full_s3_url(record["OriginalFilePath"]),
                "modified_url": modified_url,
            }
        )

    return gallery


def stage_gallery_image(image_id, user_id, temp_dir, source="original"):
    """Download the selected version of an owned gallery image."""
    record = get_gallery_image(image_id, user_id)
    if not record:
        return None

    source_key = record["OriginalFilePath"]
    if source == "edited":
        source_key = record["ModifiedFilePath"]

    if not source_key:
        return None

    source_filename = os.path.basename(source_key)
    temp_path = os.path.join(temp_dir, f"gallery-{uuid.uuid4().hex}-{source_filename}")

    if not download_s3_object(source_key, temp_path):
        return None

    return {
        "path": temp_path,
        "file_name": get_original_filename(record["OriginalFilePath"]),
        "source_key": source_key,
    }
