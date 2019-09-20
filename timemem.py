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
        profil = self.profiler(f)
        print(profil)
        if str(profil).find("NON-PROFILE") != 0:
            print("tester = self.prof_tester("+str(f)+","+str(profil)+")")
            # shutil.move(self.repin+f,self.repend)
            # print("Le fichier : " + f + " est déplacé dans " + self.repout)
        else:
            print("Aucun profil, le fichier n'est pas un dump de RAM exploitable")
            shutil.move(self.repin+f, self.repnok)
            print("Le fichier : " + f + " est déplacé dans " + self.repnok)

    def start (self):
        _thread.start_new_thread(self.run,())

    def stop (self):
        print("STOP-Timemem")
        self.terminer = True

    def profiler (self, f):
        print("Profiler : " + str(f) + "\n ----- Imageinfo -----")
        p = subprocess.Popen(["vol.py","-f", self.repin+f , "imageinfo"], stdout=subprocess.PIPE)
        result = p.communicate()
        # Opti with split("\n")
        print("##################" + str(result) + "#####################")
        lines_result = str(result).split("\n")
        for line in lines_result:
            if str(line).find("Suggested Profile(s)") >= 0:
                # Line with profile(s)
                profiles = str(line).split(",")
                print("Suggested profile(s) : " + str(profiles))
            if str(line).find("Service Pack") >= 0:
                # Service pack number
                serv_pack = str(line).split(":")
                print("Service pack : " + str(serv_pack))
        return "Testing"

    def prof_tester (self, f, prof):
        print("Profile tester : " +f)
        # Windows profile but linux and mac too.
        if str(prof).find("Win") >= 0 or str(prof).find("Vista") >= 0:
            p = subprocess.Popen(["vol.py","-f", self.repin+f , "pslist"], stdout=subprocess.PIPE)
            result = p.communicate()
        else:
            # Linux ou Mac
            if str(prof).find("Linux") >= 0:
                p = subprocess.Popen(["vol.py","-f", self.repin+f , "linux_pslist"], stdout=subprocess.PIPE)
                result = p.communicate()
            else:
                # Mac
                p = subprocess.Popen(["vol.py","-f", self.repin+f , "mac_pslist"], stdout=subprocess.PIPE)
                result = p.communicate()
        print("result")
