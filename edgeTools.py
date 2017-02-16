from datetime import datetime

from flask import Flask
from flask import abort
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import configs

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'This is a secret'


manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'))


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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello %s</h1>' %name

if __name__ == '__main__':
    manager.run()