# Eight Puzzle Solver

A small Python project for exploring search strategies on the 3×3 sliding-tile puzzle. The board uses `0` for the empty space, and the goal is:

```text
1 2 3
4 5 6
7 8 0
```

## Run

Requires Python 3. Run the script from this directory:

```bash
python solver.py
```

The starting board and search function are selected at the bottom of `solver.py`. The current script prints boards as it explores them.

`solve_via_bfs` is also available. The function named `solve_via_a_star` currently orders boards by its heuristic score alone, without adding the path length, so it behaves like greedy best-first search rather than standard A*.
