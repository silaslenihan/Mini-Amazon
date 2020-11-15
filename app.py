from flask import *
import sqlite3, hashlib, os
from functools import wraps
from werkzeug.utils import secure_filename
#from form import ItemSearchForm
import json
import os
import psycopg2
import datetime
from dateutil.relativedelta import relativedelta


# TODO:
# -modify item
conn = psycopg2.connect(
user="hshgoekz",
password="0-_hWpr8BBMyZe-EO1A0iwRTOEfZzGY8",
host="hattie.db.elephantsql.com",
port="5432"
)
cur = conn.cursor()


app = Flask(__name__)
# Secret key necessary for session login
app.secret_key = 'sahara'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




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
        findMax = "SELECT MAX(price) FROM SellsItem WHERE item_id = %d;" % row[0]
        cur.execute(findMax)
        maxPrice = round(cur.fetchall()[0][0], 2)
        findMin = "SELECT MIN(price) FROM SellsItem WHERE item_id = %d;" % row[0]
        cur.execute(findMin)
        minPrice = round(cur.fetchall()[0][0], 2)
        data_row['range'] = str(minPrice)+" - $"+str(maxPrice)
        data_row['name'] = row[2]
        data_row['category'] = row[1]
        data_row['rating'] = row[3]
        data.append(data_row)
    return render_template('result.html', item = data)

@app.route('/purchaseHistory', methods=['GET', 'POST'])
@login_required
def purchase_history():
    query = f"SELECT * FROM OrderEntry WHERE buyer_username = '{session['username']}';"
    cur.execute(query)
    results = cur.fetchall()
    data = []
    for result in results:
        data_row = {}
        item_id = result[6]
        itemName = "SELECT name FROM Items WHERE item_id = %d;" % item_id
        cur.execute(itemName)
        item_name = str(cur.fetchall()[0][0])
        data_row['order_id'] = result[0]
        data_row['entry_id'] = result[1]
        data_row['item_id'] = item_id
        data_row['item_name'] = item_name
        data_row['seller_username'] = result[9]
        data_row['price_per_item'] = round((result[3]/result[8]), 2)
        data_row['count'] = result[8]
        data_row['purchase_timestamp'] = result[4]
        data_row['delivery'] = result[5]
        data.append(data_row)
    return render_template('purchaseHistory.html', items=data)

@app.route('/sellingHistory', methods=['GET', 'POST'])
@login_required
def selling_history():
    username = session['username']
    query = f"SELECT * FROM OrderEntry WHERE seller_username = '{username}';"
    cur.execute(query)
    results = cur.fetchall()
    data = []
    for result in results:
        data_row = {}
        item_id = result[1]
        query1 = f"select name from Items where item_id = {item_id};"
        cur.execute(query1)
        item_name = cur.fetchall()[0][0]

        data_row['item_image'] = ''
        data_row['item_name'] = item_name
        data_row['buyer_username'] = result[2]
        payment_amount = result[3]
        count = result[8]
        price = round((payment_amount/count), 2)
        data_row['price_per_item'] = price
        data_row['quantity'] = result[8]
        data_row['timestamp'] = result[4]
        data_row['item_id'] = item_id
        data_row['totalSale'] = round((price*count), 2)
        data.append(data_row)
    return render_template('sellingHistory.html',data=data)

@app.route('/sellingList', methods=['GET'])
@login_required
def sellingList():
    username = session['username']
    query = f"select * from SellsItem where seller_username = '{username}';"
    cur.execute(query)
    results = cur.fetchall()
    data = []
    for result in results:
        item_id = result[1  ]
        query1 = f"select name from Items where item_id = {item_id};"
        cur.execute(query1)
        item_name = cur.fetchall()[0][0]
        data_row = {}
        data_row['item_image'] = ''
        data_row['item_name'] = item_name
        data_row['price'] = result[3]
        data_row['stock'] = result[4]
        data_row['item_id'] = item_id
        data.append(data_row)
    return render_template('sellingList.html', data=data)


@app.route("/productDescription", methods=['GET', 'POST'])
@login_required
def productDescription():
    item_id = int(request.args['itemid'])
    cur = conn.cursor()
    checkExists = "SELECT item_id FROM Items;"
    cur.execute(checkExists)
    allItems = cur.fetchall()
    exists=False
    for i in range(len(allItems)):
        if allItems[i][0] == item_id:
            exists=True
    if exists == False:
        flash("Item does not exist!")
        return redirect(url_for('root'))
    # get matching item from db
    query1 = "SELECT * FROM Items WHERE item_id = %d;" % int(item_id)
    cur.execute(query1)
    results1 = cur.fetchall()[0]
    # get parameters we need for product page
    name = results1[2]
    description = results1[5]
    rating = results1[3]
    # get matching sellers from db
    query2 = f"SELECT * FROM SellsItem WHERE item_id = {item_id};"
    cur.execute(query2)
    results2 = cur.fetchall()
    # get list of sellers who sell that item
    currUserSellsItem = False
    seller_list = []
    for result in results2:
        seller = {}
        if (result[0]==session['username']):
            currUserSellsItem = True
        seller['username'] = result[0]
        seller['price'] = result[3]
        seller['stock'] = result[4]
        seller_list.append(seller)
    # get matching reviews from db
    query3 = f"SELECT * FROM Reviews WHERE item_id = {item_id};"
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
    return render_template("productDescription.html", data =data, sellsItem = currUserSellsItem)


@app.route("/addItem", methods=["GET", "POST"])
@login_required
def addItem():
    username = "'"+str(session['username'])+"'"
    if request.method == 'POST':
        item_name = "'"+str(request.form['name'])+"'"
        # if 2 products have the same name, then their itemID is the same
        cur = conn.cursor()
        checkItemExists = "SELECT item_id FROM Items WHERE name = %s;" % item_name
        cur.execute(checkItemExists)
        exists=cur.fetchall()
        if len(exists) != 0:
            flash('Item name already exists, cannot add item for existing item name.')
            return redirect(url_for('root'))

        item_id = request.form['itemid']
        username = session['username']
        price = str(request.form['price'])
        count = str(request.form['count'])
        if item_id == "-1":
            # new item
            query = "SELECT * FROM ITEMS ORDER BY item_id desc LIMIT 1"
            cur.execute(query)
            result = cur.fetchall()[0]
            item_id = result[0] + 1

            item_name = str(request.form['name'])
            image = str(request.form['image'])
            description = str(request.form['description'])
            category = str(request.form['category'])
            price = str(request.form['price'])
            count = str(request.form['count'])
            # TODO: change 1 to 0 once DB guys fix the setup
            query2 = f"INSERT INTO Items VALUES('{item_id}','{category}','{item_name}',1,0,'{description}');"
            cur.execute(query2)
            query1 = f"INSERT INTO SellsItem VALUES('{str(username)}','{item_id}','{category}','{price}','{count}');"
            cur.execute(query1)
        else:


            query3 = f"SELECT cat_name from items where item_id = {item_id}"
            cur.execute(query3)
            category = cur.fetchall()[0][0]

            query4 = f"INSERT INTO SellsItem VALUES('{str(username)}','{item_id}','{category}','{price}','{count}');"
            cur.execute(query4)
        flash("Item sucessfully listed.")
        conn.commit()
    itemid = request.args.get('itemid', -1)
    itemname = request.args.get('itemname', '')
    return render_template("addItem.html",itemid=itemid,itemname=itemname)

@app.route("/modifyItem", methods=["GET", "POST"])
@login_required
def modifyItem():
    username = "'" +str(session['username'])+"'"
    itemID = int(request.args['item_id'])
    cur= conn.cursor()
    findName="SELECT name FROM Items WHERE item_id = %d;" % itemID
    cur.execute(findName)
    itemName=str(cur.fetchall()[0][0])
    name = {"name": itemName}
    # having trouble with FE interaction 
    return render_template("modifyItem.html", name=name)


@app.route("/removeItem", methods=["GET", "POST"])
@login_required
def removeItem():
    if request.method == 'POST':
        item_id = int(request.form['itemid'])
        seller = "'"+str(session['username'])+"'"
        cur= conn.cursor()
        remove = "DELETE From SellsItem WHERE item_id=%d AND seller_username=%s;" % (item_id, seller)
        cur.execute(remove)
        return redirect(url_for('sellingList'))
    return redirect(url_for('sellingList'))

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

@app.route("/addToCart", methods = ['GET', 'POST'])
@login_required
def addToCart():
    if request.method == 'POST':
        alreadyAdded=False
        itemID = int(request.form['itemid'])
        username = session['username']
        username = "'"+str(username)+"'"
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        seller = request.form['seller']
        seller = "'"+str(seller)+"'"
        cur = conn.cursor()
        checkAlreadyinCart = "SELECT quantity FROM Cart WHERE username = %s and item_id = %d and seller_username=%s;" % (username, itemID, seller)
        cur.execute(checkAlreadyinCart)
        quant = cur.fetchall()
        if len(quant) != 0:
            alreadyAdded=True
            quantity += int(quant[0][0])
        if alreadyAdded:
            cur = conn.cursor()
            updateCart = "UPDATE Cart SET quantity = %d WHERE username=%s AND item_id=%d AND seller_username=%s;" % (quantity, username, itemID, seller)
            cur.execute(updateCart)
            flash("Item(s) added to cart!")
            return redirect(url_for('cart'))
        else:
            cur = conn.cursor()
            addCart = "INSERT INTO Cart VALUES (%d, %s, %d, %.2f, %s);" % (itemID, username, int(quantity), price, seller)
            cur.execute(addCart)
            flash("Item(s) added to cart!")
            return redirect(url_for('cart'))
    return redirect(url_for('cart'))

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
    cur = conn.cursor()
    cost = "SELECT total_price FROM CartSummary WHERE username = %s;" % username
    cur.execute(cost)
    try:
        totalCost = float(cur.fetchall()[0][0])
        totalCost = "{:.2f}".format(totalCost)
    except:
        totalCost=0
        totalCost = "{:.2f}".format(totalCost)
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
    return render_template('cart.html', items=items, cost=totalCost)

@app.route("/removeFromCart", methods=['GET', 'POST'])
@login_required
def removeFromCart():
    username = "'" + str(session['username']) + "'"
    if request.method == 'POST':
        itemID = request.form['item_id']
        seller = "'"+str(request.form['seller'])+"'"
        quantity = (request.form['quantity'])
        cur = conn.cursor()
        removeItems="DELETE FROM Cart WHERE username=%s AND item_id=%d AND seller_username=%s;" % (username, int(itemID), seller)
        cur.execute(removeItems)
        addBacktoStock="UPDATE SellsItem SET stock=stock+%d WHERE seller_username=%s AND item_id=%d;" % (int(quantity), seller, int(itemID))
        cur.execute(addBacktoStock)
        flash("Item(s) removed from cart!")
        return redirect(url_for('cart'))
    return redirect(url_for('cart'))

@app.route("/purchase", methods=['GET', 'POST'])
@login_required
def purchase():
    username = "'" + str(session['username']) + "'"
    cost = "SELECT total_price FROM CartSummary WHERE username = %s;" % username
    cur=conn.cursor()
    cur.execute(cost)
    try:
        totalCost = float(cur.fetchall()[0][0])
    except:
        totalCost = 0
    #Check if user has enough balance
    cur=conn.cursor()
    checkEnoughBalance = "SELECT balance from Users where username = %s;" % username
    cur.execute(checkEnoughBalance)
    userBalance = float(cur.fetchall()[0][0])
    if totalCost>userBalance:
        flash("You do not have enough funds in balance to complete this order!")
        return redirect(url_for('cart'))
    #Update the user balance
    updateBalance = "UPDATE Users Set balance = balance - %.2f WHERE username = %s;" % (totalCost, username)
    session['balance'] = "{:.2f}".format(userBalance - totalCost)
    # Add money to respective seller
    cur= conn.cursor()
    getCartItems = "SELECT * FROM Cart WHERE username = %s;" % username
    cur.execute(getCartItems)
    itemsList = cur.fetchall()
    entry_id = 1
    for row in itemsList:
        newMoney = float(row[2]*row[3])
        seller = "'"+str(row[4])+"'"
        updateSellerBalance = "UPDATE Users SET balance = balance + %.2f WHERE username = %s;" % (newMoney, seller)
        cur.execute(updateSellerBalance)
        # Add each item to order items
        # get category of item
        item_id = int(row[0])
        findCat = "SELECT cat_name FROM Items WHERE item_id = %d;" % item_id
        cur.execute(findCat)
        category = "'"+str(cur.fetchall()[0][0])+"'"
        # get order and delivery date
        dt_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        orderDate = "'" + str(dt_string) + "'"
        delivery = datetime.datetime.now() + relativedelta(weeks=1)
        delivery = "'" + str(delivery.strftime("%Y-%m-%d")) + "'"
        # find max order_id in OrderEntry
        findMax = "SELECT MAX(order_id) FROM OrderEntry;"
        cur.execute(findMax)
        order_id = int(cur.fetchall()[0][0]) + 1
        # Insert to OrderITems
        insertOrder = "INSERT INTO OrderEntry " \
                      "VALUES (%d, %d, %s, %.2f, %s, " \
                      "%s, %d, %s, %d, %s);" % (order_id, entry_id, username, newMoney, orderDate, delivery, item_id, category, row[2], seller)
        cur.execute(insertOrder)
        entry_id += 1
    clearCart = "DELETE FROM Cart WHERE username = %s;" % username
    cur.execute(clearCart)
    return redirect(url_for('purchase_history'))

def pass_valid(p1, p2):
    if p1 == p2:
        return True
    return False

@app.route("/addreview", methods = ['GET', 'POST'])
@login_required
def addreview():
    item_id = request.args['itemid']
    if request.method == 'POST':
        username= session['username']
        username = "'" +str(username)+"'"
        dt_string = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        day = "'"+str(dt_string)+"'"
        content = str(request.form['body'])
        content = "'"+str(content)+"'"
        stars= float(request.form['numstars'])
        cur = conn.cursor()
        checkSeller = "SELECT * FROM SellsItem WHERE seller_username = %s AND item_id=%d;" % (username, int(item_id))
        cur.execute(checkSeller)
        checker=cur.fetchall()
        if len(checker)>0:
            flash("Cannot review an item you are selling!")
            return redirect(url_for('productDescription', itemid=item_id))
        else:
            cur = conn.cursor()
            AlreadyReviewToday = "SELECT * FROM Reviews WHERE username = %s AND item_id=%d AND date_time=%s;" % (username, int(item_id), day)
            cur.execute(AlreadyReviewToday)
            checker2=cur.fetchall()
            if len(checker2)>0:
                flash("Cannot review an item twice on same day!")
                return redirect(url_for('productDescription', itemid=item_id))
            else:
                cur = conn.cursor()
                addRev = "INSERT INTO Reviews VALUES (%s, %d, %s, %s, %d);" % (username, int(item_id), day, content, stars)
                cur.execute(addRev)
                flash("Review submitted successfully")
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
        balance = "{:.2f}".format(balance)
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
                insert4= "INSERT INTO Buyers VALUES (%s);" % (username)
                cur.execute(insert2)
                cur.execute(insert4)
            if seller.lower() =='n' or seller.lower() == 'no':
                insert3= "INSERT INTO Buyers VALUES (%s);" % (username)
                cur.execute(insert3)
            flash('Registered successfully')
            conn.commit()
            return redirect(url_for('login'))
    return render_template('register.html', error=error)


def parse(data):
    ans = []
    return ans

if __name__ == '__main__':
    app.run(debug=True)
