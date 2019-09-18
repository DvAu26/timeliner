#!/usr/bin/python3.5
# coding=utf-8

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil

CHECK_TIME = 500

class Rechercheur:

    def __init__ (self,qdd,qmm,rep,repo):
        self.qdd = qdd
        self.qmem = qmm
        self.repin = rep
        self.repout = repo
        self.terminer = False
        print("INIT-Rechercheur")

    def run (self):
        while not self.terminer:
            fichiers = os.listdir(self.repin)
            test = False
            for f in fichiers:
                print(f)
                if self.verif_hdd(magic.from_file(self.repin+f)) and self.verif_plaso(f):
                    self.qdd.put(f)
                    print("Rechercheur : " + f)
                else:
                     # gros bourrin a affiner...
                     self.qmm.put(f)
                     print("Timemem : " + f)
            time.sleep(CHECK_TIME)

    def verif_hdd(self,typ):
        test = False
        print(typ)
        if typ.find("DOS/MBR") >=0 or typ.find("filesystem") >= 0:
            test = True
        return test

    def verif_plaso(self,fic):
        test2 = True
        if os.path.isfile(self.repout+fic+".plaso"):
            test2 = False
        return test2

    def start (self):
        _thread.start_new_thread(self.run,())

    def stop (self):
        print("STOP-Rechercheur")
        self.terminer = True
