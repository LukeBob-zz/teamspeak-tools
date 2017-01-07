# teamspeak-tools

## afk-bot.py 

 **afk bot uses Benedikt Schmitt's ts3 api in conjunction with ts3 query. It just sits there waiting for clients 
 idle time to reach above 90 min's then it will move them to any channel you specify, with the cid variable.**
 
 **Usage**
 
     python3 afk-bot.py or chmod 755 afk-bot.py && ./afk-bot.py 


## Pokebot.py

 **Pokebot takes 3 arguments, 'name of target', 'num of times', 'message', it will then connect to the ts3 server and 
 look for the specified target when found it will begin to poke the shit out of the target.**
 
 **Usage**
 
     ./pokebot.py <target name> <times to poke> <'message wrapped in quotes'> 
 
## Jokebot.py
 
**Give it a lits of comments or jokes to read from and set it off, the bot will read through the jokes/comments
at random untill it has read every one.**
 
**Usage**
 
 
## adminMenu.py
 
**Small admin menu for simple task's like banning, kicking, moving, messaging etc.
Requires host, port, user and password to run**
 
**Usage**
 
     usage: adminMenu.py [-h] [--host HOST] [--port PORT] [--user USER] [--password PASSWORD]
                   
    Admin pannel for Teamspeak-3

    optional arguments:
      -h, --help            show this help message and exit
      --host HOST, -s HOST  Server to connect to.
      --port PORT, -p PORT  Server port to connect to.
      --user USER, -u USER  Username to connect
      --password PASSWORD, -v PASSWORD   password to connect  
  
 ** Example **
 
     ./adminMenu.py --host ts3.myserver.com --port 10011 --user serveradmin --password mySecretPassword 
              
        

