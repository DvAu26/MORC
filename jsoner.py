#!/usr/bin/python3.5
# coding=utf-8

import csv
import json
import os
import magic
import subprocess
import queue
import time
import _thread
import shutil
import csv
import string


class Jsoner:

    def __init__ (self,q_in,q_ou,w_dir,o_dir):
        self.q_inp = q_in
        self.q_out = q_ou
        self.wk_dir = w_dir
        self.ou_dir = o_dir
        self.end = False
        self.pending = 0
        self.file = 0
        print("== INIT JSONer ==")

    def start (self):
        _thread.start_new_thread(self.run,())

    def stop (self):
        print("## STOP JSONer ##")
        self.end = True

    def run (self):
        while not self.end:
            if self.q_inp.qsize() > 0:
                pfic_csv = self.q_inp.get()
                _thread.start_new_thread(self.run2,(pfic_csv,))

    def run2 (self,pf):
        self.file += 1
        self.pending += 1
        print("--> JSONer Pending/Files :" + str(self.pending) + "/" + str(self.file))
        md5dfir = self.get_md5(pf)
        filename = pf.split("/")[-1]
        newfilename = str(filename).replace(".","-") + ".json"
        data = ""
        with open(pf,"r",encoding="ascii",errors="ignore") as csvFile, open(self.ou_dir+md5dfir+"/JSON_ELK/"+newfilename,"w") as jsonFile:
            csvReader = csv.DictReader(csvFile,delimiter=',',quotechar='"')
            for csvRow in csvReader:
                if len(csvRow) > 500:
                    jsonFile.write(str(csvRow).replace("'",'"').replace('="',"='").replace('"",',"'\",").replace(" '\"",' ""').replace('")',')') + "\n")
        csvFile.close()
        jsonFile.close()
        
        # Queue out to be pushed in Splunk or another software
        self.q_out.put(self.ou_dir+md5dfir+"/JSON_ELK/"+newfilename)
        self.pending -= 1

    def get_md5 (self,pf):
        # Method to get the DFIR MD5 from a pathfile
        tpath = pf.split("/")
        for d in tpath:
            if len(d) == 32:
                return d
        return ""

    def get_dfir_originalName (self,md5):
        # Method to get the DFIR name from a DFIR MD5
        fics = os.listdir(self.ou_dir+md5+"/")
        for f in fics:
            if str(f).find(".originalName") >= 0:
                return str(f).split(".")[0]
        return ""

"""
        with open(self.ou_dir+md5dfir+"/JSON_ELK/"+newfilename,"w") as jsonFile:
            jsonFile.write(data)
"""
