from flask import Blueprint, render_template, request, flash, url_for, redirect, session
from werkzeug.security import check_password_hash
from models.user import User
from flask_login import current_user, login_user, logout_user, login_required
from instagram_web.util.oauth import oauth
sessions_blueprint = Blueprint(
    "sessions", __name__, template_folder="templates")

# routes to login form
@sessions_blueprint.route('/login_page', methods=['GET'])
def login_page():
    return render_template('sessions/login.html')


@sessions_blueprint.route('/login_now', methods=["POST"])
def login_now():
    # checks db for a user with a matching email
    user = User.get_or_none(
        User.email == request.form['email_input'])

    # if returning true, proceed to check
    if user:
        check_password = request.form['password_input']
        hashed_password = user.password
        password_match = check_password_hash(hashed_password, check_password)

        if password_match:
            login_user(user)
            return redirect(url_for('home'))

        else:
            flash(f"Login failed, incorrect username/password")
            return render_template('sessions/login.html')

    else:
        flash(f"Login failed, incorrect username/password")
        return render_template('sessions/login.html')


@sessions_blueprint.route('/sign_out')
def sign_out():
    logout_user()

    return redirect(url_for('home'))


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
        return redirect(url_for('sessions.login'))
    else:
        return redirect(url_for('sessions.login'))
