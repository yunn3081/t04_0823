import smtplib
from email.mime.text import MIMEText

def send_mail(customer, email, location):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '4f234275d29ea6'
    password = 'd8f26682595ca3'
    message = f"<h3>Account Information</h3><ul><li>Customer: {customer}</li><li>Email: {email}</li><li>Location: {location}</li></ul>"

    sender_email = 's1061439@mail.yzu.edu.tw'
    receiver_email = 'yunn3081@gmail.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Cancerfree Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    #send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login,password)
        server.sendmail(sender_email, receiver_email, msg.as_string())