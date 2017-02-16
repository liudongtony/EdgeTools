from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask import abort
from flask import render_template

from flask_script import Manager
from flask_bootstrap import Bootstrap

import configs

app = Flask(__name__)
app.debug = True


manager = Manager(app)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.route('/headers')
def get_headers():
    user_agent = request.headers.get('User_Agent')
    return 'Request with User Agent: %s' %user_agent


@app.route('/bad')
def bad_request():
    return '<h1>Bad Request!</h1>', 400


@app.route('/coo')
def make_cookie():
    response = make_response('<h1>This page carries a cookie.</h1>')
    response.set_cookie('cookie_user', 'Tony')
    return response


@app.route('/redir')
def make_redirect():
    return redirect("http://localhost:5000/coo")


@app.route('/users/<id>')
def find_user(id):
    user=configs.users[id]
    if not user:
        abort(404)
    return '<h1>Hello %s!</h1>' %user

if __name__ == '__main__':
    manager.run()