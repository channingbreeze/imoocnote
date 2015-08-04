# coding=utf-8
import MySQLdb
from tClass import TClass
from tTitle import TTitle
class DBHelper:
    def __init__(self, host, user, passwd, db, port):
        self.conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, port=port, charset='utf8')
    def selectClassByMid(self, mid):
        cursor = self.conn.cursor()
        f = 'select * from t_class where mid=%d'
        v = (mid)
        sql = (f % v)
        cursor.execute(sql)
        row = cursor.fetchone()
        if(row != None):
            c = TClass(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
        else:
            c = None
        cursor.close()
        return c
    def selectTitleByMid(self, mid):
        cursor = self.conn.cursor()
        f = 'select * from t_title where mid=%d'
        v = (mid)
        sql = (f % v)
        cursor.execute(sql)
        row = cursor.fetchone()
        if(row != None):
            t = TTitle(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        else:
            t = None
        cursor.close()
        return t
    def selectTitleByTitle(self, title):
        cursor = self.conn.cursor()
        f = 'select * from t_title where title=\'%s\''
        v = (title)
        sql = (f % v)
        cursor.execute(sql)
        row = cursor.fetchone()
        if(row != None):
            t = TTitle(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        else:
            t = None
        cursor.close()
        return t
    def insertClass(self, c):
        cursor = self.conn.cursor()
        f = 'insert into t_class (mid, title, image, subtitle, timespan, hasnote, hasover, lorder) values (%d, \'%s\', \'%s\', \'%s\', \'%s\', %d, %d, %d)'
        v = (c.mid, c.title, c.image, c.subtitle, c.timespan, c.hasnote, c.hasover, c.lorder)
        sql = (f % v)
        cursor.execute(sql)
        id = cursor.lastrowid
        self.conn.commit()
        cursor.close()
        return id
    def insertTitle(self, t):
        cursor = self.conn.cursor()
        f = 'insert into t_title (cid, title, titletype, mid, tid, timespan, pid) values (%d, \'%s\', \'%s\', %d, %d, \'%s\', %d)'
        v = (t.cid, t.title, t.titletype, t.mid, t.tid, t.timespan, t.pid)
        sql = (f % v)
        cursor.execute(sql)
        id = cursor.lastrowid
        self.conn.commit()
        cursor.close()
        return id
    def deleteTitleByCid(self, cid):
        cursor = self.conn.cursor()
        f = 'delete from t_title where cid=%d'
        v = (cid)
        sql = (f % v)
        cursor.execute(sql)
        self.conn.commit()
        cursor.close()
    def __del__(self):
        self.conn.close()
if __name__ == '__main__':
    db = DBHelper('localhost', 'root', '', 'test', 3306)
    c = db.selectClassByMid(454)
    if(c != None):
        print c.tostring()
        i = db.insertClass(c)
        print i
    else:
        print 'no such class'
    t = db.selectTitleByMid(8820)
    if(t != None):
        print t.tostring()
        i = db.insertTitle(t)
        print i
    else:
        print 'no such title'
    t = db.selectTitleByTitle('课程准备')
    if(t != None):
        print t.tostring()
    else:
        print 'no such title'
    db.deleteTitleByCid(334)