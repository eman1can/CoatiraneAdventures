from random import randint, shuffle

# Use Recursive Backtracking to generate maze
N, S, E, W = 1, 2, 4, 8  # 0001 0010 0100 1000
NONE = 0
NS = N | S
NE = N | E
NW = N | W
EW = E | W
ES = E | S
SW = S | W
NSW = NS | W
NSE = NS | E
NEW = NE | W
SEW = ES | W
NSEW = NS | EW


DIR = {(1, 0): W, (0, 1): N, (-1, 0): E, (0, -1): S}


def connections_to_char(connects):
    if connects == NSEW:
        return '┼'
    elif connects == NS:
        return '│'
    elif connects == EW:
        return '─'
    elif connects == ES:
        return '┌'
    elif connects == SW:
        return '┐'
    elif connects == NE:
        return '└'
    elif connects == NW:
        return '┘'
    elif connects == NSE:
        return '├'
    elif connects == NSW:
        return '┤'
    elif connects == SEW:
        return '┬'
    elif connects == NEW:
        return '┴'
    elif connects == N:
        return '╵'
    elif connects == S:
        return '╷'
    elif connects == E:
        return '╶'
    elif connects == W:
        return '╴'


def format_output(b, c):
    directions = {}
    for y in range(len(b)):
        for x in range(len(b[y])):
            if len(c[(x, y)]) == 0:
                continue
            connects = NONE
            for (dx, dy) in c[(x, y)]:
                connects |= DIR[(x - dx, y - dy)]
            b[y][x] = expand_char(connections_to_char(connects))
            directions[(x, y)] = connects
    return b, directions


def walk(v, conn, x, y, s, w, h):
    v[y][x] = 1

    d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]  # Directions
    shuffle(d)

    ds = []
    for (xx, yy) in d:
        if xx < 0 or xx >= w or yy < 0 or yy >= h:
            continue
        if v[yy][xx]:
            continue
        conn[(x, y)].append((xx, yy))
        conn[(xx, yy)].append((x, y))
        return xx, yy
    return False


def expand_char(char):
    if char in ['┼', '─', '┐', '┘', '┤', '┬', '┴', '╴']:
        return '─' + char
    else:
        return ' ' + char


def generate_maze(w):
    h=w

    box = [[' ' for _ in range(w)] for _ in range(h)]

    vis = [[0 for _ in range(w)] for _ in range(h)]

    connections = {}
    for y in range(h):
        for x in range(w):
            connections[(x, y)] = []

    stack = [(randint(0, w - 1), randint(0, h - 1))]
    while len(stack) > 0:
        (x, y) = stack.pop()
        node = walk(vis, connections, x, y, stack, w, h)
        if node:
            stack.append((x, y))
            stack.append(node)
    return format_output(box, connections)


def wrap_box(box):
    new_box = [['' for _ in range(len(box[0]) + 2)] for _ in range(len(box) + 2)]
    for y in range(len(new_box)):
        for x in range(len(new_box[y])):
            if y == 0 and x == 0:
                new_box[y][x] = '┌'
            elif y == 0 and x == len(new_box[y]) - 1:
                new_box[y][x] = '─┐'
            elif y == len(new_box) - 1 and x == 0:
                new_box[y][x] = '└'
            elif y == len(new_box) - 1 and x == len(new_box) - 1:
                new_box[y][x] = '─┘'
            elif y == 0 or y == len(new_box[y]) - 1:
                new_box[y][x] = '──'
            elif x == 0:
                new_box[y][x] = '│'
            elif x == len(new_box) - 1:
                new_box[y][x] = ' │'
            else:
                new_box[y][x] = box[y - 1][x - 1]
    return new_box


def strip_box(box_string):
    rows = box_string.split('\n')[1:-1]
    for index in range(len(rows)):
        rows[index] = rows[index][1:-2]
    return rows


def get_box_from_string(box_string):
    rows = strip_box(box_string)
    size = len(rows)
    box = []
    for y in range(size):
        box.append([])
        for x in range(size):
            box[y].append(rows[y][x * 2:(x + 1) * 2])
    return box


def solve_path(last, start, end, nodes):
    if start == end:
        return [end]
    node = nodes[start]
    if (node & N) == N and last != S:
        path = solve_path(N, (start[0], start[1] - 1), end, nodes)
        if path:
            return [start] + path
    if (node & E) == E and last != W:
        path = solve_path(E, (start[0] + 1, start[1]), end, nodes)
        if path:
            return [start] + path
    if (node & S) == S and last != N:
        path = solve_path(S, (start[0], start[1] + 1), end, nodes)
        if path:
            return [start] + path
    if (node & W) == W and last != E:
        path = solve_path(W, (start[0] - 1, start[1]), end, nodes)
        if path:
            return [start] + path
    return False
