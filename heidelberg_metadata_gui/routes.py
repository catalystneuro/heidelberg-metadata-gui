from flask import redirect, request
from flask import current_app as app


@app.route('/')
def home():
    """Landing page."""
    return redirect('/metadata-forms/')


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is not None:
        # raise RuntimeError('Not running with the Werkzeug Server')
        func()
    return


@app.route('/shutdown/')
def shutdown():

    shutdown_server()
    return 'Server down...'
