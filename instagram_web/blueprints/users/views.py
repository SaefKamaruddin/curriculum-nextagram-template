from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from flask_login import current_user, login_user, login_required


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


# function to create new a new user
@users_blueprint.route('/', methods=['POST'])
def create():
    username_input = request.form["username"]
    email_input = request.form["email"]
    password_input = request.form["password"]
    user = User.create(username=username_input,
                       email=email_input, password=password_input)

    if len(user.errors) > 0:
        flash(f"An error has occured.Sign up failed")
        print("failed")
        return render_template('users/new.html', errors=user.errors)

    else:
        login_user(user)
        print("pass")
        return redirect(url_for("home"))


@users_blueprint.route('/post')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('users/post.html', title='Home', user=user, posts=posts)
