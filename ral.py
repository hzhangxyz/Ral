#!/usr/bin/env python
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
    port = 80
    ip = "0.0.0.0"
elif len(sys.argv) is 2:
    set_port(sys.argv[1])
    ip = "0.0.0.0"
else:
    set_port(sys.argv[2])
    set_ip(sys.argv[1])

print ip
print port
