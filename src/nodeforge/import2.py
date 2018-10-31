"""
Allows plugins to have periods in their folder names.
Unfortunately, it hooks into all import statements which 
means imports will be slower.
"""


import __builtin__, sys
oldimport = __builtin__.__import__

def customimport(name, globals=None, locals=None, fromlist=None):
    try:    
        mod = oldimport(name, globals, locals, fromlist)
    except SystemError as e:
        # Get the module to save the import to.
        # It should be saved as _self.
        # This is defined in main.PluginManager.loadModule
        parent = e.message[15:-12]
        sys.modules[parent] = sys._getframe(1).f_locals['_self']
        mod = oldimport(name, globals, locals, fromlist)
        del sys.modules[parent]
    

    return mod

__builtin__.__import__ = customimport

