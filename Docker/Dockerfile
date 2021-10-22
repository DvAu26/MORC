FROM ubuntu:20.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y 
RUN DEBIAN_FRONTEND=noninteractive apt install p7zip-full python3-magic python3-pip autoconf automake default-jdk libewf-dev sqlite3 -y
RUN pip3 install --upgrade requests

RUN apt install git sudo -y

RUN git clone https://github.com/simsong/bulk_extractor.git --recursive
WORKDIR ./bulk_extractor
RUN ./etc/CONFIGURE_UBUNTU18LTS.bash
RUN chmod +x bootstrap.sh
RUN ./bootstrap.sh
RUN ./configure
RUN make
RUN make install 
WORKDIR /

RUN git clone https://github.com/DvAu26/MORC
WORKDIR MORC
RUN pip3 install -r requirements.txt

CMD ["python3","MORC.py"]
