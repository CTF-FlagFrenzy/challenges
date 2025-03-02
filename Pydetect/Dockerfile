FROM python:3.12

COPY . c
WORKDIR /c

RUN bash build.sh

EXPOSE 80

ENTRYPOINT [ "bash", "entry.sh" ]
