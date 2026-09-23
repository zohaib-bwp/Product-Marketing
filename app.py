from flask import Flask
from config import Config
from database import init_db

# Import all controllers
from controllers.auth_controller import auth_bp
from controllers.product_controller import product_bp
from controllers.cart_controller import cart_bp
from controllers.order_controller import order_bp
from controllers.admin_profile_controller import admin_profile_bp
from controllers.user_profile_controller import user_profile_bp
from controllers.admin_product_controller import admin_product_bp
from admin import admin_bp

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
init_db(app)

# Register all blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(order_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(admin_profile_bp)
app.register_blueprint(user_profile_bp)
app.register_blueprint(admin_product_bp)

# Direct logout route (fallback)
@app.route('/logout')
def logout():
    """Direct logout route"""
    from flask import session, redirect, url_for
    session.clear()
    return redirect(url_for('auth.login_page'))

# Home route (redirect to product index)
@app.route('/home')
def home():
    return redirect(url_for('product.index'))

if __name__ == '__main__':
    print("=" * 50)
    print("Product Marketing System Starting...")
    print("=" * 50)
    print(f"Database: {Config.MYSQL_DB}")
    print(f"Host: {Config.MYSQL_HOST}")
    print("\nRegistered Blueprints:")
    print("  - auth (login/register)")
    print("  - product (products listing)")
    print("  - cart (shopping cart)")
    print("  - order (orders)")
    print("  - admin (admin panel)")
    print("  - admin_profile (admin profile)")
    print("  - user_profile (user profile)")
    print("  - admin_product (product management with images)")
    print("\n" + "=" * 50)
    print("Server running at: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True)