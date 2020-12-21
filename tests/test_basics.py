
def test_app_is_created(app):
    assert app.name == 'heidelberg_metadata_gui'


def test_converter_200(client):
    assert client.get('/metadata-forms/').status_code == 200


def test_shutdown(client):
    assert client.get('/shutdown/').status_code == 200
