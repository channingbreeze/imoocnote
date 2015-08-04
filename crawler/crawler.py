# coding=utf-8
import urllib2
import re
from tClass import TClass
from tTitle import TTitle
class Crawler:
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
        chapterReg = '<div class="learnchapter  learnchapter-active " ><h3><span>-</span><strong><i class="hasOpenOn"></i>(.*?)(\d+)(.*?)</strong></h3>(.*?)</div>'
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
        titleReg = '<li><a target="_blank" href=\'/([^/]*?)/(\d+)\' class="(?:[a-z]*?)">(\d+)-(\d+) ([^<]*?)\((\d*):(\d*)\)</a></li>|<li><a target="_blank" href=\'/([^/]*?)/(\d+)\' class="(?:[a-z]*?)">(\d+)-(\d+) ([^<]*?)</a></li>'
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
    classes = c.getClasses('http://www.imooc.com/course/list?page=1')
    for cls in classes:
        print cls.tostring()
    titles = c.getTitles(2, 405)
    for title in titles:
        print title.tostring()
    titles = c.getTitles(4, 373)
    for title in titles:
        print title.tostring()