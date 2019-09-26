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

    def __init__ (self,q_ext,i_dir,w_dir):
        self.q_ext = q_ext
        self.in_dir = i_dir
        self.wk_dir = w_dir
        self.end = False
        print("== INIT Extractor ==")

    def start (self):
        _thread.start_new_thread(self.run,())

    def stop (self):
        print("## Stop Extractor ##")
        self.terminer = True

    def run (self):
        while not self.terminer:
            if self.q_ext.qsize() > 0:
                fic_ext = self.q_ext.get()
                _thread.start_new_thread(self.run2,(fic_ext,))

    def run2 (self,fic):
        print("Extracting file : " + f)
        p = subprocess.Popen(["7z","","",""], stdout=subprocess.PIPE)
        result = p.communicate()
        if str(result).find("Finale message 7z") >= 0:
            self.qpl.put(f)
        else:
            print("*** Error for the extracting process for the file " + f + " ***")
