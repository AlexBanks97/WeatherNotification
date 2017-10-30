import os
import os.path
import sys
import smtplib
import argparse
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import WeatherApp

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("mailinglist")
parser.add_argument("mail_password")
args = parser.parse_args()

COMMASPACE = ", "
mail_list_path = args.mailinglist
sender = "alexbanksrpi@gmail.com"
sender_pw = args.mail_password

os.chdir(mail_list_path)

# Read recipients:
with open(mail_list_path, "r", encoding="utf8") as f:
    next(f)
    for line in f:
        recipients = []
        mailAndLocation = line.split(",")
        message = WeatherApp.GetWeather(mailAndLocation[1].strip())
        recipients.append(mailAndLocation[0].strip())

        # Build the email
        outer = MIMEMultipart()
        outer["Subject"] = "Weather of the day"
        outer["To"] = COMMASPACE.join(recipients)
        outer["From"] = sender
        outer.attach(MIMEText(message, "plain"))
        outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

        composed = outer.as_string()

        # Send the emial
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as s:
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(sender, sender_pw)
                s.sendmail(sender, recipients, composed)
                s.close()
            print("Email sent to", mailAndLocation[0] )
        except:
            print("Unable to send the email. Error: ", sys.exc_info()[0])
            raise
