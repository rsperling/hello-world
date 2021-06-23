#!/usr/bin/sh -x
# stop and delete all containers
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
# delete all images
docker rmi -f $(docker images -q)

## cleanup user data
cd $HOME/devops-workshop/data/userdata
sudo rm -rf user*

## cleanup app data
cd $HOME/devops-workshop/data/appdata
sudo rm -rf gitea
sudo rm -rf jenkins

