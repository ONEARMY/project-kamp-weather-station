"""
This is made for python >= 3.8 please make sure you have updated your python.

This script downloads a geojson from the ipma api and only stores the desired stations to the local geojson file.
The script will create a file if none is present and will add to an excisting file if one is present.
The data downloaded is hourly measuring data from a weatherstation in Santa Comba Dão.
The station has stationID (idEstacao) "6213019" and 'coordinates' "-8.14, 40.3964".
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
from typing import Union, Dict, List, Any
from typeguard import typechecked


@typechecked
def list_unique(some_list: List[Any]) -> List[Any]:
    return [
        element
        for idx, element in enumerate(some_list)
        if element not in some_list[:idx]
    ]


@typechecked
def list_difference(li1: List[Any], li2: List[Any]) -> List[Any]:
    # from https://www.geeksforgeeks.org/python-difference-two-lists/
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif


@typechecked
class station_logger:
    def __init__(self):
        # TODO this is still hardcoded and could use a better solution
        self.url: str = "https://api.ipma.pt/open-data/observation/meteorology/stations/obs-surface.geojson"
        self.wanted_coordinates: List[List[float]] = [[-8.14, 40.3964]]
        self.save_file: str = "../data/geo_data_filtered.geojson"

    def new_request(self) -> None:
        if not os.path.exists(self.save_file):
            self._save_to_json(self._get_json())
        else:
            self._add_to_db()

    def _save_to_json(self, data) -> None:
        with io.open(self.save_file, "w") as f:
            json.dump(data, f, sort_keys=True, indent=4)

    def _add_to_db(self) -> None:
        new_db = self._get_json()
        with io.open(self.save_file, "r") as f:
            db = json.loads(f.read())

        # only add data that was not measured before
        actual_new_data = [
            feature for feature in new_db["features"] if feature not in db["features"]
        ]
        db["features"].extend(actual_new_data)

        self._save_to_json(db)

    def _get_json(
        self,
    ) -> Dict[str, Union[str, list]]:
        """
        Downloads and processes the geojson file downloaded form self.url.
        Processing is done by stripping all locations which are not in self.wanted_coordinates.

        Returns:
            Dict[str, Union[str, list]]: The stripped geojson file.
        """
        try:
            request = requests.get(self.url)
            request.raise_for_status()

            data = json.loads(request.text)

            # only keep the stations that are wanted
            filtered_data = [
                feature
                for feature in data["features"]
                if feature["geometry"]["coordinates"] in self.wanted_coordinates
            ]
            data["features"] = filtered_data

            # list with all unique coordinates that were retrieved
            filtered_coordinates = list_unique(
                [feature["geometry"]["coordinates"] for feature in data["features"]]
            )

            # if there are coordinates wanted but they are not found in the geojson file this is printed
            not_available = list_difference(filtered_coordinates, self.wanted_coordinates)
            if not_available:
                print(
                    "❌ these stations are not available:",
                    not_available,
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
    print(datetime.now(), "succes")
