#!/usr/bin/env python3

# MQTT Minecraft server feeder
# Feeds Minecraft server via RCON with commands received via MQTT

# requirements
# pip3 install paho-mqtt
# pip3 install mcrcon

import paho.mqtt.client as mqtt
from time import time, sleep
import signal
import socket
from mcrcon import MCRcon
import config    # my local config file


# configuration
base_topic = 'PI1'
mqtt_hostname = config.mqtt_hostname
mqtt_clientname = 'test client'
rcon_hostname = '127.0.0.1'
rcon_port = 25575
rcon_password = config.rcon_password


def send_to_RCON(command):

    print('Sending to RCON:', command)
    
    response = mcr.command(command)
    
    print('Response from RCON:', response)


# MQTT receive callback
######## edit here what to do when MQTT message is received ################
def on_message(client, userdata, message):
    value=str(message.payload.decode("utf-8"))
    print("message received ",message.topic,value)

    if "temperature" in message.topic:
        command='execute at 7a278519-5e0d-4ed5-b847-f5fc311b2170 run data merge block 217 6 -13 {Text2:"{\\"text\\":\\"\\\\u1405 ' + value + '°C \\\\u140a\\",\\"bold\\":true}"}'
        send_to_RCON(command)
        
        if float(value) < 25 :
            command='execute at 7a278519-5e0d-4ed5-b847-f5fc311b2170 run clone 247 4 90 243 4 82 215 4 -23'
            send_to_RCON(command)
        elif float(value) < 27 :
            command='execute at 7a278519-5e0d-4ed5-b847-f5fc311b2170 run clone 247 4 100 243 4 92 215 4 -23'
            send_to_RCON(command)
        else:
            command='execute at 7a278519-5e0d-4ed5-b847-f5fc311b2170 run clone 247 4 110 243 4 102 215 4 -23'
            send_to_RCON(command)
            


    elif "humidity" in message.topic:
        command='execute at 7a278519-5e0d-4ed5-b847-f5fc311b2170 run data merge block 217 6 -13 {Text4:"{\\"text\\":\\"\\\\u1405 ' + value + '% \\\\u140a\\",\\"bold\\":true}"}'
        send_to_RCON(command)
       
        if float(value) < 50 :
            command='execute at 7a278519-5e0d-4ed5-b847-f5fc311b2170 run function minecraft:greenhouse-normal'
            send_to_RCON(command)
        else:
            command='execute at 7a278519-5e0d-4ed5-b847-f5fc311b2170 run function minecraft:greenhouse-mossy'
            send_to_RCON(command)

    elif "weather" in message.topic:
        command='execute at 7a278519-5e0d-4ed5-b847-f5fc311b2170 run weather ' + value
        send_to_RCON(command)

    elif "button" in message.topic:
       
        if value == "on" :
            command='execute at 7a278519-5e0d-4ed5-b847-f5fc311b2170 run setblock 180 4 113 minecraft:redstone_block'
            send_to_RCON(command)
        else:
            command='execute at 7a278519-5e0d-4ed5-b847-f5fc311b2170 run setblock 180 4 113 minecraft:air'
            send_to_RCON(command)

    elif "joystickX" in message.topic:
       
        if value == "R" :
            command='execute at 052497cd-b045-4eae-ae37-2513b3593671 run tp 052497cd-b045-4eae-ae37-2513b3593671 ~0.25 ~ ~'
            send_to_RCON(command)
        else:
            command='execute at 052497cd-b045-4eae-ae37-2513b3593671 run tp 052497cd-b045-4eae-ae37-2513b3593671 ~-0.25 ~ ~'
            send_to_RCON(command)

    elif "joystickY" in message.topic:
       
        if value == "U" :
            command='execute at 052497cd-b045-4eae-ae37-2513b3593671 run tp 052497cd-b045-4eae-ae37-2513b3593671 ~ ~ ~-0.25'
            send_to_RCON(command)
        else:
            command='execute at 052497cd-b045-4eae-ae37-2513b3593671 run tp 052497cd-b045-4eae-ae37-2513b3593671 ~ ~ ~0.25'
            send_to_RCON(command)

    elif "joystickB" in message.topic:
            
            command='execute at 052497cd-b045-4eae-ae37-2513b3593671 run setblock 183 4 113 minecraft:redstone_block'
            send_to_RCON(command)

######  END of the section to be edited


# Hook for cleanup after interrupt
def signal_handler(signal, frame):
    global interrupted
    interrupted = True

signal.signal(signal.SIGINT, signal_handler)
interrupted = False
    
# MQTT connection initialization
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message

try:
  mqtt_client.connect(mqtt_hostname)
except:
  print("MQTT connection error.")
  sys.exit(1)
else:
  print("MQTT connection established.")

# RCON connection initialization
try:
  mcr = MCRcon(rcon_hostname, rcon_password)
  mcr.connect()
except:
  print("Connect to rcon failed. Incorrect rcon IP or passwd?")
  sys.exit(1)
else:
  print("RCON connection established.")


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
      mcr.disconnect()

      break
