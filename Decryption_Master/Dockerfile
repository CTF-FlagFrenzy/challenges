FROM ubuntu:latest

COPY ./create_flags.py /root

RUN apt update && apt install -y openssh-server python3 python3-pip python3-venv
RUN useradd -m -s /bin/bash j007 && echo 'j007:'$PASSWORD | chpasswd
RUN python3 -m venv /env && /env/bin/pip install pycryptodome

EXPOSE 22

ENTRYPOINT ["/bin/bash", "-c", "source /env/bin/activate && python3 /root/create_flags.py && rm /root/create_flags.py && service ssh start && sleep infinity"]