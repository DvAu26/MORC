#!/usr/bin/python3.5
# coding=utf-8

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil
import hashlib



class Hasher:

    def __init__ (self,q_hash,q_hashed,i_dir,w_dir,b_size):
        self.q_hash = q_hash
        self.q_hashed = q_hashed
        self.in_dir = i_dir
        self.wk_dir = w_dir
        self.bk_size = b_size
        self.end = False
        print("== INIT Hasher ==")

    def start (self):
        _thread.start_new_thread(self.run,())

    def stop (self):
        print("## STOP Hasher ##")
        self.end = True

    def run (self):
        while not self.end:
            if self.q_hash.qsize() > 0:
                fic_hash = self.q_hash.get()
                _thread.start_new_thread(self.run2,(fic_hash,))

    def run2 (self,f):
        print("Hasher on : " + f)
        # f.md5 exist ?
        # md5(f) == f.md5 ?
        # q_hashed.put(f)

    def check_md5_file (self,f):
        # method to check if f.md5 exist with something like MD5
        if os.path.isfile(self.i_dir+f+".md5"):
            with open(self.i_dir+f+".md5") as hfile:
                f_line = hfile.readline()
                f_other = hfile.read()
                hfile.close()
            print(f_line.split()[0])
            print(f_line.split()[1])

    def calc_md5 (self,f):
        # method to calculate md5(f)
        calculating_md5 = hashlib.md5()
        with open(self.i_dir+f,"rb") as ficrb:
            for byt_block in iter(lambda f.read(self.b_size),b""):
                 calculating_md5.update(byt_block)
        md5_file = calculating_md5.hexdigest()
        return md5_file

    def check_md5_cf (self,f):
        # method to check the calculate md5 and the md5 in the .md5 file
        

