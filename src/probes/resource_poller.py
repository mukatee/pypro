__author__ = 'teemu kanstren'

import importlib
import os
import time

PluginFolder = "plugins"
MainModule = "__init__"

def get_plugins():
    plugins = []
    possibleplugins = os.listdir(PluginFolder)
    for i in possibleplugins:
        if not i.endswith(".py") or i.startswith("_"):
            continue
        info = importlib.import_module(PluginFolder+"."+os.path.splitext(i)[0])
        plugins.append({"name": i, "info": info})
    return plugins

def run_poller():
    plugins = get_plugins()
    for p in plugins:
        header = getattr(p["info"], "header")
        println = getattr(p["info"], "println")
        println(header())

    while (True):
        for p in plugins:
            poll = getattr(p["info"], "poll")
            println = getattr(p["info"], "println")
            println(poll())
        time.sleep(1)

run_poller()

