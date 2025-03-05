from typing import List, Optional, Tuple

import numpy as np

from cities import Cities


def dfs(
    start_city: int, end_city: int, cities: Cities
) -> Tuple[Optional[List[int]], float]:
    """
    Perform depth-first search to find a path from start_city to end_city.

    Args:
        start_city: Index of the starting city
        end_city: Index of the destination city
        cities: class containing cities, their indexes, adjacency matrix, and some other goodies

    Returns:
        A tuple containing:
        - A list of city indices representing the path from start to end (or None if no path)
        - The total cost of the path (or float('inf') if no path)
    """
    # Initialize visited set and path stack
    visited = set()

    def dfs_recursive(
        current: int, path: List[int], cost: float
    ) -> Tuple[Optional[List[int]], float]:
        # Mark current city as visited
        visited.add(current)
        path.append(current)

        # If we've reached the destination, return the path and cost
        if current == end_city:
            return path.copy(), cost

        # Get all neighbors of the current city
        row = cities.adjacency_matrix[current].toarray().flatten()
        neighbors = np.nonzero(row)[0]

        for neighbor in neighbors:
            if neighbor not in visited:
                # Calculate new cost
                edge_cost = cities.adjacency_matrix[current, neighbor]
                new_cost = cost + edge_cost

                # Recursively explore this neighbor
                result_path, result_cost = dfs_recursive(neighbor, path, new_cost)

                # If a path was found, return it
                if result_path is not None:
                    return result_path, result_cost

        # If we get here, this path didn't work - backtrack
        path.pop()
        return None, float("inf")

    # Start the recursive DFS
    path, cost = dfs_recursive(start_city, [], 0.0)
    return path, cost
