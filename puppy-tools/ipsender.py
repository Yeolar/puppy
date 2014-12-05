#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014, Yeolar <yeolar@gmail.com>
#

import argparse
import ConfigParser
import fcntl
import os.path
import smtplib
import socket
import struct
from email.mime.text import MIMEText


PROG_NAME = 'pp-ipsender'
DEFAULT_CONF_FILE = '~/.pp-tools/pp-tools.cfg'


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def update_records(record_file, ip):
    update = False
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
            prog=PROG_NAME,
            description='An IP mail sender.',
            epilog='Author: Yeolar <yeolar@gmail.com>')
    ap.add_argument('-c', '--conf', action='store', dest='conf_file', type=file,
                    default=os.path.expanduser(DEFAULT_CONF_FILE),
                    help='configuration file, default: %s' % DEFAULT_CONF_FILE)
    args = ap.parse_args()

    conf = ConfigParser.ConfigParser()
    conf.readfp(args.conf_file)

    ifname = conf.get('pp-ipsender', 'ifname')
    record_file = os.path.expanduser(conf.get('pp-ipsender', 'record_file'))
    mail_server = conf.get('pp-ipsender', 'mail_server')
    mail_user = conf.get('pp-ipsender', 'mail_user')
    mail_pass = conf.get('pp-ipsender', 'mail_pass')
    mail_from = conf.get('pp-ipsender', 'mail_from')
    mail_to = conf.get('pp-ipsender', 'mail_to')
    mail_subject = conf.get('pp-ipsender', 'mail_subject')

    ip = get_ip_address(ifname)
    sender = MailSender(mail_server, mail_user, mail_pass)

    if update_records(record_file, ip):
        sender.send(mail_from, mail_to, mail_subject, ip)


if __name__ == '__main__':
    main()

