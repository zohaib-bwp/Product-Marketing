import pymysql

print("Testing MySQL connection...")
print(f"Service: MySQL (running)")

try:
    # Try to connect to MySQL
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Malik@123',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    print("✅ Successfully connected to MySQL!")
    
    cursor = connection.cursor()
    
    # Show MySQL version
    cursor.execute("SELECT VERSION() as version")
    version = cursor.fetchone()
    print(f"MySQL Version: {version['version']}")
    
    # Show all databases
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    print("\nAvailable databases:")
    for db in databases:
        print(f"  - {list(db.values())[0]}")
    
    # Check if our database exists
    cursor.execute("SHOW DATABASES LIKE 'product_marketing'")
    if cursor.fetchone():
        print("\n✅ Database 'product_marketing' exists")
    else:
        print("\n⚠️  Database 'product_marketing' does not exist")
        print("Creating database...")
        cursor.execute("CREATE DATABASE product_marketing")
        print("✅ Database created!")
    
    cursor.close()
    connection.close()
    
    print("\n✅ MySQL is ready to use!")
    
except pymysql.err.OperationalError as e:
    print(f"❌ Cannot connect to MySQL!")
    print(f"Error: {e}")
    print("\nTroubleshooting:")
    print("1. Check password is correct: 'Malik@123'")
    print("2. Try resetting MySQL password")
    print("3. Check if MySQL is accepting connections")
    
except Exception as e:
    print(f"❌ Error: {e}")