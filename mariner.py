#!/usr/bin/python3

import urlock
import threading
import time
import baseconvert
import random
import json
import sys
import re

class UrbThread(threading.Thread):
    url = ""
    code = ""
    ship = ""

    def __init__(self, host, code, chan):
        super().__init__()
        self.work = False
        self.url = "https://" + host + ".arvo.network"
        self.host = host
        self.code = code

    def run(self):
        self.work = True
        self.ship = urlock.Urlock(self.url, self.code)
        r = self.ship.connect()
        s = self.ship.subscribe(self.host, "chat-store", "/mailbox/" + chan)

        pipe = self.ship.sse_pipe()

        for m in pipe.events():
            j = json.loads(m.data).get('json')
            self.ship.ack(int(m.id))
            if(j):
                cu = j.get('chat-update')
                mess = cu.get('message')

                if(mess and 'envelope' in mess):
                    env = mess.get('envelope')
                    letter = env.get('letter')
                    text = ""
                    if('url' in letter):
                        text = letter.get('url')
                    elif('text' in letter):
                        text = letter.get('text')
                    else:
                        text = "unknown message type: "
                        print(letter)
                    print("\n===\n~" + env.get('author') + ": " + text + "\n===\n")
            if(self.work is False):
                break

    def stop(self):
        self.work = False


if __name__ == '__main__':
    host = input("host: ")
    code = input("code: ")
    chan = input("chan: ")
    ut = UrbThread(host, code, chan)
    ut.start()
    zod = ut.ship

    urlregex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    while True:
        message = input("=> ")
        if(message == "/quit"):
            ut.stop()
            ut.join()
            sys.exit()
        else:
            s = baseconvert.base(random.getrandbits(128), 10, 32, string=True).lower()
            uid = '0v' + '.'.join(s[i:i+5] for i in range(0, len(s), 5))[::-1]
            msgtype = "text"
            if(re.match(urlregex, message) is not None):
                msgtype = "url"
            p = zod.poke(host, "chat-hook", "json", {"message": {"path": "/" + chan,
                                                                  "envelope": {"uid": uid,
                                                                               "number": 1,
                                                                               "author": "~" + host,
                                                                               "when": int(time.time() * 1000),
                                                                               "letter": {msgtype: message}}}})
