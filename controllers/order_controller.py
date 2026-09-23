from flask import Blueprint, jsonify, render_template, request, session

cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/cart")
def cart_page():
    return render_template("cart.html", items=[], total=0)


@cart_bp.route("/api/cart")
def cart_api():
    return jsonify({"success": True, "items": [], "total": 0})


@cart_bp.route("/api/cart/add", methods=["POST"])
def add_to_cart():
    data = request.get_json(silent=True) or {}
    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 1) or 1)
    if not product_id:
        return jsonify({"success": False, "message": "Product is required."})
    return jsonify({"success": True, "message": "Item added to cart.", "product_id": product_id, "quantity": quantity})
