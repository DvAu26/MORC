# MORC

Auto extract french DFIR ORC

Tested : Ubuntu 20.04 LTS and Ubuntu 20.10

## Requirements

1. Install fresh Ubuntu 20.04 x64

2. Update and upgrade packages

```
sudo apt update && sudo apt upgrade -y
```

3. Install packages for MORC and Bulk_extractor

```
sudo apt install p7zip-full python3-magic python3-pip autoconf automake default-jdk libewf-dev sqlite3 -y
pip3 install --upgrade requests
```

4. Install Bulk extractor

Bulk_extractor install, follow : https://github.com/simsong/bulk_extractor

```
cd ~
git clone https://github.com/simsong/bulk_extractor.git --recursive
cd bulk_extractor
./etc/CONFIGURE_UBUNTU18LTS.bash
chmod +x bootstrap.sh
./bootstrap.sh
./configure
make
sudo make install
cd ~
```

5. MORC work with lot of files, we must update your ulimits for system and user environment.

```
sudo bash -c "cat <<EOF >> /etc/security/limits.conf
# Ulimits max 1 000 000 files
*               soft               nofile               1000000
*               hard               nofile               1000000
root            soft               nofile               1000000
root            hard               nofile               1000000
EOF
"

sudo bash -c "cat <<EOF >> /etc/pam.d/common-session
session required pam_limits.so
EOF
"
```
Need logout or reboot to take change :

```
exit
```

or
```
reboot
```

6. Install MORC with its python requirements

```
cd ~
git clone https://github.com/DvAu26/MORC
cd MORC
pip3 install -r requirements.txt
```

## Using

1. Configure working directories

Edit the config.ini file of MORC (with vi, vim or nano)

```
vim ~/MORC/config.ini
```

- Change the __BASE_DIR__ in _config.ini_

`BASE_DIR = /mnt/MORC/`

BASE_DIR is the root directory where MORC will work in.
In this folder, MORC will create directories INPUT, WORKSPACE and OUTPUT (by default).

`BASE_DIR = /case/MORC/`

- Change the __BASE_NAME__ in _config.ini_ (optional)

Default configuration work fine.
You can modify or adapt the naming of DFIR-ORC files that you have to submit to MORC.

`BASE_NAME =['ORCSYS','ORCMEM']`

`BASE_NAME =['ORCSYS','DFIR-ORC','ORCYARA','ORCMEM']`

2. MORC initialization

```
python3 MORC.py
```

This will create default directories INPUT, WORKSPACE and OUTPUT in the path specified in the variable BASE_DIR. 

NB: For Logs

```
python3 MORC.py 2>&1 | tee -a MORC.log
```

3. DFIR-ORCs submission

Copy the DFIR-ORC files to the INPUT directory.

Nothing more to do...
You just have to wait a minute for the file(s) to be detected by MORC 
and for the magic to work.

## How it works

The system archi will have a repository (export NFS, SMB, glusterFS...) with the _DFIR-ORCs_ to be extract and analyze.

- __BASE_DIR__ : directory where MORC will search _DFIR-ORC_ and where MORC will perform the extraction
- __IN_DIR__ : directory where you put your own _DFIR-ORCs_.
- __WORK_DIR__ : directory where MORC will extract, analyze...
- __OUT_DIR__ : directory where MORC put the analyzable files.

The _DFIR-ORC_ format the output archives names.
- __BASE_NAME__ : list of start name for your own _DFIR-ORCs_. ([BASE_NAME]\_[COMPUTER_NAME]\_[DATE]\_[SUFFIX_NAME].7z)

### Little Workflow

You will perform an Hash check or at least an Hash calculate before any action.

- MORC calculate a MD5 hash for all files in the __IN_DIR__ and create _file.md5_ file with the calculate MD5 in the __OUT_DIR__.
(MD5 is the first step before it will perform SHA-1 and SHA-256)
- MORC extract _DFIR-ORCs_ in __WORK_DIR__/__MD5__/
- MORC create in __OUT_DIR__/__MD5__/__AV__/ an archive with all artefacts have to go to AV check
- MORC move all _CSV_ files in __OUT_DIR__/__MD5__/__CSV__/ to go to ELK/Splunk/others SIEM.
- MORC will launch __log2timeline/psort__ over evtx at least and put the csv timeline result in __OUT_DIR__/__MD5__/__CSV__/
- MORC will launch Tzworks binaries over the artefacts.
- MORC will launch Metadata extractor over the __EXE__ files.


## Roadmap

Little roadmap :

- PoC with subprocess and queues
- PoC with celery tasker and rabbitmq (backend and broker)

### OLD

1. Package APT

```
python3-csvkit python-plaso
```
