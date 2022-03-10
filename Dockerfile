FROM python:3.10-slim-buster

ADD src /app
RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y vim \
 && pip install --upgrade pip \
 && pip install -r /app/requirements.txt \
 && useradd -mb /tmp -s /bin/bash -u 1000 mutator \
 && chown -R mutator /app
USER mutator
WORKDIR /app
ENTRYPOINT [ "uvicorn", "--reload", "--host", "0.0.0.0", "--ssl-keyfile", "/app/certs/tls.key", "--ssl-certfile", "/app/certs/tls.crt", "--ssl-ca-certs", "/app/certs/ca.crt", "main:app"]
