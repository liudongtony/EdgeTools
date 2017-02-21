from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, make_response
from flask_login import login_required

from . import main
from .forms import NameForm
from .. import db
from ..models import User, Permission
from ..email import send_email
from ..decorators import permission_required, admin_required


# @main.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.name.data).first()
#         if user is None:
#             user = User(username=form.name.data, role_id=2)
#             db.session.add(user)
#             session['known'] = False
#             if current_app.config['EDGETOOLS_ADMIN']:
#                 send_email(current_app.config['EDGETOOLS_ADMIN'], 'New User', 'mail/new_user', user=user)
#         else:
#             session['known'] = True
#         session['name'] = form.name.data
#         return redirect(url_for('.index'))
#     return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'),
#                            known=session.get('known', False))


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/coo')
def make_cookie():
    response = make_response('<h1>This page carries a cookie.</h1>')
    response.set_cookie('cookie_user', 'Tony')
    return response


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"


@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return "For comment moderators!"

