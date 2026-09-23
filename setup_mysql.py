import pymysql
from werkzeug.security import generate_password_hash

def setup_database():
    print("="*60)
    print("SETTING UP DATABASE FOR PRODUCT MARKETING")
    print("="*60)
    
    # Connection parameters
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Malik@123',
        'cursorclass': pymysql.cursors.DictCursor
    }
    
    try:
        # Connect to MySQL
        print("\n1. Connecting to MySQL...")
        connection = pymysql.connect(**config)
        cursor = connection.cursor()
        print("   ✅ Connected to MySQL")
        
        # Create database
        print("\n2. Creating database...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS product_marketing")
        cursor.execute("USE product_marketing")
        print("   ✅ Database 'product_marketing' ready")
        
        # Create users table
        print("\n3. Creating users table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                address TEXT,
                role VARCHAR(20) DEFAULT 'customer',
                profile_picture VARCHAR(255),
                bio TEXT,
                last_login TIMESTAMP NULL,
                last_login_ip VARCHAR(45),
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("   ✅ Users table created")
        
        # Create categories table
        print("\n4. Creating categories table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                category_id INT AUTO_INCREMENT PRIMARY KEY,
                category_name VARCHAR(50) NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("   ✅ Categories table created")
        
        # Create products table
        print("\n5. Creating products table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(150) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL,
                stock_quantity INT NOT NULL DEFAULT 0,
                category_id INT,
                image_url VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE SET NULL
            )
        """)
        print("   ✅ Products table created")
        
        # Create cart table
        print("\n6. Creating cart table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                cart_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL DEFAULT 1,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
                UNIQUE KEY unique_user_product (user_id, product_id)
            )
        """)
        print("   ✅ Cart table created")
        
        # Create orders table
        print("\n7. Creating orders table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(50) DEFAULT 'Pending',
                total_amount DECIMAL(10, 2) NOT NULL,
                shipping_address TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """)
        print("   ✅ Orders table created")
        
        # Create order_items table
        print("\n8. Creating order_items table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                order_item_id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL,
                price_at_purchase DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
            )
        """)
        print("   ✅ Order items table created")
        
        # Create admin_activity_log table
        print("\n9. Creating admin_activity_log table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_activity_log (
                log_id INT AUTO_INCREMENT PRIMARY KEY,
                admin_id INT NOT NULL,
                action VARCHAR(100) NOT NULL,
                details TEXT,
                ip_address VARCHAR(45),
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (admin_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """)
        print("   ✅ Activity log table created")
        
        # Create system_settings table
        print("\n10. Creating system_settings table...")
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
        print("   ✅ System settings table created")
        
        # Insert default categories
        print("\n11. Inserting default categories...")
        categories = [
            'Electronics', 'Clothing', 'Books', 'Home & Garden', 
            'Sports', 'Toys & Games', 'Beauty & Health', 'Automotive',
            'Food & Beverages', 'Office Supplies'
        ]
        for cat in categories:
            cursor.execute("INSERT IGNORE INTO categories (category_name) VALUES (%s)", (cat,))
        print("   ✅ Categories inserted")
        
        # Create admin user
        print("\n12. Creating admin user...")
        hashed_password = generate_password_hash('admin123')
        
        # Delete existing admin
        cursor.execute("DELETE FROM users WHERE email = 'admin@example.com'")
        
        # Insert new admin
        cursor.execute("""
            INSERT INTO users (name, email, password, phone, address, role) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, ('Admin User', 'admin@example.com', hashed_password, '12345678901', 'Admin Office', 'admin'))
        print("   ✅ Admin user created")
        
        # Insert system settings
        print("\n13. Inserting system settings...")
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
            cursor.execute("""
                INSERT IGNORE INTO system_settings (setting_key, setting_value, setting_type, description) 
                VALUES (%s, %s, %s, %s)
            """, setting)
        print("   ✅ Settings inserted")
        
        # Commit all changes
        connection.commit()
        
        print("\n" + "="*60)
        print("✅ DATABASE SETUP COMPLETE!")
        print("="*60)
        print("\n📊 DATABASE INFO:")
        print(f"   Database: product_marketing")
        print(f"   Tables: 9 tables created")
        print("\n👤 ADMIN LOGIN:")
        print(f"   Email: admin@example.com")
        print(f"   Password: admin123")
        print("\n🚀 NEXT STEPS:")
        print(f"   1. Run: python app.py")
        print(f"   2. Open browser to: http://localhost:5000")
        print(f"   3. Login with admin credentials")
        print("="*60)
        
        cursor.close()
        connection.close()
        
    except pymysql.err.OperationalError as e:
        print(f"\n❌ MySQL Connection Error: {e}")
        print("\nPlease check:")
        print("1. MySQL service is running (it is!)")
        print("2. Password is correct")
        print("3. Try resetting password if needed")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    setup_database()