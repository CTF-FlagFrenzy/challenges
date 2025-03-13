FROM python:3.12

COPY . c
WORKDIR /c

RUN sh ./build.sh

EXPOSE 80

ENTRYPOINT [ "sh", "entry.sh" ]

