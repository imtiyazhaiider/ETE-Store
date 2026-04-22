@app.route('/')
def home():
    from models import Product
    products = Product.query.all()
    return render_template('home.html', products=products)

from models import Wishlist
from flask_login import current_user

@app.route('/')
def home():
    products = Product.query.all()

    wishlist_items = []
    if current_user.is_authenticated:
        wishlist_items = [
            item.product_id for item in Wishlist.query.filter_by(user_id=current_user.id).all()
        ]

    return render_template(
        'home.html',
        products=products,
        wishlist_items=wishlist_items
    )