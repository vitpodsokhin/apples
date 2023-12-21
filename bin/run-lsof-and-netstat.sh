#!/usr/bin/env bash

DIR="$HOME/data/net/connections.d/lsof_and_netstat.d"
FILE="$DIR/$(date +%F.%H-%M-%M).txt";
echo '#$: lsof -nP -i'
lsof -nP -i; echo;

echo 'netstat -lnva -p tcp'
netstat -lnva -p tcp

echo 'netstat -lnva -p udp'
netstat -lnva -p udp
#tee $FILE;
echo $FILE