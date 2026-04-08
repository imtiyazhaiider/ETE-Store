from flask import Blueprint, render_template, request, redirect, session, url_for
from flask_login import current_user, login_required
from models import Product, Order, OrderItem
from extensions import db

orders = Blueprint('orders', __name__, url_prefix='/orders')


# 🛒 CHECKOUT (Send total to PayPal)
@orders.route('/checkout')
@login_required
def checkout():
    cart = session.get('cart', {})

    if not cart:
        return redirect('/')

    total = 0

    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            total += product.price * quantity

    return render_template("payment.html", total=total)


# ✅ SUCCESS (after payment)
@orders.route('/success')
@login_required
def success():
    cart = session.get('cart', {})

    if not cart:
        return redirect('/')

    total = 0

    # Create order
    order = Order(
        user_id=current_user.id,
        total_price=0,
        address="Paid via PayPal"
    )
    db.session.add(order)
    db.session.commit()

    # Add order items
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            total += product.price * quantity

            item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity
            )
            db.session.add(item)

    # Update total
    order.total_price = total
    db.session.commit()

    # Clear cart
    session['cart'] = {}

    return render_template('success.html')


# 📦 ORDER HISTORY
@orders.route('/history')
@login_required
def order_history():
    user_orders = Order.query.filter_by(user_id=current_user.id).all()
    order_data = []

    for order in user_orders:
        items = OrderItem.query.filter_by(order_id=order.id).all()

        detailed_items = []
        for item in items:
            product = Product.query.get(item.product_id)
            if product:
                detailed_items.append({
                    'name': product.name,
                    'price': product.price,
                    'quantity': item.quantity
                })

        order_data.append({
            'order': order,
            'order_items': detailed_items
        })

    return render_template('order_history.html', orders=order_data)