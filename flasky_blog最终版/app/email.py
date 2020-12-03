from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwagrs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY邮件主题前缀'] + subject, sender=app.config['FLASK邮件发送者'], recipients=[to])
    msg.body = render_template(template+'.txt', **kwagrs)
    msg.html = render_template(template+'.html', **kwagrs)
    # mail.send(msg)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr