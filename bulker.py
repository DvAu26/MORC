#!/usr/bin/python3.5
# coding=utf-8

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil


class Bulker:

    def __init__ (self,q_in,q_ou,w_dir,o_dir):
        self.q_inp = q_in
        self.q_out = q_ou
        self.wk_dir = w_dir
        self.ou_dir = o_dir
        self.end = False
        print("== INIT Bulker ==")

    def start (self):
        _thread.start_new_thread(self.run,())

    def stop (self):
        print("## STOP Bulker ##")
        self.end = True

    def run (self):
        while not self.end:
            if self.q_inp.qsize() > 0:
                pfic_blk = self.q_inp.get()
                _thread.start_new_thread(self.run2,(pfic_blk,))

    def run2 (self,pf):
        # Extract data from files with bulk_extractor
        # Extract in WORKSPACE to be dispatch in OUTPUT
        print("Bulker on : " + pf)
        bulk_out = self.wk_dir+self.get_md5(pf)+"/bulk_extract_"+self.getfile(pf)
        if self.extrac_file(pf,bulk_out):
            print("Bulk extract OK")
        else:
            print("Bulk extract NOK")
        

    def extrac_file (self, pf, out_dir):
        # Method to extract file f from the WORK_DIR in the WORK_DIR
        # with the MD5(pf) as extracting directory
        p = subprocess.Popen(["bulk_extractor","-e","all","-o"+out_dir,pf], stdout=subprocess.PIPE, universal_newlines=True, encoding="utf-8", errors="replace")
        for line in p.stdout:
            if str(line).find("All Threads Finished!") >= 0:
                return True
            else:
                continue
        return False

    def get_md5 (self,pf):
        # Method to get the DFIR MD5 from a pathfile
        tpath = pf.split("/")
        for d in tpath:
            if len(d) == 32:
                return d
        return ""

    def getfile (self,pf):
        # Method to diff swap, page...
        if pf.find("swap") >=0:
            return "swap"
        if pf.find("pagef") >= 0:
            return "pagefile"
        return "other"
