#!/bin/bash

nohup python3 ./server.py > /dev/null &
cd ./logs/
nohup python3 -m http.server 9001 > /dev/null &
