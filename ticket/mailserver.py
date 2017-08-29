# -*- coding: utf-8 -*-

import imaplib, email, re, time
import requests
from ticket.models import Ticket

from django.conf import settings

def save(info):
    ticket = Ticket(**info)
    ticket.save()

def confirm_fw(body):
    reg = re.compile(ur"（(.*)）")
    try:
        url = reg.findall(body)[0]
        r = requests.get(url)
    except IndexError:
        pass

def scan():
    mail = imaplib.IMAP4_SSL('imap.exmail.qq.com')
    mail.login(settings.MAIL_SERVER_UAERNAME, settings.MAIL_SERVER_PASSWD)
    mail.list()
    mail.select("inbox")
    result, data = mail.search(None, "ALL")
    ids = data[0]
    id_list = ids.split()
    for email_id in id_list:
        result, data = mail.fetch(email_id, "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_string(raw_email)
        info = {}
        for part in msg.walk():
            if part.get_content_type() == 'text/plain' or part.get_content_type()=="text/html":
                content = part.get_payload(decode=True).decode("gb2312")

                # 判断是否是来自qq邮箱的自动转发确认邮件
                title = email.Header.decode_header(msg.get('Subject'))[0][0]
                if "QQMail" in title:
                    confirm_fw(content)

                try:
                    reg = re.compile(r"1\.(.*)\r\n")
                    ticket_msg = reg.findall(content)[0]
                    ticket_msg = ticket_msg.split("，")[:5]
                    if len(ticket_msg) == 1:  # PATCH
                        ticket_msg = ticket_msg[0].split(",")[:5]
                    info["name"], info["time"], info["dist"], info["no"], info["seat"] = ticket_msg
                    info["no"] = str(info["no"].replace(u"次列车",""))
                    info["name"], info["dist"], info["seat"] = info["name"].encode("UTF-8"), info["dist"].encode("UTF-8"), info["seat"].encode("UTF-8")
                    if u"年" not in info["time"]:  # PATCH
                        info["time"] = time.strftime(u"%Y") + u"年" + info["time"]
                    ts = time.mktime(time.strptime(info["time"],u'%Y年%m月%d日%H:%M开'))
                    info["time"] = time.strftime('%Y%m%dT%H%M00Z',time.gmtime(ts))
                    break
                except IndexError:
                    continue

        if info.get("no") and info["no"] is not None:
            sender = msg.get("to")
            sender = email.Header.decode_header(sender)
            reg = re.compile(r"\<(.*)\>")
            info["sender"] = reg.findall(sender[0][0])[0]
            save(info)

        # delete the mail
        mail.store(email_id, '+FLAGS', '\\Deleted') # commited during debug
    mail.expunge()
    mail.logout()



if __name__=="__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')

    scan()