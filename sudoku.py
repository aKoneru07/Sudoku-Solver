import time
import random

rows = "ABCDEFGHI"
cols = "123456789"

def all_pairs(A, B):                            # A is XYZ, B is 123 (row, col)
    return [x + y for x in A for y in B]

def get_peers(x):
    p = all_pairs(x[0], cols)
    p += all_pairs(rows, x[1])
    r = int(rows.index(x[0]) / 3) * 3
    c = int(cols.index(x[1]) / 3) * 3
    p += all_pairs(rows[r:r + 3], cols[c:c + 3])
    p = set(p)
    p.remove(x)
    return p

def goal(state):
    for x in state.values():
        if not len(x) == 1:
            return False
    return True

def get_values_for_sqr(state, sqr):
    l = (list(state[sqr]))
    random.shuffle(l)
    return "".join(l)

def get_unassigned_sqr(state):
    for x in units:                             # ONLY one spot for VALUE
        pos = ""
        for sq in x:
            if (len(state[sq]) > 1):
                pos += state[sq]
        for c in cols:
            if pos.count(c) == 1:
                for sq in x:
                    if c in state[sq]:
                        return sq, c

    l = list(state.keys())                      # SQR w least Values
    l.sort(key=lambda x: len(state[x]) + random.random())
    for x in l:
        if len(state[x]) > 1:
            return x, False
    return False

def assign(square, val, state):
    state[square] = val
    for x in peers[square]:
        if val in state[x]:
            state[x] = state[x].replace(val, "")
            if len(state[x]) == 1:
                state = assign(x, state[x], state)
    return state

def check(state):
    for x in state.keys():
        if len(state[x]) == 0:
            return False
    return True

def recur(state):
    if goal(state):
        # print("SOLVED")
        # print()
        return state
    sqr, val = get_unassigned_sqr(state)
    if sqr is False:
        return False

    if val is False:
        val = (get_values_for_sqr(state, sqr))
    for r in val:
        newState = state.copy()
        newState = assign(sqr, r, newState)

        if check(newState):
            result = recur(newState)
            if result is not False:
                return result
    return False

def display(state):
    x = 0
    line = ""
    while x < len(squares):
        if len(state[squares[x]]) == 1:
            line = line + state[squares[x]] + " "
        else:
            line = line + ". "
        if x % 3 == 2:
            line = line + "| "
        else:
            line = line + " "
        if x % 9 == 8:
            print(rows[int(x / 9)] + " | " + line)
            line = ""
            # print()
        if x % 27 == 26 and x != 80:
            print("---------------------------------")
            # print()
        x += 1
    print()

def solve(puzzle):
    state = {}
    for x in squares:
        state[x] = cols

    pos = 0
    for x in puzzle:
        if x in cols:
            state = assign(squares[pos], x, state)
        pos += 1
    print("Initial Board: ")
    display(state)
    print()
    print("SOLUTION: ")
    return recur(state)


#####    SET UP    #####

squares = (all_pairs(rows, cols))

units = [set(all_pairs(y, cols)) for y in rows]             # ROWS
units = units + [set(all_pairs(rows, y)) for y in cols]     # COLS
for x in all_pairs("ADE", "147"):                           # SUB-SQUARES
    r = int(rows.index(x[0]) / 3) * 3
    c = int(cols.index(x[1]) / 3) * 3
    units.append(set(all_pairs(rows[r:r + 3], cols[c:c + 3])))

peers = {}
for x in squares:
    peers[x] = get_peers(x)


#####    ACTUAL SOLVING    #####

puzzle = "8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4.."
# "....14....3....2...7..........9...3.6.1.............8.2.....1.4....5.6.....7.8..."
# "49     8   3           62  5   8  9     4 61 6 1 2 5  256   3  1    2        78  "
# "3...8.......7....51..............36...2..4....7...........6.13..452...........8.."
# "8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4.."        (World's Hardest Sudoku)

toc = time.time()
display(solve(puzzle))
print("Time: " + str(time.time() - toc))
