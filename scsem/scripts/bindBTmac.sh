#!/bin/sh 
#args: $1(BTMAC) [$2 verbose]
echo "Here we go $@"
reportStatus ()
{
  sudo ls /dev/rfc*
#  sudo tree /var/lib/bluetooth/*/$2
}

if [ "$2" = "verbose" ]; then
  echo "Status before binding:"
  reportStatus
fi

sudo rfcomm release hci0 $1
if [ "$2" = "verbose" ]; then
  echo "Status after releasing:"
  reportStatus
fi

sudo rfcomm bind hci0 $1 1
if [ "$2" = "verbose" ]; then
  echo "Status after binding:"
  reportStatus
fi
