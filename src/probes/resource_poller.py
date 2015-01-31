__author__ = 'teemu kanstren'

import importlib
import os
import time
import plugins.mem_poller

PluginFolder = "plugins"
#MainModule = "__init__"

def get_plugins():
    #create an empty list to hold object references for poller objects
    plugins = []
    possibleplugins = os.listdir(PluginFolder)
    for i in possibleplugins:
        #we ignore non-python files and package initializers etc.
        if not i.endswith(".py") or i.startswith("_"):
            continue
        #load the resource poller plugins dynamically as in "plugins.cpu_poller" etc.
        info = importlib.import_module(PluginFolder+"."+os.path.splitext(i)[0])
        #create a map with name = name of module source, and info = the poller module to call
        plugins.append({"name": i, "info": info})
    return plugins

def run_poller():
    plugins = get_plugins()
    for p in plugins:
        #get references to poller functions. as in cpupoller.header. not missing () why it is not a call.
        header = getattr(p["info"], "header")
        println = getattr(p["info"], "println")
        #and here is the call
        println(header())

    while (True):
        for p in plugins:
            poll = getattr(p["info"], "poll")
            println = getattr(p["info"], "println")
            println(poll())
        time.sleep(1)

if __name__ == "__main__":
#    plugins.mem_poller.poll_swap = True
    run_poller()

