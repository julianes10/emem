#!/bin/sh

reportStatus ()
{
  sudo ls /dev/rfc*
#  sudo tree /var/lib/bluetooth/*/$1
}


echo "Status before binding:"
reportStatus

sudo rfcomm release hci0 $1
echo "Status after releasing:"
reportStatus


sudo rfcomm bind hci0 98:D3:32:20:FB:90 1
echo "Status after binding:"
reportStatus
