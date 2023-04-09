FROM alpine:3.17.3

RUN \
  apk update &&\
  apk add --no-cache \
    python3 \
    py3-pip \
    openjdk8 \
    openjdk11 \
    openjdk17

WORKDIR /paper
COPY entrypoint.py .
COPY requirements.txt .

RUN \
  pip install -r requirements.txt &&\
  mkdir /data &&\
  chmod -R ugo+rwx /paper &&\
  chmod -R ugo+rwx /data

EXPOSE 25565
VOLUME /data

ENTRYPOINT ["python3", "entrypoint.py"]