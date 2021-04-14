# what is IPMADownloader 
IPMADownloader can let's community members store and log IPMA data on their own pi. With this data local climate analysis can be performed which could possibly help Project Kamp decide on their powersource and housing situation. The data is logged because there currently isn't another way to get old data from the weather stations nearby.

`scrips` directory contains python scripts which can used to locally store weather data from a weatherstation in Santa Comba Dão (a bit south of Project Kamp).
The scripts are meant to run every 2 hours, for this `crontab` is used.

# installation
## update your pi
this may take a long time
```sudo apt update```
```sudo apt upgrade```

## setup the scripts
1.  clone the repository
    ```
    cd ~
    ```
    ```
    git clone https://github.com/ONEARMY/project-kamp-weather-station.git
    ```
2.  install packages
    ```
    cd ~/project-kamp-weather-station/IPMADownloader/
    ```
    ```
    pip3 install -r requirements.txt
    ```
    answer `Y` or `yes` if prompted
3.  setup crontab
    open crontab using
    `crontab -e`
    then append to the bottom of the file the following
    ```cron
    0 */2 * * * ~/project-kamp-weather-station/IPMADownloader/scripts/get_ipma_api_data.sh
    ```
    this will run `get_ipma_api_data.sh` every 2 hours while the pi is powered.
