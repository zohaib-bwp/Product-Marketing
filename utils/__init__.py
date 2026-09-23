from flask import Blueprint, render_template

user_profile_bp = Blueprint("user_profile", __name__)


@user_profile_bp.route("/profile")
def profile():
    return render_template("profile.html", user={"name": "Customer"})
