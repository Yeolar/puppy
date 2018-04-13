#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Yeolar
#

import argparse
import fcntl
import os
import smtplib
import socket
import struct
import sys
from email.mime.text import MIMEText

from puppytools.util.colors import *
from puppytools.util.config import load_config


PROG_NAME = os.path.splitext(os.path.basename(__file__))[0]

CONF = load_config(PROG_NAME)


def get_ip_address(ifname):
    # another way: `ip -f inet addr show IFNAME`
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])
    except IOError as e:
        print red('Error: "%s" for %s' % (e, ifname))
        sys.exit(1)


def update_records(record_file, ip):
    update = False

    dir = os.path.dirname(record_file)
    if not os.path.exists(dir):
        os.makedirs(os.path.dirname(record_file))

    with open(record_file, 'a+') as fp:
        lines = fp.readlines()
        if not lines or ip != lines[-1].strip():
            fp.write(ip + '\n')
            update = True

    return update


class MailSender(object):

    def __init__(self, server, user, passwd):
        self.server = server
        self.user = user
        self.passwd = passwd

    def make_message(self, fr, to, subject, content):
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = fr
        msg['To'] = to
        return msg.as_string()

    def send(self, fr, to, subject, content):
        s = smtplib.SMTP()
        s.connect(self.server)
        s.login(self.user, self.passwd)
        s.sendmail(fr, to, self.make_message(fr, to, subject, content))
        s.close()
        print 'Send mail to %s.' % to


def main():
    ap = argparse.ArgumentParser(
            prog='pp-' + PROG_NAME,
            description='An IP mail sender.',
            epilog='Author: Yeolar <yeolar@gmail.com>')
    args = ap.parse_args()

    ip = get_ip_address(CONF.IFNAME)
    sender = MailSender(CONF.MAIL_SERVER, CONF.MAIL_USER, CONF.MAIL_PASS)

    if update_records(os.path.expanduser(CONF.RECORD_FILE), ip):
        sender.send(CONF.MAIL_FROM, CONF.MAIL_TO, CONF.MAIL_SUBJECT, ip)


if __name__ == '__main__':
    main()

