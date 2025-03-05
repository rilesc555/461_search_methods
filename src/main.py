import time

import pandas as pd

from algos import algos
from cities import Cities


def main():
    print("Hello!")
    coordinates = pd.read_csv(
        "./src/data/coordinates.csv", index_col=0, names=["lat", "lon"]
    )
    cities = Cities(coordinates)
    while True:
        (start, end) = cities.get_cities()
        selected_algos = algos.get_algo()
        start, end = cities.city_to_index[start], cities.city_to_index[end]
        paths = {}
        for algo in selected_algos:
            start_time = time.time_ns()
            path, distance = algo(start, end, cities)
            end_time = time.time_ns()
            execution_time = int((end_time - start_time) / 1000)
            if path:
                paths[algo.__name__] = path
                print("\nPath: ")
                for index in path[:-1]:
                    print(
                        f"{cities.list_of_cities[index].replace('_', ' ').title()} -> ",
                        end="",
                    )
                print(f"{cities.list_of_cities[path[-1]].capitalize()}")
                print(f"Distance Covered: {distance:.2f} km")
            else:
                print("No path found")
            print(f"{algo.__name__} execution time: {execution_time} \u03bcs.")
        if paths:
            viz = (
                input(
                    "Would you like to see path(s) visualized in an interactive map? Y/n: "
                )
                .lower()
                .strip()
            )
            if viz == "y":
                cities.visualize_route(paths)


if __name__ == "__main__":
    main()
