from flask import Flask
from .models import db, login_manager
from flask_bootstrap import Bootstrap
from config import Config
from flask_cors import CORS
from app.api import api
# from flask_migrate import Migrate

cors = CORS()
# migrate = Migrate()

login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    db.init_app(app)
    api.init_app(app)
    # migrate.init_app(app, db)
    login_manager.init_app(app)
    Bootstrap(app)

    from app.auth.routes import auth
    from app.admin.routes import admin
    from app.user.routes import user

    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(user)

    # Register error handlers
    from app.utils import page_not_found, forbidden, server_error
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(500, server_error)

    with app.app_context():
        db.create_all()
        # Create default quizmaster if not exists
        from app.models import User
        quizmaster = User.query.filter_by(username=app.config['QUIZMASTER_USERNAME']).first()
        if not quizmaster:
            quizmaster = User(
                username=app.config['QUIZMASTER_USERNAME'],
                is_admin=True
            )
            quizmaster.set_password(app.config['QUIZMASTER_PASSWORD'])
            db.session.add(quizmaster)
            db.session.commit()

    return app