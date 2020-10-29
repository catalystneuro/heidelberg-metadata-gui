from flask import redirect
from flask import current_app as app


@app.route('/')
def home():
    """Landing page."""
    return redirect('/metadata-forms/')
