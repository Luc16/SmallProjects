import smtplib
import ssl
from getpass import getpass


def send_email(message, reciever="luc.joffily.ribas@gmail.com"):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "luc.joffily.ribas@gmail.com"
    receiver_email = reciever
    password = getpass("Senha:")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        try:
            server.login(sender_email, password)
            res = server.sendmail(sender_email, receiver_email, message)
            print('Email sent!')
        except:
            print("Could not login or send the mail.")


if __name__ == '__main__':
    send_email("TE AMO\n"
               "TE AMO\n"
               "TE AMO\n"
               "TE AMO\n"
               "O Terra eh horrivel >:|")
