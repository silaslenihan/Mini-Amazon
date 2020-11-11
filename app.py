from flask import *
import sqlite3, hashlib, os
from functools import wraps
from werkzeug.utils import secure_filename
#from form import ItemSearchForm
import json
import os
import psycopg2
from datetime import date



conn = psycopg2.connect(
user="rwrcuqxo",
password="fjAbl6HJjop7bDM9L3zfMZ9c_yT9wdM8",
host="lallah.db.elephantsql.com",
port="5432"
)
cur = conn.cursor()


app = Flask(__name__)
# Secret key necessary for session login
app.secret_key = 'sahara'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

global usernameID
global nameID


# all of the following method are required to be implemented
# there will be some function not included but required to be done
# follow the project description for detail

# my implementation is based on sqlite3, you are free to change it to sqlAlchemy



# Require user to login to access site
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/profileHome')
@login_required
def getUserDetails():
    username = session['username']
    name = session['name']
    email = session['email']
    usernameQuery = "'"+str(username)+"'"
    cur = conn.cursor()
    checkSeller = "SELECT * FROM Sellers WHERE username = %s" % (usernameQuery)
    cur.execute(checkSeller)
    version = cur.fetchall()
    seller=""
    if len(version)==0:
        seller="No"
    else:
        seller="Yes"
    info = []
    info.append({
        "name": name,
        "email": email,
        "username": username,
        "seller": seller
    })
    return render_template('profileHome.html', info=info)

@app.route('/', methods=['GET', 'POST'])
@login_required
def root():
    # Need to adjust how average rating is calculated
    cur = conn.cursor()
    query = "SELECT item_id, name, avg_rate FROM ITEMS ORDER by avg_rate desc LIMIT 3;"
    cur.execute(query)
    results = cur.fetchall()
    items = []
    for result in results:
        items.append({
            "item_id": result[0],
            "item_name": result[1],
            "avg_rate": result[2]
            })
    return render_template('home.html', items =items)

@app.route('/results', methods=['GET', 'POST'])
@login_required
def search_results():
    # Fix for SQL injection attack prevention
    search=request.args['product'].lower()
    search="'%"+str(search)+"%'"
    cur = conn.cursor()
    #Prevent SQL injection
    query="SELECT DISTINCT * FROM items WHERE LOWER (cat_name) LIKE %s OR LOWER (name) LIKE %s;" % (search, search)
    cur.execute(query)
    version = cur.fetchall()
    data=[]
    for row in version:
        data_row = {}
        data_row['item_id'] = row[0]
        data_row['name'] = row[2]
        data_row['category'] = row[1]
        data_row['rating'] = row[3]
        data.append(data_row)
    return render_template('result.html', item = data)


@app.route("/productDescription", methods=['GET', 'POST'])
@login_required
def productDescription():
    # Make sure this still aligns with updated rating method
    placetaker = ''
    item_id = int(request.args['itemid'])
    print(item_id)
    cur = conn.cursor()
    # get matching item from db
    query1 = "SELECT * FROM Items WHERE item_id = %d;" % int(item_id)
    cur.execute(query1)
    results1 = cur.fetchall()[0]
    # get parameters we need for product page
    name = results1[2]
    description = results1[5]
    rating = results1[3]
    # get matching sellers from db
    query2 = f"SELECT * FROM SellsItem WHERE item_id = {item_id}"
    cur.execute(query2)
    results2 = cur.fetchall()
    # get list of sellers who sell that item
    seller_list = []
    for result in results2:
        seller_list.append(result[0])
    # get matching reviews from db
    query3 = f"SELECT * FROM Reviews WHERE item_id = {item_id}"
    cur.execute(query3)
    results3 = cur.fetchall()
    # get list of reviews about that item
    reviews_list = []
    for result in results3:
        review = {}
        review['username'] = result[0]
        review['item_id'] = result[1]
        review['date_time'] = result[2]
        review['content'] = result[3]
        review['rating'] = result[4]
        reviews_list.append(review)

    data = {
        "item_id": item_id,
        "item_name": name,
        "description": description,
        "rating": rating,
        "sellers_list": seller_list,
        "reviews_list": reviews_list
    }
    print(data)

    return render_template("productDescription.html", data =data)

@app.route("/add")
@login_required
def add():
    # Probably not necessary

    placetaker = ''
    return render_template('add.html', placetaker =placetaker)

@app.route("/addItem", methods=["GET", "POST"])
@login_required
def addItem():
    # Seller adds a new product to sell, this will involve INSERT into the items table,
    # Check whether the product is already sold

    print(msg)
    return redirect(url_for('root'))

@app.route("/remove")
@login_required
def remove():
    # Maybe not necessary
    data = ''
    return render_template('remove.html', data=data)

@app.route("/removeItem")
@login_required
def removeItem():
    # Seller removes item, no longer wants to sell it

    print(msg)
    return redirect(url_for('root'))

@app.route("/updateProfile", methods=["GET", "POST"])
@login_required
def updateProfile():
    # Come back
    return redirect(url_for('editProfile'))

@app.route("/login", methods = ['GET', 'POST'])
def login():
    error=None
    if request.method == 'POST':
        user = str(request.form['username'])
        passwrd = str(request.form['password'])
        user = "'"+str(user)+"'"
        passwrd = "'"+str(passwrd)+"'"
        cur = conn.cursor()
        query = "SELECT * FROM Users WHERE username = %s AND password = %s;" % (user, passwrd)
        cur.execute(query)
        version = cur.fetchall()
        if len(version) == 0:
            error = 'Invalid Username / Password'
        else:
            session['logged_in'] = True
            session['username'] = str(version[0][0])
            session['email'] = str(version[0][3])
            session['name'] = str(version[0][2])
            session['balance'] = str(version[0][5])
            isSeller = "SELECT * FROM Sellers WHERE username = %s;" % user
            cur = conn.cursor()
            cur.execute(isSeller)
            version2 = cur.fetchall()
            if len(version2)==0:
                session['seller']=False
            else:
                session['seller']=True
            flash('You have logged in! Hi '+str(version[0][2])+'!')
            print(version[0])
            nameID = version[0][2]
            usernameID = version[0][0]
            return redirect(url_for('root'))
    return render_template('login.html', error=error)

@app.route("/logout")
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('name', None)
    session.pop('balance', None)
    session.pop('email', None)
    session.pop('seller', None)
    flash('You have logged out!')
    return redirect(url_for('login'))

@app.route("/addToCart")
@login_required
def addToCart():
    # Add item_id to user's cart based on their userID
    # One user can only have one cart at a time

    print('')
    return redirect(url_for('root'))

@app.route("/cart", methods=['GET', 'POST'])
@login_required
def cart():
    # Simply select all the items in a user's cart and display them
    username = "'" + str(session['username']) + "'"
    cur = conn.cursor()
    getItems = "WITH user_items AS (SELECT C.item_id, C.quantity," \
               "C.price_per_item, C.seller_username FROM Cart C WHERE username = %s)," \
               "user_items_with_info AS (SELECT UI.item_id, UI.seller_username, UI.quantity," \
               "UI.price_per_item, I.name, I.cat_name, I.avg_rate," \
               "I.description FROM user_items UI, Items I WHERE " \
               "UI.item_id = I.item_id) SELECT * FROM user_items_with_info;" % username
    cur.execute(getItems)
    cartItems = cur.fetchall()
    items = []
    for row in cartItems:
        data_row = {}
        data_row['item_id'] = row[0]
        data_row['seller_username'] = row[1]
        data_row['quantity'] = row[2]
        data_row['price_per_item'] = row[3]
        data_row['name'] = row[4]
        data_row['cat_name'] = row[5]
        data_row['avg_rate'] = row[6]
        data_row['description'] = row[7]
        items.append(data_row)
    return render_template('cart.html', items=items)

@app.route("/removeFromCart")
@login_required
def removeFromCart():

    # REMOVE item_id from user's cart based on their username
    # How do we get username?

    return redirect(url_for('root'))


@app.route("/purchase", methods=['GET', 'POST'])
@login_required
def purchase():
    return render_template("reviews.html", error=msg)

def pass_valid(p1, p2):
    if p1 == p2:
        return True
    return False

import datetime
@app.route("/addreview", methods = ['GET', 'POST'])
@login_required
def addreview():
    item_id = request.args['itemid']
    if request.method == 'POST':
        username= session['username']
        username = "'" +str(username)+"'"
        day=str(date.today())
        day = "'"+str(day)+"'"
        content = str(request.form['body'])
        content = "'"+str(content)+"'"
        stars= float(request.form['numstars'])
        addRev = "INSERT INTO Reviews VALUES (%s, %d, %s, %s, %d);" % (username, int(item_id), day, content, stars)
        cur=conn.cursor()
        try:
            cur.execute(addRev)
            flash("Review submitted successfully")
        except:
            flash("Cannot review an item you are selling!")
        return redirect(url_for('productDescription', itemid=item_id))
    getName = "SELECT name FROM Items WHERE item_id = %d;" % int(item_id)
    cur = conn.cursor()
    cur.execute(getName)
    item_name = cur.fetchall()[0][0]
    item = {
        "itemid": item_id,
        "itemname": item_name
    }
    return render_template("reviews.html", item=item)


@app.route("/addbalance", methods=['GET', 'POST'])
@login_required
def addbalance():
    error = None
    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
        except:
            error = "Please enter a numerical value"
            return render_template("addBalance.html", error=error)
        username=session['username']
        balance=float(session['balance'])
        balance+=amount
        username = "'" + str(username) + "'"
        cur = conn.cursor()
        update = "UPDATE Users SET balance = %d WHERE username = %s;" % (balance, username)
        cur.execute(update)
        session['balance']=str(balance)
        return render_template("addBalance.html", error=error)
    return render_template("addBalance.html", error=error)


@app.route("/showaverage", methods=['GET', 'POST'])
@login_required
def showaverage():
    return render_template("reviews.html", error=msg)


@app.route("/forgot", methods = ['GET', 'POST'])
def forgot():
    error = None
    if request.method == 'POST':
        username = str(request.form['username'])
        if username == "":
            error = "Please enter a username"
            return render_template("forgot.html", error=error)
        answer = str(request.form['answer'])
        if answer == "":
            error = "Please enter a response"
            return render_template("forgot.html", error=error)
        else:
            username = "'" + str(username) + "'"
            cur = conn.cursor()
            query1 = "SELECT secret FROM Users WHERE username = %s;" % username
            cur.execute(query1)
            correct = cur.fetchall()
            if len(correct)==0:
                error = "This username is not in our system"
                return render_template("forgot.html", error=error)
            if correct[0][0] == answer:
                cur = conn.cursor()
                query2 = "SELECT password FROM Users WHERE username = %s;" % username
                cur.execute(query2)
                password = cur.fetchall()[0][0]
                return render_template("forgot.html", correct=password)
            else:
                error = "Your response is incorrect"
                return render_template("forgot.html", error=error)

    return render_template("forgot.html", error=error)

@app.route("/registerationForm", methods = ['GET', 'POST'])
def registrationForm():
    error = None
    if request.method == 'POST':
        name = str(request.form['name'])
        if name == "":
            error = "Please enter a name"
            return render_template("register.html", error=error)
        email = str(request.form['email'])
        if email == "":
            error = "Please enter an email"
            return render_template("register.html", error=error)
        address = str(request.form['address'])
        if address == "":
            error = "Please enter an address"
            return render_template("register.html", error=error)
        username = str(request.form['username'])
        if username == "":
            error = "Please enter a username"
            return render_template("register.html", error=error)
        passwrd = str(request.form['password1'])
        if len(passwrd) < 8:
            error = "Password must be at least 8 characters"
            return render_template("register.html", error=error)
        confirmPass = str(request.form['password2'])
        if not pass_valid(passwrd, confirmPass):
            error = 'Passwords do not match, try again.'
            return render_template("register.html", error=error)
        secret = str(request.form['name'])
        if secret == "":
            error = "Please enter a secret answer"
            return render_template("register.html", error=error)
        seller = str(request.form['seller'])
        possibleOptions=['y','n','yes','no']
        if seller.lower() not in possibleOptions:
            error = "Please indicate if you would like to be a seller"
            return render_template("register.html", error=error)
        name = "'" + str(name) + "'"
        email = "'" + str(email) + "'"
        username = "'" + str(username) + "'"
        address = "'" + str(address) + "'"
        passwrd = "'" + str(passwrd) + "'"
        secret = "'" + str(secret) + "'"
        cur = conn.cursor()
        query1 = "SELECT * FROM Users WHERE email = %s;" % email
        cur.execute(query1)
        version1 = cur.fetchall()
        if len(version1) == 1:
            error = 'Email already use, try Forgot Password.'
            return render_template("register.html", error=error)
        cur = conn.cursor()
        query2 = "SELECT * FROM Users WHERE username = %s;" % username
        cur.execute(query2)
        version2 = cur.fetchall()
        if len(version2) == 1:
            error = 'Username already in use, pick another one or try Forgot Password.'
            return render_template("register.html", error=error)
        else:
            cur = conn.cursor()
            insert = "INSERT INTO Users VALUES(%s, %s, %s, %s, %s, 0, False, %s);" % (username, passwrd, name, email, address, secret)
            cur.execute(insert)
            if seller.lower() == 'y' or seller.lower()=='yes':
                insert2= "INSERT INTO Sellers VALUES (%s);" % (username)
                cur.execute(insert2)
            if seller.lower() =='n' or seller.lower() == 'no':
                insert3= "INSERT INTO Buyers VALUES (%s);" % (username)
                cur.execute(insert3)
            flash('Registered successfully')
            return redirect(url_for('login'))
    return render_template('register.html', error=error)


def parse(data):
    ans = []
    return ans

if __name__ == '__main__':
    app.run(debug=True)
