import pymysql
from flask import g
from config import Config

def get_db():
    """Get database connection"""
    if 'db' not in g:
        try:
            g.db = pymysql.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False
            )
        except Exception as e:
            print(f"Database connection error: {e}")
            raise e
    return g.db

def close_db(e=None):
    """Close database connection"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    """Initialize database with app"""
    app.teardown_appcontext(close_db)
    
    # Test connection and ensure columns exist
    with app.app_context():
        try:
            db = get_db()
            cursor = db.cursor()
            
            # Check if last_login column exists
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = 'product_marketing' 
                AND TABLE_NAME = 'users' 
                AND COLUMN_NAME = 'last_login'
            """)
            result = cursor.fetchone()
            
            if result['count'] == 0:
                print("⚠️ Missing columns detected. Please run: python complete_fix.py")
            
            cursor.close()
        except Exception as e:
            print(f"Warning: Could not verify database schema: {e}")