#!/usr/bin/python3
#
# Author: Luke
#
# Pokebot for teamspeak3, Pokes any client [n] ammount of times with a custom message
import time, ts3, sys, traceback

USER = 'serveradmin' # Query user
PASS = ''            # Query Password
HOST = 'localhost'   # Query Server-host
PORT = '10011'       # Query Server-Port
SID = 1              # Serveradmin sid (dont touch)

def usage():
    print ('\n./Poke-bot.py <Name> <how many times> <Message>\n')
    sys.exit(0)

def Poke(ts3conn,target,timesMany,msg):
    try:       
        clientlist = ts3conn.clientlist()
        clientlist =  [client for client in clientlist \
                       if client["client_type"] != "1"]

        for client in clientlist:        
            clid = client['clid']
            nickname = client['client_nickname']   
            if str(nickname) == str(target):
                print (' \nFound target',target,'\n\nPoking now!...\n')
                for i in range(int(timesMany)):
                    time.sleep(0.5)
                    ts3conn.clientpoke(clid=clid, msg=msg)
                sys.exit(0)
        sys.exit(0)
    
    except KeyboardInterrupt:
        print ('  \nExiting...\n')
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)    


def main(target,timesMany,message):
    with ts3.query.TS3Connection(HOST,PORT) as ts3conn:
        try:
            ts3conn.login(client_login_name=USER, client_login_password=PASS)
            ts3conn.use(sid=SID)
            Poke(ts3conn,target,timesMany,message)

        except ts3.query.TS3QueryError as err:
            if err.resp.error["id"] == "520":
                print ('\nWrong Username Or Password!\n')
            sys.exit(0)

        
if __name__ == '__main__':
    try:
        if len(sys.argv) != 4:
            usage()  
        int(sys.argv[2])
        main(sys.argv[1],sys.argv[2],sys.argv[3])
    
    except ValueError:
        print ('\nSecond Arg \''+sys.argv[2]+'\'  Must Be Integer Value!\n')
        usage() 
    
