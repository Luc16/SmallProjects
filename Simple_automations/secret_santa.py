import smtplib
from email.message import EmailMessage
from getpass import getpass
from random import random


def send_email(to_email, password, subject, message, server='smtp.gmail.com', from_email='gary.joel1622@gmail.com'):

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    msg.set_content(message)

    print("message ready")
    print("sending email to", to_email)

    server = smtplib.SMTP_SSL(server)
    print("Defined server")
    print("server conected")
    server.login(from_email, password)
    print("logged in...")
    print("sending message")
    server.send_message(msg)
    server.quit()
    print("message sent")


def shuffle(l):
    for i in reversed(range(1, len(l))):
        j = int(random() * i)
        l[i], l[j] = l[j], l[i]
    return l


def main():
    people = []
    mails = []

    shufled = shuffle(people.copy())

    password = getpass("Senha:")

    for m, s in zip(mails, shufled):
        send_email(m, password, "Amigo Secreto",
                   f"O seu amigo secreto é {s}")


if __name__ == '__main__':
    main()
