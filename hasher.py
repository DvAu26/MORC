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
        md5_file = self.calc_md5(f)        
        if not self.check_md5_file(f) and not os.path.isfile(self.in_dir+f+".md5"):
            print("No .md5 file for the file : " + f)
            print("It will generate ...")
            with open(self.in_dir+f+".md5","w") as mdfile:
                mdfile.write(md5_file + " " + f)
                mdfile.close()
        if self.check_md5_cf(f,md5_file):
            self.q_hashed.put(f)
        else:
            print("*** Error MD5 ***")
            print("There is a diff between the calculate and the .md5 file")
            os.remove(self.in_dir+f+".working")

    def check_md5_file (self,f):
        # method to check if f.md5 exist with something like MD5
        # True if len = 32 and f in the first line
        # False if not
        if os.path.isfile(self.in_dir+f+".md5"):
            with open(self.in_dir+f+".md5") as hfile:
                f_line = hfile.readline()
                f_other = hfile.read()
                hfile.close()
            if len(f_line.split()[0]) == 32 and f_line.split()[1] == f:
                return True
            else:
                return False
        else:
            return False

    def calc_md5 (self,f):
        # method to calculate md5(f)
        # return the calculate MD5
        calculating_md5 = hashlib.md5()
        with open(self.in_dir+f,"rb") as ficrb:
            byt_block = ficrb.read(self.bk_size)
            if len(byt_block) > 0:
                calculating_md5.update(byt_block)
        md5_file = calculating_md5.hexdigest()
        return md5_file

    def check_md5_cf (self,f,md5_c):
        # method to check the calculate md5 and the md5 in the .md5 file
        # md5_c -> calculate md5
        # True if calculate MD5 = md5 in the f.md5 file
        # False if not
        with open(self.in_dir+f+".md5") as hfile:
                f_line = hfile.readline()
                f_other = hfile.read()
                hfile.close()
        if md5_c == f_line.split()[0]:
            return True
        else:
            return False

