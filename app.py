from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename
#from form import ItemSearchForm
import json
import os
import psycopg2

conn = psycopg2.connect(
user="lzjtguuz",
password="uR_ejvF_D_y0ZmPVoNezR3Md0uzZfrRP",
host="salt.db.elephantsql.com",
port="5432"
)
cur = conn.cursor()


app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




# all of the following method are required to be implemented
# there will be some function not included but required to be done
# follow the project description for detail

# my implementation is based on sqlite3, you are free to change it to sqlAlchemy

def getLoginDetails():
    with sqlite3.connect('database.db') as conn:
        pass
        #
    conn.close()
    return (loggedIn, firstName, noOfItems)

@app.route('/', methods=['GET', 'POST'])
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
    print(items)
    return render_template('home.html', items =items)

@app.route('/results', methods=['GET', 'POST'])
def search_results():
    # Fix for SQL injection attack prevention
    search=request.args['product'].lower()
    cur = conn.cursor()
    query="SELECT DISTINCT * FROM items WHERE LOWER (cat_name) LIKE '%" +str(search)+"%' OR LOWER (name) LIKE '%" +str(search)+"%';"zzz
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
    print(data)
    return render_template('result.html', item = data)


@app.route("/productDescription", methods=['GET', 'POST'])
def productDescription():
    # Make sure this still aligns with updated rating method

    placetaker = ''
    item_id = request.args['itemid']
    cur = conn.cursor()
    # get matching item from db
    query1 = f"SELECT * FROM Items WHERE item_id = {item_id}"
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
        "item_name": name,
        "description": description,
        "rating": rating,
        "sellers_list": seller_list,
        "reviews_list": reviews_list
    }
    print(data)

    return render_template("productDescription.html", data =data)

@app.route("/add")
def add():
    # Probably not necessary

    placetaker = ''
    return render_template('add.html', placetaker =placetaker)

@app.route("/addItem", methods=["GET", "POST"])
def addItem():
    # Seller adds a new product to sell, this will involve INSERT into the items table,
    # Check whether the product is already sold

    print(msg)
    return redirect(url_for('root'))

@app.route("/remove")
def remove():
    # Maybe not necessary
    data = ''
    return render_template('remove.html', data=data)

@app.route("/removeItem")
def removeItem():
    # Seller removes item, no longer wants to sell it

    print(msg)
    return redirect(url_for('root'))

@app.route("/displayCategory")
def displayCategory():
    # View all items in the same category as the current item

    placetaker = ''
    return render_template('displayCategory.html', placetaker =placetaker)

@app.route("/account/profile")
def profileHome():
    # Depends on buyer or seller user
    # Show order history or show items for sale

    placetaker = ''
    return render_template("profileHome.html", placetaker =placetaker)

@app.route("/account/profile/edit")
def editProfile():
    # Probably not

    placetaker = ''
    return render_template("editProfile.html", placetaker =placetaker)

@app.route("/account/profile/changePassword", methods=["GET", "POST"])
def changePassword():
    # Come back

    placetaker = ''
    return render_template("changePassword.html", placetaker =placetaker)

@app.route("/updateProfile", methods=["GET", "POST"])
def updateProfile():
    # Come back

    return redirect(url_for('editProfile'))

@app.route("/loginForm")
def loginForm():
    # Come back

    return render_template('login.html', error='')

@app.route("/login", methods = ['POST', 'GET'])
def login():
    # Come back

    if True:

        return redirect(url_for('root'))
    else:
        error = 'Invalid UserId / Password'
        return render_template('login.html', error=error)


@app.route("/addToCart")
def addToCart():
    # Add item_id to user's cart based on their userID
    # One user can only have one cart at a time

    print('')
    return redirect(url_for('root'))

@app.route("/cart", methods=['GET', 'POST'])
def cart():
    # Simply select all the items in a user's cart and display them

    placetaker = ''
    return render_template("cart.html", placetaker =placetaker)

@app.route("/removeFromCart")
def removeFromCart():
    # REMOVE item_id from user's cart based on their username
    # How do we get username?

    return redirect(url_for('root'))


@app.route("/purchase", methods=['GET', 'POST'])
def purchase():
    return render_template("reviews.html", error=msg)

@app.route("/logout")
def logout():
    # Need to figure this out

    return redirect(url_for('root'))

def is_valid(email, password):
    # Check if email/pass exists

    if True:
        return True
    return False

@app.route("/addreview", methods = ['GET', 'POST'])
def addreview():


    return render_template("reviews.html", error=msg)


@app.route("/addbalance", methods=['GET', 'POST'])
def addbalance():
    return render_template("reviews.html", error=msg)


@app.route("/showaverage", methods=['GET', 'POST'])
def showaverage():
    return render_template("reviews.html", error=msg)


@app.route("/register", methods = ['GET', 'POST'])
def register():
    msg = ''
    return render_template("login.html", error=msg)

@app.route("/registerationForm")
def registrationForm():
    return render_template("register.html")


def parse(data):
    ans = []
    return ans

if __name__ == '__main__':
    app.run(debug=True)