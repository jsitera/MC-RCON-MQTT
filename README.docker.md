This is docker image running MC-LOG-MQTT see README.md


docker run -d -it --name mc-rcon-mqtt sitera/mc-rcon-mqtt

Get logs
docker logs mc-rcon-mqtt

Run interactively (use with screen)
docker run -it sitera/mc-rcon-mqtt

Test container
docker run -it --entrypoint /bin/bash sitera/mc-rcon-mqtt
