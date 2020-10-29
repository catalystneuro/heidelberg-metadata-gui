from flask import Flask
import os


def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.ConfigDev')

    # Variables from ENV vars
    app.config['DATA_PATH'] = os.environ.get('DATA_PATH')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    with app.app_context():
        # Import parts of our core Flask app
        from . import routes

        # Import NWB converter
        from .converter import HeidelbergNWBConverter
        converter_class = HeidelbergNWBConverter

        # Import Dash application
        from .metadata_forms.init_forms import init_forms

        init_forms(server=app, converter_class=converter_class)

        return app
