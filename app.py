import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# This handles the database file in the root folder
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'car_corals.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- MODELS ---
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
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

with app.app_context():
    db.create_all()

# --- ROUTES ---
@app.route('/')
def index():
    products = Product.query.all()
    categories = Category.query.all()
    banners = Banner.query.all()
    return render_template('index.html', products=products, categories=categories, banners=banners)

@app.route('/admin')
def admin():
    products = Product.query.all()
    categories = Category.query.all()
    banners = Banner.query.all()
    return render_template('admin.html', products=products, categories=categories, banners=banners)

# API/Action Routes
@app.route('/save_product', methods=['POST'])
def save_product():
    p_id = request.form.get('id')
    p = Product.query.get(p_id) if p_id else Product()
    p.name, p.brand, p.category = request.form['name'], request.form['brand'], request.form['category']
    p.car_model, p.quality, p.price = request.form['car_model'], request.form['quality'], request.form['price']
    p.img1, p.img2, p.img3 = request.form['img1'], request.form['img2'], request.form['img3']
    p.video, p.details = request.form['video'], request.form['details']
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
    db.session.add(Category(name=request.form['name'], icon=request.form['icon']))
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
    # This block only runs on your local computer
    app.run(debug=True)
    
