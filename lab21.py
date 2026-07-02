from heapq import heappush ,heappop

start = (
    (5, 8, 2), 
    (1, 0, 3), 
    (4, 7, 6)

)

goal =(
    (1,2, 3), 
    (4, 5, 6), 
    (7, 8, 0)
)


#h1-> number of misplace tiles
def h1(state):
    count = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal[i][j]:
                count = count + 1

    return count

#function to check 0 kata xa.

def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
            
def get_neighbours(state):
    x, y= find_blank(state)
    moves = [(-1, 0), (0, -1), (1, 0), (0,1)]
    neighbours = []
    for dx, dy in moves:
        nx = x + dx  #nx = naya x
        ny = y + dy
        if 0<= nx < 3 and 0 <= ny < 3:
            board = [list(row) for row in state]
            board[x][y], board[nx][ny] = board[nx][ny], board [x][y]
            neighbours.append(tuple(map(tuple, board)))
    return neighbours

# print (get_neighbours(start))

def display(state):
    for row in state:
        print (row)
    print()


def aStar(state, heuristic):
    pq = []
    heappush(pq, (heuristic(start), 0, start))
    parent = {start:None}
    g_cost = {start: 0}
    expanded = 0
    while pq:
        f, g, current = heappop(pq)
        expanded = expanded + 1
        if current == goal:
            return True,parent, expanded
        for neighbours in get_neighbours(current):
            naya_g = g + 1
            if neighbours not in g_cost or naya_g < g_cost[neighbours]:
                g_cost[neighbours] = naya_g
                f_cost = naya_g + heuristic(neighbours)
                heappush(
                    pq, 
                    (f_cost, naya_g, neighbours)
                )
                parent[neighbours] = current
    return False, parent, expanded

def reconstruct(parent, current):
    path = []
    while current is not None:
        path.append(current)
        current = parent[current]
    return path[::-1]

goalFound, parent,  expanded = aStar(start, h1)


if(goalFound):
    print (f"Goal state found by expanding {expanded} states")
    # display(start)
    for state in reconstruct(parent, goal):
        display(state)
else:
    (f"goal state not found after expanding {expanded} state")

