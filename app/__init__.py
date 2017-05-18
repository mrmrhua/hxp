from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .exceptions import ValidationError
from flask_mail import Mail
from flask_debugtoolbar import DebugToolbarExtension
db = SQLAlchemy()
lm = LoginManager()
mail = Mail()
toolbar = DebugToolbarExtension()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    lm.init_app(app)
    mail.init_app(app)
    toolbar.init_app(app)

    from .api_1_0 import api_bp as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint,url_prefix='/api/v1.0')
    # app.register_blueprint(api_1_0_blueprint)

    from  .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .add_project import add_project as add_project_bp
    app.register_blueprint(add_project_bp)

    from .designers import designers as designers_bp
    app.register_blueprint(designers_bp)

    # @app.errorhandler(ValidationError)
    # def validation_error(e):
    #         return "error"

    return app

