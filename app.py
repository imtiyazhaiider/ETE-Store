from flask import Flask, app, render_template, request
from config import Config
from extensions import db, login_manager
from models import User, Product


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # HOME PAGE
    @app.route('/')
    def home():
        products = Product.query.all()
        return render_template('home.html', products=products)

    # PRODUCT DETAIL PAGE
    @app.route('/product/<int:product_id>')
    def product_detail(product_id):
        product = Product.query.get_or_404(product_id)
        return render_template('product_detail.html', product=product)

    # IMPORT & REGISTER ALL BLUEPRINTS
    from routes.auth import auth
    from routes.admin import admin
    from routes.cart import cart
    from routes.orders import orders   # ✅ IMPORTANT
    from routes.wishlist import wishlist_bp
    
    app.register_blueprint(wishlist_bp)
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(cart)
    app.register_blueprint(orders)     # ✅ IMPORTANT

    @app.route('/search')
    def search():
        query = request.args.get('q')

        if query:
            products = Product.query.filter(Product.name.ilike(f"%{query}%")).all()
        else:
            products = []

        return render_template('home.html', products=products)

    return app


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

@app.route('/make-admin')
def make_admin():
    from models import User
    from extensions import db

    user = User.query.filter_by(email="imtiyazhaider00@gmail.com").first()

    if user:
        user.is_admin = True
        db.session.commit()
        return "Admin created successfully!"

    return "User not found"