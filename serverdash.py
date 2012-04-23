#!/usr/bin/env python

import pymongo
import sys
import time
import signal
from topdata import topdata
from commands import getoutput

SLEEP_DELAY = 300
class serverdash:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.topdata = topdata()
        self.hostname = getoutput('hostname')
        self.connect()

    def connect(self):
        self.con = pymongo.Connection(self.host)
        self.db = self.con.servstat
        if not self.db.authenticate(self.username, self.password):
           self.errquit("ERROR, unable to authenticate to "+self.host)
        else:
            print "Success, authenticated!"

    def publish(self):
        self.topdata.update()
        post = {"host":self.hostname, "load":self.topdata.load,
                "time":time.time()}
        self.db.top.insert(post)

    def errquit(self, reason="killed", frame=0):
        print reason
        self.con.disconnect()
        sys.exit(1)

def main():
    if len(sys.argv) < 4:
        print sys.argv[0]+" <hostname> <username> <password>"
        sys.exit(1)
    dash = serverdash(sys.argv[1],sys.argv[2],sys.argv[3])
    signal.signal(signal.SIGINT, dash.errquit)
    while(1):
        dash.publish()
        time.sleep(SLEEP_DELAY)
    dash.con.disconnect()

if __name__ == "__main__":
    main()
