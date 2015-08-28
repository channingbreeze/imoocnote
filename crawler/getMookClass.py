# coding=utf-8
import sys, getopt, time
from dbHelper import DBHelper
from crawler import Crawler
class GetMookClass:
    def __init__(self):
        self.c = Crawler()
        self.db = DBHelper('localhost', 'root', '', 'test', 3306)
        self.lorder = int(time.time())
    def usage(self):
        print '''
            -h print this message
            -e everyday run, just check first page and find new classes
            -a all refresh, check all the pages and add new classes
        '''
    def run(self):
        if len(sys.argv) == 1:
            self.usage()
        else:
            try:
                opts, args = getopt.getopt(sys.argv[1:], "hea")
                for op, value in opts:
                    if op == "-h":
                        self.usage()
                    elif op == "-e":
                        self.startCrawl()
                    elif op == "-a":
                        self.startCrawl(1)
                    else:
                        self.usage()
            except:
                self.usage()
    def startCrawl(self, all=0):
        self.c.login("http://www.imooc.com/course/list", "http://www.imooc.com/user/login")
        if(all):
            index = 1
            while(self.crawlSinglePage(index)):
                index = index + 1
        else:
            self.crawlSinglePage(1)
    def crawlSinglePage(self, pageId):
        url = 'http://www.imooc.com/course/list?page=%d' % pageId
        classes = self.c.getClasses(url)
        if(len(classes) == 0):
            return 0
        else:
            for cls in classes:
                dbcls = self.db.selectClassByMid(cls.mid)
                if(not dbcls):
                    cls.lorder = self.lorder
                    cid = self.db.insertClass(cls)
                    self.refreshTitles(cid, cls.mid)
            return 1
    def refreshTitles(self, cid, mid):
        titles = self.c.getTitles(cid, mid)
        pid = 0
        for title in titles:
            if(title.mid == 0):
                pid = self.db.insertTitle(title)
            else:
                title.pid = pid
                self.db.insertTitle(title)
if __name__ == '__main__':
    g = GetMookClass()
    g.run()