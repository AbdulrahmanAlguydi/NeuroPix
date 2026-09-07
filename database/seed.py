import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mysql.connector import Error

from database.database import get_db_connection


def seed_database():
    # This is a development-only reset: it removes existing test rows first.
    conn = get_db_connection()
    if not conn:
        print("Connection failed. Seed stopped.")
        return

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE Images;")
        cursor.execute("TRUNCATE TABLE Users;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

        users_to_insert = [
            # These are placeholder development accounts, not real users.
            ("main_dev", "mock_hash_xyz123"),
            ("second_editor", "mock_hash_abc789"),
            ("test_user", "mock_hash_qwert555")
        ]
        
        user_ids = []
        for username, pwd_hash in users_to_insert:
            cursor.execute(
                "INSERT INTO Users (Username, PasswordHash) VALUES (%s, %s);",
                (username, pwd_hash),
            )
            user_ids.append(cursor.lastrowid)

        images_to_insert = [
            # The paths are example S3 keys used to exercise database queries.
            (user_ids[0], "inputs/mock_sunset.jpg", "outputs/mock_sunset_ai.jpg", "ai"),
            (user_ids[0], "inputs/mock_profile.png", None, None),
            (user_ids[1], "inputs/mock_car.jpg", "outputs/mock_car_crop.jpg", "standard"),
            (user_ids[2], "inputs/mock_nature.png", "outputs/mock_nature_enhanced.png", "ai")
        ]

        cursor.executemany(
            """
                INSERT INTO Images (UserID, OriginalFilePath, ModifiedFilePath, EditType)
                VALUES (%s, %s, %s, %s);
            """,
            images_to_insert,
        )

        conn.commit()
        print("Database seeded with 3 users and 4 images.")

    except Error as error:
        print(f"Error during seeding: {error}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    seed_database()
