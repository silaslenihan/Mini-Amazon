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
    placetaker = ''
    return render_template('home.html', placetaker =placetaker)

@app.route('/results', methods=['GET', 'POST'])
def search_results():
    search=request.args['product']
    database = "sampledata.json"
    cur = conn.cursor()
    query="SELECT * FROM items WHERE cat_name='" +str(search)+"';"
    cur.execute(query)
    version = cur.fetchall()
<<<<<<< HEAD
    for row in version:
        print(row)
=======
    data = []
    for row in version:
        data_row = {}
        data_row['item_id'] = row[0]
        data_row['name'] = row[2]
        data_row['cateogry'] = row[1]
        data_row['rating'] = row[3]
        data.append(data_row)
>>>>>>> b7c5f9a85a0c9d412674db3f616d04893a4e2528
    placetaker = ''
    return render_template('result.html', items=data)

@app.route("/add")
def admin():
    placetaker = ''
    return render_template('add.html', placetaker =placetaker)

@app.route("/addItem", methods=["GET", "POST"])
def addItem():
    print(msg)
    return redirect(url_for('root'))

@app.route("/remove")
def remove():
    data = ''
    return render_template('remove.html', data=data)

@app.route("/removeItem")
def removeItem():
    print(msg)
    return redirect(url_for('root'))

@app.route("/displayCategory")
def displayCategory():
    placetaker = ''
    return render_template('displayCategory.html', placetaker =placetaker)

@app.route("/account/profile")
def profileHome():
    placetaker = ''
    return render_template("profileHome.html", placetaker =placetaker)

@app.route("/account/profile/edit")
def editProfile():
    placetaker = ''
    return render_template("editProfile.html", placetaker =placetaker)

@app.route("/account/profile/changePassword", methods=["GET", "POST"])
def changePassword():
    placetaker = ''
    return render_template("changePassword.html", placetaker =placetaker)

@app.route("/updateProfile", methods=["GET", "POST"])
def updateProfile():
    return redirect(url_for('editProfile'))

@app.route("/loginForm")
def loginForm():
    return render_template('login.html', error='')

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if True:

        return redirect(url_for('root'))
    else:
        error = 'Invalid UserId / Password'
        return render_template('login.html', error=error)

@app.route("/productDescription", methods=['GET', 'POST'])
def productDescription():
    placetaker = ''
    return render_template("productDescription.html", placetaker =placetaker)

@app.route("/addToCart")
def addToCart():
    print('')
    return redirect(url_for('root'))

@app.route("/cart", methods=['GET', 'POST'])
def cart():
    placetaker = ''
    return render_template("cart.html", placetaker =placetaker)

@app.route("/removeFromCart")
def removeFromCart():

    return redirect(url_for('root'))

@app.route("/logout")
def logout():

    return redirect(url_for('root'))

def is_valid(email, password):
    if True:
        return True
    return False

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