# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from .models import Ticket
from .mailserver import scan

import time

# Create your views here.

def show_ics(req, sender):
    tickets = Ticket.objects.filter(sender = sender)
    template = u"""
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//6vdata.com//ical-generator//EN
METHOD:REQUEST
NAME:12306 Calendar
X-WR-CALNAME:12306 Calendar
TIMEZONE-ID:Asia/Hong_Kong
X-WR-TIMEZONE:Asia/Hong_Kong"""
    uid = 0
    for ticket in tickets:
        end_ts = time.mktime(time.strptime(ticket.time,u'%Y%m%dT%H%M%SZ'))
        end_time = time.strftime('%Y%m%dT%H%M00Z', time.localtime(end_ts+1*3600))
        uid = uid + 1
        template = template + u"""
BEGIN:VEVENT
UID:{uid}
SEQUENCE:0
DTSTAMP:{time}
DTSTART:{time}
DTEND:{end_time}
SUMMARY:{summary}
END:VEVENT""".format(time = ticket.time, summary=ticket.no+" "+ticket.seat+" "+ticket.dist, end_time=end_time, uid = str(uid)+"ticket")
    template = template + u"END:VCALENDAR"
    return HttpResponse(template, content_type='text/calendar; charset=utf-8')


def renew_ics(req):
    scan()
    return HttpResponse("OK", content_type='text/plain; charset=utf-8')

