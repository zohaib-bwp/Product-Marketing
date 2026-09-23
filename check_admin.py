import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

# Database configuration
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Malik@123',
    'database': 'product_marketing'
}

def check_and_fix_admin():
    try:
        connection = pymysql.connect(**config, cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        
        # Check if admin exists
        cursor.execute("SELECT user_id, email, password, role FROM users WHERE email = 'admin@example.com'")
        admin = cursor.fetchone()
        
        if admin:
            print("✓ Admin user found!")
            print(f"  User ID: {admin['user_id']}")
            print(f"  Email: {admin['email']}")
            print(f"  Role: {admin['role']}")
            print(f"  Password hash: {admin['password'][:50]}...")
            
            # Test if password 'admin123' works
            if check_password_hash(admin['password'], 'admin123'):
                print("  ✓ Password 'admin123' is correct!")
            else:
                print("  ✗ Password 'admin123' is incorrect!")
                print("  Resetting password...")
                
                # Reset password
                new_hash = generate_password_hash('admin123')
                cursor.execute("UPDATE users SET password = %s WHERE email = 'admin@example.com'", (new_hash,))
                connection.commit()
                print("  ✓ Password reset to 'admin123'")
        else:
            print("✗ Admin user not found!")
            print("Creating admin user...")
            
            # Create admin user
            hashed_password = generate_password_hash('admin123')
            cursor.execute("""
                INSERT INTO users (name, email, password, phone, address, role) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, ('Admin User', 'admin@example.com', hashed_password, '12345678901', 'Admin Office', 'admin'))
            connection.commit()
            print("✓ Admin user created with password 'admin123'")
        
        # Verify login works
        cursor.execute("SELECT password FROM users WHERE email = 'admin@example.com'")
        user = cursor.fetchone()
        if user and check_password_hash(user['password'], 'admin123'):
            print("\n✅ SUCCESS! Login credentials work:")
            print("   Email: admin@example.com")
            print("   Password: admin123")
        else:
            print("\n❌ Still having issues. Please run the SQL fix below.")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_and_fix_admin()