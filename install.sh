#!/bin/bash

current=`pwd`
sed -i "s|mydir|${current}|" ploos-cli
printf "\nInstalling ploos...\n\nI need your password to copy some file in /usr/share\n\n"

sudo cp -p ploos-cli /usr/local/bin/.

cat $current/ploos.desktop | sed "s|mydir|${current}|" > $current/tmp_ploos
sudo mv $current/tmp_ploos /usr/share/applications/ploos.desktop
sudo chmod 644 /usr/share/applications/ploos.desktop
