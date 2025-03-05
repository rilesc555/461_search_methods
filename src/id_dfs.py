from collections import deque
from typing import List, Optional, Tuple

import numpy as np

from cities import Cities


def idDfs(
    start_city: int, end_city: int, cities: Cities
) -> Tuple[Optional[List[int]], float]:
    """
    Perform iterative deepening depth-first search to find a path from start_city to end_city.

    Args:
        start_city: Index of the starting city
        end_city: Index of the destination city
        matrix: Sparse adjacency matrix where matrix[i, j] is the cost to go from i to j

    Returns:
        A tuple containing:
        - A list of city indices representing the path from start to end (or None if no path)
        - The total cost of the path (or float('inf') if no path)
    """
    # Get the number of nodes in the graph
    n = cities.adjacency_matrix.shape[0]

    # Define a depth-limited search function
    def depth_limited_search(
        depth_limit: int,
    ) -> Tuple[Optional[List[int]], float]:
        # Stack contains: (node, path_so_far, cost_so_far, depth)
        stack = deque([(start_city, [start_city], 0.0, 0)])
        visited = set()

        while stack:
            current, path, cost, depth = stack.pop()

            # If we've reached the destination, return the path and cost
            if current == end_city:
                return path, cost

            # If we've reached the depth limit, skip expanding this node
            if depth >= depth_limit:
                continue

            # Mark as visited for this iteration
            visited.add(current)

            # Get all neighbors of the current city
            row = cities.adjacency_matrix[current].toarray().flatten()
            neighbors = np.nonzero(row)[0]

            # Add neighbors to stack in reverse order (to maintain DFS order)
            for neighbor in reversed(list(neighbors)):
                if neighbor not in visited:
                    edge_cost = cities.adjacency_matrix[current, neighbor]
                    new_path = path + [neighbor]
                    new_cost = cost + edge_cost
                    stack.append((neighbor, new_path, new_cost, depth + 1))

        # If we get here, no path was found within the depth limit
        return None, float("inf")

    # Iterative deepening - try increasing depth limits
    max_depth = n  # Maximum possible depth is the number of nodes

    for depth_limit in range(max_depth):
        path, cost = depth_limited_search(depth_limit)
        if path is not None:
            return path, cost

    # If no path is found after trying all possible depths
    return None, float("inf")
