#!/usr/bin/python3.5
# coding=utf-8

#-------------------------------------------
# Just PoC for the moment...
# - Unserialize vol commands
# - Send to a volWorker and take the result
#-------------------------------------------

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil

class Timemem:

    def __init__ (self,qpl,repi,repo,repe,repnok,repmem):
        self.qpl = qpl
        self.repin = repi
        self.repout = repo
        self.repend = repe
        self.repnok = repnok
        self.repmm = repmem
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
        # Better with and empty profil
        if len(profil) > 1:
            tester = self.prof_tester(str(f),str(profil))
            if tester:
                ok_body = self.timelisable(str(f),str(profil),self.repout)
                if ok_body:
                    ok_timeline = self.robbeur(str(f))
                    if ok_timeline:
                        timeline_end = self.sorteur(str(f))
                        if timeline_end:
                            print("Memory timeline : " + str(f) + "-timeline.csv in " + str(self.repout))
                            shutil.move(self.repin+f,self.repmm)
                            os.remove(self.repin+f+".working")
                            print("The file : " + f + " move in this directory " + self.repmm)
                        else:
                            print("*** Sorteur error ***\nFile : "+f)
                    else:
                        print("*** Robbeur error ***\nFile : "+f)
                else:
                    print("*** Timelisable error ***\nFile : "+f)
            else:
                print("*** Prof_Tester error ***\nFile : "+f)
        else:
            print("No profile, the memory dump is not available.")
            shutil.move(self.repin+f, self.repnok)
            os.remove(self.repin+f+".working")
            print("The file : " + f + " move in the directory " + self.repnok)

    def start (self):
        _thread.start_new_thread(self.run,())

    def stop (self):
        print("STOP-Timemem")
        self.terminer = True

    def best_profile(self,profiles, sp):
        profile = ""
        if len(profiles) == 0:
            return ""
        else:
            for p in profiles:
                if "SP"+sp in p:
                    profile = p
            if profile == "":
                profile = profiles[0]
        return profile

    def check_result(self,result):
        check = False
        for rline in result.stdout:
            if str(rline).find("putting to") >= 0:
                check = True
        return check

    def profiler (self, f):
        # Only Windows with imageinfo, mac_get_profile or a "linux_get_profile"
        profilers = []
        serv_pack = ""
        result = subprocess.Popen(["vol.py","-f", self.repin+f , "imageinfo", "--output=text"], stdout=subprocess.PIPE)
        for line in result.stdout:
            line = str(line).replace('\n',' ')
            strip_line = str(line).strip()
            if str(strip_line).find("Suggested Profile(s)") >= 0:
                # Profiles
                profiles = str(str(strip_line).rsplit(":")).rsplit(",")
                for pp in profiles:
                    if str(pp).find("Suggested Profile(s)") >=0:
                        continue
                    else:
                        profilers.append(str(str(pp).split("(")[0].strip()).replace('"','').strip())
            if str(strip_line).find("Service Pack") >= 0:
                # Service pack number
                serv_pack = str(strip_line).rsplit(":")
                serv_pack = str(serv_pack[1])[1]
        return self.best_profile(profilers,serv_pack)

    # Better with an volatility class with threat and args (command, profile,...)
    def prof_tester (self, f, prof):
        okay = False
        print("Profile tester : " + str(f) + "  " + str(prof))
        # Windows profile but linux and mac too.
        if str(prof).find("Win") >= 0 or str(prof).find("Vista") >= 0:
            p = subprocess.Popen(["vol.py","-f", self.repin+f ,"--profile="+str(prof), "pslist"], stdout=subprocess.PIPE)
            # result = p.communicate()
        else:
            # Linux ou Mac
            if str(prof).find("Linux") >= 0:
                p = subprocess.Popen(["vol.py","-f", self.repin+f , "linux_pslist"], stdout=subprocess.PIPE)
                # result = p.communicate()
            else:
                # Mac
                p = subprocess.Popen(["vol.py","-f", self.repin+f , "mac_pslist"], stdout=subprocess.PIPE)
                # result = p.communicate()
        for line in p.stdout:
            #print(line)
            if str(line).find("0x") >=0 and str(line).find("lsass"):
                okay = True
        return okay

    # Just windows timeline
    def timelisable (self, f, prof, repout):
        print("Timelisable : " + str(f) + "  " + str(prof) + "  " + str(repout))
        # Windows profile but linux and mac too.
        timeliner = True
        mftparser = True
        shellbags = True
        # if not file exist so ...
        # better with async method
        if not os.path.isfile(repout+f+"-timeliner.body"):
            t = subprocess.Popen(["vol.py","-f", self.repin+f ,"--profile="+str(prof), "timeliner", "--output=body", "--output-file="+repout+f+"-timeliner.body"], stdout=subprocess.PIPE)
            timeliner = self.check_result(t)
        if not os.path.isfile(repout+f+"-mftparser.body"):
            m = subprocess.Popen(["vol.py","-f", self.repin+f ,"--profile="+str(prof), "mftparser", "--output=body", "--output-file="+repout+f+"-mftparser.body"], stdout=subprocess.PIPE)
            mftparser = self.check_result(m)
        if not os.path.isfile(repout+f+"-shellbags.body"):
            s = subprocess.Popen(["vol.py","-f", self.repin+f ,"--profile="+str(prof), "shellbags", "--output=body", "--output-file="+repout+f+"-shellbags.body"], stdout=subprocess.PIPE)
            shellbags = self.check_result(s)
        # result = p.communicate()
        if timeliner and mftparser and shellbags:
            return True
        else:
            return False

    def robbeur(self,f):
        # ascii replace OK
        # utf-8 replace ??
        fichiers = [self.repout+f+"-timeliner.body",self.repout+f+"-mftparser.body",self.repout+f+"-shellbags.body"]
        for fichier in fichiers:
            r = subprocess.Popen(["mactime","-y","-d","-b", fichier], stdout=subprocess.PIPE, universal_newlines=True, encoding="utf-8", errors="replace")
            print("MACTIME ---> : " + fichier)
            with open(fichier+".csv","w") as csvtime:
                for line in r.stdout:
                    csvtime.write(str(line))
            csvtime.close()
        return True

    def sorteur(self,f):
        fichiers = [self.repout+f+"-timeliner.body.csv",self.repout+f+"-mftparser.body.csv",self.repout+f+"-shellbags.body.csv"]
        with open(self.repout+f+"unsort","w") as unsorted:
            for fichier in fichiers:
                print("Reading ... "+fichier)
                with open(fichier,"r") as csvnotsorted:
                    csv_header = csvnotsorted.readline()
                    unsorted.write(csvnotsorted.read())
                csvnotsorted.close()
        unsorted.close()
        r = subprocess.Popen(["sort", self.repout+f+"unsort"], stdout=subprocess.PIPE, universal_newlines=True, encoding="utf-8", errors="replace")
        with open(self.repout+f+"-timeline.csv","w") as final_csv:
            final_csv.write(csv_header)
            for line in r.stdout:
                final_csv.write(line)
        final_csv.close()
        return True
