from flask import Flask, request, make_response, abort, render_template, url_for, session, redirect, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = '12345678a'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://puser:123456@127.0.0.1/pblog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(FlaskForm):
    name = StringField('你叫什么名字？', validators=[DataRequired(message='请输入你的名字')])
    submit = SubmitField('提交')


@app.route('/', methods=['GET', 'POST'])
def index():
    user_agent = request.headers.get('User-Agent')
    # print(request.headers)

    # 11-9
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False), current_time=datetime.utcnow())

    '''
    ######11-5###############
    name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = form.name.data
        if old_name is not None and old_name != session.get('name'):
            flash('你改变了你的名字', 'danger')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.utcnow())
    '''
    # return '<p>你的浏览器是 {},</p>'.format(user_agent)
    # return '<h1>Bad Request</h1>', 400
    # response = make_response('<h1>This document carries a cookie!</h1>') 
    # response.set_cookie('answer', '42')
    # return response



@app.route('/user/<name>')
def user(name):
    # return '<h1>Hello, {}!</h1>'.format(name)
    return render_template('user.html', name=name)

@app.route('/user1/<id>')
def get_user(id):
    user = None
    if not user:
        print(id)
        abort(404)
    return '<h1>Hello, {}!</h1>'.format(id)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)