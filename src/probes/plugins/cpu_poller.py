__author__ = 'teemu kanstren'

import psutil
import time

def println(str):
    "Print a line to console and to a file"
    f.write(str+"\n")
    f.flush()
    print(str)

def name():
    return "cpu"

def header():
    return "time;user;system;idle"

def poll():
    cpu_times = psutil.cpu_times()
    user_cnt = cpu_times.user
    system_cnt = cpu_times.system
    idle_cnt = cpu_times.idle
    return (";"+str(user_cnt)+";"+str(system_cnt)+";"+str(idle_cnt))

if __name__ == "__main__":
    f = open("perf-log.csv", "w", encoding="utf-8")
    println(header)
    while (True):
        counter = round(time.perf_counter(), 1)
        println(str(counter)+";"+poll())
        time.sleep(1)
    f.close()

print("?")