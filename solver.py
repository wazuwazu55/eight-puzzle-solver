"""Breadth-first and heuristic search examples for the 8-puzzle."""

from collections import deque
from copy import deepcopy


# The empty square is represented by 0.
GOAL = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0],
]

START = [
    [3, 6, 8],
    [1, 0, 4],
    [7, 2, 5],
]


class PriorityQueue:
    """A binary heap ordered by a caller-supplied comparison function.

    ``compare(a, b)`` should return True when ``a`` belongs before ``b``.
    """

    def __init__(self, compare):
        self.compare = compare
        self.heap = []

    def add(self, value):
        """Add a value and restore the heap ordering."""
        self.heap.append(value)
        self._bubble_up()

    def poll(self):
        """Remove and return the value at the top of the heap."""
        return self._extract()

    def empty(self):
        """Return True when the queue contains no values."""
        return len(self.heap) == 0

    def _extract(self):
        """Remove the root value, then move the last value into its place."""
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        value = self.heap.pop()
        if self.heap:
            self._bubble_down()
        return value

    def _bubble_up(self):
        """Move the newest value toward the root while it has higher priority."""
        current_index = len(self.heap) - 1

        while current_index > 0:
            parent_index = (current_index - 1) // 2
            if self.compare(self.heap[parent_index], self.heap[current_index]):
                break

            self.heap[current_index], self.heap[parent_index] = (
                self.heap[parent_index],
                self.heap[current_index],
            )
            current_index = parent_index

    def _bubble_down(self):
        """Move the root value down until the heap ordering is restored."""
        current_index = 0

        while True:
            left_child = (2 * current_index) + 1
            right_child = (2 * current_index) + 2
            if left_child >= len(self.heap):
                break

            # Choose the child that should appear first according to compare().
            child_index = left_child
            if right_child < len(self.heap) and not self.compare(
                self.heap[left_child], self.heap[right_child]
            ):
                child_index = right_child

            if self.compare(self.heap[current_index], self.heap[child_index]):
                break

            self.heap[current_index], self.heap[child_index] = (
                self.heap[child_index],
                self.heap[current_index],
            )
            current_index = child_index


def make_neighbors(board):
    """Return boards reachable by moving one tile into the empty square."""
    neighbors = []
    blank_row = 0
    blank_col = 0

    # Locate the empty square.
    for row_index in range(3):
        for col_index in range(3):
            if board[row_index][col_index] == 0:
                blank_row = row_index
                blank_col = col_index

    def add_neighbor(new_row, new_col):
        """Copy the board and swap a neighboring tile with the empty square."""
        neighbor = deepcopy(board)
        neighbor[new_row][new_col], neighbor[blank_row][blank_col] = (
            neighbor[blank_row][blank_col],
            neighbor[new_row][new_col],
        )
        neighbors.append(neighbor)

    # Add each legal move: up, down, left, and right.
    if blank_row >= 1:
        add_neighbor(blank_row - 1, blank_col)
    if blank_row <= 1:
        add_neighbor(blank_row + 1, blank_col)
    if blank_col >= 1:
        add_neighbor(blank_row, blank_col - 1)
    if blank_col <= 1:
        add_neighbor(blank_row, blank_col + 1)

    return neighbors


def stringify(board):
    """Create a stable string key for a board state."""
    return "-".join(str(row) for row in board)

def solve_via_a_star(start):
    """Print boards explored using a score based on matching goal positions.

    This keeps the original heuristic-only priority behavior. Since the search
    does not add the path length, it behaves like greedy best-first search rather
    than standard A*.
    """

    def heuristic(board):
        # Negative matches make the min-heap prefer boards closer to the goal.
        score = 0
        for row_index in range(3):
            for col_index in range(3):
                if board[row_index][col_index] == GOAL[row_index][col_index]:
                    score -= 1
        return score

    priority_queue = PriorityQueue(lambda first, second: first[1] < second[1])
    priority_queue.add((start, heuristic(start)))
    visited = set()

    while not priority_queue.empty():
        current, _score = priority_queue.poll()
        state_key = stringify(current)
        if state_key in visited:
            continue

        visited.add(state_key)
        print(current)

        if current == GOAL:
            print("Goal Found")
            return

        for neighbor in make_neighbors(current):
            neighbor_key = stringify(neighbor)
            if neighbor_key not in visited:
                priority_queue.add((neighbor, heuristic(neighbor)))


if __name__ == "__main__":
    solve_via_a_star(START)
