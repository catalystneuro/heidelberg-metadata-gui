import pytest
from heidelberg_metadata_gui import init_app



@pytest.fixture(scope='module')
def app():
    """Instance of main flask app"""
    app = init_app()
    return app
