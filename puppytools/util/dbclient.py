# -*- coding: utf-8 -*-
#
# Copyright (C) 2015, Yeolar
#

import MySQLdb


class DBClient(object):

    def __init__(self, host, port, user, password, database, charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.conn = MySQLdb.connect(
                host=host,
                port=port,
                user=user,
                passwd=password,
                db=database,
                charset=charset)

    def __del__(self):
        self.conn.close()

    def __call__(self):
        return DBCursor(self.conn)


class DBCursor(object):

    def __init__(self, conn):
        self.conn = conn

    def __enter__(self):
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()


class DBTable(object):

    def __init__(self, db, table):
        self.db = db
        self.table = table

    def _make_select_sql(self, *args, **kwargs):
        fields = ','.join(args)
        condition = ' AND '.join([k + '=' + str(v) for k, v in kwargs.items()])
        return 'SELECT %s FROM %s WHERE %s' % (fields, self.table, condition)

    def description(self):
        with self.db() as cursor:
            cursor.execute('DESC %s' % self.table)
            d = cursor.fetchall()
            return d

    def col_names(self):
        return [i[0] for i in self.description()]

    def get(self, *args, **kwargs):
        with self.db() as cursor:
            cursor.execute(self._make_select_sql(*args, **kwargs))
            d = cursor.fetchone()
            return d

    def getall(self, *args, **kwargs):
        with self.db() as cursor:
            cursor.execute(self._make_select_sql(*args, **kwargs))
            d = cursor.fetchall()
            return d

