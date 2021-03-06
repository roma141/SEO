#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb as mdb

class DB(object):

    def __init__(self, nombrebd="seo", user="root", passwd=""):
#         self.db = mdb.connect(host="mysql.myprodu.com",user="carlos",passwd="siempre1",db=nombrebd)
        self.db = mdb.connect(host="gtienda.com",user="carlos",passwd="siempre1",db=nombrebd, charset='utf8')
#         self.db = mdb.connect(host="localhost",user="root",passwd="siempre1",db=nombrebd)
        #self.db = mdb.connect(host="192.168.1.109",user="carlos",passwd="123",db=nombrebd, charset='utf8')
        # self.db = mdb.connect(host="localhost",user="carlos",passwd="123",db=nombrebd, charset='utf8')
        self.c = self.db.cursor(mdb.cursors.DictCursor)
        
    def cierra(self):
        self.commit()
        self.c.close()
        self.db.close()
        
    def commit(self):
        self.db.commit()

    def Ejecuta(self, sql):
        self.c.execute(sql.encode("utf-8"))
        return [row for row in self.c.fetchall()]

    def Ejecuta1(self, sql):
        self.c.execute(sql)
        rows = self.c.fetchall()
        self.cierra()
        return [row for row in rows]

    def UltimoID(self):
        rows = self.Ejecuta("select last_insert_id() as ID")
        r = rows[0]["ID"]
        return r
    
    def escape_string(self, s):
        return mdb.escape_string(s)
