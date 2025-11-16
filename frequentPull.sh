#!/bin/bash

while true; do
    cd /home/pi/TAK_RFID_Reader
    git pull origin main -q
    sleep 1
done