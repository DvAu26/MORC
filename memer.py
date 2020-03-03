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
        # self.q_in = queue.Queue()
        # self.q_ou = queue.Queue()
        self.end = False
        self.cmd_vol_dump = ["cachedump","dlldump","dumpcerts","dumpfiles","dumpregistry","hashdump","hivedump","lsadump","memdump","moddump","procdump","vaddump"]
        self.cmd_vol_csv = ["amcache","apihooks","atoms","atomscan","auditpol","bigpools","bioskbd","callbacks","clipboard","cmdline","cmdscan","connections","connscan","consoles","crashinfo","deskscan","devicetree","dlllist","driverirp","drivermodule","driverscan","editbox","envars","eventhooks","evtlogs","filescan","gahti","gditimers","gdt","getservicesids","getsids","handles","hibinfo","hivelist","hivescan","hpakextract","hpakinfo","idt","iehistory","impscan","joblinks","kdbgscan","kpcrscan","ldrmodules","machoinfo","malfind","mbrparser","memmap","messagehooks","modscan","modules","multiscan","mutantscan","notepad","objtypescan","patcher","poolpeek","printkey","privs","pslist","psscan","pstree","psxview","screenshot","servicediff","sessions","shimcache","shutdowntime","sockets","sockscan","ssdt","strings","svcscan","symlinkscan","thrdscan","threads","timers","truecryptmasterRecover","truecryptpassphraseTrueCrypt","truecryptsummaryTrueCrypt","unloadedmodulesPrint","userassist","userhandles","vadinfo","vadtree","vadwalk","vboxinfo","verinfo","windows","wintree","wndscan","yarascan"]
        self.cmd_vol_timeline = ["mftparser","shellbags","timeliner"]
        # self.vol = VolWorker(self.q_in,self.q_ou)
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
        # -------------------
        # 1 - Get the profile
        # 2 - Check the profile
        # 3 - Get the memory timeline
        # 4 - Get out text memory (pslist, netscan, dlllist...)
        # 5 - Get out dump memory (vaddump, dlldump...)
        # VolVorker : f = file## o = output format## c = command## p = profile
        # --------------------
        # print(f + "##csv##imageinfo##profile")
        profile = self.profiler(f)
        print("Profile --> " + profile)
        if len(profile) > 1:
            # Profile Find
            # Testing profile suggested
            if self.prof_tester(f,profile):
                print("profile OK")
            else:
                print("-- Not good profile - " + profile + " - for the file :\n" + f)
        else:
            print("-- No suggested profile  for the file : \n --" + f)



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

    def check_result(self,result):
        check = False
        for rline in result.stdout:
            if str(rline).find("putting to") >= 0:
                check = True
        return check

    def volWorker(self,f,prof,cmd,outfor):
        # Worker with volatility
        result = ""
        p = subprocess.Popen(["vol.py","-f", str(f) , "--profile="+str(prof), "--output="+str(outfor), str(cmd)], stdout=subprocess.PIPE, universal_newlines=True, encoding="utf-8", errors="replace")
        for line in p.stdout:
            result += line
        print(result)
        return result

    def profiler (self, f):
        # Only Windows with imageinfo, mac_get_profile or a "linux_get_profile"
        profilers = []
        serv_pack = ""
        result = subprocess.Popen(["vol.py","-f", f , "imageinfo", "--output=text"], stdout=subprocess.PIPE)
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

    def prof_tester (self, f, prof):
        okay = False
        print("Profile tester : " + str(f) + "  " + str(prof))
        # Windows profile but linux and mac too.
        r = self.volWorker(str(f),str(prof),"pslist","text")
        for line in r.readlines:
            print(line)
            if str(line).find("0x") >=0 and str(line).find("lsass"):
                okay = True
        return okay
