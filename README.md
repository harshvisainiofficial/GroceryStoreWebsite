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

Following are the major technologies used in the project<br>
● flask<br><br>
    ○ Flask<br>
    ○ render_template <br>
    ○ request<br>
    ○ flash<br>
    ○ redirect<br>
    ○ url_for<br>
● flask_sqlalchemy<br><br>
    ○ SQLAlchemy<br>
● sqlalchemy.exe <br><br>
    ○ Integrityerror<br>

The IntegrityError is used to resolve the error made when the unique value constraint of the 
database is violated.


# DB Schema Design

● Product<br><br>
    ○ product_id :- primary key, auto increment, unique, not null<br>
    ○ product_name :- unique, not null<br>
    ○ category_id :- not null, foreign key(category)<br>
    ○ manufacturing_date <br>
    ○ expiry_date <br>
    ○ price :- not null<br>
    ○ stock :- not null<br>
● category<br><br>
    ○ category_id :- primary key, not null, unique, auto increment<br>
    ○ category_name :- not null, unique<br>
● user<br><br><br>
    ○ user_id :- primary key, not null, unique, auto increment<br>
    ○ email_id :- not null, unique <br>
    ○ password :- not null<br>
● bag<br><br><br>
    ○ bag_id :- primary key, not null, unique, auto increment<br>
    ○ user_id :- not null, foreign key(user)<br>
    ○ tprice <br>
    ○ status :- not null<br>
● shopping_details<br><br>
    ○ sr_no :- primary key, not null, unique, auto increment<br>
    ○ bag_id :- not null, foreign key(bag)<br>
    ○ product_id :- not null, foreign key(product)<br>
    ○ quantity :- not null<br>
    ○ price :- not null<br>

The reason behind using this structure was that it was the most sorted and easy to work
with configuration. Having a single table for bag(1 bag for every time they shop) and
shopping_details for product information is convenient to store the shopping details.

# API Design

All the APIs have been created using flask, following are the major functionalities for
which APIs have been created.<br>
● For the crud functionalities<br>
● For decreasing the stocks when the product is brought<br>
● Ability to show a product is out of stock<br>
● To make sure that the user has not logged in with invalid user id or password

# Architecture and Features

The project and its code is organised in the following way:<br>

● GroceryStoreWebsite :- This is the main repository.<br><br>
    ○ .vscode <br>
    ○ __pycache__<br>
    ○ templates:- It contains the HTML code <br>
    ○ app.py:- This is the main page which is running all the templates<br>
    ○ Grocery Store.db :- This is the database in which all the data is being stored.<br>

The application, on running, will first show two login pages.<br>

● Admin Login<br>
● User Login<br><br>

➢ Only the admin can log into the admin login page that also with a specific email ID. Then
the admin or the store manager can see the categories stored in the database and can
add, edit or remove them. It is also possible to see the products available in a particular
category, add new products, edit already added products and delete them if wanted.<br>

➢ Any user can login multiple times to the user page, the user then can buy multiple 
products and add them to cart. The application has the ability to tell the user when the 
product is not available in the stocks and show the total amount of the purchase.
