#!/bin/bash 

docker run -it -v $(pwd)/config.ini:/MORC/config.ini -v $(pwd)/MORCFILES:/mnt/MORC/ morc
