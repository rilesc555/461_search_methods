from collections import defaultdict
from typing import Dict, List, Tuple

import branca.colormap as cm
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

    def visualize_route(self, paths=Dict[str, List[int]]):
        # lats = [self.coordinates.at[city, "lat"] for city in cities]
        # lons = [self.coordinates.at[city, "lon"] for city in cities]
        my_map = folium.Map(location=[37.5, -98.5], zoom_start=10)
        colors = ["blue", "blue", "green", "red", "orange", "black"]
        # segments format: (start, end): [algos]
        segments = defaultdict(list)
        lats, lons = [], []
        for algo, cities in paths.items():
            for i in range(len(cities)):
                if i < len(cities) - 1:
                    start, end = cities[i], cities[i + 1]
                    segment = (min(start, end), max(start, end))
                    segments[segment].append(algo)

        for segment, algos in segments.items():
            start, end = segment[0], segment[1]
            start_city = self.list_of_cities[start]
            end_city = self.list_of_cities[end]
            start_lat = self.coordinates.at[start_city, "lat"]
            lats.append(start_lat)
            start_lon = self.coordinates.at[start_city, "lon"]
            lons.append(start_lon)
            end_lat = self.coordinates.at[end_city, "lat"]
            lats.append(end_lat)
            end_lon = self.coordinates.at[end_city, "lon"]
            lons.append(end_lon)
            if len(algos) > 1:
                extra_points = self.geod.npts(
                    start_lon, start_lat, end_lon, end_lat, len(algos) - 1
                )
                for i in range(len(extra_points)):
                    coords = extra_points[i]
                    new_coords = (coords[1], coords[0])
                    extra_points[i] = new_coords
            colormap = cm.LinearColormap(colors[: len(algos) + 1])
            folium.ColorLine(
                [(start_lat, start_lon), *extra_points, (end_lat, end_lon)],
                colors=np.linspace(0.0, 1.0, len(algos) + 2),
                colormap=colormap,
                weight=20,
            ).add_to(my_map)

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
