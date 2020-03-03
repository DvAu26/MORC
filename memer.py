#!/usr/bin/python3.5
# coding=utf-8

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil
from volWorker import VolWorker


class Memer:

    def __init__ (self,q_mem,q_memed,w_dir,o_dir):
        self.q_mem = q_mem
        self.q_memed = q_memed
        self.wk_dir = w_dir
        self.ou_dir = o_dir
        self.end = False
        # self.vol = VolWorker(q_in,q_ou,self.wk_dir,self.ou_dir)
        print("== INIT Memer ==")

    def start (self):
        _thread.start_new_thread(self.run,())

    def stop (self):
        print("## STOP Memer ##")
        self.end = True

    def run (self):
        while not self.end:
            if self.q_mem.qsize() > 0:
                fic_mem = self.q_mem.get()
                _thread.start_new_thread(self.run2,(fic_mem,))

    def run2 (self,f):
        print("Memer on : " + f)
        profile = self.profiler(f)
        print("Profil --> " + profile)

    def best_profile(self,profiles, sp):
        profile = ""
        if len(profiles) == 0:
            return ""
        else:
            for p in profiles:
                if "SP"+sp in p:
                    profile = p
            if profile == "":
                profile = profiles[0]
        return profile

    def profiler (self, f):
        # Only Windows with imageinfo, mac_get_profile or a "linux_get_profile"
        profilers = []
        serv_pack = ""
        result = subprocess.Popen(["vol.py","-f", f , "imageinfo", "--output=text"], stdout=subprocess.PIPE, universal_newlines=True, encoding="utf-8", errors="replace")
        for line in result.stdout:
            line = str(line).replace('\n',' ')
            strip_line = str(line).strip()
            if str(strip_line).find("Suggested Profile(s)") >= 0:
                # Profiles
                profiles = str(str(strip_line).rsplit(":")).rsplit(",")
                for pp in profiles:
                    if str(pp).find("Suggested Profile(s)") >=0:
                        continue
                    else:
                        profilers.append(str(str(pp).split("(")[0].strip()).replace('"','').strip())
            if str(strip_line).find("Service Pack") >= 0:
                # Service pack number
                serv_pack = str(strip_line).rsplit(":")
                serv_pack = str(serv_pack[1])[1]
        return self.best_profile(profilers,serv_pack)
