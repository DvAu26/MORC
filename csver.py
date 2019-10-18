#!/usr/bin/python3.5
# coding=utf-8

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil
import csv
import string

COLUMNS_ADDED = ("DFIR_MD5","DFIR_NAME")
OPT_COLUMNS_ADDED = ("ComputerName")

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
        if self.check_csv(pf):
            if self.clean_header(pf):
                if self.add_columns(pf):
                    print("CSV OK go to CSV_Splunk OUTPUT")
                else:
                     print("**** Error CSVer 3 "+pf+" ****")
            else:
                print("**** Error CSVer 2 "+pf+" ****")
        else:
            print("**** Error CSVer 1 "+pf+" ****")

    def check_csv (self,pf):
        # Method to check, 1st line like an CSV header
        # If not find it and put it at the header place
        print("Check csv : " + pf)
        # TODO check if not empty !!
        md5dfir = self.get_md5(pf)
        dfirname = self.get_dfir_originalName(md5dfir) + ".7z"
        filename = pf.split("/")[-1]
        # !! ComputerName with _ will have a named part !!
        compName = dfirname.split("_")[2]
        withcompName = False
        if filename.find("GetThis.csv") >= 0 or filename.find("volstat") >= 0:
            newfilename = pf.split("/")[-2].split(".")[0] + "_" + filename
        else:
            newfilename = filename
        
        with open(pf, newline='',encoding='utf-8', errors='ignore') as inpcsv, open(self.ou_dir+md5dfir+"/CSV_Splunk/"+newfilename, "w", encoding='utf-8') as outcsv:
            headerinpcsv = inpcsv.readline()
            if len(headerinpcsv.split(",")) > 1:
                if headerinpcsv.find("ComputerName") >= 0 and headerinpcsv.find("PSComputerName") < 0:
                    headeroutcsv = ",".join(COLUMNS_ADDED)
                    withcompName = True
                else:
                    headeroutcsv = ",".join(COLUMNS_ADDED) + "," + str(OPT_COLUMNS_ADDED)
                headeroutcsv += "," + ",".join(self.clean_header(headerinpcsv))
                outcsv.write(headeroutcsv + "\n")
            else:
                # TODO TODO TODO !!
                print("Not like a csv header")
            
            startline = md5dfir.upper() + "," + dfirname.upper() + ","
            if not withcompName:
                startline += compName.upper() + ","
            
            for line in inpcsv:
                newline = startline + line
                outcsv.write(newline)
        inpcsv.close()
        outcsv.close()
        return False

    def clean_header (self,header):
        # Method to clean the header 
        # No space replace by _ not host name or other just ComputerName
        # That's not to have different fields for the same information
        # print("Add Columns csv : " + header)
        tbhead = header.split(",")
        tpclhead = ()
        for ithead in tbhead:
            # To clean space before and after field
            stithead = ithead.strip()
            # To clean non printable char
            filstithead = filter(lambda x: x in string.printable, stithead)
            strstithead = "".join(list(filstithead))
            # To replace whitespace by _, '"' by '', (): too
            strstithead = str(strstithead).replace(" ","_").replace('"','').replace('(','').replace(')','').replace(':','')
            # To append in the tuple
            tpclhead = tpclhead + (strstithead,)
        return tpclhead

    def add_columns (self,pf):
        # Method to add columns in the header and
        # in the csv with MD5DFIR, NameDFIR, ComputerName
        print("Add Columns csv : " + pf)

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
