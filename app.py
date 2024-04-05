from flask import Flask, abort, render_template,request
from forms import LoginForm,SignupForm
from flask import session, redirect,url_for
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db=SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    pets = db.relationship('Pets', backref='user')
    
class Pets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    age = db.Column(db.Integer)
    bio = db.Column(db.String)
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'))

 
with app.app_context():
    db.create_all()
   
pets=[

    {'id': 1, 'name': 'Buddy', 'age': 5, 'bio': 'Loyal and obedient'},
    {'id': 2, 'name': 'Lucy', 'age': 3, 'bio': 'Friendly and playful'},
    {'id': 3, 'name': 'Max', 'age': 8, 'bio': 'Very energetic'},
    {'id': 4, 'name': 'Bailey', 'age': 6, 'bio': 'Loves to cuddle'},
    {'id': 5, 'name': 'Molly', 'age': 4, 'bio': 'Shy but sweet'}

]

users=[
    {'praneethmails18@gmail.com':'123'},
    {'tangudupraneeth@yahoo.com':'456'}
    
]

@app.route("/") 
def hello():
    return render_template("home.html",pets=pets)

@app.route('/pet/<int:pet_id>')
def pet_details(pet_id):
    pet = next((pet for pet in pets if pet["id"]==pet_id),None)
    if pet is None:
        abort(404,description= "No pets are available with this ID")
    return render_template("details.html", pet=pet)

@app.route("/about") 
def about():
    return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = get_user_by_email(email)

        if user and user.check_password(password):  # Assuming you have a method check_password to verify the password
            session['user_id'] = user.id  # Store user id in the session
            return render_template("login.html", message="Successfully logged in!")

        return render_template("login.html", form=form, message="Wrong credentials. Please try again.")

    return render_template("login.html", form=form)        
    
        
        
    """if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if email in users  and password == users[email]:
            return render_template("login.html",message="u r successfully loggedin")
        return render_template("login.html",message="check ypur credentials")"""
   

@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')  
    return redirect(url_for('hello'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        try:
            new_user = User(name=form.name.data, email=form.email.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            message = "Account created successfully!"
            return render_template("signup.html", form=None, message=message)
        except Exception as e:
            db.session.rollback()
            error_message = "An error occurred: " + str(e)
            return render_template("signup.html", form=form, message=error_message)

    elif form.errors:
        print(form.errors.items())
        return render_template("signup.html", form=form)

    return render_template("signup.html", form=form)

        
    
@app.route("/<name>")
def you(name):
    return "hi "+ name + " !"

@app.route("/sqaure/<int:num>")
def youuu(num):
    return "square of "+ str(num) + " is "+ str(num*num)

if __name__ == '__main__':
    app.run(debug = True) 
