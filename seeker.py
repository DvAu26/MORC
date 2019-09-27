#!/usr/bin/python3.5
# coding=utf-8

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil


class Seeker:

    def __init__ (self,q_dis,i_dir,b_name,ch_time):
        self.q_dis = q_dis
        self.in_dir = i_dir
        self.b_name = b_name
        self.check_time = ch_time
        self.end = False
        print("== INIT Seeker ==")

    def start (self):
        _thread.start_new_thread(self.run,())

    def stop (self):
        print("## STOP Seeker ##")
        self.end = True

    def run (self):
        while not self.end:
            fichiers = os.listdir(self.in_dir)
            test = False
            for f in fichiers:
                # With f + .working to not retake
                if str(f).find(".working") >= 0:
                    continue
                if self.verif_arch(magic.from_file(self.in_dir+f),f) and not self.verif_working(f):
                    self.q_dis.put(f)
                    fw = open(self.in_dir+f+".working","w")
                    fw.close()
                    print("Seeker : " + f)
                else:
                    print("-- No new DFIR-ORCs --")
            time.sleep(self.check_time)


    def verif_arch (self,mag_f,fic):
        test = False
        if mag_f.find("archive") >=0 and fic.find(self.b_name) >= 0:
            test = True
        return test

    def verif_working (self,fic):
        return os.path.isfile(self.in_dir+fic+".working")
