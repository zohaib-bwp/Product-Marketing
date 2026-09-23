from flask import Blueprint, jsonify, redirect, request, send_from_directory, session, url_for
import os
from werkzeug.security import check_password_hash, generate_password_hash

from database import get_db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET"])
def login_page():
    """Serve the login page."""
    root_dir = os.path.dirname(os.path.dirname(__file__))
    return send_from_directory(root_dir, "login.html")


@auth_bp.route("/register", methods=["GET"])
def register_page():
    """Serve the registration page."""
    root_dir = os.path.dirname(os.path.dirname(__file__))
    return send_from_directory(root_dir, "register.html")


@auth_bp.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required."})

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s LIMIT 1", (email,))
        user = cursor.fetchone()
        cursor.close()

        if not user:
            return jsonify({"success": False, "message": "Invalid email or password."})

        if not check_password_hash(user["password"], password):
            return jsonify({"success": False, "message": "Invalid email or password."})

        session["user_id"] = user["user_id"]
        session["user_name"] = user["name"]
        session["role"] = user.get("role", "customer")

        redirect_path = "/admin" if session["role"] == "admin" else "/products"
        return jsonify({"success": True, "message": "Login successful.", "redirect": redirect_path})
    except Exception as exc:  # pragma: no cover - runtime guard
        return jsonify({"success": False, "message": f"Database error: {exc}"})


@auth_bp.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""
    phone = (data.get("phone") or "").strip()
    address = (data.get("address") or "").strip()

    if not all([name, email, password, phone]):
        return jsonify({"success": False, "message": "Please fill in all required fields."})

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT user_id FROM users WHERE email = %s LIMIT 1", (email,))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "An account with this email already exists."})

        hashed = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (name, email, password, phone, address, role) VALUES (%s, %s, %s, %s, %s, 'customer')",
            (name, email, hashed, phone, address),
        )
        db.commit()
        cursor.close()
        return jsonify({"success": True, "message": "Registration successful. Please log in.", "redirect": "/login"})
    except Exception as exc:  # pragma: no cover - runtime guard
        return jsonify({"success": False, "message": f"Registration failed: {exc}"})


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login_page"))
