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
from timemem import Timemem

IN="/mnt/Timeliner/in/"
OUT="/mnt/Timeliner/out/"
END="/mnt/Timeliner/end/"
MEM="/mnt/Timeliner/mem/"
NOK="/mnt/Timeliner/nok/"

if __name__ == '__main__':

    '''Initiation des queues'''
    # queue_fic queues pour les fichiers du répertoire IN
    # queue_fic = queue.Queue()
    # queue_dd queues pour les fichiers considérés comme Image disque
    queue_dd = queue.Queue()
    # queue_mem queues pour les fichiers considérés comme dump de RAM
    queue_mem = queue.Queue()
    # queue_plaso queues pour les fichiers plaso pour psorting
    queue_plaso = queue.Queue()

    '''Initiation des répertoires'''

    for f in IN,OUT,END,MEM:
        if not os.path.exists(f):
            os.makedirs(f)

    r = Rechercheur(queue_dd,queue_mem,IN,OUT)
    p = Plaseur(queue_dd,queue_plaso,IN,OUT)
    m = Timemem(queue_mem,IN,OUT,END,NOK)
    c = Timeliner(queue_plaso,IN,OUT,END)

    c.start()
    p.start()
    m.start()
    r.start()

    input()

    r.stop()
    m.stop()
    p.stop()
    c.stop()
