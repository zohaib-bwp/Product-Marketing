import pymysql
from werkzeug.security import generate_password_hash

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Malik@123',
    'database': 'product_marketing',
    'cursorclass': pymysql.cursors.DictCursor
}

def complete_fix():
    print("="*60)
    print("COMPLETE DATABASE FIX")
    print("="*60)
    
    try:
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        
        # Step 1: Add missing columns to users table
        print("\n1. Adding missing columns to users table...")
        
        columns = {
            'profile_picture': 'VARCHAR(255) DEFAULT NULL',
            'bio': 'TEXT',
            'last_login': 'TIMESTAMP NULL',
            'last_login_ip': 'VARCHAR(45)',
            'is_active': 'BOOLEAN DEFAULT TRUE'
        }
        
        for col_name, col_def in columns.items():
            try:
                cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_def}")
                print(f"   ✅ Added column: {col_name}")
            except Exception as e:
                if "Duplicate column" in str(e):
                    print(f"   ✓ Column already exists: {col_name}")
                else:
                    print(f"   ⚠️ Could not add {col_name}: {e}")
        
        # Step 2: Create admin_activity_log table
        print("\n2. Creating admin_activity_log table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_activity_log (
                log_id INT AUTO_INCREMENT PRIMARY KEY,
                admin_id INT NOT NULL,
                action VARCHAR(100) NOT NULL,
                details TEXT,
                ip_address VARCHAR(45),
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("   ✅ admin_activity_log table ready")
        
        # Step 3: Create system_settings table
        print("\n3. Creating system_settings table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_settings (
                setting_id INT AUTO_INCREMENT PRIMARY KEY,
                setting_key VARCHAR(100) UNIQUE NOT NULL,
                setting_value TEXT,
                setting_type VARCHAR(50) DEFAULT 'text',
                description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        print("   ✅ system_settings table ready")
        
        # Step 4: Ensure admin user exists with correct password
        print("\n4. Setting up admin user...")
        hashed_password = generate_password_hash('admin123')
        
        # Check if admin exists
        cursor.execute("SELECT user_id FROM users WHERE email = 'admin@example.com'")
        admin = cursor.fetchone()
        
        if admin:
            cursor.execute("UPDATE users SET password = %s, role = 'admin' WHERE email = 'admin@example.com'", (hashed_password,))
            print("   ✅ Admin password updated")
        else:
            cursor.execute("""
                INSERT INTO users (name, email, password, phone, address, role) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, ('Admin User', 'admin@example.com', hashed_password, '12345678901', 'Admin Office', 'admin'))
            print("   ✅ Admin user created")
        
        # Step 5: Insert default system settings
        print("\n5. Inserting system settings...")
        settings = [
            ('site_name', 'Product Marketing System', 'text', 'Website name'),
            ('site_description', 'Your one-stop shop for amazing products', 'textarea', 'Site description'),
            ('contact_email', 'admin@example.com', 'email', 'Main contact email'),
            ('items_per_page', '12', 'number', 'Products per page'),
            ('maintenance_mode', '0', 'boolean', 'Enable maintenance mode'),
            ('currency_symbol', '$', 'text', 'Currency symbol'),
            ('currency_code', 'USD', 'text', 'Currency code')
        ]
        
        for setting in settings:
            try:
                cursor.execute("""
                    INSERT INTO system_settings (setting_key, setting_value, setting_type, description) 
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                    setting_value = VALUES(setting_value),
                    setting_type = VALUES(setting_type),
                    description = VALUES(description)
                """, setting)
            except Exception as e:
                print(f"   ⚠️ Error with {setting[0]}: {e}")
        
        print("   ✅ Settings inserted")
        
        conn.commit()
        
        print("\n" + "="*60)
        print("✅ DATABASE FIX COMPLETE!")
        print("="*60)
        print("\n👤 LOGIN CREDENTIALS:")
        print("   Email: admin@example.com")
        print("   Password: admin123")
        print("\n🚀 Restart your Flask app and try logging in!")
        print("="*60)
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    complete_fix()
    