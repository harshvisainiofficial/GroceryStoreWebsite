# Author

Harshvi Saini

I am a student of diploma level. Currently I am pursuing bachelors of arts from B.K Birla
Institute of Higher Education, Pilani along with BS in Data Science and Applications from IITM BS.

# Description

This project is about builting a grocery shopping application which has separate login
pages for admin and users. The admin should be able to read, add, remove and edit the 
categories and products in the database and users should be able to add multiple 
products from any category to the cart and shop them.

# Technologies used

Following are the major technologies used in the project
● flask
    ○ Flask
    ○ render_template 
    ○ request
    ○ flash
    ○ redirect
    ○ url_for
● flask_sqlalchemy
    ○ SQLAlchemy
● sqlalchemy.exe 
    ○ Integrityerror

The IntegrityError is used to resolve the error made when the unique value constraint of the 
database is violated.


# DB Schema Design

● Product
    ○ product_id :- primary key, auto increment, unique, not null
    ○ product_name :- unique, not null
    ○ category_id :- not null, foreign key(category)
    ○ manufacturing_date 
    ○ expiry_date 
    ○ price :- not null
    ○ stock :- not null
● category
    ○ category_id :- primary key, not null, unique, auto increment
    ○ category_name :- not null, unique
● user
    ○ user_id :- primary key, not null, unique, auto increment
    ○ email_id :- not null, unique 
    ○ password :- not null
● bag
    ○ bag_id :- primary key, not null, unique, auto increment
    ○ user_id :- not null, foreign key(user)
    ○ tprice 
    ○ status :- not null
● shopping_details
    ○ sr_no :- primary key, not null, unique, auto increment
    ○ bag_id :- not null, foreign key(bag)
    ○ product_id :- not null, foreign key(product)
    ○ quantity :- not null
    ○ price :- not null

The reason behind using this structure was that it was the most sorted and easy to work
with configuration. Having a single table for bag(1 bag for every time they shop) and
shopping_details for product information is convenient to store the shopping details.

# API Design

All the APIs have been created using flask, following are the major functionalities for
which APIs have been created.
● For the crud functionalities
● For decreasing the stocks when the product is brought
● Ability to show a product is out of stock
● To make sure that the user has not logged in with invalid user id or password

# Architecture and Features

The project and its code is organised in the following way:

● GroceryStoreWebsite :- This is the main repository.
    ○ .vscode 
    ○ __pycache__
    ○ templates:- It contains the HTML code 
    ○ app.py:- This is the main page which is running all the templates
    ○ Grocery Store.db :- This is the database in which all the data is being stored.

The application, on running, will first show two login pages.

● Admin Login
● User Login

➢ Only the admin can log into the admin login page that also with a specific email ID. Then
the admin or the store manager can see the categories stored in the database and can
add, edit or remove them. It is also possible to see the products available in a particular
category, add new products, edit already added products and delete them if wanted.

➢ Any user can login multiple times to the user page, the user then can buy multiple 
products and add them to cart. The application has the ability to tell the user when the 
product is not available in the stocks and show the total amount of the purchase.
