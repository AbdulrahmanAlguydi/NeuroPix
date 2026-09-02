import mysql.connector
from database.database import get_db_connection

def register_user(username, password_hash):
    """
    Inserts a new user into the Users table.
    """
    query = """
        INSERT INTO Users (Username, PasswordHash) 
        VALUES (%s, %s);
    """
    connection = get_db_connection()
    if not connection:
        return False
    cursor = connection.cursor()
    try:
        cursor.execute(query, (username, password_hash))
        connection.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Database Error during registration: {err}")
        return False
    finally:
        cursor.close()
        connection.close()

def get_user_by_username(username):
    """
    Retrieves a user's record to validate credentials.
    """
    query = """
        SELECT UserID, Username, PasswordHash 
        FROM Users 
        WHERE Username = %s;
    """
    connection = get_db_connection()
    if not connection:
        return None
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, (username,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Database Error during user fetch: {err}")
        return None
    finally:
        cursor.close()
        connection.close()

def log_image_edit(user_id, original_path, modified_path, edit_type):
    """
    Logs an image transaction into the Images table.
    edit_type must be either 'standard' or 'ai' to satisfy the ENUM constraint.
    """
    query = """
        INSERT INTO Images (UserID, OriginalFilePath, ModifiedFilePath, EditType) 
        VALUES (%s, %s, %s, %s);
    """
    connection = get_db_connection()
    if not connection:
        return False
    cursor = connection.cursor()
    try:
        cursor.execute(query, (user_id, original_path, modified_path, edit_type))
        connection.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Database Error during image logging: {err}")
        return False
    finally:
        cursor.close()
        connection.close()

def get_user_gallery(user_id):
    """
    Pulls all images belonging to a specific UserID ordered by the newest uploads.
    """
    query = """
        SELECT ImageID, OriginalFilePath, ModifiedFilePath, EditType, UploadDate 
        FROM Images 
        WHERE UserID = %s 
        ORDER BY UploadDate DESC;
    """
    connection = get_db_connection()
    if not connection:
        return []
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, (user_id,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Database Error during gallery fetch: {err}")
        return []
    finally:
        cursor.close()
        connection.close()

def delete_image_record(image_id, user_id):
    """
    Verifies ownership and deletes the database record.
    Returns the file keys so the caller can clean up S3.
    """
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        # 1. Fetch keys first to ensure ownership and get S3 paths
        fetch_query = """
            SELECT OriginalFilePath, ModifiedFilePath 
            FROM Images 
            WHERE ImageID = %s AND UserID = %s;
        """
        cursor.execute(fetch_query, (image_id, user_id))
        record = cursor.fetchone()

        if not record:
            print(f"[DB WARN] Image {image_id} not found for User {user_id}")
            return None

        # 2. Delete the row
        delete_query = "DELETE FROM Images WHERE ImageID = %s AND UserID = %s;"
        cursor.execute(delete_query, (image_id, user_id))
        conn.commit()

        print(f"[DB] Image record {image_id} deleted successfully.")
        return record  # Returns dict with OriginalFilePath and ModifiedFilePath

    except mysql.connector.Error as e:
        print(f"[DB ERROR] Failed to delete image record: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()