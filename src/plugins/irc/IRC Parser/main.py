"""
An IRC parser.
This is by no means complete.
"""
from __future__ import print_function

from nodeforge.PluginUtils import *
from twisted.internet.task import LoopingCall
import time, random

class Main(Plugin):
    
    priority = Priority.parser
    
    def send(self, string):
        
        if isinstance(string, unicode):
            string = string.encode('raw_unicode_escape')
        
        self.core.sendLine(string)
        print('>>> %s' % string)
        
    def privmsg(self, who, msg):
        """
        http://www.irchelp.org/irchelp/rfc/chapter4.html#c4_4_1
        """
        
        self.send('PRIVMSG %s :%s' % (who, msg) )
        
    def join(self, channels, passes=""):
        """
        http://www.irchelp.org/irchelp/rfc/chapter4.html#c4_2_1
        """
        self.send("JOIN %s %s" % (channels, passes) )
        
        
    def ping(self, msg="a"):
        self.send("PING :%s" % msg)
        
    def setnick(self, name):
        self.send("NICK %s" % name)
        
    def onData(self, raw):
        '''
        First we will parse the stream and save it to self.context
        Then we will do the login procedure.
        '''
        
        p = parseirc(raw)
        self.context = p
 
        if p[1] == 'PING':
            self.send("PONG :%s" % p[2][0])
        elif p[1] == ERR_NICKNAMEINUSE:
            self.nick = "%s%s" %(self.core.nick, random.randint(1,999))
            self.setnick(self.nick)
            
        
    def onLoad(self):
        self.core.delimiter = '\r\n'
        
        if not hasattr(self.core, 'nick'):
            self.nick = 'AnonymousPerson'
        else:
            self.nick = self.core.nick
    
    def onConnect(self):
        self.setnick(self.nick)
        self.send("USER %s host server :Madewith http://code.google.com/p/nodeforge/" % self.nick)
        
        LoopingCall(self.ping).start(60)
        
    
def parseirc(input):
    """
    BNF in rfc2812
    message    =  [ ":" prefix SPACE ] command [ params ] crlf
    params     =  *14( SPACE middle ) [ SPACE ":" trailing ]
               =/ 14( SPACE middle ) [ SPACE [ ":" ] trailing ]
    trailing   =  *( ":" / " " / nospcrlfcl )
    """
    \
    prefix = ""
    trailing = []
    
    
    if input == "":
        raise Exception("Parse string is empty")
    
    if input[0] == ":":
        prefix, input = input[1:].split(' ', 1)
        
    
    data = input.split(" :",1)
    
    if len(data) == 1:
        params = input.split()
    else:
        input, trailing = data
        params = input.split()
        params.append(trailing)
        
    command = params.pop(0)
    
    return prefix, command, params
    
    
ERR_NICKNAMEINUSE = '433'