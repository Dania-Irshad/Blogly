from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "sec_ret$0987"
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def home_page():
    return redirect("/users")

@app.route("/users")
def list_users():
    """Display all users"""
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/users/new")
def new_user():
    """Display new user form."""
    return render_template("new.html")

@app.route("/users/new", methods=["POST"])
def get_user():
    """Add new user and redirect to users"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()
    return redirect(f"/users")

@app.route("/users/<int:user_id>")
def get_detail(user_id):
    """Display details of the user"""
    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["GET"])
def edit_user(user_id):
    """Display edit user form."""
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def get_updated_user(user_id):
    """Edit user and redirect to detail page"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url
    db.session.add(user)
    db.session.commit()
    return redirect(f"/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete user and redirect to homepage"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")