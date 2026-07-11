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
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        return user
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
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, (user_id,))
        gallery = cursor.fetchall()
        return gallery
    except mysql.connector.Error as err:
        print(f"Database Error during gallery fetch: {err}")
        return []
    finally:
        cursor.close()
        connection.close()

def update_image_record(image_id, user_id, modified_path, edit_type):
    """
    Directly updates the processing results for a specific image record.
    """
    query = """
        UPDATE Images 
        SET ModifiedFilePath = %s, EditType = %s 
        WHERE ImageID = %s AND UserID = %s;
    """
    
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute(query, [modified_path, edit_type, image_id, user_id])
        connection.commit()

        return cursor.rowcount > 0

    except Exception as err:
        print(f"[DB ERROR] Failed to update image record: {err}")
        if connection:
            connection.rollback()
        return False
    finally:
        if cursor: cursor.close()
        if connection: connection.close()