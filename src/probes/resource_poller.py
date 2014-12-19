__author__ = 'teemu kanstren'

import importlib
import os

PluginFolder = "plugins"
MainModule = "__init__"

def get_plugins():
    plugins = []
    possibleplugins = os.listdir(PluginFolder)
    for i in possibleplugins:
#        location = os.path.join(PluginFolder, i)
        if not i.endswith(".py") or i.startswith("_"):
#            print("not "+i)
            continue
#        print("yes:"+i)
        info = importlib.import_module(PluginFolder+"."+os.path.splitext(i)[0])
#        print(info)
        poll = getattr(info, "poll")
        print(poll())
        plugins.append({"name": i, "info": info})
    return plugins

def loadPlugin(plugin):
    return importlib.load_module(MainModule, *plugin["info"])

get_plugins()

