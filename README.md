# emem
Estacion Meteorologica EM

This project consist of:
- temperature and humidity sensors prototype based or arduino UNO and dht22. See thsUNO chapter
- temperature and humidity device battery powered. See thsnano chapter
- sensors collector software system for raspberry pi raspbian based. See scsem chapter

## thsUNO

Prototype to learn and play

## thsNANO

The real used sensor low power consumption device up to 2 DHT-22 sensors and one HC-05 device


## scsem 

It consists of some scripts and nice docker to run influxdb and grafana so that store and show fancy graphs in a web interface
Main script collectorMain launch several threads one per device or local dht onboard on gpi in raspberrys. Sensors home layout is in global dict easy to understand.
It logs for debugging to 2 files, one per traces an other only for exceptions.

# Miscelaneus 

## Some helper notes

### BT setup 

NOTE: to review with several peers BT arrives...
Setup bt devs in rpi and or ubuntu
>sudo rfcomm release all
>sudo rfcomm bind hci0 <hc5-addr> 1  // this creates /dev/rfcomm0 dev, and when any program open it, it connects automatically, e.g minicom -D /dev/xxx

in /etc/bluetooth/rfcomm.conf can be setup binding too

Alternative working in ubuntu
sudo hcitool cc 98:D3:32:20:FB:90  //connect
sudo hcitool cc 98:D3:32:20:FB:90  //disconnect

If you have problems with setting up the pin, you can force in: sudo su,  echo "zzzzzz 1234" >/var/lib/bluetooth/xxxxx/pincodes   xxxx is host mac bt address and zzzz mac bt address of dht 
https://myraspberryandme.wordpress.com/2013/11/20/bluetooth-serial-communication-with-hc-05/

In this project, bindBTmac.sh is used to setup. It is launched by collectorMain.py.

### Docker images and raspberry

Search raspberry images as armhf architecture in docker hub. It isn't the same that your tipically x86 laptop.  For an easy hack compatibility check docker_influxdb or docker_grafana launcher script in this repo.  Fortunately comunity is great, however there is some concern about security... 

## Some interesting links

Some of the best links used during this learning journey. Thanks to all 

[RPI learning resources](https://www.raspberrypi.org/resources/learn/)

[RPI GPIO pin out](https://pinout.xyz/pinout/pin12_gpio18#)

[RPI witn a connected DHT22](https://github.com/adafruit/Adafruit_Python_DHT)

[RPI and HC05 setup](https://myraspberryandme.wordpress.com/2013/11/20/bluetooth-serial-communication-with-hc-05/)

[Docker getting started](https://docs.docker.com/get-started/)

[Docker hub](https://hub.docker.com/)

[Docker in raspberry pi](https://blog.alexellis.io/5-things-docker-rpi/)

[Arduino power mode explained](https://aprendiendoarduino.wordpress.com/2016/11/16/arduino-sleep-mode/)

[ATmega328-328P_Datasheet](http://www.atmel.com/Images/Atmel-42735-8-bit-AVR-Microcontroller-ATmega328-328P_Datasheet.pdf)

[Json on line validator](https://jsonlint.com/)


# TODO LIST
- Maybe i should create a docker image for thscollector dividing it in two part one per bt access and other pure ip and process so that deploy will be smarter and out of python deps
- pass dict with definitions to a yaml, upload an example but keeps our out of github just for a bit privacy
- echo to bluetooth'ers
- try nano with dht including easy on pin vcc
- try more than one bluethoot, still big doubts about how to setup rfcom stuff and take decision over main id for devices/sensors
- play with grafana to show more than one sensor
- rotate logs and make it configurable ? or input args?
- try more than one dht on arduino
- battery stuff 



