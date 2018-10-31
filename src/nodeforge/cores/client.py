"""
Core file for TCP/IP Clients
"""
from __future__ import with_statement
from __future__ import print_function

import socket, sys

from nodeforge.PluginManager import loadFolder
from threading import Lock

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet.error import ConnectionRefusedError

class Client(ClientFactory, LineReceiver):

    plugins  = []    
    lock     = Lock()

    def __init__(self, **kwargs):
        """
        This should be initialized with the following variables:
        address
        port
        
        Any other variables are optional?
        
        """
        
        # To be overriden by a protocol plugin
        self.delimiter  = '\n'
        self.MAX_LENGTH = 16384
        
        # set the kwargs as instance variables.
        self.__dict__.update(kwargs)
        
        # load plugins by calling method
        self.loadPlugins(reload=False)
        self.connect()
        
    def connect(self):
        """
        Used to connect to a server
        """
        
        reactor.connectTCP(self.address, self.port, self)
        
        
    def disconnect(self):
        """
        Disconnect the socket manually.
        """
        
        self.transport.loseConnection()
        
    
    def buildProtocol(self, addr):
        """
        This is executed when a connection is successful.
        """
        
        print('%s: Connected at %s' % (self, addr))

        # this line is necessary because some plugins need to know what
        # the protocol object is, which is only defined when 
        # "return self" runs.
        reactor.callLater(0, self._buildProtocolTrigger)

        return self
    
    def _buildProtocolTrigger(self):
        """
        Only used by buildProtocol method!!!
        """
        
        for plugin in self.plugins:
            plugin.onConnect()
    
    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)
        
        for plugin in self.plugins:
            plugin.onConnectFailed(reason)
    
    def clientConnectionLost(self, connector, reason):
        """
        Called when a connection is lost.
        """
        
        print('%s: Disconnected.' % self, file=sys.stderr)
        
        for plugin in self.plugins:
            plugin.onDisconnect(reason)
        
    
    def startedConnecting(self, connector):
        print('Started to connect.')
    
        
    def lineReceived(self, msg):
        """
        This should intialize plugin global vars and send the message
        to all the plugins
        """
        
        # I think this happens and should be ignored.
        if len(msg) == 0: return
        
        print(msg)
        
        for each in self.plugins:
            each.onData(msg)
    
    
    def loadPlugins(self, *a, **b):
        reactor.callLater(0, lambda:self._loadPlugins(*a,**b))
    
    def _loadPlugins(self, reload=True):
        """
        Load the plugins and call the onLoad method for all of them.
        Give each a reference to the protocol object.
        TODO: try/catch 
        """
        
        self.unloadPlugins()
        
        self.plugins = loadFolder(self.folder, reload)
        
        for each in self.plugins:
            each.core = self
            each.onLoad()
    
    def unloadPlugins(self):
        """
        Call the unload method of all plugins and delete them.
        """
        
        for each in self.plugins:
            each.onUnload()
            del each
            
        
    def findPlugin(self, name):
        """
        Find a loaded plugin by the name variable.
        Return None if it was not found.
        """
        
        for plugin in self.plugins:
            if name == plugin.name:
                return plugin
        
        return None
    
    def findCore(self, name):
        """
        Find a core by name.
        TODO: everything
        """
        pass