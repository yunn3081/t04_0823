from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail
from export_db import get_data
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
getdata = get_data()

#ENV = 'prod'
ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/cellline'
    app.config['SECRET_KEY'] = 'mysecret'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bgbfkkhaaxvsqz:4651cb865eab9a07557a214fe78c5828f68f1bc240dfdc3d79972722a927f2f5@ec2-3-231-69-204.compute-1.amazonaws.com:5432/dfhrugeougj002'
    #app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
admin = Admin(app)

class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200), unique=True)
    pwd = db.Column(db.String(200))
    location = db.Column(db.String(200))

    def __init__(self, customer, email, pwd, location):
        self.customer = customer
        self.email = email
        self.pwd = pwd
        self.location = location

class Cellline(db.Model):
    __tablename__ = 'cellline'
    index = db.Column(db.Integer, primary_key=True)
    no = db.Column(db.String)
    product_category = db.Column(db.String)
    organism = db.Column(db.String)
    age = db.Column(db.String)
    gender = db.Column(db.String)
    ethnicity = db.Column(db.String)
    biopsy_site = db.Column(db.String)
    tissue = db.Column(db.String)
    cancer_type = db.Column(db.String)
    growth_properties = db.Column(db.String)
    stock = db.Column(db.String)
    img = db.Column(db.String)

    def __init__(index, no, product_category, organism, age, gender, ethnicity, biopsy_site, tissue, cancer_type, growth_properties, stock, img):
        self.index = index
        self.no = no
        self.product_category = product_category
        self.organism = organism
        self.age = age
        self.gender = gender
        self.ethnicity = ethnicity
        self.biopsy_site = biopsy_site
        self.tissue = tissue
        self.cancer_type = cancer_type
        self.growth_properties = growth_properties
        self.stock = stock
        self.img = img

admin.add_view(ModelView(Account, db.session))
admin.add_view(ModelView(Cellline, db.session))



@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/signup')
def index():
    return render_template('signup.html') 

@app.route('/login')
def login():
    return render_template('login.html') 

@app.route('/about_whoWeAre')
def about_whoWeAre():
    return render_template('about_whoWeAre.html')

@app.route('/about_whatWeDo')
def about_whatWeDo():
    return render_template('about_whatWeDo.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/product_submit', methods=['POST'])
def product_submit():
    if request.method == 'POST':
        Product_Category = request.form['Product Category']
        Age = request.form['Age']
        Gender = request.form['Gender']
        Ethnicity = request.form['Ethnicity']
        Cancer_type = request.form['Cancer type']
        Growth_Properties = request.form['Growth Properties']
        filter_list = [Product_Category, Age, Gender, Ethnicity, Cancer_type, Growth_Properties]
        return render_template('showup_cellline.html', showupcellline = getdata, myfilter = filter_list)
    else:
        Product_Category = request.form['Product Category']
        Age = request.form['Age']
        Gender = request.form['Gender']
        Ethnicity = request.form['Ethnicity']
        Cancer_type = request.form['Cancer type']
        Growth_Properties = request.form['Growth Properties']
        filter_list = [Product_Category, Age, Gender, Ethnicity, Cancer_type, Growth_Properties]
        return render_template('showup_cellline.html', showupcellline = getdata, myfilter = filter_list)

@app.route('/showup_cellline')
def showup_cellline():
    return render_template('showup_cellline.html')

@app.route('/cellline_submit', methods=['POST'])
def cellline_submit():
    if request.method == 'POST':
        No = request.form['No']
        return render_template('cellline_detail.html', showupcellline = getdata, mycell = No)

@app.route('/cellline_detail')
def cellline_detail():
    return render_template('cellline_detail.html')

@app.route('/links')
def links():
    return render_template('links.html')

@app.route('/others')
def others():
    return render_template('support.html') 

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        email = request.form['email']
        pwd = request.form['pwd']
        location = request.form['location']
        
        if customer == '' or email == '' or pwd == '' or location == '':
           return render_template('index.html', message = 'Please enter required fields')
        
        if db.session.query(Account).filter(Account.customer == customer).count() == 0:
            data = Account(customer, email, pwd, location)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, email, location)
            return render_template('success.html')

        return render_template('index.html', message = 'This email address have already registered.')

if __name__ == '__main__':
    app.run()