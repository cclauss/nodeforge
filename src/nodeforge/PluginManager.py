"""
Plugin Handling Functions

All plugins should be stored in the "plugins" directory.

They should be seperated with folders. Then they are to be organized by usage.
Finally, each plugin module should have its own folder. The 


Example Directory Structure

plugins/
        
        hub/                    - plugin directory for "hub
            greeting/           - the "greeting" plugin folder
                main.py         - Important entry point for the plugin.
                helperfile.py   - some extra file for helping.
        
        
        irc/                    - plugin directory for "irc"
            trivia/             - the "trivia" plugin folder
                main.py         - this holds initialization code
                db.py           - extra file for helping.



"""

import sys, imp
import os.path, os

from PluginUtils import comparePlugin

import import2

# Maybe use weakref.WeakValueDictionary()?
module_cache = {}


def loadFolder(path, reload=False):
    """
    Search the given path for plugin directories.
    Return intialized plugin objects.
    
    If reload is true, then changes made to the plugin files will be reloaded.
    """
    
    dir = os.listdir( os.path.normpath(path) )
    
    # find directories with main.py in them
    possible_modules = []
    for item in dir:
        item = os.path.join(path, item)
        # check if it contains main.py
        if os.path.isfile( os.path.join(item, 'main.py') ):
            possible_modules.append(item)

   
    # load the modules and make plugins
    plugins = []    
    for modulepath in possible_modules:
        mod = loadModule(modulepath, reload)
        plugins.append(loadPlugin(mod))
    

    # sort the plugins
    plugins.sort(comparePlugin)

    return plugins



def loadModule(path, reload=False):
    """
    Load a single module from it's folder.
    Used by loadFolder
    """
    
    absolute_path = os.path.abspath(path)
    
    # try getting the module from the cache
    if reload == False:
        try:
            return module_cache[absolute_path]
        except KeyError:
            pass
        
    # load the module
    mod          = imp.new_module(os.path.basename(path))
    mod.__file__ = os.path.join(absolute_path, 'main.py')
    
    # Create a reference to itself for import2.py
    mod.__dict__['_self'] = mod
    
    # add the directory to the module searchpath temporarily.
    # so plugins can import files in their own directory
    sys.path.insert(0, absolute_path)
    
    # Behavior: the working directory of all plugins default to where the program was run.
    # This can be overriden by os.chdir(). But, maybe the seperation between plugins, and working data is fine.
    
    # create the module
    with open(mod.__file__) as in_file:
        exec(in_file.read(), mod.__dict__)
    
    # remove the directory to clean it up now that we are done.
    sys.path.pop(0)
    
    # save to cache
    module_cache[mod.__file__] = mod
    
    return mod
    
    
def loadPlugin(mod):
    """
    Spawn a plugin class given a module object.
    Used by loadModule
    """
    plugin = mod.Main()
    plugin.name = plugin.__module__
    plugin.__file__ = mod.__file__
    
    return plugin
    
