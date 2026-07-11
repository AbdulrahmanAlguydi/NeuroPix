import os
from database.database import get_db_connection

def run_connection_test():
    print("=========================================")
    print("🔄 NEUROPIX: Testing Database Connection...")
    print("=========================================")
    
    # 1. Check if the environment file is actually being read
    if not os.getenv('DB_HOST'):
        print("❌ Error: Could not read environment variables.")
        print("💡 Fix: Make sure your local '.env' file exists in the root folder.")
        return

    # 2. Attempt the database handshake
    conn = get_db_connection()
    
    if conn and conn.is_connected():
        print("✅ Handshake Success! Python is talking to your MySQL server.")
        
        # 3. Pull active database metadata as the final verification
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE(), VERSION();")
        db_name, db_version = cursor.fetchone()
        
        print(f"📁 Target Database: {db_name}")
        print(f"⚙️ MySQL Version:    {db_version}")
        print("=========================================")
        
        cursor.close()
        conn.close()
        print("🔌 Connection closed cleanly. Your environment is 100% ready!")
    else:
        print("❌ Handshake Failed! Python could not connect to MySQL.")
        print("💡 Fix: Double-check your password in '.env' and ensure MySQL is running.")
        print("=========================================")

if __name__ == '__main__':
    run_connection_test()