#!/usr/bin/env python
# encoding: utf-8

#process_youyuan_mysql.py

# -*- coding: utf-8 -*-

import json
import redis
import MySQLdb


def main():
    # 指定redis数据库信息
    rediscli = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    # 指定mysql数据库
    mysqlcli = MySQLdb.connect(host='127.0.0.1', user='root', passwd='qwer1234', db='DuzheMysql', port=3306, charset='utf8')

    while True:
        # FIFO模式为 blpop，LIFO模式为 brpop，获取键值
        source, data = rediscli.blpop(["duzhe:items"])
        item = json.loads(data)

        try:
            # 使用cursor()方法获取操作游标
            cur = mysqlcli.cursor()
            # 使用execute方法执行SQL INSERT语句
            cur.execute("INSERT INTO duzhe_2010_2017(title, author, source, content, link, journal, topic) VALUES (%s, %s, %s, %s, %s, %s, %s)", [item['title'], item['author'], item['source'], item['Content'], item['link'], item['journal'], item['topic']])
            # 提交sql事务
            mysqlcli.commit()
            #关闭本次操作
            cur.close()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

if __name__ == '__main__':
    main()

