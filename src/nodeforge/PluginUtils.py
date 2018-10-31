"""
Useful stuff for plugin files. 
Every plugin file should import this with the line:

from nodeforge.PluginUtils import *

"""
from Plugin import Plugin, Priority
import sys, imp, os, types

def comparePlugin(x,y):
    """
    Customized comparison function for sorting based on
    priority and then name in alphabetical order.
    
    Usage: ListOfPluginInstances.sort(comparePlugin)
    """
    
    if x.priority != y.priority:
        return x.priority-y.priority
    
    if x.name > y.name:
        return 1
    elif x.name < y.name:
        return -1
    return 0
    

def dimport(name):
    """
    A customized import statement. Short for dynamic import.
    
    For plugin use only. This is like a regular import except it wil reload the target
    if the main module is reloaded. Python normally only reloads the main module.
    
    name: string representation of something you would normally use in a import statement.
    """
    

    # Get the module of the caller and global variables
    directory = os.path.dirname(sys._getframe(1).f_locals['__file__'])
    locals    = sys._getframe(1).f_locals
    
    # Search for module in the directory of the file that called.
    info = imp.find_module(name, [directory])
    
    # Try initializing the module and making it available to the caller.
    # Then close the file object.
    # Warning: modules will get loaded to sys.modules.
    try:
        locals[name] = imp.load_module(name, *info)
    finally:
        info[0].close()
        

def functionToMethod(func, instance):
    """
    Convert a function into a method. 
    You can use this to overwrite class methods during runtime.
    The instance must be an instance of the object you will overwrite.
    
    TODO: You might be able to use a method in place of a function.
    """
    
    return types.MethodType(func, instance, instance.__class__)

def EntryPoint(classobj):
    """
    Currently Unused
    
    Decorator for specifying the main object
    Usage: type @EntryPoint right before the class definition to be instantiated.
    
    Example: 
    
    @EntryPoint 
    class MyPlugin(Plugin):
    ...
    
    """
    sys._getframe(1).f_locals.update({'main': classobj})
    return classobj
