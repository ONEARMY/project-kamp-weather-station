# What is IPMADownloader 
IPMADownloader can let community members store and log IPMA data on their own pi. With this data, local climate analysis can be performed which could possibly help Project Kamp decide on their power source and housing situation. The data is logged because there currently isn't another way to get old data from the weather stations nearby.

`scrips` directory contains python scripts that can be used to locally store weather data from a weather station in Santa Comba Dão (a bit south of Project Kamp).
The scripts are meant to run every 2 hours, for this `crontab` is used.

# Installation
## Update your pi
This may take a long time.
```
sudo apt update
```
```
sudo apt upgrade
```

## Setup the scripts
1.  Clone the repository
    ```
    cd ~
    ```
    ```
    git clone https://github.com/ONEARMY/project-kamp-weather-station.git
    ```
2.  Install packages
    ```
    cd ~/project-kamp-weather-station/IPMADownloader/
    ```
    ```
    pip3 install -r requirements.txt
    ```
    answer `Y` or `yes` if prompted
3.  Setup crontab
    Open crontab using
    `crontab -e`
    Then append to the bottom of the file the following
    ```cron
    0 */2 * * * ~/project-kamp-weather-station/IPMADownloader/scripts/get_ipma_api_data.sh
    ```
    This will run `get_ipma_api_data.sh` every 2 hours while the pi is powered.
