#!/bin/bash 
# Deploy and setup release into pi system

echo "Here we go: $@"
usage(){
	echo "Usage: $0 latest | tag <HASH> | local"
	exit 1
}
rt=55
echo "This script will deploy software in your pi"

DEPLOY_FOLDER=/home/pi/emem
aux="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Check that your current directory '$aux' is not deploy one $DEPLOY_FOLDER/scsem..."
if [ "$aux" = "$DEPLOY_FOLDER/scsem/" ]; then
  echo "ERROR: you must not deploy from deployed directory. Exiting"
  exit
fi


echo "Check the options and deploy folder '$DEPLOY_FOLDER' status..."
echo "TODO if git exist there and option is not local, just pull..."
rm -rf $DEPLOY_FOLDER
if [ "$1" = "latest" ]; then
  echo "Clonning latest..."
  git clone git@github.com:julianes10/emem.git $DEPLOY_FOLDER
  rt=$?
elif [ "$1" = "tag" ]; then
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
  echo "Copying local version to $DEPLOY_FOLDER... "
  cp -rf ../ $DEPLOY_FOLDER
  rt=$?
else
  echo "ERROR: no option selected for deployed"
  usage
fi

if [ $rt -eq 0 ]; then
  echo "Deployment is DONE. Now is recommended you run setup from $DEPLOY_FOLDER"
else
  echo "Deployment FAILED. Check above messages"
fi


