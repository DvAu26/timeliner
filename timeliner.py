#!/usr/bin/python3.5
# coding=utf-8

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil

class Timeliner:

    def __init__ (self,qpl,repi,repo,repe):
        self.qpl = qpl
        self.repin = repi
        self.repout = repo
        self.repend = repe
        self.terminer = False
        print("INIT-Timeliner")

    def run (self):
        while not self.terminer:
            if self.qpl.qsize() > 0:
                fic_pls = self.qpl.get()
                _thread.start_new_thread(self.run2,(fic_pls,))

    def run2 (self,f):
        print("Timeliner : " + f)
        p = subprocess.Popen(["psort.py","-w", self.repout+f+".csv", self.repout+f+".plaso"], stdout=subprocess.PIPE)
        result = p.communicate()
        if str(result).find("Processing completed") >= 0:
            shutil.move(self.repin+f,self.repend)
            os.remove(self.repin+f+".working")
            print("Le fichier : " + f + " est déplacé dans " + self.repout)
        else:
            print("Une erreur est survenue pendant la génération du csv")

    def start (self):
        _thread.start_new_thread(self.run,())

    def stop (self):
        print("STOP-Timeliner")
        self.terminer = True
