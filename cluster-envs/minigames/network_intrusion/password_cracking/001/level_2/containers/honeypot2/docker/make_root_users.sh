#!/bin/bash

# -r: create system account, -d: path to home dir, -s login shell of new acc, -g primary group,
# -G supplementary groups, name, -p specify encrypted password

userslist=`cat root_users.txt`
for u in $userslist; do
  set -- "$u"
  IFS=":"; declare -a Array=($*)
  username=${Array[0]}
  pw=${Array[1]}
  useradd -rm -d /home/${username} -s /bin/bash -g root -G sudo -p "$(openssl passwd -1 ${pw})" ${username}
done
