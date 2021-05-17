"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()


def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__)
    app.config.from_object('config.Config')
    # Init database
    db.init_app(app)
    # session and Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    with app.app_context():
        # Import parts of our core Flask app
        from . import main

        # Import Dash application
        from .plotlyDash.dashboard import init_dashboard
        #from .plotlyDash.dashboard import init_dashboard_test

        app = init_dashboard(app)
        #app = init_dashboard_test(app)

        # Import models
        from .models import User, association_table, Role

        # Create tables from models
        db.create_all()
        db.session.commit()
        print("tables created")

        @login_manager.user_loader
        def load_user(user_id):
            # since the user_id is just the primary key of our user table, use it in the query for the user
            return User.query.get(int(user_id))

        # Add Admin views
        admin = Admin(app, name='CovidApp')
        admin.add_view(ModelView(User, db.session))
        # blueprint for auth routes in our app
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        # blueprint for non-auth parts of app
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        return app
