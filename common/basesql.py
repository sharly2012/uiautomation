#!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # @Author: Samuel

import pymysql
from common.baseutil import *
from common.logger import logger

db_host = get_config_value('MySql', 'host')
port = get_config_value('MySql', 'port')
username = get_config_value('MySql', 'username')
password = get_config_value('MySql', 'password')
db_name = get_config_value('MySql', 'db_name')
charset = get_config_value('MySql', 'charset')


class MysqlDB(object):

    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host=db_host,
                port=int(port),
                user=username,
                password=password,
                database=db_name,
                charset=charset
            )
        except pymysql.err.MySQLError as e:
            logger.error('Mysql Error %d: %s' % (e.args[0], e.args[1]))

    def execute_dql_sql(self, sql_query):
        """
        执行DQL SQL
        :param sql_query:
        :return:
        """
        conn = self.connection
        cursor = conn.cursor()
        cursor.execute(sql_query)
        query_result = cursor.fetchall()
        return query_result

    def execute_dml_sql(self, sql_query):
        """
        执行DML SQL，如果失败rollback
        :param sql_query:
        :return:
        """
        conn = self.connection
        cursor = conn.cursor()
        try:
            cursor.execute(sql_query)
            conn.commit()
        except pymysql.err.OperationalError as e:
            conn.rollback()
            logger.error(e)

    def __del__(self):
        self.connection.close()


if __name__ == '__main__':
    aaa = 'select * from candidate_application_referral order by id desc limit 10;'
    db = MysqlDB()
    rows = db.execute_dql_sql(aaa)
    for row in rows:
        uid = row[0]
        name = row[1]
        print(uid, name)
