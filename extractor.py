#!/usr/bin/python3.5
# coding=utf-8

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil

class Extractor:

    def __init__ (self,q_ext,q_exted,i_dir,w_dir):
        self.q_ext = q_ext
        self.q_extd = q_exted
        self.in_dir = i_dir
        self.wk_dir = w_dir
        self.end = False
        print("== INIT Extractor ==")

    def start (self):
        _thread.start_new_thread(self.run,())

    def stop (self):
        print("## Stop Extractor ##")
        self.end = True

    def run (self):
        while not self.end:
            if self.q_ext.qsize() > 0:
                fic_ext = self.q_ext.get()
                _thread.start_new_thread(self.run2,(fic_ext,))

    def run2 (self,f):
        # check if wk_dir/MD5/ exists
        # if MD5 exist q_extrad(f)
        # if not extract in the wk_dir/MD5 folder
        if not os.path.isdir(self.wk_dir+self.md5_recup(f)+"/"):
            print("Extracting file : " + f)
            if self.extrac_file(f):
                print("=== Extract OK in the MD5 folder ===")
                self.q_extd.put(self.wk_dir+self.md5_recup(f)+"/")
            else:
                print("**** Error extracting file : " + f + "****")
                os.remove(self.in_dir+f+".working")
        else:
            print("=== MD5 dir exist ===")
            self.q_extd.put(self.wk_dir+self.md5_recup(f)+"/")

    def extrac_file (self,f):
        p = subprocess.Popen(["7z","x",self.in_dir+f,"-o"+self.wk_dir+self.md5_recup(f)+"/"], stdout=subprocess.PIPE, universal_newlines=True, encoding="utf-8", errors="replace")
        for line in p.stdout:
            if str(line).find("Everything is Ok") >= 0:
                return True
            else:
                continue
        return False

    def md5_recup (self,f):
        with open(self.in_dir+f+".md5") as hfile:
            f_line = hfile.readline()
            f_other = hfile.read()
            hfile.close()
        return str(f_line.split()[0]).upper()
