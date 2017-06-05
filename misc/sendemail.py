def __send_email(user, passwd, receiver, subject, content, mailserver):
    '''
    user = gmail sender name
    passwd = gmail sender password
    receiver = receiver or multiple receiver by list
    subject = email subject
    content = email content
    '''
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    try:
        if isinstance(receiver, list): receiver = ','.join(receiver)
        message = MIMEMultipart()
        message['From'] = user
        message['To'] = receiver
        message['Subject'] = subject
        message.attach(MIMEText(content))
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()
        mailserver.login(user, passwd)
        mailserver.sendmail(user, receiver, message.as_string())
        mailserver.close()
        return 'Send email success'
    except Exception as e:
        print(e)
        return 'Send email failed'

def send_by_gmail(user, passwd, receiver, subject, content):
        mailserver = smtplib.SMTP('smtp.gmail.com', 587)
        __send_email(user, passwd, receiver, subject, content, mailserver)

def send_by_iis(user, passwd, receiver, subject, content):mailserver = smtplib.SMTP('smtp.gmail.com', 587)
        mailserver = smtplib.SMTP('mail.iis.sinica.edu.tw')
        __send_email(user, passwd, receiver, subject, content, mailserver)
