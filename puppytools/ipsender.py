#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014, Yeolar <yeolar@gmail.com>
#

import argparse
import config
import ConfigParser
import fcntl
import os
import smtplib
import socket
import struct
from email.mime.text import MIMEText


PROG_NAME = 'pp-ipsender'


def get_ip_address(ifname):
    # another way: `ip -f inet addr show IFNAME`
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def update_records(record_file, ip):
    update = False

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
    default_conf_file = config.DEFAULT_CONF_FILE

    ap = argparse.ArgumentParser(
            prog=PROG_NAME,
            description='An IP mail sender.',
            epilog='Author: Yeolar <yeolar@gmail.com>')
    ap.add_argument('-c', '--conf', action='store', dest='conf_file', type=file,
                    default=os.path.expanduser(default_conf_file),
                    help='configuration file, default: %s' % default_conf_file)
    args = ap.parse_args()

    conf = config.Config()
    conf.read_config_fp('pp-ipsender', args.conf_file)

    ip = get_ip_address(conf.ifname)
    sender = MailSender(conf.mail_server, conf.mail_user, conf.mail_pass)

    if update_records(os.path.expanduser(conf.record_file), ip):
        sender.send(conf.mail_from, conf.mail_to, conf.mail_subject, ip)


if __name__ == '__main__':
    main()

