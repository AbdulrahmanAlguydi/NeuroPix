from database.database import get_db_connection
from mysql.connector import Error

def seed_database():
    print("NEUROPIX: Seeding local database...")
    conn = get_db_connection()
    
    if not conn:
        print("Connection failed. Aborting seed.")
        return

    try:
        cursor = conn.cursor(dictionary=True)

        # 1. Temporarily disable foreign keys so we can safely wipe old data
        print("Wiping existing table data...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE Images;")
        cursor.execute("TRUNCATE TABLE Users;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

        # 2. Insert Dummy Users (Passwords are placeholders; backend will hash real ones later)
        print("Inserting mock users...")
        users_to_insert = [
            ("main_dev", "mock_hash_xyz123"),
            ("second_editor", "mock_hash_abc789"),
            ("test_user", "mock_hash_qwert555")
        ]
        
        user_ids = []
        for username, pwd_hash in users_to_insert:
            query = "INSERT INTO Users (Username, PasswordHash) VALUES (%s, %s);"
            cursor.execute(query, (username, pwd_hash))
            # Capture the auto-incremented ID MySQL just made for this user
            user_ids.append(cursor.lastrowid)

        # 3. Insert Dummy Images linked to our new user IDs
        print("Inserting mock image metadata...")
        images_to_insert = [
            (user_ids[0], "/uploads/raw/sunset.jpg", "/uploads/edited/sunset_ai.jpg", "ai"),
            (user_ids[0], "/uploads/raw/profile.png", None, None), # Not edited yet
            (user_ids[1], "/uploads/raw/car.jpg", "/uploads/edited/car_crop.jpg", "standard"),
            (user_ids[2], "/uploads/raw/nature.bmp", "/uploads/edited/nature_enhanced.bmp", "ai")
        ]

        query_image = """
            INSERT INTO Images (UserID, OriginalFilePath, ModifiedFilePath, EditType) 
            VALUES (%s, %s, %s, %s);
        """
        cursor.executemany(query_image, images_to_insert)

        # 4. Save changes permanently
        conn.commit()
        print("Database successfully seeded with 3 users and 4 images!")

    except Error as e:
        print(f"Error during seeding: {e}")
        conn.rollback() # Undo changes if anything crashed midway
    finally:
        cursor.close()
        conn.close()
        print("Connection closed cleanly.")

if __name__ == '__main__':
    seed_database()