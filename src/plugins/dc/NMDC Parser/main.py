from __future__ import print_function
from nodeforge.PluginUtils import *
from twisted.internet.task import LoopingCall

password = 'mypassword'
tag      = "http://code.google.com/p/nodeforge/<++ V:0.707,M:A,H:1/0/0,S:4>$ $0.005 $No Email$0$"

class Main(Plugin):
    priority = Priority.parser
    
    def onConnect(self):
        # keepalive message every minute.
        LoopingCall(self.tell, self.nick, 'a').start(60)
        

    def onData(self, raw):
        '''
        First we will parse the stream and save it to self.context
        Then we will do the login procedure.
        '''
        
        self.parse(raw)
        
        # load the parse information here.
        context = self.context
        
        # start processing
        if context.infotype == 'Lock':
            lock = context.split[1]
            self.send('$Key '+lock2key(lock))
            self.send('$ValidateNick %s' % self.nick)
        elif context.infotype == 'Hello' and context.split[1] == self.nick:
            self.send('$Version 1,0091')
            self.send('$MyINFO $ALL %s %s' % (self.nick, tag))
            self.send('$GetNickList')
        elif context.infotype == 'GetPass':
            self.send('$MyPass %s' % password)
            
        
    def onLoad(self):
        self.core.delimiter = '|'
        
        if not hasattr(self.core, 'nick'):
            self.nick = 'AnonymousPerson'
        else:
            self.nick = self.core.nick
    
    
    
    def parse(self, raw):
        """
        Perform parsing on a string and save results to self.context.
        
        Parsing Guide
        
        what:     Either 'chat' for a public chat message or 'info' for anything else.
        
        infotype: Specifies the kind of message for 'info'.
        Ex. $Exit --> infotype == 'Exit'
        
        sender: the person that sent the message. None if the server sent it without
        a name.
        
        msg: 
        
        """
        
        split = raw.split(' ')
        
        what = infotype = sender = msg = cmd = args = None
        
        if raw[0] == '<':
            what = 'chat'
            sender = split[0][1:-1]
            msg    = raw[raw.find('>')+1:]
            
            temp = raw.count(' ')
            if temp == 1:
                cmd  = raw.split(' ', 2)[1]
            else:
                temp = raw.split(' ', 3)
                cmd  = temp[1]
                args = temp[2]
                
            
            reply = lambda msg: self.chat(msg)
            tell  = lambda msg: self.tell(sender, msg)
            
        elif raw[0] == '$':
            what = 'info'
            infotype = split[0][1:]
            
            if infotype == 'To:':
                sender = split[3]
                
                try:
                    msg  = ' '.join(split[5:])
                    cmd  = split[5]
                    args = ' '.join(split[6:])
                except IndexError:
                    pass
                
            reply = lambda msg: self.tell(sender, msg)
            tell  = lambda msg: self.tell(sender, msg)
        
        
        # copy the current parse context into a variable
        self.context = Context(locals())

    
    
    def send(self, string):
        """
        TODO: thread safe
        """
        
        if isinstance(string, unicode):
            string = string.encode('raw_unicode_escape')
        
        string = string.replace('|','&#124').replace('|','&#36')
        
        try:
            self.core.sendLine(string)
            print('>>> %s' % string)
        except Exception as e:
            print(e)
            
    def tell(self, target, msg):
        self.send('$To: %s From: %s $<%s> %s' % (target, self.nick, self.nick, msg))
    
    def chat(self, msg):
        self.send('<%s> %s'% (self.nick, msg))
    
    def emote(self, msg):
        self.send('<%s> +me %s' % (self.nick, msg) )
        


class Context(object):
    """
    This is a storage object.
    It basically turns a dictionary into an object.
    
    You can now use shortcuts like this.
    context.blah == context['blah']
    
    Currently used by the parser here.
    """
    def __init__(self, dic):
        self.__dict__.update(dic)


# WARNING This algorithm doesn't work with YnHub 1.036 all the time.
import array
def lock2key(lock):
    """
    Generates response to $Lock challenge from Direct Connect Servers
    Borrowed from free sourcecode online.
    """
    lock = array.array('B', lock)
    ll = len(lock)
    key = list('0'*ll)
    for n in xrange(1,ll):
        key[n] = lock[n]^lock[n-1]
    key[0] = lock[0] ^ lock[-1] ^ lock[-2] ^ 5
    for n in xrange(ll):
        key[n] = ((key[n] << 4) | (key[n] >> 4)) & 255
    result = ""
    for c in key:
        if c in (0, 5, 36, 96, 124, 126):
            result += "/%%DCN%.3i%%/" % c
        else:
            result += chr(c)
    return result