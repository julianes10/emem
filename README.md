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


## TODO LIST
- Maybe i should create a docker image for thscollector dividing it in two part one per bt access and other pure ip and process so that deploy will be smarter and out of python deps
- I have to investigate how store dasboard setting in git without storing temp db data

## Some helper notes

### Setup bt devs in rpi and or ubuntu
>sudo rfcomm release all
>sudo rfcomm bind hci0 <hc5 addr> 1  // this creates /dev/rfcomm0 dev, and when any program open it, it connects automatically, e.g minicom -D /dev/xxx

in /etc/bluetooth/rfcomm.conf can be setup binding too

### Alternative working in ubuntu
sudo hcitool cc 98:D3:32:20:FB:90  //connect
sudo hcitool cc 98:D3:32:20:FB:90  //disconnect

If you have problems with setting up the pin, you can force in: sudo su,  echo "zzzzzz 1234" >/dev/lib/bluetooth/xxxxx/pincodes   xxxx is host mac bt address and zzzz mac bt address of dht 
https://myraspberryandme.wordpress.com/2013/11/20/bluetooth-serial-communication-with-hc-05/









