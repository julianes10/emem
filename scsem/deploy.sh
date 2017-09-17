#!/bin/bash 
# Deploy and setup release into pi system
PI_USER=pi
PI_IPNAME=omegastar.ddns.net
PI_PORT=5555

echo "Here we go: $@"
usage(){
	echo "Usage: $0 (latest | tag <HASH> | local | remote  (latest | tag <HASH> | local))"
	exit 1
}
rt=55


DEPLOY_FOLDER=/home/pi/emem


echo "This script will deploy software in your pi"

aux="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Check that your current directory '$aux' is not deploy one $DEPLOY_FOLDER/scsem..."
if [ "$aux" == "$DEPLOY_FOLDER/scsem/" ]; then
  echo "ERROR: you must not deploy from deployed directory. Exiting"
  exit
fi

echo "Check the options and deploy folder '$DEPLOY_FOLDER' status..."
rm -rf $DEPLOY_FOLDER
if [ "$1" == "latest" ]; then
  echo "Clonning latest..."
  git clone git@github.com:julianes10/emem.git $DEPLOY_FOLDER
  rt=$?
elif [ "$1" == "tag" ]; then
  echo "Clonning latest..."
  git clone git@github.com:julianes10/emem.git $DEPLOY_FOLDER
  echo "Moving to tag $2..."
  pushd $DEPLOY_FOLDER
  if [ $? -eq 0 ];  then
    git reset --hard $2
    rt=$?
  else
    echo "Error... exiting"
    exit
  fi 
  popd
elif [ "$1" = "local" ]; then
  echo "WARNING this will use local version. Deployed version will be removed"
  echo "TODO uninstall legacy service, bbdd... "
  rm -rf $DEPLOY_FOLDER
  if [ $? -eq 0 ]; then
    echo "Copying local version to $DEPLOY_FOLDER... "
    cp -rf ../ $DEPLOY_FOLDER
    rt=$?
  else
    echo "Error deleting current deploy dir, exiting..."
  fi 
elif [ "$1" == "remote" ]; then
  if [ "$2" == "latest" ] || [ "$2" == "tag" ]; then
    echo "TODO"
  elif [ "$2" == "local" ]; then
    echo "Copying local files"
    scp -r -P $PI_PORT . pi@$PI_IPNAME:/home/pi/scsem.tmp
    ssh -p $PI_PORT pi@$PI_IPNAME "sudo systemctl stop scsem;sudo rm -rf $DEPLOY_FOLDER; mkdir -p $DEPLOY_FOLDER; mv /home/pi/scsem.tmp $DEPLOY_FOLDER/scsem;sudo systemctl start scsem;sudo systemctl status scsem"
  else
    echo "ERROR: no extra option selected for deployed remotely"
    usage
  fi
else
  echo "ERROR: no option selected for deployed"
  usage
fi

if [ $rt -eq 0 ]; then
  echo "Deployment is DONE. Now is recommended you run setup from $DEPLOY_FOLDER"
else
  echo "Deployment FAILED. Check above messages"
fi


