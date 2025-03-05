from typing import Dict, List, Tuple

import folium
import numpy as np
import pandas as pd
from pyproj import Geod
from scipy.sparse import csr_matrix


class Cities:
    """
    Attributes:
        geod (pyproj.Geod): provides ability to find distance between points (as well as other stuff).
        coordinates (Pandas Dataframe): the dataframe imported from the csv.
    """

    def __init__(self, coordinates: pd.DataFrame) -> None:
        self.geod = Geod(ellps="WGS84")
        self.coordinates = coordinates
        self.coordinates.index = coordinates.index.map(lambda x: x.strip().lower())
        self.list_of_cities = coordinates.index.unique().values
        self.city_to_index: Dict[str, int] = {
            city: i for i, city in enumerate(self.list_of_cities)
        }
        self.num_cities = len(self.list_of_cities)
        with open("./src/data/Adjacencies.txt", "r") as f:
            lines = f.readlines()

        adjacency_matrix = np.zeros((self.num_cities, self.num_cities), float)

        for adjacency in lines:
            start, end = adjacency.strip().lower().split()
            start_ll = self.coordinates.loc[start, "lat":"lon"]
            end_ll = self.coordinates.loc[end, "lat":"lon"]
            _, _, distance = self.geod.inv(
                start_ll["lon"], start_ll["lat"], end_ll["lon"], end_ll["lat"]
            )
            distance *= 0.001
            start_index, end_index = self.city_to_index[start], self.city_to_index[end]
            adjacency_matrix[start_index][end_index] = distance
            adjacency_matrix[end_index][start_index] = distance

        self.adjacency_matrix = csr_matrix(adjacency_matrix)

    def visualize_route(self, cities: List[int]):
        # lats = [self.coordinates.at[city, "lat"] for city in cities]
        # lons = [self.coordinates.at[city, "lon"] for city in cities]
        lats = [
            self.coordinates.at[self.list_of_cities[city], "lat"] for city in cities
        ]
        lons = [
            self.coordinates.at[self.list_of_cities[city], "lon"] for city in cities
        ]
        [center_lat, center_lon] = ((sum(lats) / len(lats)), (sum(lons) / len(lons)))
        my_map = folium.Map(location=[center_lat, center_lon], zoom_start=10)
        for i in range(len(cities)):
            lat, lon = lats[i], lons[i]
            (next_lat, next_lon) = (
                (lats[i + 1], lons[i + 1]) if i < (len(lats) - 1) else (None, None)
            )
            folium.Marker(
                [lat, lon],
                popup=self.list_of_cities[cities[i]].replace("_", " ").title(),
            ).add_to(my_map)
            if next_lat:
                folium.PolyLine([(lat, lon), (next_lat, next_lon)]).add_to(my_map)

        lat_range, lon_range = abs(max(lats) - min(lats)), abs(max(lons) - min(lons))
        sw = (min(lats) - lat_range / 10, min(lons) - lon_range / 10)
        ne = (max(lats) + lat_range / 10, max(lons) + lon_range / 10)
        my_map.fit_bounds([sw, ne])

        my_map.show_in_browser()

    def get_cities(self) -> Tuple[str, str]:
        start = (
            input("\nEnter starting city (or L/l to list cities): ")
            .strip()
            .lower()
            .replace(" ", "_")
        )
        while start == "l":
            print(self.list_of_cities)
            start = (
                input("\nEnter starting city (or L/l to list cities): ")
                .strip()
                .lower()
                .replace(" ", "_")
            )
        end = input("Enter ending city: ").strip().lower().replace(" ", "_")
        while end == "l":
            print(self.list_of_cities)
            end = input("\nEnter ending city: ").strip().lower().replace(" ", "_")
        while start not in self.list_of_cities or end not in self.list_of_cities:
            if start not in self.list_of_cities:
                start = input(f"{start} not found. Enter a new starting location: ")
                while start == "l":
                    print(self.list_of_cities)
                    start = input("Enter starting location: ")
            if end not in self.list_of_cities:
                end = input(f"{end} not found. Enter a new ending location: ")
                while end == "l":
                    print(self.list_of_cities)
                    end = input("Enter ending location: ")
        return start, end
