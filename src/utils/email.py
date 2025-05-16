from src.middleware import mail
from flask_mail import Message


def send_mail(to: str, title: str, content: str) -> None:
    msg = Message(subject=title, recipients=[to], body=content)
    mail.send(msg)
