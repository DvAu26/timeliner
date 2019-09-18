#!/usr/bin/python3.5
# coding=utf-8

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil

class Timemem:

    def __init__ (self,qpl,repi,repo,repe,repnok):
        self.qpl = qpl
        self.repin = repi
        self.repout = repo
        self.repend = repe
        self.repnok = repnok
        self.terminer = False
        print("INIT-Timemem")

    def run (self):
        while not self.terminer:
            if self.qpl.qsize() > 0:
                fic_pls = self.qpl.get()
                _thread.start_new_thread(self.run2,(fic_pls,))

    def run2 (self,f):
        print("Timeliner Memory : " + f)
        profil = profiler(f)
        '''p = subprocess.Popen(["vol.py","-w", self.repout+f+".csv", self.repout+f+".plaso"], stdout=subprocess.PIPE)
        result = p.communicate()
        if str(result).find("Processing completed") >= 0:
            shutil.move(self.repin+f,self.repend)
            print("Le fichier : " + f + " est déplacé dans " + self.repout)
        else:
            print("Aucun profil, le fichier n'est pas un dump de RAM exploitable")
            shutil.move(self.repin+f, self.repnok)
            print("Le fichier : " + f + " est déplacé dans " + self.repnok)'''

    def start (self):
        _thread.start_new_thread(self.run,())

    def stop (self):
        print("STOP-Timemem")
        self.terminer = True

    def profiler (self, f):
        print("Profiler : " +f)
        p = subprocess.Popen(["vol.py","-f", self.repout+f , "imageinfo"], stdout=subprocess.PIPE)
        result = p.communicate()
        print(result)
        '''if str(result).find("Processing completed") >= 0:
            shutil.move(self.repin+f,self.repend)
            print("Le fichier : " + f + " est déplacé dans " + self.repout)
        else:
            print("Une erreur est survenue pendant la génération du csv")'''
