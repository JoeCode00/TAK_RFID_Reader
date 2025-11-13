#!/bin/bash

while true; do
    cd ~/TAK_RFID_Reader
    git pull origin main -q
    sleep 1
done