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
  if [ "$1" = "verbose" ]; then
    echo "Running on ARM - Assuming pi"
  fi
fi
    

docker kill emem_influxdb 
docker kill emem_grafana

if [ "$1" = "verbose" ]; then
  echo "Status after releasing:"
  reportStatus
fi
pushd ../containers/ 
./docker_influxdb $pi &
sleep 2
./docker_grafana $pi &
popd
if [ "$1" = "verbose" ]; then
  echo "Status after binding:"
  reportStatus
fi
