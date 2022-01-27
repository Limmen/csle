#!/bin/sh

nick="sdgacsletest"
config=/tmp/irclog

[ -n "$1" ] && server=$1
config="${config}_${channel}"

echo "NICK $nick" > $config
echo "USER $nick +i * :$0" >> $config

trap "rm -f $config;exit 0" INT TERM EXIT

tail -f $config | nc $server 6667 | while read MESSAGE
do
  case "$MESSAGE" in
    PING*) echo "PONG${MESSAGE#PING}" >> $config;;
    *QUIT*) ;;
    *PART*) ;;
    *JOIN*) ;;
    *NICK*) ;;
    *PRIVMSG*) echo "${MESSAGE}" | sed -nr "s/^:([^!]+).*PRIVMSG[^:]+:(.*)/[$(date '+%R')] \1> \2/p";;
    *) echo "${MESSAGE}";;
  esac
done