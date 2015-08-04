# coding=utf-8
class TNote:
    def __init__(self, id, cid, notetime, content):
        self.id = id
        self.cid = cid
        self.notetime = notetime
        self.content = content
    def tostring(self):
        format = 'id=%d, cid=%d, notetime=%s, content=%s'
        value = (self.id, self.cid, self.notetime, self.content)
        return (format % value)
if __name__ == '__main__':
    t = TNote(1, 1, 'aa', 'aa')
    print t.tostring()