from collections import deque

def is_valid(state):
    F, W, G, C = state

    # Wolf eats Goat
    if W == G and F != W:
        return False

    # Goat eats Cabbage
    if G == C and F != G:
        return False

    return True


def get_next_states(state):
    F, W, G, C = state
    next_states = []

    # Farmer crosses alone
    new_state = (1-F, W, G, C)
    if is_valid(new_state):
        next_states.append(new_state)

    # Farmer takes Wolf
    if F == W:
        new_state = (1-F, 1-W, G, C)
        if is_valid(new_state):
            next_states.append(new_state)

    # Farmer takes Goat
    if F == G:
        new_state = (1-F, W, 1-G, C)
        if is_valid(new_state):
            next_states.append(new_state)

    # Farmer takes Cabbage
    if F == C:
        new_state = (1-F, W, G, 1-C)
        if is_valid(new_state):
            next_states.append(new_state)

    return next_states


def bfs():
    start = (0,0,0,0)
    goal = (1,1,1,1)

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
                queue.append((next_state, path+[next_state]))

    return None


solution = bfs()

print("Solution Path:")
for state in solution:
    print(state)