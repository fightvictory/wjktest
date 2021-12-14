from flask import Flask, url_for, redirect, render_template, request, current_app, Markup
import flask_admin as admin
from flask_admin.contrib import sqla
from flask_admin import helpers, expose
from flask_wtf import FlaskForm
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required, UserMixin
from wtforms import form, fields, validators

from app import db
from app.models import User, Post, Role


def phone_number_formatter(view, context, model, name):
    return Markup("<nobr>{}</nobr>".format(model.phone)) if model.phone else None


def is_numberic_validator(form, field):
    if field.data and not field.data.isdigit():
        raise validators.ValidationError(gettext('只允许输入数字'))

class UserAdmin(sqla.ModelView):

    can_view_details = True  # show a modal dialog with records details
    action_disallowed_list = ['delete', ]

    form_choices = {
        'type': [role.name for role in Role.query.all()],
    }
    form_args = {
        'dialling_code': {'label': 'Dialling code'},
        'local_phone_number': {
            'label': 'Phone number',
            'validators': [is_numberic_validator]
        },
    }
    form_widget_args = {
        'id': {
            'readonly': True
        }
    }
    column_list = [
        'role',
        'username',
        'email',
        'confirmed',
        'phone',
    ]
    column_labels = {
        'role': '角色',
        'username': '用户名',
        'confirmed': '认证状态',
        'phone': '电话号码'
    }
    column_formatters = dict(role='王继魁')
    # column_searchable_list = [
    #     'role',
    #     'username',
    #     'phone_number',
    #     'email',
    # ]
    column_editable_list = ['role_id', 'username', 'phone', 'confirmed']
    # column_details_list = [
    #     'id',
    #     'featured_post',
    #     'website',
    #     'enum_choice_field',
    #     'sqla_utils_choice_field',
    #     'sqla_utils_enum_choice_field',
    # ] + column_list
    form_columns = [
        'id',
        'username',
        'email',
        'role_id',
        'password_hash',
        'confirmed',
        'name',
        'location',
        'phone',
        'about_me',
        'member_since',
        'last_seen',
    ]
    form_create_rules = [
        'username',
        'first_name',
        'role_id',
        'email',
    ]

    column_auto_select_related = True
    # column_default_sort = [('last_name', False), ('first_name', False)]  # sort on multiple columns

    # custom filter: each filter in the list is a filter operation (equals, not equals, etc)
    # filters with the same name will appear as operations under the same filter
    # column_filters = [
    #     'first_name',
    #     FilterEqual(column=User.last_name, name='Last Name'),
    #     FilterLastNameBrown(column=User.last_name, name='Last Name',
    #                         options=(('1', 'Yes'), ('0', 'No'))),
    #     'phone_number',
    #     'email',
    #     'ip_address',
    #     'currency',
    #     'timezone',
    # ]
    column_formatters = {'phone': phone_number_formatter}

    # setup edit forms so that only posts created by this user can be selected as 'featured'
    def edit_form(self, obj):
        return self._filtered_posts(
            super(UserAdmin, self).edit_form(obj)
        )

    def _filtered_posts(self, form):
        form.featured_post.query_factory = lambda: Post.query.filter(Post.user_id == form._obj.id).all()
        return form

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
admin.add_view(UserAdmin(User, db.session))
admin.add_view(MyModelView(Post, db.session))