from database.database import get_db_connection
from mysql.connector import Error

def seed_database():
    print("NEUROPIX: Seeding local database with S3 object keys...")
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
            user_ids.append(cursor.lastrowid)

        # 3. Insert Dummy Images linked using realistic S3 Object Keys
        print("Inserting mock image metadata using S3 object keys...")
        images_to_insert = [
            (user_ids[0], "inputs/mock_sunset.jpg", "outputs/mock_sunset_ai.jpg", "ai"),
            (user_ids[0], "inputs/mock_profile.png", None, None), # Not edited yet
            (user_ids[1], "inputs/mock_car.jpg", "outputs/mock_car_crop.jpg", "standard"),
            (user_ids[2], "inputs/mock_nature.png", "outputs/mock_nature_enhanced.png", "ai")
        ]

        query_image = """
            INSERT INTO Images (UserID, OriginalFilePath, ModifiedFilePath, EditType) 
            VALUES (%s, %s, %s, %s);
        """
        cursor.executemany(query_image, images_to_insert)

        # 4. Save changes permanently
        conn.commit()
        print("Database successfully seeded with 3 users and 4 object-key images!")

    except Error as e:
        print(f"Error during seeding: {e}")
        conn.rollback() # Undo changes if anything crashed midway
    finally:
        cursor.close()
        conn.close()
        print("Connection closed cleanly.")

if __name__ == '__main__':
    seed_database()