# MORC
Auto extract french DFIR ORC

## Prerequis


```
sudo apt install p7zip-full log2timeline python3-magic python3-plaso
```

```
python hashlib
```


## Roadmap

Little roadmap :

- PoC with subprocess and queues
- PoC with celery tasker and rabbitmq (backend and broker)

## Using

```
git clone it
```

- Change the BASE_DIR in _MORC.py_
- Change the BASE_NAME in _MORC.py_

```
python3 MORC.py
```

## How it works

The system archi will have a repository (export NFS, SMB, glusterFS...) with the _DFIR-ORCs_ to be extract and analyze.

- __BASE_DIR__ : directory where MORC will search _DFIR-ORC_ and where MORC will perform the extraction
- __IN_DIR__ : directory where you put your own _DFIR-ORCs_.
- __WORK_DIR__ : directory where MORC will extract, analyze...
- __OUT_DIR__ : directory where MORC put the analyzable files.

The _DFIR-ORC_ format the output archives names.
- __BASE_NAME__ : list of start name for your own _DFIR-ORCs_. ([BASE_NAME]\_[COMPUTER_NAME]\_[DATE]\_[SUFFIX_NAME].7z)

### 1st Step

You will perform an Hash check or at least an Hash calculate before any action.

- MORC calculate a MD5 hash for all files in the __IN_DIR__ and create _file.md5_ file with the calculate MD5 in the __OUT_DIR__.
(MD5 is the first step before it will perform SHA-1 and SHA-256)
- MORC extract _DFIR-ORCs_ in __WORK_DIR__/__MD5__/
- MORC create in __OUT_DIR__/__MD5__/__AV__/ an archive with all artefacts have to go to AV check
- MORC move all _CSV_ files in __OUT_DIR__/__MD5__/__CSV__/ to go to ELK/Splunk/others SIEM.
- MORC launch __log2timeline/psort__ over evtx at least and put the csv timeline result in __OUT_DIR__/__MD5__/__CSV__/
- MORC launch Tzworks binaries over the artefacts.
- MORC launch Metadata extractor over the __EXE__ files.
