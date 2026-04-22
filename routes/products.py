@app.route('/')
def home():
    from models import Product
    products = Product.query.all()
    return render_template('home.html', products=products)