"""
This is made for python >= 3.8 please make sure you have updated your python.

This script downloads a json from the ipma api and only stores the desired stations to the local json file.
The script will create a file if none is present and will add to an excisting file if one is present.
The data downloaded is hourly measuring data from a weatherstation in Santa Comba Dão.
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
"""

__author__ = "Joost Scheffer"
__version__ = "1.0"
__maintainer__ = "Sani7"
__status__ = "Production"

import requests
import io
import json
import os
from datetime import datetime
from typing import Union, Set, Dict
from typeguard import typechecked


@typechecked
class station_logger:
    def __init__(self):
        # this is still hardcoded an could use a better solution
        self.url: str = "https://api.ipma.pt/open-data/observation/meteorology/stations/observations.json"
        self.wanted_stations: Set[str] = {"6213019"}
        self.save_file: str = "../data/data_filtered.json"

    def new_request(self) -> None:
        if not os.path.exists(self.save_file):
            self._save_to_json(self._get_json())
        else:
            self._add_to_db()

    def _save_to_json(
        self, data: Dict[str, Dict[str, Dict[str, Union[int, float]]]]
    ) -> None:
        with io.open(self.save_file, "w") as f:
            json.dump(data, f, sort_keys=True, indent=4)

    def _add_to_db(self) -> None:
        new_db = self._get_json()
        with io.open(self.save_file, "r") as f:
            db = json.loads(f.read())

        db.update(new_db)
        self._save_to_json(db)

    def _get_json(self) -> Dict[str, Dict[str, Dict[str, Union[int, float]]]]:
        """
        Downloads and processes the json file downloaded form self.url.
        Processing is done by stripping all locations which are not in self.wanted_stations.

        Returns:
            Dict[str, Dict[str, Dict[str, Union[int, float]]]]: The stripped json file.
        """
        try:
            # if request.status_code == 200:
            request = requests.get(self.url)
            request.raise_for_status()

            data = json.loads(request.text)

            # itterate_over dates
            for date in data:
                available_stations = set(data[date].keys())

                # take note of which stations are not available on the specified date
                not_available = self.wanted_stations - available_stations
                if not_available:
                    print(
                        "❌ these stations are not available:",
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

            return data

        except requests.exceptions.HTTPError as err:
            print(
                f"❌ {datetime.now()} could not request data, got errorcode: {request.status_code} and got HTTPError {err}"
            )
            exit(1)
        except requests.ConnectionError as err:
            print(
                f"❌ {datetime.now()} could not request data, got errorcode: {request.status_code} and got ConnectionError {err}"
            )
            exit(1)


if __name__ == "__main__":
    logger = station_logger()
    logger.new_request()