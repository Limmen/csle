#!/bin/bash

flaginfo=`cat fl_info.txt`
for fl in $flaginfo; do
  set -- "$fl"
  IFS=":"; declare -a Array=($*)
  flagpath=${Array[0]}
  flagname=${Array[1]}
  echo "${flagname}" > "${flagpath}/${flagname}.txt"
done

