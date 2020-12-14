import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from phonebook import phonebook

#define now
now = datetime.now().strftime("%I:%M%p on %B %d, %Y")

#create list of emails
to_emails=[]
for name, [number, email] in phonebook.items():
    if email:
        to_emails.append(email)
print(to_emails)


# set up server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login('', '')


#send log to ultracold@gmail.com every two weeks
def update():
    msg_update = MIMEMultipart()
    msg_update['To'] = ''
    msg_update['From'] = ''
    msg_update['Subject'] = ''
    body = "Attached is log of power check program as of %s." % now
    content = MIMEText(body, 'plain')
    msg_update.attach(content)

#attach log
    with open('power.log', 'r') as f:
        log = MIMEText(f.read())
    log.add_header('Content-Disposition', 'log', filename='power.log')
    msg_update.attach(log)

    server.send_message(msg_update)

#send exception to ultracold@gmail.com as soon as it occurs
def exception(exception):
    msg_exception = MIMEMultipart()
    msg_exception['To'] = ''
    msg_exception['From'] = ''
    msg_exception['Subject'] = 'Power check software exception'
    body = "Exception logged at %s: %s" % (now, exception)
    content = MIMEText(body, 'plain')
    msg_exception.attach(content)

    server.send_message(msg_exception)

#send outage alert to emails in phonebook as soon as it occur
def outage():
    msg_outage = MIMEMultipart()
    msg_outage['To'] =', '.join(to_emails)
    msg_outage['From'] = ''
    msg_outage['Subject'] = 'URGENT: Power outage alert'

    body = "Power outage recorded at %s." % now
    content = MIMEText(body, 'plain')
    msg_outage.attach(content)

    server.send_message(msg_outage)

#send power restored alert to emails in phonebook as soon as it occurs
def restored():
    msg_restored = MIMEMultipart()
    msg_restored['To'] = ', '.join(to_emails)
    msg_restored['From'] = ''
    msg_restored['Subject'] = 'Power restored'
    body = "Power restored at %s" % now
    content = MIMEText(body, 'plain')
    msg_restored.attach(content)

    server.send_message(msg_restored)
    
