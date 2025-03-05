import heapq
from typing import Dict, List, Optional, Tuple

import numpy as np

from cities import Cities


def a_star(
    start_city: int, end_city: int, cities: Cities
) -> Tuple[Optional[List[int]], float]:
    def heuristic(start_city: int, end_city: int) -> float:
        start_lat = cities.coordinates.at[cities.list_of_cities[start_city], "lat"]
        start_lon = cities.coordinates.at[cities.list_of_cities[start_city], "lon"]
        end_lat = cities.coordinates.at[cities.list_of_cities[end_city], "lat"]
        end_lon = cities.coordinates.at[cities.list_of_cities[end_city], "lon"]

        _, _, distance = cities.geod.inv(start_lon, start_lat, end_lon, end_lat)
        return float(distance) / 1000

    # Priority queue for A* search
    # Format: (f_score, current_city, path_so_far, g_score)
    # where f_score = g_score + heuristic(current, end)
    # and g_score is the cost from start to current
    open_set = [(heuristic(start_city, end_city), start_city, [start_city], 0.0)]

    # Keep track of the best known g_score for each city
    g_scores: Dict[int, float] = {start_city: 0.0}

    # Keep track of visited cities for path reconstruction
    optimal_parent = {}

    while open_set:
        # Get the city with the lowest f_score
        _, current, path, g_score = heapq.heappop(open_set)

        # If we've reached the destination, return the path and cost
        if current == end_city:
            return path, g_score

        # Get all neighbors of the current city
        row = cities.adjacency_matrix[current].toarray().flatten()
        neighbors = np.nonzero(row)[0]

        for neighbor in neighbors:
            # Calculate tentative g_score
            edge_cost = cities.adjacency_matrix[current, neighbor]
            tentative_g_score = g_score + edge_cost

            # If we found a better path to this neighbor
            if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                # Update our records
                optimal_parent[neighbor] = current
                g_scores[neighbor] = tentative_g_score

                # Calculate f_score = g_score + heuristic
                f_score = tentative_g_score + heuristic(neighbor, end_city)

                # Create the new path
                new_path = path + [neighbor]

                # Add to priority queue
                heapq.heappush(
                    open_set, (f_score, neighbor, new_path, tentative_g_score)
                )

    # If no path is found
    return None, float("inf")
