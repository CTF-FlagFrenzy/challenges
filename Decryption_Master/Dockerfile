FROM ubuntu:latest

COPY ./create_flags.py /root

RUN mkdir /usr/share/wordlists
COPY ./rockyou.txt.gz /usr/share/wordlists

RUN gunzip /usr/share/wordlists/rockyou.txt.gz && apt update && apt install -y openssh-server python3 python3-pip python3-venv nano
RUN python3 -m venv /env && /env/bin/pip install pycryptodome

EXPOSE 22

ENTRYPOINT ["/bin/bash", "-c", "useradd -m -s /bin/bash j007 && echo 'j007:'$PASSWORD | chpasswd && source /env/bin/activate && python3 /root/create_flags.py && rm /root/create_flags.py && service ssh start && sleep infinity"]