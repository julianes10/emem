#!/bin/bash 
# Thanks to easy to follow guide http://www.diegoacuna.me/how-to-run-a-script-as-a-service-in-raspberry-pi-raspbian-jessie/

DEPLOY_FOLDER=/home/pi/emem

echo "This script will install in your pi a service scsem from $DEPLOY_FOLDER usign systemctl utility"
sudo cp -rf scsem.service /lib/systemd/system/scsem.service
sudo chmod 644 /lib/systemd/system/scsem.service
chmod +x ./scripts/scsem.py
sudo systemctl daemon-reload
sudo systemctl enable scsem.service
sudo systemctl start scsem.service
sudo systemctl status scsem.service

echo "Remember cheatsheet:"
echo "  Check status: sudo systemctl status scsem.service"
echo "  Start service: sudo systemctl start scsem.service"
echo "  Stop service: sudo systemctl stop scsem.service"
echo "  Check service's log: sudo journalctl -f -u scsem.service"

