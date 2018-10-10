#!/usr/bin/python
# coding=utf-8

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil
from rechercheur import Rechercheur
from timeliner import Timeliner
from plaseur import Plaseur

IN="in_hdd/"
OUT="out_hdd/"
END="end_hdd/"

if __name__ == '__main__':
    queue_fic = queue.Queue()
    queue_dd = queue.Queue()
    queue_plaso = queue.Queue()

    '''Initiation des répertoires'''

    for f in IN,OUT,END:
        if not os.path.exists(f):
            os.makedirs(f)

    r = Rechercheur(queue_dd,IN)
    p = Plaseur(queue_dd,queue_plaso,IN,OUT)
    c = Timeliner(queue_plaso,IN,OUT,END)

    r.start()
    p.start()
    c.start()

    input()

    r.stop()
    p.stop()
    c.stop()
