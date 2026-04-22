from app import app
from models import Product
from extensions import db
import csv

with app.app_context():
    with open('products.csv', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            product = Product(
                name=row['name'],
                description=row['description'],
                price=float(row['price']),
                image=row['image']
            )
            db.session.add(product)

        db.session.commit()

    print("✅ Products imported successfully!")