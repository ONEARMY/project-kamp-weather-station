#!/bin/sh
cd ~/WeatherStation/IPMADownloader/scripts/

# if there is no folder for the data yet make one
if [ ! -d ~/WeatherStation/IPMADownloader/data ]; then
  mkdir -p ~/WeatherStation/IPMADownloader/data;
fi

python3 download_json.py >> ../json_log.txt
python3 download_geojson.py >> ../geojson_log.txt

# write date to file so that a malfunction can be located if needed
echo $(date) >> ../cron.txt
