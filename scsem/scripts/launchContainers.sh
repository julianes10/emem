#!/bin/bash 
#args: $1 verbose
echo "Here we go $@"
reportStatus ()
{
  docker ps
}

if [ "$1" = "verbose" ]; then
  echo "Status before launching:"
  reportStatus
fi

pi=""
uname -a | grep arm
res=$?

if [ $res = 0 ]; then
  pi="pi"
  if [ "$1" = "verbose" ]; then
    echo "Running on ARM - Assuming pi"
  fi
fi
    

docker kill emem_grafana emem_influxdb 
sleep 2
docker kill --signal 9 emem_grafana emem_influxdb

if [ "$1" = "verbose" ]; then
  echo "Status after releasing:"
  reportStatus
fi
MY_PATH="`dirname \"$0\"`"
pushd $MY_PATH/../containers 
./docker_influxdb $pi &
sleep 2
./docker_grafana $pi &
popd
if [ "$1" = "verbose" ]; then
  echo "Status after binding:"
  reportStatus
fi
exit 0
