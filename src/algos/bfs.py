from collections import deque
from typing import List, Optional, Tuple

from main import Cities


def bfs(
    start_city: int, end_city: int, cities: Cities
) -> Tuple[Optional[List[int]], float]:
    if start_city == end_city:
        return [start_city], 0.0

    visited = set([start_city])
    queue = deque([start_city])
    parent = dict()
    parent[start_city] = None

    while queue:
        current_city = queue.popleft()
        row_start = cities.adjacency_matrix.indptr[current_city]
        row_end = cities.adjacency_matrix.indptr[current_city + 1]

        for idx in range(row_start, row_end):
            neighbor = cities.adjacency_matrix.indices[idx]

            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current_city

                if neighbor == end_city:
                    # reconstruct path
                    path = []
                    distance = 0.0
                    current = neighbor
                    while current is not None:
                        path.append(current)
                        current_parent = parent[current]
                        # get the distance between current and it's parent
                        if current_parent is not None:
                            distance += cities.adjacency_matrix[current, current_parent]
                        current = current_parent
                    path.reverse()

                    return path, distance

                queue.append(neighbor)

    return None, float("inf")
