#!/usr/bin/python3

# Author: LukeBob
# Requires pip3 install ts3
# teamspeak AFK bot, moves afk clients to a specified channel

import sys, time, ts3
import ts3.definitions

minutes       = 45                         # Max idle time minutes (This is where to set your max idle time)                 
cid           = 5                          # Channel "cid" to move AFK clients to (Look up your list of channels to get id)
USER          = 'serveradmin'              # server username
PASS          = ''                         # server password
HOST          = 'localhost'                # server host
PORT          = '10011'                    # server port
SID           = 1                          # admin-sid (leave this)
MAX_IDLE_TIME = (int(minutes) * 1000 * 60) # max idle time, miliseconds (leave this)


def Welcome(ts3conn): 
    print ('\n      AFK-BOT: Connected to host: %s:%s\n      Max-afk-time: %s Minutes\n'%(HOST,PORT,str(minutes)))
    while True:
        try:
            time.sleep(10)       
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
                            msg = ('Client: '+client['client_nickname']+' Got Moved Reason: AFK TOO LONG!')
                            ts3conn.clientmove(clid=clid, cid=cid)
                            ts3conn.gm(msg=msg)
                            #ts3conn.clientmove(clid=clid, msg=msg)               Also Poke AFK client
                            print ('Client '+client['client_nickname']+' Moved: AFK', )

                    except KeyboardInterrupt:
                        print ('\nExiting...\n')
                        sys.exit(0)
                    except:
                        pass

                

        except KeyboardInterrupt:
            print ('\nExiting...\n')
            sys.exit(0)
        except:
            pass  

def main():
    with ts3.query.TS3Connection(HOST,PORT) as ts3conn:
        ts3conn.login(client_login_name=USER, client_login_password=PASS)
        ts3conn.use(sid=SID)
        Welcome(ts3conn)

if __name__ == '__main__':
    main()
 
