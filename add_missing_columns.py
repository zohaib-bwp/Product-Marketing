import pymysql

# Database configuration
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Malik@123',
    'database': 'product_marketing',
    'cursorclass': pymysql.cursors.DictCursor
}

def add_missing_columns():
    print("="*60)
    print("ADDING MISSING COLUMNS TO USERS TABLE")
    print("="*60)
    
    try:
        connection = pymysql.connect(**config)
        cursor = connection.cursor()
        
        # List of columns to add
        columns_to_add = [
            ("profile_picture", "VARCHAR(255) DEFAULT NULL"),
            ("bio", "TEXT"),
            ("last_login", "TIMESTAMP NULL"),
            ("last_login_ip", "VARCHAR(45)"),
            ("is_active", "BOOLEAN DEFAULT TRUE")
        ]
        
        print("\nChecking and adding columns...")
        
        for column_name, column_definition in columns_to_add:
            try:
                # Check if column exists
                cursor.execute(f"""
                    SELECT COUNT(*) as count 
                    FROM information_schema.COLUMNS 
                    WHERE TABLE_SCHEMA = '{config['database']}' 
                    AND TABLE_NAME = 'users' 
                    AND COLUMN_NAME = '{column_name}'
                """)
                
                result = cursor.fetchone()
                if result['count'] == 0:
                    # Add the column
                    alter_query = f"ALTER TABLE users ADD COLUMN {column_name} {column_definition}"
                    cursor.execute(alter_query)
                    print(f"  ✅ Added column: {column_name}")
                else:
                    print(f"  ✓ Column already exists: {column_name}")
                    
            except Exception as e:
                print(f"  ⚠️ Error adding {column_name}: {e}")
        
        connection.commit()
        print("\n✅ All columns added successfully!")
        
        # Show table structure
        print("\n📋 Current users table structure:")
        cursor.execute("DESCRIBE users")
        columns = cursor.fetchall()
        for col in columns:
            print(f"   - {col['Field']}: {col['Type']}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    add_missing_columns()