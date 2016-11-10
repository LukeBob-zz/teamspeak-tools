#!/usr/bin/python3

# Author: LukeBob
#
# teamspeak AFK bot, moves afk clients to a specified channel
#
# uses Benedikt Schmitt's ts3 api in conjunction with ts3 query. to find out more visit https://github.com/benediktschmitt/py-ts3

import sys
import time
import ts3
import ts3.definitions

msg='AFK TOO LONG!'            # Poke message, only if you enable poke by uncommenting it in the loop.
cid = 5                        # Channel "cid" to move AFK clients to
USER = 'serveradmin'           # server username
PASS = ''                      # server password
HOST = 'localhost'             # server host
PORT = '10011'                 # server port
SID = 1                        # leave this
MAX_IDLE_TIME = 5400000        # max idle time


def Welcome(ts3conn): 
    while True:
        time.sleep(2)       
        clientlist = ts3conn.clientlist()
        clientlist =  [client for client in clientlist \
                       if client["client_type"] != "1"]         
     
        for client in clientlist:            
            clid = client['clid']
            info = ts3conn.clientinfo(clid=clid)
            for ino in info:
                try:
                    time.sleep(1)
                    if (int(ino['client_idle_time'])) > (int(MAX_IDLE_TIME)):
                        ts3conn.clientmove(clid=clid, cid=cid)
                        #ts3conn.clientmove(clid=clid, msg=msg)               Also Poke AFK client
                        print ('Client Moved AFK')
                
                except ts3.query.TS3QueryError as err:
                    if err.resp.error["id"] != "770" and err.resp.error["id"] != "512":  # Stops client already in channel error
                        raise  

def main():
    with ts3.query.TS3Connection(HOST,PORT) as ts3conn:
        ts3conn.login(client_login_name=USER, client_login_password=PASS)
        ts3conn.use(sid=SID)
        Welcome(ts3conn)

if __name__ == '__main__':
    main()
