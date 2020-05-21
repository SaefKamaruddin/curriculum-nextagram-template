from flask import Blueprint, render_template, request, flash, url_for, redirect, session
from werkzeug.security import check_password_hash
from models.user import User
from flask_login import current_user, login_user, logout_user, login_required

sessions_blueprint = Blueprint(
    "sessions", __name__, template_folder="templates")
