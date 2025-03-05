import time

import pandas as pd

import algos
from cities import Cities


def main():
    print("Hello!")
    coordinates = pd.read_csv(
        "./src/coordinates.csv", index_col=0, names=["lat", "lon"]
    )
    cities = Cities(coordinates)
    while True:
        (start, end) = cities.get_cities()
        algo = algos.get_algo()
        start, end = cities.city_to_index[start], cities.city_to_index[end]
        start_time = time.time_ns()
        path, distance = algo(start, end, cities)
        end_time = time.time_ns()
        execution_time = int((end_time - start_time) / 1000)
        print(
            f"Execution time to search for path from {start} to {end} using {algo.__name__}: {execution_time} \u03bcs."
        )
        if path:
            print("\nPath: ")
            for index in path[:-1]:
                print(
                    f"{cities.list_of_cities[index].replace('_', ' ').title()} -> ",
                    end="",
                )
            print(f"{cities.list_of_cities[path[-1]].capitalize()}")
            print(f"\nDistance Covered: {distance:.2f} km\n")
            viz = (
                input(
                    "Would you like to see this path visualized in an interactive map? Y/n: "
                )
                .lower()
                .strip()
            )
            if viz == "y":
                cities.visualize_route(path)
        else:
            print("No path found")


if __name__ == "__main__":
    main()
