import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os


def send_email(receiver_email_id, photos_dir):

    mail_content = '''Hello From PicSearch,
        "Face Detection from Group Photos" is a web application designed to automatically detect and highlight faces in group photos.
        We Sending Your Photos from an event.
        '''
    # The mail addresses and password
    files = os.listdir(photos_dir)
    sender_address = 'aumkan23@gmail.com'
    sender_pass = 'fltwcowuyrzkneyn'
    receiver_address = receiver_email_id
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Photos For You'
    # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    for f in files:  # add files to the message
        file_path = os.path.join(photos_dir, f)
        attachment = MIMEApplication(
            open(file_path, "rb").read(), _subtype="txt")
        attachment.add_header('Content-Disposition', 'attachment', filename=f)
        message.attach(attachment)
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    # login with mail_id and password
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


if __name__=="__main__":
    send_email("aumkan23@gmail.com",'static/events/maniac_week')