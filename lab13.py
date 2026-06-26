from collections import deque

grid = [
    ['S', '.', '.', 'X', '.'],
    ['.', 'X', '.', 'X', '.'],
    ['.', 'X', '.', '.', '.'],
    ['.', '.', 'X', 'X', '.'],
    ['.', '.', '.', '.', 'G']
]

ROWS = 5
COLS = 5

start = (0,0)
goal = (4,4)

directions = [
    (-1,0),   # Up
    (1,0),    # Down
    (0,-1),   # Left
    (0,1)     # Right
]


def get_next_states(state):

    row, col = state

    next_states = []

    for dr, dc in directions:

        new_row = row + dr
        new_col = col + dc

        if (0 <= new_row < ROWS and
            0 <= new_col < COLS and
            grid[new_row][new_col] != 'X'):

            next_states.append((new_row,new_col))

    return next_states


def bfs():

    queue = deque([(start,[start])])

    visited = set()

    while queue:

        state, path = queue.popleft()

        if state in visited:
            continue

        visited.add(state)

        if state == goal:
            return path

        for next_state in get_next_states(state):

            if next_state not in visited:

                queue.append((next_state,path+[next_state]))

    return None


solution = bfs()

print("Shortest Path:")

for state in solution:
    print(state)