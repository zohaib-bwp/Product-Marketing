import pymysql

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Malik@123',
    'database': 'product_marketing',
    'cursorclass': pymysql.cursors.DictCursor
}

def fix_tables():
    try:
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        
        print("Creating missing tables and columns...")
        
        # Create regions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS regions (
                region_id INT AUTO_INCREMENT PRIMARY KEY,
                region_name VARCHAR(100) UNIQUE NOT NULL,
                currency VARCHAR(3),
                currency_symbol VARCHAR(5),
                tax_rate DECIMAL(5,2) DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Regions table ready")
        
        # Insert regions if empty
        cursor.execute("SELECT COUNT(*) as count FROM regions")
        count = cursor.fetchone()['count']
        if count == 0:
            regions = [
                ('USA', 'USD', '$', 0),
                ('Europe', 'EUR', '€', 0),
                ('UK', 'GBP', '£', 0),
                ('Canada', 'CAD', 'C$', 0),
                ('Australia', 'AUD', 'A$', 0),
                ('India', 'INR', '₹', 0),
                ('Pakistan', 'PKR', 'Rs', 0),
                ('UAE', 'AED', 'د.إ', 0),
                ('Singapore', 'SGD', 'S$', 0),
                ('Malaysia', 'MYR', 'RM', 0)
            ]
            for region in regions:
                cursor.execute("""
                    INSERT INTO regions (region_name, currency, currency_symbol, tax_rate) 
                    VALUES (%s, %s, %s, %s)
                """, region)
            print(f"✓ Inserted {len(regions)} regions")
        
        # Add columns to users table
        columns_to_add = [
            ("country", "VARCHAR(100)"),
            ("city", "VARCHAR(100)"),
            ("zip_code", "VARCHAR(20)"),
            ("region", "VARCHAR(100)")
        ]
        
        for col_name, col_type in columns_to_add:
            try:
                cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
                print(f"✓ Added column: {col_name}")
            except Exception as e:
                if "Duplicate column" in str(e):
                    print(f"✓ Column already exists: {col_name}")
                else:
                    print(f"⚠️ Could not add {col_name}: {e}")
        
        # Add columns to products table
        try:
            cursor.execute("ALTER TABLE products ADD COLUMN base_price DECIMAL(10, 2)")
            print("✓ Added base_price to products")
        except:
            print("✓ base_price already exists")
            
        try:
            cursor.execute("ALTER TABLE products ADD COLUMN region_pricing JSON")
            print("✓ Added region_pricing to products")
        except:
            print("✓ region_pricing already exists")
        
        # Create user_profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                profile_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                profile_picture VARCHAR(500),
                date_of_birth DATE,
                gender VARCHAR(20),
                occupation VARCHAR(100),
                company VARCHAR(100),
                website VARCHAR(200),
                social_media JSON,
                preferences JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                UNIQUE KEY unique_user_profile (user_id)
            )
        """)
        print("✓ User_profiles table ready")
        
        # Create product_images table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_images (
                image_id INT AUTO_INCREMENT PRIMARY KEY,
                product_id INT NOT NULL,
                image_url VARCHAR(500) NOT NULL,
                is_primary BOOLEAN DEFAULT FALSE,
                sort_order INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
                INDEX idx_product_images (product_id, is_primary)
            )
        """)
        print("✓ Product_images table ready")
        
        conn.commit()
        print("\n✅ All tables and columns created successfully!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    fix_tables()