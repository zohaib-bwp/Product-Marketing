from flask import Blueprint, jsonify, render_template, request, session

order_bp = Blueprint("order", __name__)


@order_bp.route("/orders")
def orders_page():
    return render_template("orders.html", orders=[])


@order_bp.route("/checkout")
def checkout_page():
    return render_template("checkout.html")


@order_bp.route("/api/orders")
def api_orders():
    return jsonify({"success": True, "orders": []})


@order_bp.route("/api/orders/checkout", methods=["POST"])
def checkout():
    return jsonify({"success": True, "message": "Order placed successfully."})
