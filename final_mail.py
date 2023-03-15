from email.mime.text import MIMEText
import ssl
import smtplib
from datetime import datetime
from datetime import timedelta
import sys
from github import Github
import os
import re

smtp_server = "smtp.gmail.com"
port = 587  # for starttls
sender_email = "smit.softvan@gmail.com"
password = (os.environ['EMAIL_PASSWORD'])


# create a GitHub instance using a personal access token
g = Github(os.environ['GITHUB_TOKEN'])


# get the Python repository by name
repo = g.get_repo("smit-darji/On_Github_RELEASE_EMAIL")

repository_name = str(repo.full_name)

today = datetime.utcnow().date()
last_week = today - timedelta(days=7)

# get all releases for the last 7 days
releases = repo.get_releases()
if releases.totalCount == 0:
    print("No releases found.")
else:
    recent_releases = [release for release in releases if release.published_at.date() > last_week]
    
    # loop through recent releases and print their version and body details
    
    email_body = ""
    for release in recent_releases:
        email_body += f"\n\tRelease : {release.title}\n"
        email_body += f"\tVersion   : {release.tag_name}\n"
        email_body += f"\tReleas URL: = {release.html_url}\n"
        email_body += f"\tBody      : {release.body}\n\t------------------------------------------"
    
    # set up the email message
    
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        
        # send the message
        message = ("Subject: NEW RELEASE OF LAST WEEK. \n\nHello Team,\n\nWe're pleased to announce the availability of a new release of {0} \nHere are the details:{1} \nThank you for your interest in {2}!\n\nBest regards,\nTeam ABC".format(repository_name,email_body,repository_name))
        print(message)
        recipient_email = "sahilvandra.softvan@gmail.com"
        server.sendmail(sender_email, recipient_email, message)
    