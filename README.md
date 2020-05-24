# MC-RCON-MQTT
Feeds Minecraft server via RCON with commands received via MQTT. 
# Description
Easy to use tool for connecting your Minecraft world with anything via IoT standards. Provided script is a base for your data flows, it is a generic gateway between MQTT and Minecraft at it can be easily adapted to your projects. It works only one way, from MQTT to Minecraft.
# How it works
The script runs on the Minecraft server accessing locally the RCON port. It subscribes to a particular topic on MQTT server and waits for messages. Wher a message is received the on_message routine genarates appropriate Minecraft command and sends it to the server console.
# Demo setup
The script is feeded by temperature/humidity sensor and generates commands to update a particular sign. The real world measurement is visible in the Minecraft world. We have the sensor in our real world greenhouse and the sign in the Minecraft is located on the greenhouse located there.
