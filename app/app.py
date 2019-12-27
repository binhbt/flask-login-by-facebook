from facebook import get_user_from_cookie, GraphAPI
from flask import Flask, g, render_template, redirect, request, session, url_for, Blueprint
from faceook_test.views import fb_blueprint

app = Flask(__name__)
app.register_blueprint(fb_blueprint)
@app.route('/', methods=['GET'])
def get():
    return 'Hello world'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)