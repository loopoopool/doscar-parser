#!/bin/bash

current=`pwd`
printf "\nInstalling ploos...\n\nI need your password to copy some file in /usr/share"

sed -n "s/mydir/$current/p" ploos.desktop > ploos
sudo cp ploos /usr/share/applications/ploos.desktop
sudo chmod 644 /usr/share/applications/ploos.desktop
rm ploos
