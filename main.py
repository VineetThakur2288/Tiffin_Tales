from flask import Flask,render_template,request,redirect,session,flash,url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
from datetime import datetime

local_server=True
app=Flask(__name__)
app.secret_key='tiffintales'
app.config['SQLALCHEMY_DATABASE_URI']= "mysql://root:@localhost/tiffin_tales"

db= SQLAlchemy(app)


class meals_plan(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    day=db.Column(db.String(20),nullable=False)
    meal_type=db.Column(db.String(100),nullable=False)
    breakfast=db.Column(db.String(100),nullable=False)
    lunch=db.Column(db.String(100),nullable=False)
    dinner=db.Column(db.String(100),nullable=False)

class Orders(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    user_mobile=db.Column(db.String(100),nullable=False)
    status=db.Column(db.String(100),nullable=False)
    ordered_at=db.Column(db.String(100),nullable=False)


class premium_thali_meals(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    day=db.Column(db.String(20),nullable=False)
    meal_type=db.Column(db.String(100),nullable=False)
    breakfast=db.Column(db.String(100),nullable=False)
    lunch=db.Column(db.String(100),nullable=False)
    dinner=db.Column(db.String(100),nullable=False)

class standard_thali_meals(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    day=db.Column(db.String(20),nullable=False)
    meal_type=db.Column(db.String(100),nullable=False)
    breakfast=db.Column(db.String(100),nullable=False)
    lunch=db.Column(db.String(100),nullable=False)
    dinner=db.Column(db.String(100),nullable=False)


class Users(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(20),unique=True,nullable=False)
    mobile_no=db.Column(db.String(100),unique=True,nullable=True)
    password=db.Column(db.String(100),nullable=False)
    cnfpass=db.Column(db.String(100),nullable=False)
    gender=db.Column(db.String(10),nullable=False,default="Not Specified")
    dob=db.Column(db.String(15),nullable=True,default=None)
    address=db.Column(db.String(500),nullable=False,default="Not Provided")
    # Relationship to CustomizedMealPlan
    meal_plans = db.relationship('Customized_meal_plan', backref='user', lazy=True)
    
    
class Contact(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    mob=db.Column(db.String(12),nullable=False)
    email=db.Column(db.String(30),nullable=False)
    msg=db.Column(db.String(500),nullable=False)
    date=db.Column(db.String(20),nullable=True)

class Customized_meal_plan(db.Model):
    sno= db.Column(db.Integer, primary_key=True)  # Primary key for the table
    user_id = db.Column(db.Integer, db.ForeignKey('users.sno'), nullable=False)
    meal_freq=db.Column(db.String(5),nullable=False)
    noofdays=db.Column(db.String(5),nullable=False)
    day=db.Column(db.String(10),nullable=False)
    breakfast=db.Column(db.String(30),nullable=False)
    lunch=db.Column(db.String(30),nullable=False)
    dinner=db.Column(db.String(30),nullable=False)
    date=db.Column(db.String(20),nullable=True) 
    created_at=db.Column(db.DateTime, default=datetime.utcnow)
    
    

@app.route("/")
def home():
    return render_template("Index.html")


@app.route("/SignUp",methods=['GET',"POST"])
def signup():
    if request.method=="POST":
        'Add Entry to our Database'
        name=request.form.get('name')
        email=request.form.get('email')
        mobile_no=request.form.get('mobile_no')
        password=request.form.get('password')
        cnfpass=request.form.get('cnfpass')
        if not all([name, email, mobile_no, password, cnfpass]):
            flash("All fields are required.")
            return render_template("SignUp.html")
        if password != cnfpass:
            return "Password do not match"
        user=Users(name=name,email=email,mobile_no=mobile_no,password=password,cnfpass=cnfpass)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("SignUp.html")


@app.route("/login",methods=['GET','POST'])
def login():
    if 'person' in session:
        return redirect(url_for("afterlogin"))
    if request.method=="POST":
        email_or_usno=request.form.get('email_or_usno')
        user_pass=request.form.get('pwd')
        value=Users.query.filter(((Users.email == email_or_usno) | (Users.mobile_no == email_or_usno)) & (Users.password==user_pass)).first()
        if value:
            session['person']=value.sno
            return redirect(url_for("afterlogin"))
        else:
            flash("Invalid login credentials.")
    return render_template("login.html")



@app.route("/afterlogin")
def afterlogin():
    flash("You have Successfully logged In","success")
# Write this in after login page to dispaly flash message
#     <div class="flash-container">  
#     {% with messages = get_flashed_messages(with_categories=true) %}
#       {% if messages %}
#         {% for category, message in messages %}
#           <div class="flash-message {{ category }}">
#             {{ message }}
#             <button class="close-btn" onclick="dismissMessage(this)">X</button>
#           </div>
#         {% endfor %}
#       {% endif %}
#     {% endwith %}
#   </div>
    return render_template("afterlogin.html")

@app.route("/profile",methods=['GET','POST'])
def profile():
        person=session.get('person')
        if not person:
            return redirect("/login")
        user = Users.query.filter_by(sno=person).first()
        return render_template("profile.html",user=user)

@app.route("/editprofile/<string:sno>", methods=['GET', 'POST'])
def editprofile(sno):
    person = session.get('person')
    if not person:
        return (url_for("login"))

    # Fetch user by sno depending on what is stored in session
    user = Users.query.filter_by(sno=sno).first()

    if request.method == "POST":
        user.name = request.form.get('name')
        user.mobile_no = request.form.get('mobile_no')
        user.email = request.form.get('email')
        user.gender = request.form.get('gender')
        user.dob = request.form.get('dob')
        user.address = request.form.get('address')
        db.session.commit()
        return redirect(url_for("profile"))
    return render_template("editprofile.html", user=user)

    

@app.route("/currentOrders")
def currentOrders():
    return render_template("currentOrders.html")

@app.route("/mealTracking")
def mealTracking():
    return render_template("mealTracking.html")

@app.route("/ordr")
def ordr():
    return render_template("ordr.html")

@app.route("/logout")
def logout():
    session.pop('person',None)
    return redirect(url_for("home"))


@app.route("/AboutUs")
def aboutus():
    return render_template("AboutUs.html")

@app.route("/ContactUs",methods=['GET','POST'])
def contact():
    if request.method == "POST":
        name=request.form.get('name')
        mob=request.form.get('mob')
        email=request.form.get('email')
        msg=request.form.get('msg')
        entry=Contact(name=name,mob=mob,email=email,msg=msg,date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        flash("Thanks for Submitting your detail.We will get back to you soon","success") # css to look better
    return render_template("ContactUs.html")


@app.route("/basicplan")
def basicplan():
    return render_template("BasicPlan.html")

@app.route("/standardplan")
def standardplan():
    return render_template("StandardPlan.html")

@app.route("/premiumplan")
def premiumplan():
    return render_template("PremiumPlan.html")

@app.route('/customizeplan', methods=['GET', 'POST'])
def customize_plan():
    if request.method=="POST":
        if 'person' not in session:
            flash("Please login first.")
            return redirect(url_for('login'))

        user_id = session['person']
        meal_freq = request.form.get("meal_frequency")
        noofdays = request.form.get("meal_days")
        #  Delete old_plan
        Customized_meal_plan.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        #  Creating New_plan
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i, day in enumerate(days):
            breakfast = request.form.get(f"breakfast_{i}")
            lunch = request.form.get(f"lunch_{i}")
            dinner = request.form.get(f"dinner_{i}")

            new_plan = Customized_meal_plan(
                user_id=user_id,
                meal_freq=meal_freq,
                noofdays=noofdays,
                day=day,
                breakfast=breakfast,
                lunch=lunch,
                dinner=dinner,
                date=datetime.today().strftime('%Y-%m-%d')
            )
            db.session.add(new_plan)

        db.session.commit()
        flash("Your customized meal plan has been saved.")
        return redirect(url_for("afterlogin"))
    return render_template("CustomizePlan.html")


@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/payment")
def payment():
    return render_template("payment.html")

@app.route("/confirmod")
def confirmod():
    if request.method=="POST":
        pass
    return render_template("confirm_order.html")

@app.route("/Terms&Cond")
def termsCond():
    return render_template("Terms&Cond.html")

@app.route("/PrivacyPol")
def PrivacyPol():
    return render_template("PrivacyPol.html")

@app.route("/Breakfast")
def breakfast():
    return render_template("Breakfast.html")

@app.route("/Lunch")
def lunch():
    return render_template("LunchMenu.html")

@app.route("/Dinner")
def dinnermenu():
    return render_template("DinnerMenu.html")

if __name__=="__main__":
    app.run(debug=True)




