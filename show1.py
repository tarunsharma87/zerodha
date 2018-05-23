import os, os.path
import random
import string
import cherrypy
import redis
from pprint import pprint
from mako.template import Template


class MyPage(object):
    @cherrypy.expose
    def index(self):
        r = redis.Redis(host='localhost', port=6379, db=0, password=None)
        data = []
        for i in range(0,10):
            data.append(r.hgetall('member:'+str(i+1)))
        return Template(filename='page1.html').render(data=data)

    @cherrypy.expose
    def submit(self, name):
        print("entering into function")
        name = name.upper()
        result = []
        r = redis.Redis(host='localhost', port=6379, db=0, password=None)
        total = int(r.get("total").decode())
        for i in range(1,total):
            temp = r.hgetall("member:"+str(i))
            string = temp[b'name'].decode()
            print(string)
            if name in string:
                result.append(temp)
        pprint(result)
        print("returning from function")
        return result
        


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        }
    }
    cherrypy.quickstart(MyPage(), '/', conf)

    
