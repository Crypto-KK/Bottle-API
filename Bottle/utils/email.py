from Bottle import mail
from flask_mail import Message
from flask import current_app, render_template
import threading

def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass

def send_mail(to, subject, template, **kwargs):
    msg = Message(
        '[Bottle]' + subject,
        sender=current_app.config['MAIL_USERNAME'],
        body='感谢您的注册',
        recipients=[to]

    )
    msg.html = render_template(template, **kwargs)
    app = current_app._get_current_object()
    t = threading.Thread(target=send_async_email, args=[app, msg])
    t.start()