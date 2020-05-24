#!/usr/bin/env python3

# MQTT Minecraft server feeder
# Feeds Minecraft server via RCON with commands received via MQTT

# requirements
# pip3 install paho-mqtt

import paho.mqtt.client as mqtt
from time import time, sleep
import signal

# configuration
base_topic = 'PI1'
mqtt_hostname = '147.228.121.4'
mqtt_clientname = 'test client'

# MQTT receive callback
def on_message(client, userdata, message):
    print("message received ",message.topic,str(message.payload.decode("utf-8")))

# Hook for cleanup after interrupt
def signal_handler(signal, frame):
    global interrupted
    interrupted = True

signal.signal(signal.SIGINT, signal_handler)
interrupted = False
    
# MQTT connection
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message

try:
  mqtt_client.connect(mqtt_hostname)
except:
  print("MQTT connection error.")
  sys.exit(1)
else:
  print("MQTT connection established.")


mqtt_client.loop_start()
sleep(1)

topic = '{}/#'.format(base_topic)
try:
  mqtt_client.subscribe(topic)
except:
  print("MQTT subscribe error.")
  sys.exit(1)
else:
  print("MQTT subscribed to topic ", topic)

# main loop
while True:
  sleep(1)

  if interrupted:
      # cleanup
      print("mc-rcon-mqtt ending.")
      mqtt_client.disconnect()
      break
