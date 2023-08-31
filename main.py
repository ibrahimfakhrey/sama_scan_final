import json
import os



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


    class News(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(100))
        des = db.Column(db.String(1000))

    class Discounts(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        des = db.Column(db.String(1000))
    class Results_done(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        case = db.Column(db.String(100))
        notes = db.Column(db.String(1000))
        phone=db.Column(db.String(100))
        photo_filenamee = db.Column(db.String(1000))

        def save_profile_photo(self, photo_file):
            """
            Saves the user's profile photo to the uploads folder
            and updates the user's photo filename in the database.
            """
            # Get the uploads folder path
            uploads_folder = os.path.join(os.getcwd(), 'static', 'uploads')

            # Create the uploads folder if it doesn't exist
            if not os.path.exists(uploads_folder):
                os.makedirs(uploads_folder)

            # Save the photo file to the uploads folder with a unique filename
            photo_filename = f"{self.id}_{photo_file.filename}"
            photo_path = os.path.join(uploads_folder, photo_filename)
            photo_file.save(photo_path)

            # Update the user's photo filename in the database
            self.photo_filenamee = photo_filename
            db.session.commit()


    db.create_all()

class MyModelView(ModelView):
        def is_accessible(self):
            return True


admin = Admin(app)
admin.add_view(MyModelView(Paid_user, db.session))
admin.add_view(MyModelView(Results, db.session))
admin.add_view(MyModelView(News, db.session))
admin.add_view(MyModelView(Discounts, db.session))
admin.add_view(MyModelView(Results_done, db.session))





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


            return redirect("/dash")
    return render_template("login.html")

@app.route("/dash")
def dash():
    user=current_user
    username=user.name

    items=Results.query.all()
    results=[]
    for i in items:
        if i.phone==user.phone:
            results.append(i)
    y = [10, 50, 30, 40, 50]
    x = ["urin1", "urin2", "urin3", "urin4", "urin5"]
    news=News.query.all()
    discounts=Discounts.query.all()
    resuts_done=Results_done.query.all()
    done=[]
    for i in resuts_done:
        if i.phone==user.phone:
            done.append(i)

    return render_template("dash.html", user_name=username, items=results, labels=x, data=y,news=news,discounts=discounts,done=done)
@app.route('/show/<int:id>')
def show_item(id):
   item=Results_done.query.filter_by(id=id).first()
   name =item.name
   file=item.photo_filenamee
   notes=item.notes
   y = [10, 50, 30, 40, 50]
   x = ["urin1", "urin2", "urin3", "urin4", "urin5"]
   news=News.query.all()
   discounts=Discounts.query.all()
   return render_template('item.html', name=name,file=file,notes=notes, labels=x, data=y,news=news,discounts=discounts)
@app.route("/add result",methods=["GET","POST"])
def add_result():
    if request.method=="POST":
        name=request.form.get("name")
        phone=request.form.get("phone")
        case=request.form.get("case")
        notes=request.form.get("notes")
        photo_file = request.files['profile_photo']
        new_result=Results_done(
            name=name,
            case=case,
            notes=notes,
            phone=phone
        )
        db.session.add(new_result)
        db.session.commit()
        instance=Results_done.query.get(new_result.id)
        instance.save_profile_photo(photo_file)
        return "done"
    return render_template("add_result.html")
if __name__=="__main__":
    app.run(debug=True)