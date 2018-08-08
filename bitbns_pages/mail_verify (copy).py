#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 22:48:16 2018

@author: chennam
"""

import imaplib
#import logging
import email
import requests
import time
def login():
    SERVER ="imap.gmail.com"
#    SMTP_PORT   = 993
    USER  = "###############"
    PASSWORD = "###############"

    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(USER,PASSWORD)
    return mail
def select_inbox(mail):
    return mail.select("inbox")
def search_bitbns(mail):
    return mail.search(None,'FROM','"Bitbns Support"')
def subj_body(mail,mailid):
    typ, data = mail.fetch(mailid, '(RFC822)')
    for response_part in data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            email_subject = msg['subject']
            #email_from = msg['from']
    rrec=msg.get_payload()
    body=rrec[0].get_payload(decode=True)
    return email_subject,body
def get_url_from_body(body):
    x=body.decode().split()
    text=" ".join(x[1:-92])
    start=text.find("<")
    
    end=text.find(">")
    url=text[start+1:end]
    return url
def verify_mail():
    mail=login()
    select_inbox(mail)
    typ,data=search_bitbns(mail)
    e_id=data[0].split()[-1]
    subj,body=subj_body(mail,e_id)
    url=get_url_from_body(body)
    r=requests.get(url)
    if "Successfully Verified" in r.text:
        print(r.text)
    else:
        time.sleep(60)
        verify_mail()
