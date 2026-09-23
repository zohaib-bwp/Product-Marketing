from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_db
from utils.decorators import admin_required
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# --- Helper Function for Database Operations ---
def execute_query(query, args=(), fetchone=False, fetchall=False):
    """Execute database query and return results"""
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute(query, args)
        
        if fetchone:
            result = cursor.fetchone()
            # If result is a dict and we just need count, extract the value
            if result and isinstance(result, dict) and 'COUNT(*)' in result:
                result = result['COUNT(*)']
            return result
        elif fetchall:
            result = cursor.fetchall()
            return result
        else:
            db.commit()
            return cursor.lastrowid if query.strip().upper().startswith('INSERT') else None
    finally:
        cursor.close()

# --- 1. Admin Dashboard ---
@admin_bp.route('/')
@admin_required
def dashboard():
    """Admin Dashboard"""
    try:
        # Fetch summary data - Fixed to handle return values properly
        total_products_result = execute_query("SELECT COUNT(*) as count FROM products", fetchone=True)
        total_products = total_products_result['count'] if isinstance(total_products_result, dict) else total_products_result
        
        total_orders_result = execute_query("SELECT COUNT(*) as count FROM orders", fetchone=True)
        total_orders = total_orders_result['count'] if isinstance(total_orders_result, dict) else total_orders_result
        
        pending_orders_result = execute_query("SELECT COUNT(*) as count FROM orders WHERE status = 'Pending'", fetchone=True)
        pending_orders = pending_orders_result['count'] if isinstance(pending_orders_result, dict) else pending_orders_result
        
        return render_template('admin/dashboard.html', 
                               total_products=total_products, 
                               total_orders=total_orders, 
                               pending_orders=pending_orders)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'danger')
        return render_template('admin/dashboard.html', 
                               total_products=0, 
                               total_orders=0, 
                               pending_orders=0)

# --- 2. Product Management ---
@admin_bp.route('/products')
@admin_required
def manage_products():
    """Manage Products"""
    try:
        products = execute_query("""
            SELECT p.*, c.category_name 
            FROM products p 
            LEFT JOIN categories c ON p.category_id = c.category_id
            ORDER BY p.product_id DESC
        """, fetchall=True)
        return render_template('admin/products.html', products=products or [])
    except Exception as e:
        flash(f'Error loading products: {str(e)}', 'danger')
        return render_template('admin/products.html', products=[])

@admin_bp.route('/product/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    """Add new product"""
    try:
        categories = execute_query("SELECT * FROM categories ORDER BY category_name", fetchall=True)
        
        if request.method == 'POST':
            name = request.form.get('name')
            description = request.form.get('description')
            price = request.form.get('price')
            stock_quantity = request.form.get('stock_quantity')
            category_id = request.form.get('category_id')
            image_url = request.form.get('image_url', '')

            # Basic validation
            if not all([name, price, stock_quantity, category_id]):
                flash('Please fill in all required fields.', 'danger')
                return redirect(url_for('admin.add_product'))

            # Insert product
            query = """
                INSERT INTO products (name, description, price, stock_quantity, category_id, image_url) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            execute_query(query, (name, description, float(price), int(stock_quantity), int(category_id), image_url))
            
            flash(f'Product "{name}" added successfully!', 'success')
            return redirect(url_for('admin.manage_products'))
            
        return render_template('admin/add_edit_product.html', categories=categories, product=None)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('admin.manage_products'))

@admin_bp.route('/product/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    """Edit product"""
    try:
        categories = execute_query("SELECT * FROM categories ORDER BY category_name", fetchall=True)
        product = execute_query("SELECT * FROM products WHERE product_id = %s", (product_id,), fetchone=True)
        
        if not product:
            flash('Product not found.', 'danger')
            return redirect(url_for('admin.manage_products'))

        if request.method == 'POST':
            name = request.form.get('name')
            description = request.form.get('description')
            price = request.form.get('price')
            stock_quantity = request.form.get('stock_quantity')
            category_id = request.form.get('category_id')
            image_url = request.form.get('image_url', product.get('image_url', ''))

            query = """
                UPDATE products SET 
                name = %s, description = %s, price = %s, stock_quantity = %s, 
                category_id = %s, image_url = %s
                WHERE product_id = %s
            """
            execute_query(query, (name, description, float(price), int(stock_quantity), 
                                 int(category_id), image_url, product_id))
            
            flash(f'Product "{name}" updated successfully!', 'success')
            return redirect(url_for('admin.manage_products'))
            
        return render_template('admin/add_edit_product.html', categories=categories, product=product)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('admin.manage_products'))

@admin_bp.route('/product/delete/<int:product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    """Delete product"""
    try:
        product = execute_query("SELECT name FROM products WHERE product_id = %s", (product_id,), fetchone=True)
        if product:
            product_name = product['name'] if isinstance(product, dict) else product
            execute_query("DELETE FROM products WHERE product_id = %s", (product_id,))
            flash(f'Product "{product_name}" deleted successfully!', 'success')
        else:
            flash('Product not found.', 'danger')
    except Exception as e:
        flash(f'Error deleting product: {str(e)}', 'danger')
        
    return redirect(url_for('admin.manage_products'))

# --- 3. Order Management ---
@admin_bp.route('/orders')
@admin_required
def manage_orders():
    """Manage orders"""
    try:
        orders = execute_query("""
            SELECT o.*, u.name as user_name, u.email 
            FROM orders o 
            JOIN users u ON o.user_id = u.user_id
            ORDER BY o.order_date DESC
        """, fetchall=True)
        return render_template('admin/orders.html', orders=orders or [])
    except Exception as e:
        flash(f'Error loading orders: {str(e)}', 'danger')
        return render_template('admin/orders.html', orders=[])

@admin_bp.route('/order/details/<int:order_id>')
@admin_required
def order_details(order_id):
    """View order details"""
    try:
        order = execute_query("SELECT * FROM orders WHERE order_id = %s", (order_id,), fetchone=True)
        if not order:
            flash('Order not found.', 'danger')
            return redirect(url_for('admin.manage_orders'))

        items = execute_query("""
            SELECT oi.*, p.name as product_name 
            FROM order_items oi 
            JOIN products p ON oi.product_id = p.product_id 
            WHERE oi.order_id = %s
        """, (order_id,), fetchall=True)
        
        return render_template('admin/order_details.html', order=order, items=items or [])
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('admin.manage_orders'))

@admin_bp.route('/order/update_status/<int:order_id>', methods=['POST'])
@admin_required
def update_order_status(order_id):
    """Update order status"""
    try:
        new_status = request.form.get('status')
        
        valid_statuses = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']
        if new_status not in valid_statuses:
            flash('Invalid status provided.', 'danger')
            return redirect(url_for('admin.order_details', order_id=order_id))

        execute_query("UPDATE orders SET status = %s WHERE order_id = %s", (new_status, order_id))
        
        flash(f'Order #{order_id} status updated to "{new_status}"!', 'success')
        return redirect(url_for('admin.order_details', order_id=order_id))
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('admin.order_details', order_id=order_id))