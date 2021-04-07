#!/bin/sh
cd ~/WeatherStation/IPMADownloader/scripts/
python3 download_json.py
python3 download_geojson.py

# write date to file so that a malfunction can be located if needed
echo $(date) >> ../cron.txt