from enum import Enum
from typing import Callable, List

from algos.a_star import a_star
from algos.best_first import bestFirst
from algos.bfs import bfs
from algos.dfs import dfs
from algos.id_dfs import idDfs


class Algos(Enum):
    BFS = 1
    DFS = 2
    ID_DFS = 3
    A_STAR = 4
    BEST_FIRST = 5
    ALL_ALGOS = 6


def get_algo_input():
    print("Which algorithm would you like to use?")
    prompt = """[1] Breadth-First Search (BFS)\n[2] Depth-First Search (DFS)\n[3] Iterative Deepening DFS\n[4] A*\n[5] Best-First Search\n"""

    while True:
        answer = input(prompt)

        try:
            algo = int(answer)

            try:
                selected_algo = Algos(algo)
                return selected_algo
            except ValueError:
                print(f"Error: {selected_algo} is not a valid algorithm option")

        except ValueError:
            print(f"Error: {answer} is not a valid number. Please select a number 1-5")


def get_algo() -> List[Callable]:
    algo = get_algo_input()
    algorithm_map = {
        Algos.BFS: [bfs],
        Algos.DFS: [dfs],
        Algos.ID_DFS: [idDfs],
        Algos.A_STAR: [a_star],
        Algos.BEST_FIRST: [bestFirst],
        Algos.ALL_ALGOS: [bfs, dfs, idDfs, a_star, bestFirst],
    }

    return algorithm_map[algo]
