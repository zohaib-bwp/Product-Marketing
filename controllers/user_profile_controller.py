from flask import Blueprint, render_template

admin_profile_bp = Blueprint("admin_profile", __name__, url_prefix="/admin")


@admin_profile_bp.route("/profile")
def profile():
    return render_template("admin/profile.html", user={"name": "Admin"})
