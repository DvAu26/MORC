#!/usr/bin/python3.5
# coding=utf-8

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil


class Dispatcher:

    def __init__ (self,q_dis,q_extrac,q_extrad,q_av,q_hsh,q_hsd,i_dir,w_dir,o_dir):
        self.q_dis = q_dis
        self.q_extrac = q_extrac
        self.q_extrad = q_extrad
        self.q_av = q_av
        self.q_hash = q_hsh
        self.q_hashed = q_hsd
        self.in_dir = i_dir
        self.wk_dir = w_dir
        self.ou_dir = o_dir
        self.end = False
        print("== INIT Dispatcher ==")

    def start (self):
        _thread.start_new_thread(self.run,())

    def stop (self):
        print("## STOP Dispacher ##")
        self.end = True

    def run (self):
        while not self.end:
            if self.q_dis.qsize() > 0:
                fic_dis = self.q_dis.get()
                _thread.start_new_thread(self.run2,(fic_dis,))
            if self.q_hashed.qsize() > 0:
                fic_hsd = self.q_hashed.get()
                _thread.start_new_thread(self.run3,(fic_hsd,))
            if self.q_hashed.qsize() > 0:
                dir_ext = self.q_extrad.get()
                _thread.start_new_thread(self.run4,(dir_ext,))


    def run2 (self,f):
        print("Dispatcher on : " + f)
        self.q_hash.put(f)

    def run3 (self,f):
        print("Dispatch after hash on : " + f)
        self.q_extrac.put(f)

    def run4 (self,d):
        print("Dispatch after extract on : " + d)
        # self.q_extrac.put(f)
        # Calculate MD5?
        # Check MD5?
        # Check Extract?
        # Extract
        # Check AV?
        # Create AV arch
        # Check CSV?
        # Copy and move CSV
        # Check timeline
        # Create timeline
