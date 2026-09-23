import pymysql
from werkzeug.security import generate_password_hash

print("Attempting to connect to MySQL...\n")

try:
    # First, try to connect without database to create it
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Malik@123',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    print("[SUCCESS] Connected to MySQL!\n")
    cursor = connection.cursor()
    
    # Create database if not exists
    print("Creating database...")
    cursor.execute("CREATE DATABASE IF NOT EXISTS product_marketing")
    cursor.execute("USE product_marketing")
    print("[SUCCESS] Database ready!\n")
    
    # Create users table if not exists
    print("Creating users table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            phone VARCHAR(11) NOT NULL,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("[SUCCESS] Users table ready!\n")
    
    # Delete existing test user
    cursor.execute("DELETE FROM users WHERE email = 'test@example.com'")
    
    # Add test user
    email = 'test@example.com'
    password = 'test1234'
    name = 'Test User'
    phone = '03001234567'
    address = 'Test Address, Test City'
    
    hashed_password = generate_password_hash(password)
    
    cursor.execute("""
        INSERT INTO users (name, email, password, phone, address) 
        VALUES (%s, %s, %s, %s, %s)
    """, (name, email, hashed_password, phone, address))
    
    connection.commit()
    
    print("="*60)
    print("[SUCCESS] TEST USER CREATED")
    print("="*60)
    print(f"Email:    {email}")
    print(f"Password: {password}")
    print("="*60)
    print("\nNow run:")
    print("  python app.py")
    print("\nThen open:")
    print("  http://localhost:5000/login")
    print("="*60 + "\n")
    
    cursor.close()
    connection.close()

except pymysql.err.OperationalError as e:
    print("[ERROR] Cannot connect to MySQL server!")
    print(f"\nError details: {e}\n")
    print("SOLUTION:")
    print("1. Open Command Prompt as Administrator")
    print("2. Run: net start MySQL80")
    print("3. If that fails, try: net start MySQL")
    print("\nOR use Windows Services:")
    print("1. Press Win+R, type: services.msc")
    print("2. Find MySQL80 or MySQL")
    print("3. Right-click -> Start")
    print("\nIf MySQL is not installed:")
    print("Download XAMPP from: https://www.apachefriends.org/")
    
except pymysql.err.InternalError as e:
    print(f"[ERROR] Database Error: {e}")
    print("\nTry running your db_schema.sql file first")

except Exception as e:
    print(f"[ERROR] Unexpected Error: {e}")
    import traceback
    traceback.print_exc()