from flask import Blueprint, jsonify, render_template, request

product_bp = Blueprint("product", __name__)


@product_bp.route("/")
@product_bp.route("/products")
def index():
    """Render the product catalog."""
    products = [
        {
            "product_id": 1,
            "name": "Sample Laptop Pro",
            "price": 999.99,
            "description": "Starter product used when the database is still initializing.",
            "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853",
            "category_name": "Electronics",
        },
        {
            "product_id": 2,
            "name": "Classic Chair",
            "price": 159.50,
            "description": "Comfortable home-office seating.",
            "image_url": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85",
            "category_name": "Home & Garden",
        },
    ]
    return render_template("products.html", products=products)


@product_bp.route("/product/<int:product_id>")
def product_detail(product_id):
    product = {
        "product_id": product_id,
        "name": f"Sample Product {product_id}",
        "price": 199.99,
        "description": "A working placeholder product detail page for the starter app.",
        "image_url": "https://images.unsplash.com/photo-1511512578047-dfb367046420",
    }
    return render_template("product_detail.html", product=product)


@product_bp.route("/api/products")
def api_products():
    return jsonify({"success": True, "products": []})
