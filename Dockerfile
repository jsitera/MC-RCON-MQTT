FROM python:3

#RUN apt-get update

COPY README.docker.md /
COPY README.md /
CMD mkdir /workdir
WORKDIR /workdir

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY mc-rcon-mqtt.py /workdir
COPY config.py /workdir

ENTRYPOINT ["python3", "/workdir/mc-rcon-mqtt.py"]
