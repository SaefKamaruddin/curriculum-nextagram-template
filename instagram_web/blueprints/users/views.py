from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from models.images import Images
from flask_login import current_user, login_user, login_required
from instagram_web.util.helpers import upload_file_to_aws


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/my_profile', methods=['GET'])
def my_profile():
    return render_template('users/my_profile_page.html')


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


@users_blueprint.route('/<id>/profile_image', methods=["POST"])
@login_required
def upload_profile_image(id):
    file = request.files.get('upload_profile_image')
    print(file)
    print(file.filename)
    result = upload_file_to_aws(file)
    user = User.update(profile_image=file.filename).where(User.id == id)
    user.execute()
    print(result)

    # images = Images(user = current_user.id, img = result)
    # images.save()

    return redirect(url_for("users.my_profile"))


@users_blueprint.route('/<id>/image', methods=["POST"])
@login_required
def upload_image(id):
    file = request.files.get('upload_profile_image')
    print(file)
    print(file.filename)
    result = upload_file_to_aws(file)
    image = Images()
    image.image = file.filename
    image.user = id
    image.save()

    print(result)

    # images = Images(user = current_user.id, img = result)
    # images.save()

    return redirect(url_for("users.my_profile"))


@users_blueprint.route('/<id>/update_username', methods=["POST"])
@login_required
def update_username(id):
    username_input = request.form["username"]
    user = User.update(username=username_input).where(User.id == id)
    check_username = User.get_or_none(User.username == username_input)
    if check_username:
        flash(f"This username has already been taken, try another name")
        return render_template('users/my_profile_page.html')
    else:
        user.execute()
        return redirect(url_for("users.my_profile"))
