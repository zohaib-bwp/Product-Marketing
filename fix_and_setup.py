import pymysql
from werkzeug.security import generate_password_hash
from config import Config

def setup_database():
    print("="*60)
    print("FIXING DATABASE SETUP")
    print("="*60)
    
    print("\n📝 Configuration being used:")
    print(f"   Host: {Config.MYSQL_HOST}")
    print(f"   User: {Config.MYSQL_USER}")
    print(f"   Password: {Config.MYSQL_PASSWORD}")
    print(f"   Database: {Config.MYSQL_DB}")
    
    try:
        # First connect without database
        print("\n1. Connecting to MySQL server...")
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = connection.cursor()
        print("   ✅ Connected to MySQL server")
        
        # Create database if not exists
        print("\n2. Creating database...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DB}")
        cursor.execute(f"USE {Config.MYSQL_DB}")
        print(f"   ✅ Database '{Config.MYSQL_DB}' ready")
        
        # Create users table
        print("\n3. Creating tables...")
        
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
        print("   ✅ Users table")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                category_id INT AUTO_INCREMENT PRIMARY KEY,
                category_name VARCHAR(50) NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("   ✅ Categories table")
        
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
        print("   ✅ Products table")
        
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
        print("   ✅ Cart table")
        
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
        print("   ✅ Orders table")
        
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
        print("   ✅ Order items table")
        
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
        print("   ✅ Activity log table")
        
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
        print("   ✅ System settings table")
        
        # Insert default categories
        print("\n4. Inserting default data...")
        categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 
                     'Sports', 'Toys & Games', 'Beauty & Health', 'Automotive',
                     'Food & Beverages', 'Office Supplies']
        
        for cat in categories:
            cursor.execute("INSERT IGNORE INTO categories (category_name) VALUES (%s)", (cat,))
        print("   ✅ Categories inserted")
        
        # Create admin user
        hashed_password = generate_password_hash('admin123')
        cursor.execute("DELETE FROM users WHERE email = 'admin@example.com'")
        cursor.execute("""
            INSERT INTO users (name, email, password, phone, address, role) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, ('Admin User', 'admin@example.com', hashed_password, '12345678901', 'Admin Office', 'admin'))
        print("   ✅ Admin user created")
        
        # Insert system settings
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
        print("   ✅ System settings inserted")
        
        # Insert sample products
        print("\n5. Adding sample products...")
        
        # Get category IDs
        cursor.execute("SELECT category_id FROM categories WHERE category_name = 'Electronics'")
        electronics_id = cursor.fetchone()['category_id']
        
        sample_products = [
            ('Laptop Pro', 'High performance laptop', 999.99, 10, electronics_id, 'https://via.placeholder.com/300'),
            ('Wireless Mouse', 'Ergonomic wireless mouse', 29.99, 50, electronics_id, 'https://via.placeholder.com/300'),
            ('Mechanical Keyboard', 'RGB mechanical keyboard', 89.99, 30, electronics_id, 'https://via.placeholder.com/300'),
        ]
        
        for product in sample_products:
            cursor.execute("""
                INSERT IGNORE INTO products (name, description, price, stock_quantity, category_id, image_url)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, product)
        print("   ✅ Sample products added")
        
        connection.commit()
        
        print("\n" + "="*60)
        print("✅ DATABASE SETUP COMPLETE!")
        print("="*60)
        print("\n📊 DATABASE INFO:")
        print(f"   Database: {Config.MYSQL_DB}")
        print(f"   Host: {Config.MYSQL_HOST}")
        print(f"   User: {Config.MYSQL_USER}")
        print("\n👤 ADMIN LOGIN:")
        print(f"   Email: admin@example.com")
        print(f"   Password: admin123")
        print("\n🚀 TO START THE APP:")
        print(f"   python app.py")
        print("\n🌐 TO ACCESS:")
        print(f"   http://localhost:5000")
        print("="*60)
        
        cursor.close()
        connection.close()
        
    except pymysql.err.OperationalError as e:
        print(f"\n❌ MySQL Connection Error!")
        print(f"   Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure MySQL service is running")
        print("   2. Check password in config.py")
        print("   3. Try: net start MySQL")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    setup_database()