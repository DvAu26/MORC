#!/usr/bin/python3.5
# coding=utf-8

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil
import json

from evtx2es import evtx2es
from datetime import datetime
from elasticsearch import Elasticsearch, helpers



class Elasticer:

    def __init__ (self,q_in,w_dir,o_dir):
        self.q_inp = q_in
        self.wk_dir = w_dir
        self.ou_dir = o_dir
        self.pending = 0
        self.nbfile = 0
        self.end = False
        self.elashost = "192.168.1.12"
        self.elasport = 9200
        self.elashostport = self.elashost + ":" + str(self.elasport)
        self.client = Elasticsearch(self.elashostport)
        print("== INIT Elasticer ==")

    def start (self):
        _thread.start_new_thread(self.run,())

    def stop (self):
        print("## STOP Elasticer ##")
        self.end = True

    def run (self):
        while not self.end:
            if self.q_inp.qsize() > 0:
                self.pending += 1
                self.nbfile += 1
                pfic_es = self.q_inp.get()
                _thread.start_new_thread(self.run2,(pfic_es,))

    def run2 (self,pf):
        # Copy from WORKSPACE to OUTPUT/AVCheck
        print("--> Elasticer Pending/Files : " + str(self.pending) + " / " + str(self.nbfile))
        md5dfir = self.get_md5(pf)
        filename = self.get_filename(pf)
        if filename.find("evtx") > 0:
            evtx2es(pf,host=self.elashost, port=self.elasport, index='dfir-orc-evtx', size=500)
        else:
            indextogo = self.get_index(filename)

            # call the function to get the string data containing docs
            docs = self.get_data_from_text_file(pf)
            
            # define an empty list for the Elasticsearch docs
            doc_list = []
            
            # use Python's enumerate() function to iterate over list of doc strings
            for num, doc in enumerate(docs):
            
                # catch any JSON loads() errors
                try:
                    
                    # prevent JSONDecodeError resulting from Python uppercase boolean
                    doc = doc.replace("True", "true")
                    doc = doc.replace("False", "false")
                    
                    # convert the string to a dict object
                    dict_doc = json.loads(doc)
                    
                    # add a new field to the Elasticsearch doc
                    dict_doc["timestamp"] = datetime.now()
                    
                    # add a dict key called "_id" if you'd like to specify an ID for the doc
                    dict_doc["_id"] = num
                    
                    # append the dict object to the list []
                    doc_list += [dict_doc]
                
                except json.decoder.JSONDecodeError as err:
                    # print the errors
                    print ("ERROR for num:", num, "-- JSONDecodeError:", err, "for doc:", doc)
                    
                    print ("Dict docs length:", len(doc_list))
                    
                # attempt to index the dictionary entries using the helpers.bulk() method
                try:
                    #print ("\nAttempting to index the list of docs using helpers.bulk()")
                    
                    # use the helpers library's Bulk API to index list of Elasticsearch docs
                    resp = helpers.bulk(
                    self.client,
                    doc_list,
                    index = indextogo,
                    doc_type = "_doc"
                    )
                    
                    # print the response returned by Elasticsearch
                    print ("helpers.bulk() RESPONSE:", resp)
                    #print ("helpers.bulk() RESPONSE:", json.dumps(resp, indent=4))
                    
                except Exception as err:
                
                    # print any errors returned w
                    ## Prerequisiteshile making the helpers.bulk() API call
                    print("Elasticsearch helpers.bulk() ERROR:", err)
                    quit()
        
        self.pending -= 1    
        
        


    # define a function that will load a text file
    def get_data_from_text_file(self,pf):
        # the function will return a list of docs
        return [l.strip() for l in open(str(pf), encoding="utf8", errors='ignore')]

    def get_filename (self,f):
        # Method to get the filename from a pathfile
        return str(f.split("/")[-1]).lower()

    def get_index (self,f):
        # Method to get the index name and check if exist or create its
        # from a filename
        index = "dfir-orc-" + f.split("-")[0]
        self.client.indices.create(index=index,ignore=400)
        self.client.indices.create(index='dfir-orc-evtx',ignore=400)
        return index


    def get_md5 (self,f):
        # Method to get the DFIR MD5 from a pathfile
        tpath = f.split("/")
        for d in tpath:
            if len(d) == 32:
                return d
        return ""


"""
        newfilename = filename + ".json"
 
        with open(self.ou_dir+md5dfir+"/CSV_Splunk/"+newfilename, "w", encoding='utf-8') as outjson:
           result: List[dict] = evtx2json(pf)
           outjson.write(result)
        outjson.close() 
                evtx2es(pf, host="192.168.1.12", port=9200, index="MORC_evtx")

"""
