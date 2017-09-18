#!/bin/bash 
#args: $1(BTMAC) $2(dev file) [$3 verbose]

echo "Here we go $@"


hcitool scan | grep $1
aux=$?

if [ $aux = 0 ]; then
  echo "Scannner detected to $1"
else
  echo "Scannner NOT detected to $1. But $echo. Exiting..."
##  #exit 1
fi

reportStatus ()
{
  sudo ls /dev/rfc*
#  sudo tree /var/lib/bluetooth/*/$2
}

if [ "$3" = "verbose" ]; then
  echo "Status before binding:"
  reportStatus
fi

sudo rfcomm release $2
if [ "$3" = "verbose" ]; then
  echo "Status after releasing:"
  reportStatus
fi

sudo rfcomm bind $2 $1 1
if [ "$3" = "verbose" ]; then
  echo "Status after binding:"
  reportStatus
fi
exit 0
