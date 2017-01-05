# Author: Luke
#
# Teamspeak 3 joke bot. for python 3^
#
# Requires pip instilation of ts3

import ts3
from pathlib import Path
import time
import random

user       = 'serveradmin'  # server query password
password   = ''             # server query user
host       = ''             # server query host
port       = 10011          # server query port

interval   = 600            # Joke, insult interval - (seconds)

insultList = []
jokelist   = ''             # path to joke-list, insult list


def SendInsult(Joke, ts3conn):
    if Joke:
        try:
            print('Sending joke ...')
            ts3conn.gm(msg=Joke)
            print('Joke sent Successfully')
        
    
        except ts3.query.TS3QueryError as err:
            print('\nSending Failed with error message -', err.resp.error['msg'])


def getJokes(jokelist):
    myfile = Path(jokelist)

    if myfile.is_file:
        with open (jokelist, 'r') as file:
            for line in file:
                lines = file.readline()
                insultList.append(lines)
    else:
        print('Cannot Find Specified file.')
        exit(1)


def main():        
    with ts3.query.TS3Connection(host, port) as ts3conn:

        try:
            ts3conn.login(client_login_name=user, client_login_password=password) # trys to login with user and password
            print('\n\n Successfully Connected to %s on port %s'%(host, port))

        except ts3.query.TS3QueryError as err:
            print('login Failed:', err.resp.error['msg'])
            exit(1)

        try:
            ts3conn.clientupdate(client_nickname='Insult-Bot')  # trys to change name to insult bot
        except ts3.query.TS3QueryError as err:
            print('Could not change name:', err.resp.error['msg'])
            pass
        
        getJokes(jokelist)

        for insult in range(len(insultList)):
            insult = random.choice(insultList)
            SendInsult(insult, ts3conn)
            if insult in insultList: insultList.remove(insult)  # removes used joke, insult
            time.sleep(interval)
            print('Next insult in 5 minutes')
        exit(0)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n Exiting ! \n')
        exit(0)
