from flask_mail import Mail, Message
from threading import Thread
from flask import current_app, render_template
from app import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    # 获取当前的线程的app
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY邮件前缀'] + subject, sender=app.config['FLASKY邮件发送人'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    # mail.send(msg)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr