
from flask import Flask, render_template,request,redirect,session
from flask_pymongo import pymongo
from pymongo import results
from bson.json_util import dumps
CONNECTION_STRING = "mongodb+srv://dheeraj97:fashionstore@cluster0.bwjys.mongodb.net/FashionStore?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('FashionStore')
user_collection = pymongo.collection.Collection(db, 'users')
app = Flask(__name__)
app.secret_key = "super secret key"
print(user_collection)
def createUsers(email,password,number):
    db.users.insert_one({
         "email":email,
         "password":password,
         "number":number
    })
    return "user inserted"
def createOrder(order):
    db.order.insert_many(order)
    db.cart.delete_many({})
    return "order inserted"

def createCart(email,pName,Price,picture,Category):
    db.cart.insert_one({
         "email":email,
         "productName":pName,
         "price":Price,
         "picture":picture,
         "category":Category
    })
    return "cart inserted"

@app.route("/test")
def test():
    db.users.insert_one({"name": "John"})
    return "Connected to the data base!"

@app.route('/')
def index():
    if 'email' in session:
        user=session["email"]
        return render_template('index.html',user=user)
    else:
        return render_template('index.html')
@app.route('/login',methods=['POST','GET'])
def login():
    return render_template('login.html')
@app.route('/login1',methods=['POST','GET'])
def login1():
    cur=db.users.find({"email":request.form['inputEmail'],
                        "password":request.form['inputPassword']})
    result=list(cur)

    if len(result) > 0:
        session["email"]=request.form['inputEmail']
        user=session["email"]
        return render_template('index.html',user=user)
    else:
        return("incorrect emailpassword")

@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/register1',methods=['POST','GET'])
def register1():
    createUsers(request.form['inputEmail4'],request.form['inputPassword4'],request.form['inputNumber4'])
    return redirect('/')

@app.route('/cart/<string:id>',methods=['POST','GET'])
def cart(id):
    if 'email' in session:
        cur=db.shoe.find({"id":id})
        result=list(cur)
        print(result[0]["pName"])
        createCart(session["email"],result[0]["pName"],result[0]["price"],result[0]["picture"],result[0]["category"])
        cur= db.cart.find({"email":session["email"]})
        res=list(cur)
        user=session["email"]
        return render_template('cart.html',products=res,user=user)
    else:
        return redirect('/login')
@app.route('/checkout',methods=['POST','GET'])
def order():
    cur=db.cart.find({"email":session["email"]})
    result=list(cur)
    createOrder(result)
    cur= db.order.find({"email":session["email"]})
    res=list(cur)
    user=session["email"]
    return render_template('order.html',products=res,user=user)
@app.route('/orders')
def order1():
    cur= db.order.find({"email":session["email"]})
    res=list(cur)
    user=session["email"]
    # res1=dumps(res)
    # print(dumps(res))
    return render_template('order.html',products=res,user=user)

# @app.route('/shop')
# def shop():
#     return render_template('shop.html')
@app.route('/cart')
def cart1():
    cur= db.cart.find({"email":session["email"]})
    res=list(cur)
    user=session["email"]
    # res1=dumps(res)
    # print(dumps(res))
    return render_template('cart.html',products=res,user=user)
@app.route('/deleteCartItem/<string:id>',methods=["GET","POST"])
def delete1(id):
    myquery={"email":session["email"],"productName":id}
    db.cart.delete_one(myquery)
    cur= db.cart.find({"email":session["email"]})
    res=list(cur)
    user=session["email"]
    # res1=dumps(res)
    # print(dumps(res))
    return render_template('cart.html',products=res,user=user)
@app.route('/Shoes')
def shoes():
    if 'email' in session:
        cur= db.shoe.find({"category":"shoes"})
        res=list(cur)
        user=session["email"]
    # res1=dumps(res)
    # print(dumps(res))
        return render_template('shoes.html',products=res,user=user)
    else:
        cur= db.shoe.find({"category":"shoes"})
        res=list(cur)
        return render_template('shoes.html',products=res)
@app.route('/Wallet')
def wallet():
    if 'email' in session:
        cur= db.shoe.find({"category":"wallet"})
        res=list(cur)
        user=session["email"]
    # res1=dumps(res)
    # print(dumps(res))
        return render_template('shoes.html',products=res,user=user)
    else:
        cur= db.shoe.find({"category":"wallet"})
        res=list(cur)
        return render_template('shoes.html',products=res)
@app.route('/Belts')
def belts():
    if 'email' in session:
        cur= db.shoe.find({"category":"belt"})
        res=list(cur)
        user=session["email"]
    # res1=dumps(res)
    # print(dumps(res))
        return render_template('shoes.html',products=res,user=user)
    else:
        cur= db.shoe.find({"category":"belt"})
        res=list(cur)
        return render_template('shoes.html',products=res)
@app.route('/products')
def products():
    if 'email' in session:
        cur= db.shoe.find({})
        res=list(cur)
        user=session["email"]
    # res1=dumps(res)
    # print(dumps(res))
        return render_template('about.html',products=res,user=user)
    else:
        cur= db.shoe.find({})
        res=list(cur)
        return render_template('about.html',products=res)

@app.route('/products1')
def products1():
    return render_template('products.html')
@app.route('/sign_out')
def sign_out():
    session.pop('email')
    return redirect("/")