# emem
Estacion Meteorologica EM

This project consist of:
- temperature and humidity device battery powered. See thsmini chapter
- temperature and humidity sensors prototype based or arduino UNO and dht22. See thsUNO chapter
- sensors collector software system for raspberry pi raspbian based. See scsem chapter
 

## thsUNO

Prototype to show up 

## thsnano

TODO

## scsem 

It consists of some scripts and nice docker to run influxdb and grafana so that store and show fancy graphs in a web interface


### TODO LIST
- Maybe i should create a docker image for thscollector dividing it in two part one per bt access and other pure ip and process so that deploy will be smarter and out of python deps
- I have to investigate bt in rpi, it seems dev rfxxx does not work 
- I have to investigate how store dasboard setting in git without storing temp db data





