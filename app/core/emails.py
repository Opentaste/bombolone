# -*- coding: utf-8 -*-
"""
emails.py
~~~~~~

:copyright: (c) 2013 by Bombolone
""" 
# Imports outside Bombolone
import os
import datetime
import types
import smtplib
from flask import current_app, render_template
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.utils import COMMASPACE
from config import STATIC_FOLDER

try:
    from email.utils import formatdate
except ImportError:
    formatdate = datetime.datetime.now


class GenericEmail(object):
    
    list_images = []
    template = None
    subject = None
    client = None
    
    def __init__(self, recipient, context):
        self.recipient = recipient
        self.context = context
        self.email_from = "My Domain <noreply@mydomain.com>"
    
    def get_client(self):
        if not self.client:
            try:
                # Send the message via local SMTP server.
                self.client = smtplib.SMTP()
                self.client.connect('connect_name')
                self.client.login('username','password')
            except BaseException, e:
                print e
                return False
        return self.client
    
    def render(self):
        if not self.subject:
            raise Exception("No Subject")
        elif not self.html_template or not self.text_template:
            raise Exception("No Template")
        else:
            self.subject = self.subject % self.context
            self.raw_body_html = render_template(self.html_template, **self.context)
            self.raw_body_text = render_template(self.text_template, **self.context)
            msg_root = MIMEMultipart('related')
            msg_root['Subject'] = self.subject
            msg_root['From'] = _encode_str(self.email_from)
            msg_root['To'] = _encode_str(self.recipient)
            msg_alternative = MIMEMultipart('alternative')
            msg_root.attach(msg_alternative)
            msg_text = MIMEText(_encode_str(self.raw_body_text))
            msg_alternative.attach(msg_text)  
            msg_text = MIMEText(_encode_str(self.raw_body_html), 'html')
            msg_alternative.attach(msg_text) 
            for filename in self.list_images:
                fullpath = os.path.join(STATIC_FOLDER,"layout/emails/",filename)
                fp = open(fullpath, 'rb')
                msg_image = MIMEImage(fp.read())
                fp.close()
                msg_image.add_header('Content-ID', '<%s>' % filename.replace(".",""))
                msg_root.attach(msg_image)           
            return msg_root.as_string()
    
    def send(self):
        client = self.get_client() # da sostituire con uno classico
        if not client:
            return {
                "error": True
            }
        email_body = self.render()
        response = client.sendmail(_encode_str(self.email_from), self.recipient, email_body)
        client.quit()
        return {
            "error": False
        }

#--- Helpers ----------------------------------------------
def _convert_to_strings(list_of_strs):
    """ """
    if isinstance(list_of_strs, (list, tuple)):
        result = COMMASPACE.join(list_of_strs)
    else:
        result = list_of_strs
    return _encode_str(result)

def _encode_str(s):
    """ """
    if type(s) == types.UnicodeType:
        return s.encode('utf8')
    return s

class WelcomeEmail(GenericEmail):
    """ """
    subject = "Welcome to Bombolone"
    html_template = "emails/welcome.html"
    text_template = "emails/welcome.txt"

class ChangeEmail(GenericEmail):
    """ """
    subject = "Bombolone Change email"
    html_template = "emails/set_new_email.html"
    text_template = "emails/set_new_email.txt"

class RememberPassword(GenericEmail):
    """ """
    subject = "Bombolone Remember Password"
    html_template = "emails/remember_password.html"
    text_template = "emails/remember_password.txt"
