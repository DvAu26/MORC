#!/usr/bin/python3.5
# coding=utf-8

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil

# TODO
# Better using of pyunpack
from pyunpack import Archive

class Extractor:

    def __init__ (self,q_ext,q_exted,q_extp,i_dir,w_dir):
        self.q_ext = q_ext
        self.q_extd = q_exted
        self.q_ext2 = q_extp
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
            if self.q_ext2.qsize() > 0:
                path_ext = self.q_ext2.get()
                _thread.start_new_thread(self.run3,(path_ext,))

    def run2 (self,f):
        # f is file name in the IN_DIR
        # check if wk_dir/MD5/ exists
        # if MD5 exist q_extrad(f)
        # if not extract in the wk_dir/MD5 folder
        if not os.path.isdir(self.wk_dir+self.md5_recup(f)+"/"):
            print("Extracting file : " + f)
            if self.extrac_file(f):
                # print("=== Extract OK in the MD5 folder ===")
                self.q_extd.put(self.wk_dir+self.md5_recup(f)+"/")
            else:
                print("**** Error extracting file : " + f + "****")
                os.remove(self.in_dir+f+".working")
        else:
            # print("=== MD5 dir exist ===")
            # print(f)
            self.q_extd.put(self.wk_dir+self.md5_recup(f)+"/")

    def run3 (self,path):
        # path is a path from an extracted archives
        # just extract in the same directory but whit
        # ".dir" like directory
        if not os.path.isdir(path+".dir"):
            print("Extracting file : " + path)
            if self.extrac_path(path):
                # print("=== Extract OK ===")
                self.q_extd.put(path+".dir/")
            else:
                print("**** Error extracting file : " + path + "****")
        else:
            # print("=== Directory exist ===")
            self.q_extd.put(path+".dir/")

    def extrac_file (self,f):
        # Method to extract file f from the IN_DIR in the WORK_DIR
        # with the MD5(f) as extracting directory
        # TODO add default password DFIR-ORC anywhere
        # p = Archive(self.in_dir+f).extractall(self.wk_dir+self.md5_recup(f)+"/",auto_create_dir=True)
        p = subprocess.Popen(["7z","x",self.in_dir+f,"-o"+self.wk_dir+self.md5_recup(f)+"/","-pV!ruS"], stdout=subprocess.PIPE, universal_newlines=True, encoding="utf-8", errors="replace")
        for line in p.stdout:
            if str(line).find("Everything is Ok") >= 0:
                return True
            else:
                continue
        return False

    def md5_recup (self,f):
        # Method to not calculate but extract from the
        # f.md5 in the IN_DIR
        with open(self.in_dir+f+".md5") as hfile:
            f_line = hfile.readline()
            f_other = hfile.read()
            hfile.close()
        return str(f_line.split()[0]).upper()

    def extrac_path (self,pth):
        # Method to extract file from a path (WORK_DIR) to path.dir
        # TODO add default password DFIR-ORC anywhere
        p = subprocess.Popen(["7z","x",pth,"-o"+pth+".dir/","-pV!ruS"], stdout=subprocess.PIPE, universal_newlines=True, encoding="utf-8", errors="replace")
        # p = Archive(pth).extractall(+pth+".dir/",auto_create_dir=True)
        for line in p.stdout:
            if str(line).find("Everything is Ok") >= 0:
                return True
            else:
                continue
        return False
