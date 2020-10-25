#!/bin/bash

flaginfo=`cat fl_info.txt`
set -- "$flaginfo"
IFS=":"; declare -a Array=($*)
flagpath=${Array[0]}
flagname=${Array[1]}
echo "${flagname}" > "${flagpath}/${flagname}.txt"
