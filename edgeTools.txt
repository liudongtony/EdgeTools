from datetime import datetime
from threading import Thread
import os

from flask import Flask
from flask import abort
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager, Shell, Server
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import config


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# app.debug = True
app.config['SECRET_KEY'] = 'This is a secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['EDGETOOLS_MAIL_SUBJECT_PREFIX'] = '[EdgeTools]'
app.config['EDGETOOLS_MAIL_SENDER'] = 'EdgeTools Admin <testofdong@gmail.com>'
app.config['EDGETOOLS_ADMIN'] = os.environ.get('EDGETOOLS_ADMIN')


manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command('runserver', Server(use_debugger=True))
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['EDGETOOLS_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['EDGETOOLS_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['EDGETOOLS_ADMIN']:
                send_email(app.config['EDGETOOLS_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
            # flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'),
                           known=session.get('known', False))


@app.route('/auser/<name>')
def auser(name):
    return render_template('auser.html', name=name)


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
    user = config.users[id]
    if not user:
        abort(404)
    return '<h1>Hello %s!</h1>' %user


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == '__main__':
    manager.run()
