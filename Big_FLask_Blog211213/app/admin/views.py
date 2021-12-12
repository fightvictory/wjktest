from flask import Flask, url_for, redirect, render_template, request, current_app
import flask_admin as admin
from flask_admin.contrib import sqla
from flask_admin import helpers, expose
from flask_wtf import FlaskForm
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required, UserMixin
from wtforms import form, fields, validators

from app import db
from app.models import User, Post


# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        return current_user.is_authenticated

# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('admin.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login

        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User.query.filter_by(email=form.email.data).first() 
            login_user(user)

        if current_user.is_authenticated:
            return redirect(url_for('admin.index'))
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()

            form.populate_obj(user)
            # we hash the users password to avoid saving it as plaintext in the db,
            # remove to use plain text:
            user.password = generate_password_hash(form.password.data)

            db.session.add(user)
            db.session.commit()

            login_user(user)
            return redirect(url_for('admin.index'))
        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('admin.index'))


class LoginForm(FlaskForm):
    email = fields.StringField(validators=[validators.DataRequired()])
    password = fields.PasswordField(validators=[validators.DataRequired()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    # def get_user(self):
    #     return User.query.filter_by(email=form.email.data).first() 

# app = current_app._get_current_object()
# Create admin

admin = admin.Admin(current_app, 'Example: Auth', index_view=MyAdminIndexView(), base_template='admin/my_master.html', template_mode='bootstrap4')


# Add view
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Post, db.session))