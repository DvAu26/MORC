#!/usr/bin/python3.5
# coding=utf-8

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil
import configparser
from seeker import Seeker
from dispatcher import Dispatcher
from hasher import Hasher
from extractor import Extractor
from csver import Csver
from bulker import Bulker
from avcheck import Avcheck
from memer import Memer
from elasticer import Elasticer


# TODO
# Incident response identification... IRXXX or other.
# Find a way with parameters or with a folder name

config = configparser.ConfigParser()
config.read("config.ini")

# To be put in config file
# Base directory
BASE_DIR = config['WORKING_DIR']['BASE_DIR']
# Directory with the DFIR-ORCs
IN_DIR = BASE_DIR + config['WORKING_DIR']['IN_DIR']
# Directory for the working process
WORK_DIR = BASE_DIR + config['WORKING_DIR']['WORK_DIR']
# Directory for the output result
OUT_DIR = BASE_DIR + config['WORKING_DIR']['OUT_DIR']

DIRECTORIES = [BASE_DIR,IN_DIR,WORK_DIR,OUT_DIR]

# DIR OUTPUT arbo
DIR_OUT = config['WORKING_DIR']['DIR_OUT']

# Base name for our DFIR-ORCs
# BASE_NAME = ["ORCSYS","ORCMEM"]
BASE_NAME = config['BASE_DIR']['BASE_NAME']

# Check time in the IN_DIR (milliseconds)
CHECK_TIME = int(config['TIME']['CHECK_TIME'])

# Block size to calculate HASH
BLOCK_SIZE_HASH = int(config['HASHES']['BLOCK_SIZE_HASH'])

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
    queue_mem = queue.Queue()
    queue_memed = queue.Queue()
    queue_rslt = queue.Queue()
    queue_elastic = queue.Queue()

    see = Seeker(queue_dis,IN_DIR,BASE_NAME,CHECK_TIME)
    dis = Dispatcher(queue_dis,queue_extrac,queue_extraced,queue_ext_path,queue_av,queue_hash,queue_hashed,queue_csv,queue_csved,queue_blk,queue_mem,queue_memed,queue_elastic,IN_DIR,WORK_DIR,OUT_DIR,DIR_OUT)
    has = Hasher(queue_hash,queue_hashed,IN_DIR,WORK_DIR,BLOCK_SIZE_HASH)
    ext = Extractor(queue_extrac,queue_extraced,queue_ext_path,IN_DIR,WORK_DIR)
    csv = Csver(queue_csv,queue_csved,WORK_DIR,OUT_DIR)
    blk = Bulker(queue_blk,queue_extraced,WORK_DIR,OUT_DIR)
    mem = Memer(queue_mem,queue_extraced,IN_DIR,WORK_DIR,OUT_DIR)
    #tim = Timeliner(queue_extrac,WORK_DIR,OUT_DIR)
    avc = Avcheck(queue_av,WORK_DIR,OUT_DIR)
    #elas = Elasticer(queue_elastic,WORK_DIR,OUT_DIR)

    see.start()
    dis.start()
    has.start()
    ext.start()
    csv.start()
    #blk.start()
    mem.start()
    #tim.start()
    avc.start()
    #elas.start()

    input()

    see.stop()
    dis.stop()
    has.stop()
    ext.stop()
    csv.stop()
    #blk.stop()
    mem.stop()
    #tim.stop()
    avc.stop()
    #elas.stop()
