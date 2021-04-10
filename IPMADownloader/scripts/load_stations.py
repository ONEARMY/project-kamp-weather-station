import io
from typing import Set
from typeguard import typechecked


@typechecked
# TODO errorhandling
def import_stations() -> Set[str]:
    """
    Return a set of the wanted weatherstations to log data from acoarding to "wanted_stations.txt".
    Assumes that the working directory is scripts.

    Returns:
        Set[str]: set containing all the stations which are found in "wanted_stations.txt"
    """
    with io.open("./wanted_stations.txt") as f:
        return eval(f.read())