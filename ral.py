#!/usr/bin/env python

#port and ip

import sys
import re

def set_port(p):
    global port
    try:
        port = int(p)
    except ValueError:
        raise Exception("the port arguement should be a number")
    if port > 65535 or port < 1:
        raise Exception("the port should between 1 and 65535")

def set_ip(i):
    global ip
    ip = i
    m = re.match(r'^([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])$',ip)
    if not m:
        raise Exception("invalid ip")
    

if len(sys.argv) is 1:
    port = 8000
    ip = "0.0.0.0"
elif len(sys.argv) is 2:
    set_port(sys.argv[1])
    ip = "0.0.0.0"
else:
    set_port(sys.argv[2])
    set_ip(sys.argv[1])

#responce

import subprocess

data404='404 NOT FOUND'
data500='500 INTERNAL SERVER ERROR'


def eva(src):
    def evenif(tail):
        sum=0
        while data[tail] is '?':
            tail = tail -1
            sum = sum + 1
        return sum % 2 is 0
    def runer(pre):
        pre = pre.replace('??','?')
        sp1 = pre.find(' ')
        sp2 = pre.find('\n')
        sp = sp1 if sp1 < sp2 else sp2
        evaler = pre[:sp]
        script = pre[sp:]
        pro = subprocess.Popen(evaler,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        pro.stdin.write("%s\n\n"%script)
        ans = pro.communicate()[0]
        return ans.replace('?','??')
    data = src
    while data.find('<?') is not -1:
        head = data.find('<?')
        tail = data.find('?>',head+1)
        while evenif(tail):
            tail = data.find('?>',tail+1)
        data = '%s%s%s'%(data[:head],runer(data[head+2:tail]),data[tail+2:])
    return data.replace('??','?')
    
def app(environ, start_response):
    method = environ["REQUEST_METHOD"]
    path = environ["PATH_INFO"]
    query = environ["QUERY_STRING"]
    if path[-4:] is '.ral':
        try:
            file = open('.%s'%path, 'r')
            src = file.read()
            file.close()
            try:
                data = eva(src)
            except Exception, e:
                print e
                start_response('500 INTERNAL SERVER ERROR',[('Content-Type','text/html')])
                return [data500]
        except IOError:
            start_response('404 NOT FOUND',[('Content-Type','text/html')])
            return [data404]
    elif path[-5:] is '.html':
        try:
            file = open('.%s'%path, 'r')
            data = file.read()
            file.close()
        except IOError:
            start_response('404 NOT FOUND',[('Content-Type','text/html')])
            return [data404]
    elif path[-1] is '/':
        try:
            file = open('.%sindex.ral'%path,'r')
            src = file.read()
            file.close()
            try:
                data = eva(src)
            except Exception, e:
                print e
                start_response('500 INTERNAL SERVER ERROR',[('Content-Type','text/html')])
                return [data500]
        except IOError:
            try:
                print path
                print '%sindex.html'%path
                file = open('.%sindex.html'%path,'r')
                data = file.read()
                file.close()
            except IOError:
                start_response('404 NOT FOUND',[('Content-Type','text/html')])
                return [data404]
    else:
        pass
    start_response('200 OK',[('Content-Type','text/html')])
    return [data]

#server

from wsgiref.simple_server import make_server

httpd = make_server(ip, port, app)
print "starting server in %s:%d" % (ip,port)
httpd.serve_forever()
