#!/usr/bin/python3.5
# coding=utf-8

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil

class Plaseur:

    def __init__ (self,qdd,qpl,repi,rep):
        self.qdd = qdd
        self.qpl = qpl
        self.repin = repi
        self.repout = rep
        self.terminer = False
        print("INIT-Plaseur")

    def run (self):
        while not self.terminer:
            if self.qdd.qsize() > 0:
                fic_hdd = self.qdd.get()
                _thread.start_new_thread(self.run2,(fic_hdd,))

    def run2 (self,f):
        print("Plaso on : " + f)
        p = subprocess.Popen(["log2timeline.py","--vss_stores","all","--partition","all", self.repout+f+".plaso", self.repin+f], stdout=subprocess.PIPE)
        result = p.communicate()
        if str(result).find("Processing completed") >= 0:
            self.qpl.put(f)
        else:
            print("Une erreur est survenue pendant la génération du plaso")

    def start (self):
        _thread.start_new_thread(self.run,())

    def stop (self):
        self.terminer = True
