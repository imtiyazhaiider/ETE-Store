from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import login_required, current_user
from models import Product
from extensions import db
import os
from werkzeug.utils import secure_filename

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@login_required
def dashboard():
    if not current_user.is_admin:
        return "Access Denied"

    return render_template("admin_dashboard.html")


@admin.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        return "Access Denied"

    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        description = request.form.get("description")

        image_file = request.files.get("image")
        image_path = None

        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)

            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)

            filepath = os.path.join(upload_folder, filename)
            image_file.save(filepath)

            # ✅ IMPORTANT: store WITHOUT 'static/'
            image_path = f"images/{filename}"

        product = Product(
            name=name,
            price=float(price),
            description=description,
            image=image_path
        )

        db.session.add(product)
        db.session.commit()

        return redirect(url_for('admin.dashboard'))

    return render_template("add_product.html")
@admin.route('/delete-product/<int:id>')
@login_required
def delete_product(id):
    if not current_user.is_admin:
        return "Access Denied"

    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('admin.dashboard'))

import csv

@admin.route('/bulk-upload', methods=['GET', 'POST'])
@login_required
def bulk_upload():
    if not current_user.is_admin:
        return "Access Denied"

    if request.method == "POST":
        file = request.files.get("file")

        if file:
            stream = file.stream.read().decode("UTF8")
            csv_input = csv.DictReader(stream.splitlines())

            for row in csv_input:
                product = Product(
                    name=row['name'],
                    price=float(row['price']),
                    description=row['description'],
                    image=row['image']
                )
                db.session.add(product)

            db.session.commit()

            return redirect(url_for('admin.dashboard'))

    return render_template("bulk_upload.html")

import csv
import shutil

@admin.route('/bulk-upload-advanced', methods=['GET', 'POST'])
@login_required
def bulk_upload_advanced():
    if not current_user.is_admin:
        return "Access Denied"

    if request.method == "POST":
        csv_file = request.files.get("csv_file")
        images = request.files.getlist("images")

        if csv_file:
            # Save images first
            image_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(image_folder, exist_ok=True)

            for img in images:
                if img and img.filename != "":
                    filename = secure_filename(img.filename)
                    img.save(os.path.join(image_folder, filename))

            # Process CSV
            stream = csv_file.stream.read().decode("UTF8")
            csv_input = csv.DictReader(stream.splitlines())

            for row in csv_input:
                product = Product(
                    name=row['name'],
                    price=float(row['price']),
                    description=row['description'],
                    image=row['image']  # must match uploaded image name
                )
                db.session.add(product)

            db.session.commit()

            return redirect(url_for('admin.dashboard'))

    return render_template("bulk_upload_advanced.html")