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
                # With f + .working to not retake
                if str(f).find(".working") >= 0:
                    continue
                if self.verif_hdd(magic.from_file(self.repin+f)) and not self.verif_working(f):
                    self.qdd.put(f)
                    fw = open(self.repin+f+".working","w")
                    fw.close()
                    print("Rechercheur : " + f)
                else:
                     # gros bourrin a affiner...
                     if not self.verif_working(f):
                         self.qmem.put(f)
                         fw = open(self.repin+f+".working","w")
                         fw.close()
                         print("Timemem : " + f)
            time.sleep(CHECK_TIME)

    def verif_hdd(self,typ):
        test = False
        if typ.find("DOS/MBR") >=0 or typ.find("filesystem") >= 0:
            test = True
        return test

    def verif_working(self,fic):
        return os.path.isfile(self.repin+fic+".working")

    def start (self):
        _thread.start_new_thread(self.run,())

    def stop (self):
        print("STOP-Rechercheur")
        self.terminer = True
