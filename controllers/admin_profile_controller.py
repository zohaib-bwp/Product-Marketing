from flask import Blueprint, flash, redirect, render_template, request, url_for

admin_product_bp = Blueprint("admin_product", __name__, url_prefix="/admin")


@admin_product_bp.route("/products")
def list_products():
    return render_template("admin/products.html", products=[])


@admin_product_bp.route("/product/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        flash("Sample mode: product addition is enabled in the starter app.", "success")
        return redirect(url_for("admin_product.list_products"))
    return render_template("admin/add_edit_product.html", product=None, categories=[])


@admin_product_bp.route("/product/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    if request.method == "POST":
        flash(f"Product #{product_id} updated in demo mode.", "success")
        return redirect(url_for("admin_product.list_products"))
    return render_template("admin/add_edit_product.html", product={"product_id": product_id, "name": "Demo product"}, categories=[])
