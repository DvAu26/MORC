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
        # Getthis, process, jobstatistics... -> DFIR-ORC Info
        # Others                             -> DFIR-ORC Artefacts
        # Test if ComputerName is present
        # Add columns MD5DFIR, NameDFIR, ComputerName if not present
        print("CSVer on : " + pf)

    def check_csv (self,pf):
        # Method to check, 1st line like an CSV header
        # If not find it and put it at the header place
        print("Check csv : " + pf)

    def add_columns (self,pf):
        # Method to add columns in the header and
        # in the csv with MD5DFIR, NameDFIR, ComputerName
        print("Add Columns csv : " + pf)

    def clean_header (self,pf):
        # Method to clen the header 
        # No space replace by _ not host name or other just ComputerName
        # That's not to have different fields for the same information
        print("Add Columns csv : " + pf)

