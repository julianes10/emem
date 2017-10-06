#!/bin/bash 
# Thanks to easy to follow guide http://www.diegoacuna.me/how-to-run-a-script-as-a-service-in-raspberry-pi-raspbian-jessie/
source ./commonvars.sh

echo "This script will install in your pi a service scsem from $DEPLOY_FOLDER usign systemctl utility. No arguments required. Run it being root or with sudo"
if [ "$1" == "-h" -o "$1" == "--help" ]; then
  exit 0
fi
  
if [ ! -f /etc/emem/scsem.conf ]; then
  echo "Taking config file example as configuration file in /etc/emem/, please review it and restart the service"
  mkdir -p /etc/emem
  cp -rf etc/scsem.conf.example /etc/emem/scsem.conf
else
  echo "Keeping existing configuration file in /etc/emem/. Only updating example one"
  cp -rf etc/scsem.conf.example /etc/emem/
fi 
cp -rf scsem.service /lib/systemd/system/scsem.service
chmod 644 /lib/systemd/system/scsem.service
chmod +x ./scripts/scsem.py
systemctl daemon-reload
systemctl enable scsem.service
systemctl start scsem.service
systemctl status scsem.service

echo "Remember cheatsheet:"
echo "  Check status: sudo systemctl status scsem.service"
echo "  Start service: sudo systemctl start scsem.service"
echo "  Stop service: sudo systemctl stop scsem.service"
echo "  Check service's log: sudo journalctl -f -u scsem.service"

