from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from models.images import Images
from models.donation import Donation
from models.following import Following
from flask_login import current_user, login_user, login_required
from instagram_web.util.helpers import upload_file_to_aws
import braintree
from decimal import Decimal
import os
import datetime


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/browse', methods=['GET'])
def browse():
    users = User.select().where((User.id != current_user.id)
                                & (User.profile_image != None))
    return render_template('users/browse.html', users=users)


@users_blueprint.route('/my_profile', methods=['GET'])
def my_profile():
    private = User.get_or_none(id=current_user.id, is_private=True)
    follow_request = Following.select().where(
        (Following.idol_id == current_user.id) & (Following.approved == False) & (Following.block == False))
    return render_template('users/my_profile_page.html', private=private, follow_request=follow_request)


# redirects user to a profile page to corresponding username
@users_blueprint.route('/profile/<username>', methods=['GET'])
def profile(username):
    user = User.get(User.username == username)
    followed = Following.get_or_none(
        fan=current_user.id, idol=user.id, approved=True)
    approve_pending = Following.get_or_none(
        fan=current_user.id, idol=user.id, approved=False)
    return render_template('users/profile_page.html', user=user, followed=followed, approve_pending=approve_pending)


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


# uploads a user profile image
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


# uploads images to aws and also saves image url into psql db
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
    return redirect(url_for("users.my_profile"))


# updates username
@users_blueprint.route('/<id>/update_username', methods=["POST"])
@login_required
def update_username(id):
    username_input = request.form["username"]
    user = User.update(username=username_input,
                       updated_at=datetime.datetime.now()).where(User.id == id)
    check_username = User.get_or_none(User.username == username_input)
    if check_username:
        flash(f"This username has already been taken, try another name")
        return render_template('users/my_profile_page.html')
    else:
        user.execute()
        return redirect(url_for("users.my_profile"))


# Handle donation from other user to individual photos
gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.environ.get('BT_MERCHANT_ID'),
        public_key=os.environ.get('BT_PUBLIC_KEY'),
        private_key=os.environ.get('BT_PRIVATE_KEY')
    )
)


# redirects user to a donation page
# also generates a client token to get braintree approval
# to do: error checks
@users_blueprint.route('/new_donation/<image_id>/<username>', methods=['GET'])
def new_donation(image_id, username):
    user = User.get(User.username == username)
    image = Images.get(Images.id == image_id)
    client_token = gateway.client_token.generate()
    print(client_token)
    return render_template('users/new_donation.html', image=image, user=user, client_token=client_token)


# processes donation and saves donation information into the psql database
# to do: error checks
@users_blueprint.route("/checkout/<image_id>/<username>", methods=["POST"])
def checkout(image_id, username):
    print(request.form.get('paymentMethodNonce'))
    amount = request.form.get('amount')
    user = User.get(User.username == username)
    image = Images.get_or_none(Images.id == image_id)

    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": request.form.get('paymentMethodNonce'),
        "options": {
            "submit_for_settlement": True
        }
    })
    Donation.create(user=current_user.id, image=image.id,
                    transaction_number=result.transaction.id, amount=result.transaction.amount)
    print(result)
    print(request.form)
    print(current_user.id)
    print(image.id)
    print(result.transaction.id)
    print(result.transaction.amount)
    return render_template('users/profile_page.html', user=user)


# function to allow current user(fan) to follow another user(idol)
# to create a check as to not add another identical record in db
@users_blueprint.route("/follow_user/<username>", methods=["POST"])
@login_required
def follow_user(username):
    user = User.get(User.username == username)
    if user.is_private == True:
        Following.create(idol=user.id, fan=current_user.id, approved=False)
        return redirect(url_for('users.profile', user=user, username=user.username))

    else:
        Following.create(idol=user.id, fan=current_user.id)
        return redirect(url_for('users.profile', user=user, username=user.username))


@users_blueprint.route("/unfollow_user/<username>", methods=["POST"])
@login_required
def unfollow_user(username):
    user = User.get(User.username == username)
    unfollow = Following.delete().where(
        (Following.idol == user.id) & (Following.fan == current_user.id))

    unfollow.execute()
    return render_template('users/profile_page.html', user=user)


@users_blueprint.route("/toggle_privacy/<id>", methods=["POST"])
@login_required
def toggle_privacy(id):

    user = User.get_or_none(User.id == id)

    if user.is_private == False:
        print(current_user.id)
        user.update(
            is_private=True, updated_at=datetime.datetime.now()).where(User.id == id).execute()
        flash(f"Your account has been set to private")
        return redirect(url_for('users.my_profile'))
    elif user.is_private == True:
        user.update(
            is_private=False, updated_at=datetime.datetime.now()).where(User.id == id).execute()
        flash(f"Your account is now public")
        return redirect(url_for('users.my_profile'))
