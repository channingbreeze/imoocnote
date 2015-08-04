# coding=utf-8
class TClass:
    def __init__(self, id, mid, title, image, subtitle, timespan, hasnote, hasover, lorder):
        self.id = id
        self.mid = mid
        self.title = title
        self.image = image
        self.subtitle = subtitle
        self.timespan = timespan
        self.hasnote = hasnote
        self.hasover = hasover
        self.lorder = lorder
    def tostring(self):
        format = 'id=%d, mid=%d, title=%s, image=%s, subtitle=%s, timespan=%s, hasnote=%d, hasover=%d, lorder=%d'
        value = (self.id, self.mid, self.title, self.image, self.subtitle, self.timespan, self.hasnote, self.hasover, self.lorder)
        return (format % value)
if __name__ == '__main__':
    t = TClass(1, 1, 'aa', 'aa', 'aa', 'aa', 0, 1, 1321123321213)
    print t.tostring()