import smtplib, ssl


smtp_address = 'smtp.gmail.com'
smtp_port = 465

email_address = 'josephdanguy5@gmail.com'
email_password = 'nplt koha qixl qsah '

email_receiver = 'josephdanguy5@gmail.com'


def send_mail():
    with smtplib.SMTP_SSL(smtp_address, smtp_port) as server:
        server.login(email_address, email_password)
        server.sendmail(email_address, email_receiver, 'Hello les psychos')
        


if __name__ == "__main__":
    send_mail()