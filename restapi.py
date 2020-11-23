# !flask/bin/python
from flask import Flask, jsonify, request, render_template
from ReadFile import *
from werkzeug.exceptions import HTTPException, InternalServerError, abort
from flask import json

app = Flask(__name__)


def index():
    return "Hello, World!"


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.errorhandler(InternalServerError)
def handle_500(e):
    original = getattr(e, "original_exception", None)

    if original is None:
        # direct 500 error, such as abort(500)
        return render_template("500.html"), 500

    # wrapped unhandled error
    return render_template("500_unhandled.html", e=original), 500


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.route('/api/home/', methods=['GET'])
def home():
    try:
        response = package_list()
        if response is None:
            abort(404, description="Resource not found")
        return render_template('index.html', dict=response)
    except KeyError:
        abort(404, description="Resource not found")


# @app.route('/api/packageList/<package_name>', methods=['GET'])
@app.route('/api/package-list')
def fetch_package_list(package_name='Anonymous'):
    try:
        package_name = request.args.get('package_name', default = '', type = str)
        response = package_list(package_name)
        if response is None:
            abort(404, description="Resource not found")
        return render_template('index.html', dict=response)
    except KeyError:
        abort(404, description="Resource not found")

    # return jsonify({'tasks': tasks})


if __name__ == '__main__':
    app.run(debug=True)
