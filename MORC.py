#!/usr/bin/python3.5
# coding=utf-8

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil
from seeker import Seeker
from dispatcher import Dispatcher
from hasher import Hasher
from extractor import Extractor
from csver import Csver
from bulker import Bulker

# TODO
# Incident response identification... IRXXX or other.
# Find a way with parameters or with a folder name

# To be put in config file
# Base directory
BASE_DIR = "/mnt/MORC/"
# Directory with the DFIR-ORCs
IN_DIR = BASE_DIR + "INPUT/"
# Directory for the working process
WORK_DIR = BASE_DIR + "WORKSPACE/"
# Directory for the output result
OUT_DIR = BASE_DIR + "OUTPUT/"

DIRECTORIES = [BASE_DIR,IN_DIR,WORK_DIR,OUT_DIR]

# Base name for our DFIR-ORCs
# BASE_NAME = ["ORCSYS","ORCMEM"]
BASE_NAME = ["ORCSYS","DFIR-ORC","ORCYARA","ORCMEM"]

# DIR OUTPUT arbo
DIR_OUT = ["AV_CHECK","CSV_Splunk","TIMELINE","LOGS"]

# Check time in the IN_DIR (milliseconds)
CHECK_TIME = 500

# Block size to calculate HASH 
BLOCK_SIZE_HASH = 4096

if __name__ == '__main__':

    # Directory initiation
    for d in DIRECTORIES:
        if not os.path.exists(d):
            os.makedirs(d)

    # Queues initiation
    queue_dis = queue.Queue()
    queue_extrac = queue.Queue()
    queue_extraced = queue.Queue()
    queue_av = queue.Queue()
    queue_hash = queue.Queue()
    queue_hashed = queue.Queue()
    queue_ext_path = queue.Queue()
    queue_csv = queue.Queue()
    queue_csved = queue.Queue()
    queue_blk = queue.Queue()

    see = Seeker(queue_dis,IN_DIR,BASE_NAME,CHECK_TIME)
    dis = Dispatcher(queue_dis,queue_extrac,queue_extraced,queue_ext_path,queue_av,queue_hash,queue_hashed,queue_csv,queue_csved,queue_blk,IN_DIR,WORK_DIR,OUT_DIR,DIR_OUT)
    has = Hasher(queue_hash,queue_hashed,IN_DIR,WORK_DIR,BLOCK_SIZE_HASH)
    ext = Extractor(queue_extrac,queue_extraced,queue_ext_path,IN_DIR,WORK_DIR)
    csv = Csver(queue_csv,queue_csved,WORK_DIR,OUT_DIR)
    blk = Bulker(queue_blk, queue_extraced,WORK_DIR,OUT_DIR)
    #tim = Timeliner(queue_extrac,WORK_DIR,OUT_DIR)
    #avc = Avcheck(queue_av,WORK_DIR,OUT_DIR)

    see.start()
    dis.start()
    has.start()
    ext.start()
    csv.start()
    blk.start()
    #tim.start()
    #avc.start()

    input()

    see.stop()
    dis.stop()
    has.stop()
    ext.stop()
    csv.stop()
    blk.stop()
    #tim.stop()
    #avc.stop()
