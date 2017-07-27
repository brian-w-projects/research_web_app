from . import main
from flask import render_template


@main.app_errorhandler(400)
@main.app_errorhandler(403)
@main.app_errorhandler(404)
@main.app_errorhandler(405)
@main.app_errorhandler(500)
def bad_request(e):
    return render_template('errors/error.html'), 404
