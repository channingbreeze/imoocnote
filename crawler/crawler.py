# coding=utf-8
import urllib
import urllib2
import cookielib
import re
from tClass import TClass
from tTitle import TTitle
class Crawler:
    def login(self, hosturl, loginurl):
        cl = cookielib.CookieJar()
        cp = urllib2.HTTPCookieProcessor(cl)
        opener = urllib2.build_opener(cp)
        urllib2.install_opener(opener)
        urllib2.urlopen(hosturl)
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Referer' : hosturl
        }
        postData = {
            'username' : 'channingbreeze@163.com',
            'password' : 'hao1lie2July',
            'remember' : '1'
        }
        postData = urllib.urlencode(postData)
        request = urllib2.Request(loginurl, postData, headers)
        content = opener.open(request)
        return content.read()
    def getClasses(self, url):
        response = urllib2.urlopen(url)
        html = response.read()
        html = html.replace(' ', '').replace('\r', '').replace('\n', '')
        regstr = '<li class="course-one"><a href="/([^/]*?)/(\d*)" target="_self"><div class="course-list-img"><img width="240" height="135" alt="(.*?)" src="(.*?)"></div><h5><span>(.*?)</span></h5><div class="tips"><p class="text-ellipsis">(.*?)</p><span class="(?:.*?)">(.*?)</span><span class="l ml20">(.*?)</span></div><span class="time-label">(.*?)</span><b class="follow-label">(.*?)</b></a></li>';
        regstr = regstr.replace(' ', '')
        items = re.findall(regstr, html, re.S)
        classes = []
        for item in items:
            if(item[6] == '更新完毕'):
                hasover = 1
            else:
                hasover = 0
            c = TClass(0, int(item[1]), item[2], item[3], item[5], item[8], 0, hasover, 0)
            classes.append(c)
        return classes
    def getTitles(self, cid, mid):
        url = 'http://www.imooc.com/learn/%d' % (mid)
        chapterReg = '<div class="chapter (?:.*?)" ><h3><span class="icon-(?:.*?)"></span><strong><i class="state-(?:.*?)"></i>(.*?)(\d+)(.*?)</strong></h3>(.*?)</div>'
        chapterReg = chapterReg.replace(' ', '')
        response = urllib2.urlopen(url)
        html = response.read()
        html = html.replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')
        items = re.findall(chapterReg, html, re.S)
        titles = []
        for item in items:
            chapter = TTitle(0, cid, item[2][3:], '', 0, int(item[1]), '', 0)
            titles.append(chapter)
            titles.extend(self.getSubTitles(item[3], cid, 0))
        return titles
    def getSubTitles(self, html, cid, pid):
        titleReg = '<li>(?:<em class=".*?">.*?</em>)?<a target="_blank" href=\'/([^/]*?)/(\d+)\' class="(?:[a-z]*?)">(\d+)-(\d+) ([^<]*?)\((\d*):(\d*)\)<i class="(?:[a-z-]*?)"></i></a></li>|<li>(?:<em class=".*?">.*?</em>)?<a target="_blank" href=\'/([^/]*?)/(\d+)\' class="(?:[a-z]*?)">(\d+)-(\d+) ([^<]*?)<i class="(?:[a-z-]*?)"></i></a></li>'
        titleReg = titleReg.replace(' ', '')
        html = html.replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')
        items = re.findall(titleReg, html, re.S)
        subs = []
        for item in items:
            if item[5] != '':
                sub = TTitle(0, cid, item[4], item[0], int(item[1]), int(item[3]), ('%s:%s') % (item[5], item[6]), pid)
            else:
                sub = TTitle(0, cid, item[11], item[7], int(item[8]), int(item[10]), '', pid)
            subs.append(sub)
        return subs
if __name__ == '__main__':
    c = Crawler()
    c.login("http://www.imooc.com/course/list", "http://www.imooc.com/user/login")
    classes = c.getClasses('http://www.imooc.com/course/list?page=1')
    for cls in classes:
        print cls.tostring()
    titles = c.getTitles(2, 491)
    for title in titles:
        print title.tostring()
    titles = c.getTitles(4, 486)
    for title in titles:
        print title.tostring()