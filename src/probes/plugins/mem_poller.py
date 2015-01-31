__author__ = 'teemu kanstren'

import psutil
import time

poll_swap = False
print_console = False
f = open("mem-log.csv", "w", encoding="utf-8")

def println(str):
    "Print a line to console and to a file"
    f.write(str+"\n")
    f.flush()
    if print_console: print(str)

def name():
    return "cpu"

def header():
    return "time;available;percent;used;free"

def poll():
    if poll_swap:
        print("Should poll swap")
    counter = round(time.perf_counter(), 1)
    mem_info = psutil.virtual_memory()
    available = mem_info.available
    percent = mem_info.percent
    used = mem_info.used
    free = mem_info.free
    return (str(counter)+";"+str(available)+";"+str(percent)+";"+str(used)+";"+str(free))

if __name__ == "__main__":
    f = open("perf-log.csv", "w", encoding="utf-8")
    println(header)
    while (True):
        counter = round(time.perf_counter(), 1)
        println(str(counter)+";"+poll())
        time.sleep(1)
    f.close()
