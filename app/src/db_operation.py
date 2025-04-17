# -*-coding:utf-8 -*-

"""
@author: hanscal
@date: 2024/10/4 10:40
"""
import time
import pymysql

from conf.config import mysql_host, mysql_port, mysql_database, mysql_user, mysql_password

class DbOperation(object):
    def __init__(self, host=mysql_host, port=mysql_port, db=mysql_database,
                 user=mysql_user, passwd=mysql_password, charset='utf8mb4'):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port
        self.charset = charset
        self.conn = None
        self._conn()

    # Establish the connection to the MySQL database using PyMySQL
    def _conn(self):
        try:
            self.conn = pymysql.connect(host=self.host,
                                        user=self.user,
                                        password=self.passwd,
                                        database=self.db,
                                        port=self.port,
                                        charset=self.charset)
            return True
        except pymysql.MySQLError as e:
            print(f"Connection Error: {e}")
            return False

    # Reconnect to the MySQL database in case of connection loss
    def _reConn(self, num=28800, stime=3):  # Retry connection with a limit (num), sleeping between retries (stime)
        _number = 0
        _status = True
        while _status and _number <= num:
            try:
                self.conn.ping(reconnect=True)  # Ping to check if the connection is still alive
                _status = False
            except:
                if self._conn():  # Try to reconnect
                    _status = False
                    break
                _number += 1
                time.sleep(stime)  # Sleep before retrying

    # Select method to fetch data from the database
    def select(self, sql=''):
        try:
            self._reConn()  # Ensure connection is alive
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
            return result
        except pymysql.MySQLError as e:
            print(f"Error executing select query: {e}")
            return False

    # Handle method for executing SQL queries like INSERT, UPDATE, DELETE
    def handle(self, sql=''):
        try:
            self._reConn()  # Ensure connection is alive
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SET NAMES utf8")  # Set UTF-8 character set
                cursor.execute(sql)
                self.conn.commit()  # Commit the transaction
            return True
        except pymysql.MySQLError as e:
            print(f"Error executing handle query: {e}")
            return False

    # Close the MySQL connection
    def close(self):
        if self.conn:
            self.conn.close()
