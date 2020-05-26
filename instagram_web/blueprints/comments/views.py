from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from models.images import Images
from models.comments import Comments
from flask_login import current_user, login_user, login_required
import os
import datetime


comments_blueprint = Blueprint('comments',
                               __name__,
                               template_folder='templates')


@comments_blueprint.route("/comment/<current_user_id>/<image_id>/<username>", methods=["POST"])
@login_required
def create_comment_profile_page(current_user_id, image_id, username):
    user = User.get_or_none(User.username == username)
    comment_input = request.form["comment_input"]
    Comments.create(commenter_id=current_user_id, user_id=user.id,
                    image_id=image_id, comment=comment_input)
    return render_template('users/profile_page.html', user=user)
