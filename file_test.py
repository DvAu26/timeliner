#!/usr/bin/python
# coding=utf-8

import os
import magic
import subprocess
import Queue
import time
import thread
import shutil

IN="in_hdd/"
OUT="out_hdd/"
END="end_hdd/"

CHECK_TIME = 500

class Rechercheur:
    
    def __init__ (self,qdd,rep):
        self.qdd = qdd
        self.repin = rep
        self.terminer = False
        print "INIT-Rechercheur"
    
    def run (self):
        while not self.terminer:
			fichiers = os.listdir(self.repin)
			test = False
			for f in fichiers:
				print f
				if self.verif_hdd(magic.from_file(self.repin+f)):
					self.qdd.put(f)
					print "Rechercheur : " + f
			time.sleep(CHECK_TIME)

    def verif_hdd(self,typ):
		test = False
		#print typ.find("DOS/MBR")
		if typ.find("DOS/MBR") >=0:
			#print typ
			test = True
		return test

    def start (self):
        thread.start_new_thread (self.run,())    
    
    def stop (self):
        self.terminer = True

class Plaseur:
    
    def __init__ (self,qdd,qpl,repi,rep):
        self.qdd = qdd
        self.qpl = qpl
        self.repin = repi
        self.repout = rep
        self.terminer = False
        print "INIT-Plaseur"
    
    def run (self):
        while not self.terminer:
			if self.qdd.qsize() > 0:
				fic_hdd = self.qdd.get()
				thread.start_new_thread(self.run2,(fic_hdd,))
    
    def run2 (self,f):
		print "Plaso on : " + f
		p = subprocess.Popen(["log2timeline.py","--vss_stores","all","--partition","all", self.repout+f+".plaso", self.repin+f], stdout=subprocess.PIPE)
		result = p.communicate()
		if str(result).find("Processing completed") >= 0:
			self.qpl.put(f)
		else:
			print "Une erreur est survenue pendant la génération du plaso"
                
    def start (self):
        thread.start_new_thread (self.run,())    
    
    def stop (self):
        self.terminer = True

class Timeliner:
    
    def __init__ (self,qpl,repi,repo,repe):
        self.qpl = qpl
        self.repin = repi
        self.repout = repo
        self.repend = repe
        self.terminer = False
        print "INIT-Timeliner"
    
    def run (self):
        while not self.terminer:
			if self.qpl.qsize() > 0:
				fic_pls = self.qpl.get()
				thread.start_new_thread(self.run2,(fic_pls,))
    
    def run2 (self,f):
		print "Timeliner : " + f
		p = subprocess.Popen(["psort.py","-w", self.repout+f+".csv", self.repout+f+".plaso"], stdout=subprocess.PIPE)
		result = p.communicate()
		if str(result).find("Processing completed") >= 0:
			shutil.move(self.repin+f,self.repend)
			print "Le fichier : " + f + " est déplacé dans " + self.repout
		else:
			print "Une erreur est survenue pendant la génération du csv"
                
    def start (self):
        thread.start_new_thread (self.run,())    
    
    def stop (self):
        self.terminer = True


if __name__ == '__main__':
	queue_fic = Queue.Queue()
	queue_dd = Queue.Queue()
	queue_plaso = Queue.Queue()
	
	'''Initiation des répertoires'''
	
	for f in IN,OUT,END:
		if not os.path.exists(f):
			os.makedirs(f)

	r = Rechercheur(queue_dd,IN)
	p = Plaseur(queue_dd,queue_plaso,IN,OUT)
	c = Timeliner(queue_plaso,IN,OUT,END)
	
	r.start()
	p.start()
	c.start()
	
	raw_input()
	
	r.stop()
	p.stop()
	c.stop()
