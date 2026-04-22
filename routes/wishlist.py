from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, current_user
from models import Wishlist, Product
from extensions import db

wishlist_bp = Blueprint('wishlist', __name__)


# ❤️ VIEW WISHLIST
@wishlist_bp.route('/wishlist')
@login_required
def view_wishlist():

    items = Wishlist.query.filter_by(user_id=current_user.id).all()

    products = []
    for item in items:
        product = Product.query.get(item.product_id)
        if product:
            products.append(product)

    return render_template('wishlist.html', products=products)


# 🔄 TOGGLE (already exists)
@wishlist_bp.route('/wishlist/toggle/<int:product_id>')
@login_required
def toggle_wishlist(product_id):

    item = Wishlist.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()

    if item:
        db.session.delete(item)
    else:
        new_item = Wishlist(
            user_id=current_user.id,
            product_id=product_id
        )
        db.session.add(new_item)

    db.session.commit()

    return redirect(request.referrer or '/')