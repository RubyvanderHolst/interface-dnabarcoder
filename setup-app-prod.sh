#!/bin/bash

APP_DIR=./dnabarcoder

if [ -d "$APP_DIR" ]
then
  echo "Application is already downloaded in current directory ($APP_DIR)."
  echo "Would you like to replace this with the newest version? "
  echo "(Files which are not stored on github (such as .env and db.sqlite3) will be removed)"
  select yn in "Yes" "No"; do
    case $yn in
      Yes )
        rm -rf $APP_DIR;
        git clone https://github.com/vuthuyduong/dnabarcoder.git;
        git clone https://github.com/RubyvanderHolst/interface-dnabarcoder.git dnabarcoder/interface-dnabarcoder;
        break;;
      No )
        echo "Current local version not replaced";
        break;;
    esac
  done
else
  git clone https://github.com/vuthuyduong/dnabarcoder.git
  git clone https://github.com/RubyvanderHolst/interface-dnabarcoder.git dnabarcoder/interface-dnabarcoder
fi

if [[ -f dnabarcoder/interface-dnabarcoder/.env-prod ]]
then
  echo "dnabarcoder/interface-dnabarcoder/.env-prod exists"
else
  echo "dnabarcoder/interface-dnabarcoder/.env-prod does not exist"
  echo "Would you like to add an .env-prod file and run the application? "
  select yn in "Yes" "No"; do
    case $yn in
      Yes )
        echo "What is the path to .env-prod? ";
        read env_path;
        if [ -f "$env_path" ]
        then
          cp "${env_path}" dnabarcoder/interface-dnabarcoder/;
        else
          echo "File ${env_path} does not exist"
          exit
        fi
        break;;
      No )
        exit;;
    esac
  done
fi

sudo docker-compose -f dnabarcoder/interface-dnabarcoder/production/docker-compose-prod.yml up

