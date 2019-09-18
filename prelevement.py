#!/usr/bin/python3.5
# coding=utf-8

#TODO TODO

class Prelevement:

    '''Un prelevement est un fichier avec un chemin, un type et une empreinte.
    Un prelevement peut être issu d'un autre fichier.'''
    def __init__ (self,fichier,path,magic,pfic):
        self.fic = fichier
        self.path = path
        self.typ = magic
        self.md5 = MD5
        self.parent_fic = pfic
