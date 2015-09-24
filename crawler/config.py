# coding=utf-8
import ConfigParser
class Config:
    def __init__(self):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read('config.ini')
    def getuserinfo(self):
        userinfo = {
            'username' : self.cf.get('userinfo', 'username'),
            'password' : self.cf.get('userinfo', 'password'),
        }
        return userinfo
if __name__ == '__main__':
    c = Config()
    print c.getuserinfo()['username']
    print c.getuserinfo()['password']