# coding=utf-8
class TTitle:
    def __init__(self, id, cid, title, titletype, mid, tid, timespan, pid):
        self.id = id
        self.cid = cid
        self.title = title
        self.titletype = titletype
        self.mid = mid
        self.tid = tid
        self.timespan = timespan
        self.pid = pid
    def tostring(self):
        format = 'id=%d, cid=%d, title=%s, titletype=%s, mid=%d, tid=%d, timespan=%s, pid=%d'
        value = (self.id, self.cid, self.title, self.titletype, self.mid, self.tid, self.timespan, self.pid)
        return (format % value)
if __name__ == '__main__':
    t = TTitle(1, 1, 'aa', 'aa', 1, 1, 'aa', 1)
    print t.tostring()