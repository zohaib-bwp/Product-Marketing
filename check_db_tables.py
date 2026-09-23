import pymysql

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Malik@123',
    'database': 'product_marketing',
    'cursorclass': pymysql.cursors.DictCursor
}

def check_tables():
    try:
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        
        # Check all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("Tables in database:")
        for table in tables:
            print(f"  - {list(table.values())[0]}")
        
        # Check users table columns
        print("\nUsers table columns:")
        cursor.execute("DESCRIBE users")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col['Field']}: {col['Type']}")
        
        # Check if regions table exists
        cursor.execute("SHOW TABLES LIKE 'regions'")
        if cursor.fetchone():
            print("\nRegions table exists!")
            cursor.execute("SELECT * FROM regions")
            regions = cursor.fetchall()
            print(f"Found {len(regions)} regions")
            for region in regions:
                print(f"  - {region['region_name']} ({region['currency_symbol']}{region['currency']})")
        else:
            print("\n⚠️ Regions table missing!")
        
        # Check if user_profiles table exists
        cursor.execute("SHOW TABLES LIKE 'user_profiles'")
        if cursor.fetchone():
            print("\nUser_profiles table exists!")
            cursor.execute("DESCRIBE user_profiles")
            profile_cols = cursor.fetchall()
            for col in profile_cols:
                print(f"  - {col['Field']}: {col['Type']}")
        else:
            print("\n⚠️ User_profiles table missing!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_tables()