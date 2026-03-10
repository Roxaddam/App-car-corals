import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration
# Render uses a temporary filesystem for SQLite. 
# For a permanent DB, you'd later switch this URI to a PostgreSQL link.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car_corals.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
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
    icon = db.Column(db.String(50)) # Emoji or SVG

class Banner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)

# Create tables
with app.app_context():
    db.create_all()

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

@app.route('/save_product', methods=['POST'])
def save_product():
    p_id = request.form.get('id')
    if p_id:
        p = Product.query.get(p_id)
    else:
        p = Product()
    
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
    p = Product.query.get(id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/save_category', methods=['POST'])
def save_category():
    name = request.form['name']
    icon = request.form['icon']
    if not Category.query.filter_by(name=name).first():
        db.session.add(Category(name=name, icon=icon))
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/save_banners', methods=['POST'])
def save_banners():
    db.session.query(Banner).delete()
    urls = request.form.getlist('banner_urls')
    for url in urls:
        if url.strip():
            db.session.add(Banner(url=url))
    db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
  
