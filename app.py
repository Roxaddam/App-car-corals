import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- DATABASE CONFIGURATION ---
# Using your provided PostgreSQL Internal URL
# We use .replace() because SQLAlchemy requires "postgresql://"
RAW_DB_URL = "postgresql://car_corals_db_user:o7H1hjQ5qc99MBEcnm7cHGv7iDupPGfs@dpg-d6p5hr7gi27c73ahcjn0-a/car_corals_db"

app.config['SQLALCHEMY_DATABASE_URI'] = RAW_DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- MODELS ---
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50))
    category = db.Column(db.String(50))
    car_model = db.Column(db.String(100))
    quality = db.Column(db.String(50))
    price = db.Column(db.String(20))
    img1 = db.Column(db.Text)
    img2 = db.Column(db.Text)
    img3 = db.Column(db.Text)
    video = db.Column(db.Text)
    details = db.Column(db.Text)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    icon = db.Column(db.String(50))

class Banner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)

# Auto-create tables on startup
with app.app_context():
    db.create_all()

# --- ROUTES ---
@app.route('/')
def index():
    products = Product.query.all()
    categories = Category.query.all()
    banners = Banner.query.all()
    
    prod_json = [{
        "id": p.id, "name": p.name, "brand": p.brand, "category": p.category,
        "car_model": p.car_model, "quality": p.quality, "price": p.price,
        "img1": p.img1, "img2": p.img2, "img3": p.img3, "video": p.video, "details": p.details
    } for p in products]
    
    return render_template('index.html', products=products, categories=categories, banners=banners, prod_json=prod_json)

@app.route('/admin')
def admin():
    products = Product.query.all()
    categories = Category.query.all()
    banners = Banner.query.all()
    
    # Add this block here to fix the "Undefined" error
    prod_list = [{
        "id": p.id, "name": p.name, "brand": p.brand, "category": p.category,
        "car_model": p.car_model, "quality": p.quality, "price": p.price,
        "img1": p.img1, "img2": p.img2, "img3": p.img3, "video": p.video, "details": p.details
    } for p in products]
    
    # Pass prod_json=prod_list to the template
    return render_template('admin.html', products=products, categories=categories, banners=banners, prod_json=prod_list)
    

@app.route('/save_product', methods=['POST'])
def save_product():
    p_id = request.form.get('id')
    p = Product.query.get(p_id) if p_id else Product()
    p.name = request.form['name']
    p.brand = request.form['brand']
    p.category = request.form['category']
    p.car_model = request.form['car_model']
    p.quality = request.form['quality']
    p.price = request.form['price']
    p.img1 = request.form['img1']
    p.img2 = request.form['img2']
    p.img3 = request.form['img3']
    p.video = request.form['video']
    p.details = request.form['details']
    if not p_id: db.session.add(p)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/delete_product/<int:id>')
def delete_product(id):
    db.session.delete(Product.query.get(id))
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/save_category', methods=['POST'])
def save_category():
    name = request.form['name']
    icon = request.form['icon']
    if name and not Category.query.filter_by(name=name).first():
        db.session.add(Category(name=name, icon=icon))
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/save_banners', methods=['POST'])
def save_banners():
    db.session.query(Banner).delete()
    for url in request.form.getlist('banner_urls'):
        if url: db.session.add(Banner(url=url))
    db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
