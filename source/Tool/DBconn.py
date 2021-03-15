
# -*- coding:utf8 -*-
import sys
sys.path.append("..")
from source.Tool.Mysqlpool import Mysql_Pool


class DBconn(object):
    def __init__(self):
        self.Mysql = Mysql_Pool().pool
        self.conn = self.Mysql.connection()
        self.cur = self.conn.cursor()

    def execute_fetchall(self, sql):
        try:
            self.cur.execute(sql)
            contents = self.cur.fetchall()
            return contents
        except Exception:
            self.conn = self.Mysql.connection()
            self.cur = self.conn.cursor()
            return None

    def execute_insert(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
            return True
        except Exception:
            self.conn = self.Mysql.connection()
            self.cur = self.conn.cursor()
            self.conn.rollback()  # 发生错误时回滚
            return False
