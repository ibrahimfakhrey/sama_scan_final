from flask import Flask, render_template, redirect, url_for, flash, abort, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # Check if user is in paid_user table
    user = Paid_user.query.get(int(user_id))
    if user:
        return user
    # If not, check if user is in free_user table

    # If user is not in either table, return None
    return None

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
with app.app_context():
    class Paid_user(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        phone = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))
        name = db.Column(db.String(1000))
        email=db.Column(db.String(100))
    class Results(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        case = db.Column(db.String(100))
        notes = db.Column(db.String(1000))
        phone=db.Column(db.String(100))

    db.create_all()

class MyModelView(ModelView):
        def is_accessible(self):
            return True


admin = Admin(app)
admin.add_view(MyModelView(Paid_user, db.session))
admin.add_view(MyModelView(Results, db.session))




@app.route("/")
def start():
    return render_template("index.html")


@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        name=request.form.get("name")
        password= hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        email=request.form.get("email")
        phone=request.form.get("phone")
        new_user=Paid_user(
            phone=phone,
            name=name,
            email=email,password=password
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect("/admin")
    return render_template("register.html")
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":

        password=  request.form.get('password')

        phone=request.form.get("phone")
        user = Paid_user.query.filter_by(phone=phone).first()
        if not user:
            flash("That email does not exist, please try again.")

            # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')

        # Email exists and password correct
        else:
            login_user(user)


            return "hi"
    return render_template("login.html")

@app.route("/dash")
def dash():
    username=current_user.name
    items=Results.query.all()
    return render_template("dash.html",user_name=username,items=items)
if __name__=="__main__":
    app.run(debug=True)