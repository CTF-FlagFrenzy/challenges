FROM ubuntu:latest

COPY ./create_flags.py /root

RUN apt update && apt install -y openssh-server python3
RUN service ssh start && useradd -m -s /bin/bash j007 && echo 'j007:Pa$$w0rd!' | chpasswd

EXPOSE 22

ENTRYPOINT ["python3", "/root/create_flags.py"]
CMD ["rm", "/root/create_flags.py", "&&", "sleep", "infinity"]