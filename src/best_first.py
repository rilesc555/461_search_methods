import heapq
from typing import List, Optional, Tuple

import numpy as np

from cities import Cities


def bestFirst(
    start_city: int,
    end_city: int,
    cities: Cities,
) -> Tuple[Optional[List[int]], float]:
    """
    Perform greedy best-first search to find a path from start_city to end_city.

    Args:
        start_city: Index of the starting city
        end_city: Index of the destination city
        matrix: Sparse adjacency matrix where matrix[i, j] is the cost to go from i to j
        heuristic: A function that estimates the cost from a city to the end city.
                   If None, uses a simple default heuristic.

    Returns:
        A tuple containing:
        - A list of city indices representing the path from start to end (or None if no path)
        - The total cost of the path (or float('inf') if no path)
    """

    def heuristic(start_city: int, end_city: int) -> float:
        start_lat = cities.coordinates.at[cities.list_of_cities[start_city], "lat"]
        start_lon = cities.coordinates.at[cities.list_of_cities[start_city], "lon"]
        end_lat = cities.coordinates.at[cities.list_of_cities[end_city], "lat"]
        end_lon = cities.coordinates.at[cities.list_of_cities[end_city], "lon"]

        _, _, distance = cities.geod.inv(start_lon, start_lat, end_lon, end_lat)
        return float(distance)

    # Priority queue for greedy best-first search
    # Format: (heuristic_value, current_city, path_so_far, cost_so_far)
    priority_queue = [(heuristic(start_city, end_city), start_city, [start_city], 0.0)]

    # Keep track of visited cities to avoid cycles
    visited = set([start_city])

    while priority_queue:
        # Get the city with the lowest heuristic value
        _, current, path, cost = heapq.heappop(priority_queue)
        print(f"Checking city: {cities.list_of_cities[current]}")
        # If we've reached the destination, return the path and cost
        if current == end_city:
            return path, cost

        # Get all neighbors of the current city
        row = cities.adjacency_matrix[current].toarray().flatten()
        neighbors = np.nonzero(row)[0]
        print("Neighbors:")
        for city in neighbors:
            print(
                f"{cities.list_of_cities[city]} is {heuristic(city, end_city) / 1000:.2f} km away from {cities.list_of_cities[end_city]}"
            )

        for neighbor in neighbors:
            if neighbor not in visited:
                # Mark as visited
                visited.add(neighbor)

                # Calculate new cost
                edge_cost = cities.adjacency_matrix[current, neighbor]
                new_cost = cost + edge_cost
                new_path = path + [neighbor]

                # Add to priority queue with heuristic value
                h_value = heuristic(neighbor, end_city)
                heapq.heappush(priority_queue, (h_value, neighbor, new_path, new_cost))

    # If no path is found
    return None, float("inf")
