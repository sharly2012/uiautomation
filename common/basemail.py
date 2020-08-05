#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Samuel

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from common.baseutil import get_config_value

mail_host = get_config_value('Email', 'mail_host')
mail_user = get_config_value('Email', 'mail_user')
mail_pwd = get_config_value('Email', 'mail_pwd')
mail_sender = get_config_value('Email', 'mail_sender')
receivers = get_config_value('Email', 'receivers')
cc = get_config_value('Email', 'cc')

subject = '接口自动化测试报告'


def mail_with_attach(html_report):
    message = MIMEMultipart()
    message['From'] = mail_sender
    message['To'] = receivers
    message['Cc'] = cc
    message['Subject'] = subject
    message.attach(MIMEText('接口自动化测试报告', 'plain', 'utf-8'))
    with open(html_report, 'r', encoding='utf-8') as f:
        att1 = MIMEText(f.read(), 'base64', 'utf-8')
        att1['Content-Type'] = 'application/octet-stream'
        att1['Content-Disposition'] = 'attachment; filename="result.html"'
        message.attach(att1)
    return message


def connect_send(message):
    try:
        server = smtplib.SMTP(mail_host)
        server.login(user=mail_user, password=mail_pwd)
        server.send_message(msg=message)
        server.close()
        print('发送成功')
    except Exception as e:
        print('发送失败')
        print(e)
