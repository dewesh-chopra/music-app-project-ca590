import os
from flask_mail import Mail, Message
from dotenv import load_dotenv

class Email:
    def __init__(self, app):
        app.config["MAIL_SERVER"] = 'smtp.office365.com'
        app.config["MAIL_PORT"] = '587'
        app.config["MAIL_USERNAME"] = os.getenv('MAIL_USERNAME')
        app.config["MAIL_PASSWORD"] = os.getenv('MAIL_PASSWORD')
        app.config["MAIL_USE_TLS"] = True
        app.config["MAIL_USE_SSL"] = False
        self.mail = Mail(app)
    
    def compose_mail(self, subject, message, email):
        msg = Message(subject, sender='chopradewesh@outlook.com', recipients=[email])
        msg.body = message
        self.mail.send(msg)
