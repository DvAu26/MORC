#!/usr/bin/python3.5
# coding=utf-8

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil


class Avcheck:

    def __init__ (self,q_in,w_dir,o_dir):
        self.q_inp = q_in
        self.wk_dir = w_dir
        self.ou_dir = o_dir
        self.end = False
        print("== INIT AVCheck ==")

    def start (self):
        _thread.start_new_thread(self.run,())

    def stop (self):
        print("## STOP AVCheck ##")
        self.end = True

    def run (self):
        while not self.end:
            if self.q_inp.qsize() > 0:
                pfic_avc = self.q_inp.get()
                _thread.start_new_thread(self.run2,(pfic_avc,))

    def run2 (self,pf):
        # Copy from WORKSPACE to OUTPUT/AVCheck
        print("AVCheck on : " + pf)
