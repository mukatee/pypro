__author__ = 'teemu kanstren'

import os

log_dir = "logs/"

def check_dir():
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
