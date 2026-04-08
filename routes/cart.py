from flask import Blueprint, session, redirect, url_for, render_template
from models import Product

cart = Blueprint('cart', __name__, url_prefix='/cart')


@cart.route('/add/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    session['cart'] = cart
    return redirect(url_for('cart.view_cart'))


@cart.route('/')
def view_cart():
    cart = session.get('cart', {})
    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            products.append({
                'product': product,
                'quantity': quantity
            })
            total += product.price * quantity

    return render_template('cart.html', products=products, total=total)


@cart.route('/remove/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    session['cart'] = cart
    return redirect(url_for('cart.view_cart'))