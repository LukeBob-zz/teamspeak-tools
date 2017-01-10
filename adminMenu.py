


#!/usr/bin/python3

# Author: Luke

import argparse
from time import sleep
from subprocess import call
import ts3
from ts3.examples.viewer import view
import os

if os.name == 'nt':
    clr = 'cls'
else:
    clr = 'clear'

class col:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    OKBLUE = '\033[94m'


class timeFormat():
    def __init__(self, msec):
        self.msec = int(msec)

    def seconds(self):
        seconds = (int(self.msec) / 1000)
        seconds = int(seconds)

        second = 0
        minute = 0
        hour   = 0
        day    = 0

        for i in range(0, seconds):

            second = (second + 1)

            if second == 60:
                second = 0
                minute = (minute + 1)

            if minute == 60:
                minute = 0
                hour = (hour + 1)

            if hour == 24:
                hour = 0
                day = (day + 1)
        return ('%s Days %s Hours %s Minutes and %s Seconds'%(day,hour, minute, second))


parser = argparse.ArgumentParser(description='Admin pannel for Teamspeak-3')
parser.add_argument('--host', '-s', help='Server to connect to.')
parser.add_argument('--port', '-p', help='Server port to connect to.')
parser.add_argument('--user', '-u', help='Username to connect')
parser.add_argument('--password', '-v', help='password to connect')

args = parser.parse_args()

if args.host and args.port and args.user and args.password:
    host = args.host
    port = args.port
    user = args.user
    password = args.password
else:
    parser.print_help()
    exit(0)


def options():
    print('\n\n'+col.OKBLUE+col.BOLD+'\t    Options'+'\n'+col.BOLD+col.OKGREEN+r'''
+-----------------------------------+
| Channelkick    |  Serverkick      |
+-----------------------------------+
| Ban            |  getinfo         |
+-----------------------------------+
| Channel-View   |  Mass-message    |
+-----------------------------------+
| Options        |  Private-message |
+-----------------------------------+
| Complain       |  Server-info     |
+-----------------------------------+
| Server-stop    |  Change-name     |
+-----------------------------------+

         ''')

    print(col.FAIL+col.BOLD+r'''             Quit
             ----'''+'\n'+col.ENDC)

def complainadd(user, reason):
    clientlist = ts3conn.clientlist()
    clientlist = [client for client in clientlist if client["client_type"] != "1"]

    for client in clientlist:
        if client['client_nickname'] == user:
            clid = client['clid']
            info = ts3conn.clientinfo(clid=clid)
            for i in info:
                cdbid = i['client_database_id']
                try:
                    ts3conn.complainadd(tcldbid=cdbid, message=reason)
                except:
                    print('\nCould Not Add Complaint !\n')
                    break

                print('\n[#] Complaint successfully submitted !\n')
            break

def UserInfo(user):
    try:
        clientlist = ts3conn.clientlist()
        clientlist = [client for client in clientlist if client["client_type"] != "1"]

        for client in clientlist:
            if client['client_nickname'] == user:
                clid = client['clid']
                info = ts3conn.clientinfo(clid=clid)
                for i in info:
                    print('\n\n[#] Client: '+i['client_nickname'])
                    print('\n[#] Client Ip               : '+i['connection_client_ip'])
                    print('[#] Client Country          : [%s]'%(i['client_country']))
                    print('[#] Client Platform         : '+i['client_platform'])
                    print('[#] Client Database ID      : [%s]'%(i['client_database_id']))
                    print('[#] Client Talk Power       : [%s]'%(i['client_talk_power']))
                    print('[#] Client Version          : '+i['client_version'])

                    idlesec = i['client_idle_time']
                    idlesec = int(idlesec)
                    print('[#] Client Idle Time        : '+timeFormat(idlesec).seconds())

                    millsec = i['client_lastconnected']
                    millsec = int(millsec)
                    print('[#] Client Last Connected   : '+timeFormat(millsec).seconds())
                    print('[#] Client Total Connections: [%s]'%(i['client_totalconnections']))
                    print('\n\n')
                    sleep(1)
                    input('\n\n[#] Press Enter to continue...\n\n')
                break

    except: raise


## Client ban ##

def ClientBan(User, Reason, time, ts3conn):
    try:
        clientlist = ts3conn.clientlist()
        clientlist = [client for client in clientlist if client["client_type"] != "1"]

        for client in clientlist:
            if client['client_nickname'] == User:
                client_sid = client['clid']
                try:
                    ts3conn.banclient(clid=client_sid, time=time, banreason=Reason)
                except: raise
    except: raise



## Channel kick ##

def ChannelKick(User, Reason, ts3conn):
    try:
        clientlist = ts3conn.clientlist()
        clientlist = [client for client in clientlist if client["client_type"] != "1"]

        for client in clientlist:
            if client['client_nickname'] == User:
                client_sid = client['clid']
                try:
                    ts3conn.clientkick(reasonid=4, reasonmsg=Reason, clid=client_sid)
                    print("\n[#] Successfully kicked "+ User+"\n")
                except: raise
    except: raise


## Server Kick ##

def ServerKick(User, Reason, ts3conn):
    try:
        clientlist = ts3conn.clientlist()
        clientlist = [client for client in clientlist if client["client_type"] != "1"]

        for client in clientlist:
            if client['client_nickname'] == User:
                client_sid = client['clid']
                try:
                    ts3conn.clientkick(reasonid=5, reasonmsg=Reason, clid=client_sid)
                    print("\n[#] Successfully kicked "+ User+"\n")
                except: raise

    except: raise


## trys to make connection ##
try:
    with ts3.query.TS3Connection(host, port) as ts3conn:

        try:
            ts3conn.login(client_login_name=user, client_login_password=password)

        except ts3.query.TS3QueryError as err:
            print("Login Failed:", err.resp.error['msg'])
            exit(1)

        print("\n  Connected to: %s's server\n"%(host))
        view(ts3conn, sid=1)
        quit = False
        while not quit:

            options()
            choice = input('\nOption: ')

            ## server kick ##

            if choice == 'Serverkick' or choice == 'serverkick':
                user = input('User:')
                Reason = input('Reason:')
                ServerKick(user, Reason, ts3conn)

            ## channel kick ##

            elif choice == 'Channelkick' or choice == 'channelkick':
                user = input('User:')
                Reason = input('Reason:')
                ChannelKick(user, Reason, ts3conn)

            ## Client Ban ##

            elif choice == 'Ban' or choice == 'ban':
                user = input('User:')
                Reason = input('Ban message:')
                time = input('Time in seconds:')
                ClientBan(user, Reason, time, ts3conn)

            ## Get Info ##

            elif choice == 'getinfo' or choice == 'Getinfo':
                user = input('\nUser:')
                UserInfo(user)

            ## quit ##

            elif choice == 'Quit' or choice == 'quit':
                exit(0)


            ## Channel View ##

            elif choice == 'channel-view' or choice == 'Channel-view' or choice == 'channelview':
                call(clr, shell=True)
                view(ts3conn, sid=1)

            ## Mass message ##

            elif choice == 'Mass-message' or choice == 'mass-message' or choice == 'massmessage':
                message = input('\nMass-message:')
                if message:
                    ts3conn.gm(msg=message)
                else:
                    print('\nCannot send Empty message !\n')

            ## Private-message ##
            elif choice == 'Private-message' or choice == 'private-message' or choice == 'privatemessage':
                user = input('\nUser:')
                messg = input('Message:')
                clientlist = ts3conn.clientlist()
                clientlist = [client for client in clientlist if client["client_type"] != "1"]
                for client in clientlist:
                    if client['client_nickname'] == user:
                        clid = client['clid']
                        ts3conn.sendtextmessage(targetmode=1, target=clid, msg=messg)
                        sleep(1)
                        print('\nMessage Successfully Sent to '+user+'\n\n')



            elif choice == 'options' or choice == 'Options':
                options()


            elif choice == 'Complain' or choice == 'complain':
                user   = input('\nUser:')
                reason = input('\nReason:')
                if user:
                    complainadd(user, reason)

            elif choice == 'Server-info' or choice == 'server-info' or choice == 'serverinfo':
                info = ts3conn.hostinfo()
                for i in info:
                    print('\nTotal connection packets sent     : [%s]'%(i['connection_packets_sent_total']))
                    print('Total Packets Recived             : [%s]'%(i['connection_packets_received_total']))
                    print('Server Instance Uptime            : [%s]'%(i['instance_uptime']))
                    print('Virtual Servers running           : [%s]'%(i['virtualservers_running_total']))
                    print("Max Clients                       : [%s]"%(i['virtualservers_total_maxclients']))

                break

            elif choice == 'Stop-server' or choice  == 'stop-server' or choice == 'stopserver':
                try:
                    ts3conn.serverstop(sid=1)
                except:
                    print('Insufficient permissions.')

            elif choice == 'Change-name' or choice == 'change-name' or choice == 'changename':
                try:
                    newname = input('\nNew name:')
                    ts3conn.clientupdate(client_nickname=newname)
                    sleep(2)
                    print('\n\n[#] Name changed to %s\n\n'%(newname))

                except ts3.query.TS3QueryError as err:
                    print("\n\[#]  unable to change name !\n\n")
                    sleep(1)



            ## Choice not recognised ##
            else:
                print('\n Option NOT Recognised !')

except KeyboardInterrupt:
        print('\n Terminating Connection \n')
        time.sleep(2)
        exit(0)












