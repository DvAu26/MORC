#!/usr/bin/python3.5
# coding=utf-8

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil


class VolWorker:

    def __init__ (self,q_in,q_ou,w_dir,o_dir):
        self.q_inp = q_in
        self.q_out = q_ou
        self.wk_dir = w_dir
        self.ou_dir = o_dir
        self.end = False
        print("== INIT VolWorker ==")

    def start (self):
        _thread.start_new_thread(self.run,())

    def stop (self):
        print("## STOP VolWorker ##")
        self.end = True

    def run (self):
        while not self.end:
            if self.q_inp.qsize() > 0:
                fil_out_command_prof = self.q_inp.get()
                _thread.start_new_thread(self.run2,(file_out_command_prof,))

    def run2 (self,focp):
        # Do some volatility commands without output format
        # f = file## o = output format## c = command## p = profile
        split_focp = focp.split("##")
        f = split_focp[0]
        o = split_focp[1]
        c = split_focp[2]
        p = split_focp[3]
        print("Volatility on : " + f)
        result = ""
        if c.find("imageinfo") >=0:
            p = subprocess.Popen(["vol.py","-f",f,c], stdout=subprocess.PIPE, universal_newlines=True, encoding="utf-8", errors="replace")
        else:
            p = subprocess.Popen(["vol.py","-f",f,c,"--output="+o,"--profile="+p], stdout=subprocess.PIPE, universal_newlines=True, encoding="utf-8", errors="replace")
        for line in p.stdout:
            result += line
        self.q_out.put(result)

