import smtplib
from index import mail
from flask import render_template
from email.message import EmailMessage
from index.config import ConfigManager


def send_password_reset_mail(user):
    token = user.get_reset_password_token()
    msg = EmailMessage() 

    msg['Subject'] = 'Reset Password'
    msg['From'] = ConfigManager.MAIL_ADDRESS
    msg['To'] = ConfigManager.MAIL_ADDRESS #send an E-Mail to myself
    msg.set_content(render_template('email/reset_password.txt', user=user, token=token))

    with smtplib.SMTP_SSL(ConfigManager.MAIL_SERVER, ConfigManager.MAIL_PORT) as server:
        server.login(user=ConfigManager.MAIL_ADDRESS,
                    password=ConfigManager.MAIL_PASSWORD)
        server.send_message(msg)
