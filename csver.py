#!/usr/bin/python3.5
# coding=utf-8

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil


class Csver:

    def __init__ (self,q_in,q_ou,w_dir,o_dir):
        self.q_inp = q_in
        self.q_out = q_ou
        self.wk_dir = w_dir
        self.ou_dir = o_dir
        self.end = False
        print("== INIT CSVer ==")

    def start (self):
        _thread.start_new_thread(self.run,())

    def stop (self):
        print("## STOP CSVer ##")
        self.end = True

    def run (self):
        while not self.end:
            if self.q_inp.qsize() > 0:
                pfic_csv = self.q_inp.get()
                _thread.start_new_thread(self.run2,(pfic_csv,))

    def run2 (self,pf):
        # Works with file path
        # Test if ComputerName is present
        # Add columns MD5DFIR, NameDFIR, ComputerName if not present
        print("CSVer on : " + pf)
