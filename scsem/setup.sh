# Thanks to easy to follow guide http://www.diegoacuna.me/how-to-run-a-script-as-a-service-in-raspberry-pi-raspbian-jessie/
echo "This script will install as a service scsem usign systemctl utility"
echo "TODO clean up and database restore if needed"
echo "TODO check dev and deploy folders is everything seems to be ok.e.g download from github master or tag..."
echo "TODO force this intallation from remote dev laptop."
echo "Its TODO check dev and deploy folders is everything seems to be ok."
sudo cp -rf scsem.service /lib/systemd/system/scsem.service
sudo chmod 644 /lib/systemd/system/scsem.service
chmod +x /home/pi/scsem_world.py
sudo systemctl daemon-reload
sudo systemctl enable scsem.service
sudo systemctl start scsem.service
sudo systemctl status scsem.service

echo "Remember cheatsheet:"
echo "  Check status: sudo systemctl status scsem.service"
echo "  Start service: sudo systemctl start scsem.service"
echo "  Stop service: sudo systemctl stop scsem.service"
echo "  Check service's log: sudo journalctl -f -u scsem.service"

