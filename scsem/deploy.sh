#!/bin/bash 
# Deploy and setup release into pi system

echo "Here we go: $@"
usage(){
	echo "Usage: $0 latest | tag <HASH> | local"
	exit 1
}

DEPLOY_FOLDER=/home/pi/emem
aux=dirname $0

echo "This script will deploy software in your pi"

echo "Check that your current directory '$aux' is not deploy one..."
if [ "$aux" = "$DEPLOY_FOLDER/scsem/"]
  echo "ERROR: you must not deploy from deployed directory. Exiting"
  exit
fi


echo "Check the options and deploy folder '$DEPLOY_FOLDER' status..."
if [ '$1' = "latest" ]
  echo "Clonning latest..."
  git clone git@github.com:julianes10/emem.git 
elif [ '$1' = "tag" ]
  echo "Clonning latest..."
  git clone git@github.com:julianes10/emem.git 
  echo "Moving to tag $2..."
  pushd $DEPLOY_FOLDER
  git checkout $2
  popd
elif [ '$1' = "local" ]
  echo "WARNING this will use local version. Deployed version will be removed"
  echo "TODO uninstall legacy service, bbdd... "
  rm -rf $DEPLOY_FOLDER
  echo "Download from git hub latest version... "
  cp -rf ../ $DEPLOY_FOLDER
else
  echo "ERROR: no option selected for deployed"
  usage
fi
echo "Deployment is DONE. Now is recommended you run setup from $DEPLOY_FOLDER"



