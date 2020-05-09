from flask import Blueprint, render_template, request, flash, url_for, redirect, session
from werkzeug.security import check_password_hash
from models.user import User
from flask_login import current_user, login_user, logout_user, login_required
from instagram_web.util.o_auth import oauth

sessions_blueprint = Blueprint(
    "sessions", __name__, template_folder="templates")

# @sessions_blueprint.route('/home')
# def index():
#     return render_template('home.html')


@sessions_blueprint.route('/google_login')
def google_login():
    redirect_uri = url_for('sessions.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@sessions_blueprint.route('/authorize/google')
def authorize():
    print(request.args)
    oauth.google.authorize_access_token()
    email = oauth.google.get(
        'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        # flash(f"Login successful.")
        return redirect(url_for('sessions.login'))
    else:
        return redirect(url_for('sessions.login'))


@sessions_blueprint.route('/')
def login():
    if not current_user.is_authenticated:
        # showing the login form if user is not logged in
        return render_template('sessions/login.html')
    else:
        # if user has already login, they will be redirected to home page
        return render_template('home.html')


@sessions_blueprint.route('/login-check', methods=["POST"])
def login_check():
    # check if the email entered inside login form is available inside our database
    user = User.get_or_none(User.email == request.form['email_input'])

    if user:  # return true if the email is available inside our database
        password_to_check = request.form['password_input']
        hashed_password = user.password
        result = check_password_hash(hashed_password, password_to_check)

        if result:
            login_user(user)

            flash(f"Login successful.")
            # session["email"] = request.form['email_input']
            # flash(f"{session['email']}")
            return redirect(url_for('sessions.login'))
        else:
            flash(f"Login failure.")
            flash("Email/password is not correct")
            return redirect(url_for('sessions.login'))
    else:
        flash("Email/password is not correct.")
        return redirect(url_for('sessions.login'))

    # if current_user.is_authenticated:
    #     return redirect('/')


@sessions_blueprint.route('/signout', methods=["POST"])
@login_required
def destroy():
    logout_user()
    return render_template('home.html')
