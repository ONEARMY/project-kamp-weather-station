"""
This is made for python >= 3.5 please make sure you have updated your python. And you are using python 3.

This script downloads a json from the ipma api and only stores the desired stations to the local json file.
The script will create a file if none is present and will add to an excisting file if one is present.
The data downloaded is hourly measuring data from the weatherstations in wanted_stations.txt.
The station has stationID (idEstacao) "6213019" and coordinates "-8.14, 40.3964".

The data in the Json should look like:
    "2021-04-06T13:00": {
        "6213019": {
            "humidade": 37.0,
            "idDireccVento": 6,
            "intensidadeVento": 3.6,
            "intensidadeVentoKM": 13.0,
            "precAcumulada": 0.0,
            "pressao": -99.0,
            "radiacao": -99.0,
            "temperatura": 21.3
        }
    },

The data in the Json should look like:
            "geometry": {
                "coordinates": [
                    -8.14,
                    40.3964
                ],
                "type": "Point"
            },
            "properties": {
                "descDirVento": "NE",
                "humidade": 36.0,
                "idDireccVento": 2,
                "idEstacao": 6213019,
                "intensidadeVento": 3.0,
                "intensidadeVentoKM": 10.8,
                "localEstacao": "Santa Comba D\u00e3o (CIM)",
                "precAcumulada": 0.0,
                "pressao": -99.0,
                "radiacao": -99.0,
                "temperatura": 21.2,
                "time": "2021-04-07T16:00:00"
            },
            "type": "Feature"

StationID's are retrieved via looking up the station name in https://api.ipma.pt/open-data/observation/meteorology/stations/obs-surface.geojson
"""

__author__ = "Joost Scheffer"
__version__ = "1.0"
__maintainer__ = "Sani7"
__status__ = "Production"

from datetime import datetime
import emojis
import io
import json
from load_stations import import_stations
import os
import requests
import sys
from typeguard import typechecked
from typing import Union, Set, Dict, List, Any, Optional


@typechecked
def list_unique(some_list: List[Any]) -> List[Any]:
    return [
        element
        for idx, element in enumerate(some_list)
        if element not in some_list[:idx]
    ]


@typechecked
class station_logger:
    def __init__(self):
        # this is still hardcoded an could use a better solution
        self.json_url: str = "https://api.ipma.pt/open-data/observation/meteorology/stations/observations.json"
        self.geoj_url: str = "https://api.ipma.pt/open-data/observation/meteorology/stations/obs-surface.geojson"
        # TODO import stations is not using csv
        # TODO import stations could load a station list from the github but that could be dangerous because of eval
        self.wanted_stations: Set[str] = import_stations()
        self.json_save_file: str = "../data/" + self.json_url.split("/")[-1]
        self.geoj_save_file: str = "../data/" + self.geoj_url.split("/")[-1]

    def new_request(self, option: int) -> None:
        """
        Request new data and add it to the local database.

        Args:
            option (int): 0 if json ; 1 if geojson
        """
        self.save_path = self.geoj_save_file if option else self.json_save_file
        get_function = self._get_geoj if option else self._get_json

        if not os.path.exists(self.save_path):
            self._save_to_json(get_function())
        else:
            if option:
                self._add_to_geoj_db(get_function())
            else:
                self._add_to_json_db(get_function())

    def _save_to_json(self, data: Dict[str, Any]) -> None:
        """
        Is used for both json and geojson.
        """
        with io.open(self.save_path, "w") as f:
            json.dump(data, f, sort_keys=True, indent=4)
        return

    def _add_to_json_db(
        self,
        data: Dict[str, Optional[Dict[Any, Any]]],
    ) -> None:
        with io.open(self.save_path, "r") as f:
            db = json.load(f)

        db.update(data)
        self._save_to_json(db)
        return

    def _add_to_geoj_db(
        self,
        data: Dict[str, Union[str, List[Any]]],
    ) -> None:
        with io.open(self.geoj_save_file, "r") as f:
            db = json.load(f)

        db["features"].extend(data["features"])
        db["features"] = list_unique(db["features"])

        self._save_to_json(db)
        return

    def _get_json(
        self,
    ) -> Dict[str, Union[dict, None]]:
        """
        Downloads and processes the json file downloaded form self.url.
        Processing is done by stripping all locations which are not in self.wanted_stations.

        Returns:
            Dict[str, Dict[str, Dict[str, Union[int, float]]]]: The stripped json file.
        """
        try:
            request: requests.Response = requests.get(self.json_url)
            # raise HTTPError if status is bad
            request.raise_for_status()

            data: dict = json.loads(request.text)

            # itterate_over dates
            for date in data:
                available_stations = set(data[date].keys())

                # take note of which stations are not available on the specified date
                not_available = self.wanted_stations - available_stations
                if not_available:
                    print(
                        emojis.encode(":x:"),
                        " these stations are not available:",
                        not_available,
                    )

                # compute which stations do not need to be stored
                stations_to_be_removed = available_stations - self.wanted_stations

                # remove unwanted stations
                # TODO I do not know if it best do have a tuple or a list here
                tuple(
                    map(
                        lambda station: data[date].pop(station),
                        stations_to_be_removed,
                    )
                )

            # TODO I do not know if list vs tuple here is faster or better
            # if all values are non or if there is no dict
            if (all(x.values() == None for x in list(data.values()))) or not data:
                print(
                    emojis.encode(":x:"),
                    f" {datetime.now()} weatherstation seems unavailable got statuscode: {request.status_code}",
                )
                exit(1)

            return data

        except requests.exceptions.HTTPError as err:
            print(
                emojis.encode(":x:"),
                f" {datetime.now()} could not request data, got errorcode: {request.status_code} and got HTTPError {err}",
            )
            exit(1)
        except requests.ConnectionError as err:
            print(
                emojis.encode(":x:"),
                f" {datetime.now()} could not request data, got errorcode: {request.status_code} and got ConnectionError {err}",
            )
            exit(1)

    def _get_geoj(self) -> Dict[str, Union[str, list]]:
        """
        Downloads and processes the geojson file downloaded form self.url.
        Processing is done by stripping all locations which are not in self.wanted_coordinates.

        Returns:
            Dict[str, Union[str, list]]: The stripped geojson file.
        """
        try:
            request = requests.get(self.geoj_url)
            request.raise_for_status()

            data = json.loads(request.text)

            # only keep the stations that are wanted
            filtered_data = [
                feature
                for feature in data["features"]
                if str(feature["properties"]["idEstacao"]) in self.wanted_stations
            ]
            data["features"] = filtered_data

            # set with all unique stationID's that were retrieved
            filtered_stations = set(
                str(feature["properties"]["idEstacao"]) for feature in data["features"]
            )

            # if there are coordinates wanted but they are not found in the geojson file this is printed
            not_available = self.wanted_stations - filtered_stations
            if not_available:
                if not_available == self.wanted_stations:
                    print(
                        emojis.encode(":x:"),
                        f" {datetime.now()} none of the stations are available:",
                        not_available,
                    )
                    exit(1)
                else:
                    print(
                        emojis.encode(":warning:"),
                        f" {datetime.now()} these stations are not available:",
                        not_available,
                    )

            return data

        except requests.exceptions.HTTPError as err:
            print(
                emojis.encode(":x:"),
                f" {datetime.now()} could not request data, got errorcode: {request.status_code} and got HTTPError {err}",
            )
            exit(1)
        except requests.ConnectionError as err:
            print(
                emojis.encode(":x:"),
                f" {datetime.now()} could not request data, got errorcode: {request.status_code} and got ConnectionError {err}",
            )
            exit(1)


if __name__ == "__main__":
    logger: station_logger = station_logger()
    option: int = int(sys.argv[1])
    logger.new_request(option)
    print("  ", datetime.now(), f"succes with option {option}")
