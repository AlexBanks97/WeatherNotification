import os
import sys
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import WeatherApp

COMMASPACE = ", "

sender = "alexbanksrpi@gmail.com"
sender_pw = open("gmpw.txt",  "r", encoding="utf8").readline()
recipients = []

# Read recipients:
with open("mailinglist.txt", "r", encoding="utf8") as f:
    next(f)
    for line in f:
        mailAndLocation = line.split(",")
        message = WeatherApp.GetWeather(mailAndLocation[1].strip())
        recipients.append(mailAndLocation[0].strip())

        # Build the email
        outer = MIMEMultipart()
        outer["Subject"] = "Python Weathercast"
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
            print("Email sent!")
        except:
            print("Unable to send the email. Error: ", sys.exc_info()[0])
            raise
