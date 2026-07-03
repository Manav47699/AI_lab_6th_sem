from heapq import heappush, heappop

# 1. Define States
start = (
    (5, 8, 2), 
    (1, 0, 3), 
    (4, 7, 6)
)

goal = (
    (1, 2, 3), 
    (4, 5, 6), 
    (7, 8, 0)
)

# --- HEURISTICS SECTION ---

# h1 -> Number of misplaced tiles (Your original function)
def h1(state):
    count = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal[i][j]:
                count = count + 1
    return count

# ADDED TASK 1: h2 -> Manhattan Distance
def h2(state):
    # Dictionary mapping each tile value to its target (row, col) coordinates in the goal state
    goal_positions = {
        1: (0, 0), 2: (0, 1), 3: (0, 2),
        4: (1, 0), 5: (1, 1), 6: (1, 2),
        7: (2, 0), 8: (2, 1)  # We skip 0 (blank)
    }
    
    distance = 0
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val != 0:
                target_i, target_j = goal_positions[val]
                # Summing absolute horizontal and vertical differences
                distance += abs(i - target_i) + abs(j - target_j)
    return distance

# ADDED TASK 2: h3 -> Combined Heuristic (h1 + h2)
def h3(state):
    return h1(state) + h2(state)


# --- HELPER & CORE SEARCH FUNCTIONS (Your original functions) ---

def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
            
def get_neighbours(state):
    x, y = find_blank(state)
    moves = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    neighbours = []
    for dx, dy in moves:
        nx = x + dx  
        ny = y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            board = [list(row) for row in state]
            board[x][y], board[nx][ny] = board[nx][ny], board[x][y]
            neighbours.append(tuple(map(tuple, board)))
    return neighbours

def display(state):
    for row in state:
        print(row)
    print()

def aStar(state, heuristic):
    pq = []
    heappush(pq, (heuristic(start), 0, start))
    parent = {start: None}
    g_cost = {start: 0}
    expanded = 0
    while pq:
        f, g, current = heappop(pq)
        expanded = expanded + 1
        if current == goal:
            return True, parent, expanded
        for neighbours in get_neighbours(current):
            naya_g = g + 1
            if neighbours not in g_cost or naya_g < g_cost[neighbours]:
                g_cost[neighbours] = naya_g
                f_cost = naya_g + heuristic(neighbours)
                heappush(pq, (f_cost, naya_g, neighbours))
                parent[neighbours] = current
    return False, parent, expanded

def reconstruct(parent, current):
    path = []
    while current is not None:
        path.append(current)
        current = parent[current]
    return path[::-1]


# --- ADDED TASK 3: COMPARISON EXECUTION ---

# Test Heuristic 1
goalFound1, parent1, expanded1 = aStar(start, h1)
print("========================================")
print(" RUNNING A* WITH h1: MISPLACED TILES")
print("========================================")
if goalFound1:
    print(f"Goal state found by expanding {expanded1} states.")
    print(f"Total Moves: {len(reconstruct(parent1, goal)) - 1}\n")
    # Optional: uncomment to see steps
    # for state in reconstruct(parent1, goal): display(state)

# Test Heuristic 2
goalFound2, parent2, expanded2 = aStar(start, h2)
print("========================================")
print(" RUNNING A* WITH h2: MANHATTAN DISTANCE")
print("========================================")
if goalFound2:
    print(f"Goal state found by expanding {expanded2} states.")
    print(f"Total Moves: {len(reconstruct(parent2, goal)) - 1}\n")

# Test Heuristic 3
goalFound3, parent3, expanded3 = aStar(start, h3)
print("========================================")
print(" RUNNING A* WITH h3: COMBINED (h1 + h2)")
print("========================================")
if goalFound3:
    print(f"Goal state found by expanding {expanded3} states.")
    print(f"Total Moves: {len(reconstruct(parent3, goal)) - 1}\n")