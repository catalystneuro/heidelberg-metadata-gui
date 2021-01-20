from flask import Flask
import os
from pathlib import Path


def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)

    if os.environ.get('FLASK_ENV') == 'development':
        app.config.from_object('heidelberg_metadata_gui.config.ConfigDev')
    else:
        app.config.from_object('heidelberg_metadata_gui.config.ConfigProduction')

    # Variables from ENV vars
    app.config['JSON_SCHEMA_PATH'] = os.environ.get('JSON_SCHEMA_PATH', str(Path.cwd()))
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
