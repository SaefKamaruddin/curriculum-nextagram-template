from app import app
from flask import render_template, session
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.comments.views import comments_blueprint
from instagram_web.util.oauth import oauth
import config
from flask_assets import Environment, Bundle
from .util.assets import bundles
oauth.init_app(app)
assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(comments_blueprint, url_prefix="/comments")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    return render_template('home.html')
