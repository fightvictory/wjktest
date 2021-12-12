from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm
from app import db
from app.email import send_email

@auth.route('/login', methods=['GET', 'POST']) 
def login(): 
    form = LoginForm() 
    if form.validate_on_submit(): 
        user = User.query.filter_by(email=form.email.data).first() 
        if user is not None and user.verify_password(form.password.data): 
            login_user(user, form.remember_me.data) 
            next = request.args.get('next') 
            if next is None or not next.startswith('/'): 
                next = url_for('main.index') 
            return redirect(next) 
        flash('用户名或密码错误') 
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '确认你的flask博客账号', 'mail/confirm', user=user, token=token)
        flash('你已经注册，一封确认邮件已经发送到你的邮箱，确认后才能登录')
        # return redirect(url_for('auth.login'))
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

@auth.route('/logout') 
@login_required 
def logout(): 
    logout_user() 
    flash('你已经退出了！') 
    return redirect(url_for('main.index'))

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('你已经邮件确认了账户，可以登录了！')
    else:
        flash('确认链接已失效，令牌已过期！')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认你的flask博客账号',
            'mail/confirm', user=current_user, token=token)
    flash('你已经注册，一封确认邮件已经发送到你的邮箱，确认后才能登录')
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))
        
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')