# emem
Estacion Meteorologica EM

This project consist of:
- temperature and humidity device battery powered. See thsnano chapter
- temperature and humidity sensors prototype based or arduino UNO and dht22. See thsUNO chapter
- sensors collector software system for raspberry pi raspbian based. See scsem chapter


## thsUNO

Prototype to show up 

## thsnano

Here it is, and load with a usb mini cable...

## scsem 

It consists of some scripts and nice docker to run influxdb and grafana so that store and show fancy graphs in a web interface


# Miscelaneus 

## Some helper notes

### BT setup 

Setup bt devs in rpi and or ubuntu
>sudo rfcomm release all
>sudo rfcomm bind hci0 <hc5 addr> 1  // this creates /dev/rfcomm0 dev, and when any program open it, it connects automatically, e.g minicom -D /dev/xxx

in /etc/bluetooth/rfcomm.conf can be setup binding too

Alternative working in ubuntu
sudo hcitool cc 98:D3:32:20:FB:90  //connect
sudo hcitool cc 98:D3:32:20:FB:90  //disconnect

If you have problems with setting up the pin, you can force in: sudo su,  echo "zzzzzz 1234" >/dev/lib/bluetooth/xxxxx/pincodes   xxxx is host mac bt address and zzzz mac bt address of dht 
https://myraspberryandme.wordpress.com/2013/11/20/bluetooth-serial-communication-with-hc-05/

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



# TODO LIST
- Maybe i should create a docker image for thscollector dividing it in two part one per bt access and other pure ip and process so that deploy will be smarter and out of python deps
- get a dht22 onboard in rpi
- echo to bluetooth'ers
- 


