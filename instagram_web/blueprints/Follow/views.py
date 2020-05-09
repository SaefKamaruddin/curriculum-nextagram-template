
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from models.follow import Follow
from models.user import User

follow_blueprint = Blueprint('follow',
                             __name__,
                             template_folder='templates')


@follow_blueprint.route('/<id>', methods=["POST"])
def follow(id):
    user_id = id
    print(f"user id : {user_id}")
    follow_id = current_user.id
    print(f"follow id : {follow_id}")
    follow_record = Follow(user=int(user_id), follower=follow_id)
    follow_record.save()
    print("Follow success")
    print(User.get(User.id == user_id).name)
    # user stays at user's profile page
    return redirect(url_for('users.show', username=User.get(User.id == user_id).name))


@follow_blueprint.route('/approve/<id>', methods=["POST"])
def approve(id):
    approval_user = Follow.get((Follow.follower_id == id) & (
        Follow.user_id == current_user.id))
    approval_user.approved = True
    approval_user.save()
    return redirect(url_for('users.show', username=current_user.name))
