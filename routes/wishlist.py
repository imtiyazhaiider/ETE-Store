from flask import Blueprint, redirect, request
from flask_login import login_required, current_user
from models import Wishlist
from extensions import db

wishlist_bp = Blueprint('wishlist', __name__)

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