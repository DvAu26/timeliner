#!/usr/bin/python
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

    def __init__ (self,qdd,rep):
        self.qdd = qdd
        self.repin = rep
        self.terminer = False
        print("INIT-Rechercheur")

    def run (self):
        while not self.terminer:
            fichiers = os.listdir(self.repin)
            test = False
            for f in fichiers:
                print(f)
                if self.verif_hdd(magic.from_file(self.repin+f)):
                    self.qdd.put(f)
                    print("Rechercheur : " + f)
            time.sleep(CHECK_TIME)

    def verif_hdd(self,typ):
        test = False
        #print typ.find("DOS/MBR")
        if typ.find("DOS/MBR") >=0:
            #print typ
            test = True
        return test

    def start (self):
        _thread.start_new_thread(self.run,())

    def stop (self):
        self.terminer = True
