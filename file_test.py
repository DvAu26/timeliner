#!/usr/bin/python3.5
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

IN="/mnt/Timeliner/in/"
OUT="/mnt/Timeliner/out/"
END="/mnt/Timeliner/end/"

if __name__ == '__main__':

    '''Initiation des queues'''

    queue_fic = queue.Queue()
    queue_dd = queue.Queue()
    queue_plaso = queue.Queue()

    '''Initiation des répertoires'''

    for f in IN,OUT,END:
        if not os.path.exists(f):
            os.makedirs(f)

    r = Rechercheur(queue_dd,IN,OUT)
    p = Plaseur(queue_dd,queue_plaso,IN,OUT)
    c = Timeliner(queue_plaso,IN,OUT,END)

    r.start()
    p.start()
    c.start()

    input()

    r.stop()
    p.stop()
    c.stop()
