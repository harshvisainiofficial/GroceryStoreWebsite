import os
from flask import Flask, render_template, request, flash
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# SECRET KEY ---------->>
app.secret_key = 'this_is_mysecretkey@secret.com'

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "Grocery store.db")
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

# DATABASE -------->>

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email_id = db.Column(db.String, unique=True)
    password = db.Column(db.String)

class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_name = db.Column(db.String, unique=True)

class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_name = db.Column(db.String, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.category_id"))
    manufacturing_date = db.Column(db.String)
    expiry_date = db.Column(db.String)
    price = db.Column(db.Numeric)
    stock = db.Column(db. Integer)

class Bag(db.Model):
   __tablename__ = 'bag'
   bag_id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True)
   user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
   tprice = db.Column(db.Integer)
   status = db.Column(db.String, default="pending")

class Shopping_details(db.Model):
  __tablename__ = 'shopping_details'
  sr_no = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
  bag_id = db.Column(db.Integer, db.ForeignKey("bag.bag_id"))
  product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"))
  quantity = db.Column(db.Integer, default=1)
  price = db.Column(db.Integer)

@app.route("/")
def home():
  return render_template("index.html")

# USER REGISTRATION ----->>

@app.route("/userlogin/<ms>")
def user_login(ms):
  return render_template("userlogin.html", ms=ms)

# USER LOGIN ----->>

@app.route("/login/<msg>")
def login(msg):
   return render_template("login.html", msg=msg)
   
# ADMIN LOGIN ----->>

@app.route("/adminlogin")
def admin_login():
  return render_template("adminlogin.html")  

# STORE MANAGER PAGE ------>>

@app.route("/storemaneger", methods=['POST'])
def store_manager():
  email = request.form.get('email')
  password = request.form.get('password')
  if email  == "admin@store.com" and password == "adminlogin":
    data = Category.query.all() 
    return render_template('category.html', data=data)
  else:
    return "<h1>Invalid user id or password</h1>"
  
# REGISTRATION INTO DATABASE AND STORE SHOPPING PAGE ------->>

@app.route("/storeshopping", methods=["get", "post"])
def store_shopping():
  email_id = request.form.get('email_id')
  password = request.form.get('password')
  if email_id != ""  and password != "":
    if request.method == 'POST':
      user = User(email_id=email_id, password=password)
      db.session.add(user)
      try:
         db.session.commit()
      except IntegrityError:
        msg = "Looks like you are already registered, login here to proceed"
        return redirect(url_for('login', msg=msg))
      user1 = User.query.filter_by(email_id=email_id).first()
      user_id = user1.user_id
      bag = Bag(user_id=user_id)
      db.session.add(bag)
      db.session.commit()
  else:
    return "<h1>Details are missing</h1>"
  bag1 = Bag.query.order_by(Bag.bag_id.desc()).first()
  bag_id = bag1.bag_id
  data1 = Category.query.all()
  data2 = Product.query.all()
  return render_template('shopstore.html', data1=data1, data2=data2, bag_id=bag_id, email_id=email_id)

# LOGIN AND STORE SHOPPING PAGE
  
@app.route("/store", methods=["get", "post"])
def store():
  email_id = request.form.get('email_id')
  password = request.form.get('password')
  if email_id != ""  and password != "":
    if request.method == 'POST':
      user1 = User.query.filter_by(email_id=email_id).first()
      if user1:
        user_id = user1.user_id
        bag = Bag(user_id=user_id)
        db.session.add(bag)
        db.session.commit()

        bag1 = Bag.query.order_by(Bag.bag_id.desc()).first()
        bag_id = bag1.bag_id
        data1 = Category.query.all()
        data2 = Product.query.all()
        return render_template('shopstore.html', data1=data1, data2=data2, bag_id=bag_id, email_id=email_id)
      else:
         ms = 'Looks like you have not registered'
         return redirect(url_for('user_login', ms=ms))
  else:
    return "<h1>Details are missing</h1>"
  

# ADD CATEGORY TO DATABASE -------->>

@app.route("/addcategory", methods=['GET','POST'])
def addcategory():
  if request.method == 'POST':
    category_name = request.form.get("category_name")
    if category_name != "":
      category = Category(category_name=category_name)
      db.session.add(category)
      try:
        db.session.commit()
      except IntegrityError:
        db.session.rollback()
  data = Category.query.all() 
  return render_template('category.html', data=data)

# EDIT CATEGORY ---------->>
                                        
@app.route("/edit/<category_id>/<category_name>/", methods=['GET'])
def editcategory(category_name, category_id):
    data = Product.query.filter_by(category_id=category_id).all()
    return render_template("editcategory.html", category_name=category_name, category_id=category_id, data=data)
   
    
# ADD PRODUCT TO DATABASE --------->>
  
@app.route("/addproduct/<category_name>/<category_id>", methods=["GET", "POST"])
def addproduct(category_name, category_id):
  if request.method == 'POST':
    product_name = request.form.get("product_name")
    category_id = request.form.get("category_id")
    manufacturing_date = request.form.get("manufacturing_date")
    expiry_date = request.form.get("expiry_date")
    price = request.form.get("price")
    stock = request.form.get("stock")
    if product_name != "":
      product = Product(product_name=product_name, category_id=category_id, manufacturing_date=manufacturing_date, expiry_date=expiry_date, price=price, stock=stock)
      db.session.add(product)
      try:
        db.session.commit()
      except IntegrityError:
        db.session.rollback()
  return redirect(url_for('editcategory', category_name=category_name , category_id= category_id))
    
# DELETE CATEGORY AND ASSOCIATED PRODUCTS --------->>

@app.route("/deletecategory/<category_id>", methods=["POST"])
def deletecategory(category_id):
    category = Category.query.get(category_id)
    if category:
        products = Product.query.filter_by(category_id=category_id).all()
        for product in products:
            db.session.delete(product)
        db.session.delete(category)
        db.session.commit()
    return redirect(url_for('addcategory'))

# CHANGE CATEOGRY NAME ---------->>

@app.route("/changename/<category_id>/", methods=["GET", "POST"])
def changecategory(category_id):
  category = Category.query.get(category_id)
  if category:
    category_name = request.form.get("category_name")
    category.category_name = category_name
    db.session.commit()
    return redirect(url_for('editcategory', category_name=category_name , category_id= category_id))

# EDIT PRODUCT IN DATABASE ----------->>

@app.route("/editproduct/<category_name>/<category_id>/<product_id>", methods=["GET", "POST"])
def changeproduct(product_id, category_id, category_name):
  product = Product.query.get(product_id)
  if product:
    product_name = request.form.get("product_name")
    category_id = request.form.get("category_id")
    manufacturing_date = request.form.get("manufacturing_date")
    expiry_date = request.form.get("expiry_date")
    price = request.form.get("price")
    stock = request.form.get("stock")
    product.product_name = product_name
    product.category_id=category_id
    product.manufacturing_date=manufacturing_date
    product.expiry_date=expiry_date
    product.price=price
    product.stock=stock
    db.session.commit()
    return redirect(url_for('editcategory', category_name=category_name , category_id=category_id))

# DELETE PRODUCT ---------->>

@app.route("/deleteproduct/<product_id>/<category_id>", methods=["POST"])
def deleteproduct(product_id, category_id):
    product = Product.query.get(product_id)
    category = Category.query.get(category_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for("editcategory", category_name=category.category_name, category_id=category.category_id))

# edit product details -------->>

@app.route("/edit/<category_id>/<product_id>/", methods=["GET", "POST"])
def editproduct(product_id, category_id):
  data = Product.query.filter_by(product_id=product_id)
  category = Category.query.get(category_id)
  return render_template("editproduct.html", product_id=product_id, category_id=category_id, category_name=category.category_name, data=data)


# STORING PRODUCTS IN CART DATABASE

@app.route("/storeshop/<email_id>/<bag_id>", methods=["get", "post"])
def store_shop(email_id, bag_id):
  shopping_details = Shopping_details.query.filter_by(bag_id=bag_id)
  data = [ item.product_id for item in shopping_details]
  data1 = Category.query.all()
  data2 = Product.query.all()
  return render_template('shopstore.html', data=data, data1=data1, data2=data2, bag_id=bag_id, email_id=email_id)

# SEARCH FUNCTIONATITY ----------->>

@app.route("/search/<email_id>/<bag_id>", methods=["post"])
def search(email_id, bag_id):
    search_query = request.form.get("search_query")
    data1 = Category.query.all()
    data2 = Product.query.all()
    matched_products = [item2 for item2 in data2 if search_query.lower() in item2.product_name.lower()]
    matched_categories = [item1 for item1 in data1 if search_query.lower() in item1.category_name.lower()]
    return render_template('shopstore.html', data1=data1, data2=data2, bag_id=bag_id, email_id=email_id, matched_products=matched_products, matched_categories=matched_categories, search_query=search_query)

# ADDING TO CART ------>>

@app.route("/addtocart/<email_id>/<bag_id>/<product_id>", methods=['GET', 'POST'])
def addtocart(bag_id, product_id, email_id):
   product = Product.query.get(product_id)
   shopping_details = Shopping_details(bag_id=bag_id, product_id=product_id, price=float(product.price))
   db.session.add(shopping_details)
   db.session.commit()
   data = Shopping_details.query.filter_by(product_id=product_id, bag_id=bag_id).all()
   return redirect(url_for('store_shop', data=data, email_id=email_id, bag_id=bag_id, product_id=product_id))

   
# OPENING CART -------->>

@app.route("/opencart/<bag_id>", methods=['post', 'get'])
def opencart(bag_id):
   data1 = Shopping_details.query.filter_by(bag_id=bag_id).all()
   data2 = Product.query.all()
   total = 0
   for item in data1:
     total += item.price
   return render_template("cart.html", data1=data1, data2=data2, bag_id=bag_id, total=total)

# Confirm product Quantity ------->>

@app.route("/confirmproduct/<bag_id>/<sr_no>/<product_id>/<price>", methods=['GET', 'POST'])
def confirmproduct(sr_no, bag_id, price, product_id):
   shopping_details = Shopping_details.query.get(sr_no)
   product = Product.query.get(product_id)
   if shopping_details:
      quantity = int(request.form.get("quantity"))
      if quantity <= product.stock:
         shopping_details.quantity = quantity
         shopping_details.price = float(price) * float(quantity)
         db.session.commit()
      else:
         flash(f"Only {product.stock} unit of {product.product_name} available in stock", "danger")
      return redirect(url_for('opencart', bag_id=bag_id))
   
# DELETE FROM CART ----------->>
   
@app.route("/deletefromcart/<bag_id>/<product_id>", methods=["GET", "POST"])
def deletefromcart(bag_id, product_id):
   shopping_details = Shopping_details.query.filter_by(bag_id=bag_id, product_id=product_id).first()
   db.session.delete(shopping_details)
   db.session.commit()
   return redirect(url_for("opencart", bag_id=bag_id))

# ORDER CONFIRM -------------->>

@app.route("/orderconfirm/<bag_id>/<total>", methods=["POST", "GET"])
def orderconfirm(bag_id, total):
  data1 = Shopping_details.query.filter_by(bag_id=bag_id).all()
  if len(data1) > 0 :
     data2 = Product.query.all()
     bag = Bag.query.get(bag_id)
     bag.tprice = total
     bag.status = "confirmed"
     db.session.commit()
     for item2 in data2:
        for item1 in data1:
           if item1.product_id == item2.product_id:
              if item2.stock >= item1.quantity:
                 item2.stock = item2.stock - item1.quantity
                 db.session.commit()
     return render_template("ordered.html", total=total, data1=data1, data2=data2)
  else:
     return "<h1>Order something first</h1>"

if __name__ == "__main__":
  app.run(debug=True)


