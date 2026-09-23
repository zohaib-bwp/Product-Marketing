import pymysql
from werkzeug.security import generate_password_hash

# Database configuration
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Malik@123',
    'database': 'product_marketing'
}

def column_exists(cursor, table, column):
    """Check if a column exists in a table"""
    cursor.execute(f"""
        SELECT COUNT(*) as count 
        FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = '{config['database']}' 
        AND TABLE_NAME = '{table}' 
        AND COLUMN_NAME = '{column}'
    """)
    result = cursor.fetchone()
    return result['count'] > 0

def setup_admin_profile():
    """Setup admin profile features"""
    try:
        connection = pymysql.connect(**config, cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        
        print("✓ Connected to database successfully!")
        
        # Add new columns to users table (checking existence first)
        print("\n📋 Checking and adding columns to users table...")
        
        columns_to_add = [
            ('profile_picture', 'VARCHAR(255) DEFAULT NULL'),
            ('bio', 'TEXT'),
            ('last_login', 'TIMESTAMP NULL'),
            ('last_login_ip', 'VARCHAR(45)'),
            ('is_active', 'BOOLEAN DEFAULT TRUE'),
            ('preferences', 'JSON')
        ]
        
        for column, definition in columns_to_add:
            if not column_exists(cursor, 'users', column):
                try:
                    cursor.execute(f"ALTER TABLE users ADD COLUMN {column} {definition}")
                    print(f"  ✓ Added column: {column}")
                except Exception as e:
                    print(f"  ⚠️ Could not add {column}: {e}")
            else:
                print(f"  ✓ Column already exists: {column}")
        
        # Create admin_activity_log table
        print("\n📋 Creating admin_activity_log table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_activity_log (
                log_id INT AUTO_INCREMENT PRIMARY KEY,
                admin_id INT NOT NULL,
                action VARCHAR(100) NOT NULL,
                details TEXT,
                ip_address VARCHAR(45),
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_admin_actions (admin_id, created_at)
            )
        """)
        print("  ✓ admin_activity_log table ready")
        
        # Add foreign key constraint if it doesn't exist
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM information_schema.KEY_COLUMN_USAGE 
            WHERE CONSTRAINT_NAME = 'admin_activity_log_ibfk_1'
            AND TABLE_SCHEMA = %s
        """, (config['database'],))
        
        fk_exists = cursor.fetchone()
        if fk_exists['count'] == 0:
            try:
                cursor.execute("""
                    ALTER TABLE admin_activity_log 
                    ADD CONSTRAINT admin_activity_log_ibfk_1 
                    FOREIGN KEY (admin_id) REFERENCES users(user_id) ON DELETE CASCADE
                """)
                print("  ✓ Foreign key constraint added")
            except Exception as e:
                print(f"  ⚠️ Foreign key constraint: {e}")
        
        # Create system_settings table
        print("\n📋 Creating system_settings table...")
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
        print("  ✓ system_settings table ready")
        
        # Insert default system settings
        print("\n📋 Inserting default system settings...")
        settings = [
            ('site_name', 'Product Marketing System', 'text', 'Website name'),
            ('site_description', 'Your one-stop shop for amazing products', 'textarea', 'Site description for SEO'),
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
                print(f"  ✓ Setting added/updated: {setting[0]}")
            except Exception as e:
                print(f"  ⚠️ Error with setting {setting[0]}: {e}")
        
        # Create default admin user if not exists
        print("\n📋 Setting up admin user...")
        admin_email = 'admin@example.com'
        admin_password = 'admin123'
        hashed_password = generate_password_hash(admin_password)
        
        # Check if admin user exists
        cursor.execute("SELECT user_id, role FROM users WHERE email = %s", (admin_email,))
        existing_admin = cursor.fetchone()
        
        if not existing_admin:
            # Insert new admin user
            cursor.execute("""
                INSERT INTO users (name, email, password, phone, address, role) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, ('Admin User', admin_email, hashed_password, '12345678901', 'Admin Office', 'admin'))
            print(f"  ✓ Admin user created!")
            print(f"     Email: {admin_email}")
            print(f"     Password: {admin_password}")
        else:
            # Update existing user to admin role if not already
            if existing_admin['role'] != 'admin':
                cursor.execute("UPDATE users SET role = 'admin' WHERE email = %s", (admin_email,))
                print(f"  ✓ Existing user updated to admin role: {admin_email}")
            else:
                print(f"  ✓ Admin user already exists: {admin_email}")
            
            # Update password for existing admin (optional - remove if not needed)
            cursor.execute("""
                UPDATE users SET password = %s WHERE email = %s AND role = 'admin'
            """, (hashed_password, admin_email))
            print(f"  ✓ Admin password reset to: {admin_password}")
        
        connection.commit()
        
        print("\n" + "="*60)
        print("✅ ADMIN PROFILE SETUP COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\n📝 LOGIN CREDENTIALS:")
        print(f"   Email: {admin_email}")
        print(f"   Password: {admin_password}")
        print("\n🌐 ACCESS YOUR APPLICATION:")
        print(f"   Homepage: http://localhost:5000")
        print(f"   Login: http://localhost:5000/login")
        print(f"   Admin Dashboard: http://localhost:5000/admin")
        print(f"   Admin Profile: http://localhost:5000/admin/profile")
        print("\n🚀 NEXT STEPS:")
        print("   1. Run: python app.py")
        print("   2. Open browser and go to http://localhost:5000")
        print("   3. Login with above credentials")
        print("   4. Access admin profile from top-right dropdown")
        print("="*60)
        
    except pymysql.err.OperationalError as e:
        print(f"\n❌ DATABASE CONNECTION ERROR!")
        print(f"   Error: {e}")
        print("\n🔧 TROUBLESHOOTING:")
        print("   1. Make sure MySQL is running:")
        print("      - Press Win+R, type: services.msc")
        print("      - Find MySQL80 or MySQL")
        print("      - Start the service if not running")
        print("   2. Verify database credentials in config.py")
        print("   3. Check if database 'product_marketing' exists:")
        print("      - Run: mysql -u root -p")
        print("      - Then: SHOW DATABASES;")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()
            print("\n✓ Database connection closed")

if __name__ == '__main__':
    print("="*60)
    print("ADMIN PROFILE SETUP SCRIPT")
    print("="*60)
    print("\nThis script will:")
    print("  • Add required columns to users table")
    print("  • Create activity log table")
    print("  • Create system settings table")
    print("  • Setup admin user")
    print("\nStarting setup...\n")
    setup_admin_profile()