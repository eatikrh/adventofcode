import numpy as np
import pandas as pd

def explore_paths(y, x, path="", visited=None):
    if visited is None:
        visited = set()
    visited.add((y, x))

    current_value = A[y, x]
    paths = []

    #print(f"---Start: y={y},  x={x},  Value={current_value}, path={path} ")
    moved = False
    for dir in ['U', 'R', 'D', 'L']:
        delta_y, delta_x = deltas[dir]

        new_y = y + delta_y
        new_x  = x + delta_x
        new_x  = x + delta_x
        #print(f"Going: {dir} delta_y={delta_y}, delta_x={delta_x}, new_y={new_y}, new_x={new_x}")

        if (
            0 <= new_y < A.shape[0]
            and 0 <= new_x < A.shape[1]
            and 0 <= y - 1 < can_move[dir].shape[0]
            and 0 <= x - 1 < can_move[dir].shape[1]
        ):
            #print(f"pre-move new_y={new_y}, new_x={new_x}, Old Value={A[y, x]} New Value={A[new_y, new_x]}, path={path}")
            if (can_move[dir][y - 1, x -1 ] == 1
            and (new_y, new_x) not in visited
            ):
                #print(f"can move: can_move[dir][y - 1, x - 1] = {can_move[dir][y - 1, x - 1]}, visited: {(new_y, new_x) in visited}")
                moved = True
                #print(f"moved=True, new_y={new_y}, new_x={new_x}, Old Value={A[y, x]} New Value={A[new_y, new_x]}, path={path}")
                new_paths = explore_paths(new_y, new_x, path + dir, visited.copy())
                paths.extend(new_paths)
            #else:
                #print(f"cannot move: can_move[dir][y - 1, x - 1] = {can_move[dir][y - 1, x -1]}, visited: {(new_y, new_x) in visited}")
        #else:
            #print(f"what is going on here? some dimension issue:  0 <= new_y < A.shape[0] { 0 <= new_y < A.shape[0]}, 0 <= new_x < A.shape[1]  {0 <= new_x < A.shape[1]  }, 0 <= y < can_move[dir].shape[0]  {0 <= y < can_move[dir].shape[0] }, 0 <= x < can_move[dir].shape[1]={ 0 <= x < can_move[dir].shape[1]} ")
            #print(f"what is going on here? some dimension issue:  new_y ={new_y}, A.shape[0]={A.shape[0]}, new_x={new_x}, A.shape[1]={A.shape[1]}")


    if not moved:
        # print(f"returning current_value={current_value}, moved={moved},  x={x}, y={y}")
        ends_at_9 = (current_value == 9)
        paths.append((path, ends_at_9))

    return paths

# Original matrix
A_original = np.array([
    [8, 9, 0, 1, 0, 1, 2, 3],
    [7, 8, 1, 2, 1, 8, 7, 4],
    [8, 7, 4, 3, 0, 9, 6, 5],
    [9, 6, 5, 4, 9, 8, 7, 4],
    [4, 5, 6, 7, 8, 9, 0, 3],
    [3, 2, 0, 1, 9, 0, 1, 2],
    [0, 1, 3, 2, 9, 8, 0, 1],
    [1, 0, 4, 5, 6, 7, 3, 2]
])

# Pad the matrix with 10s
A = np.pad(A_original, pad_width=1, mode='constant', constant_values=100)

U = np.roll(A, -1, axis=0); U[-1, :] = 0  # Up
D = np.roll(A, +1, axis=0); D[0, :] = 0   # Down
L = np.roll(A, -1, axis=1); L[:, -1] = 0  # Left
R = np.roll(A, +1, axis=1); R[:, 0] = 0   # Right

# Compute directional differences where neighbor = self + 1
diffs = {
    'U': (diff_U_A := (U - A == 1)),
    'D': (diff_D_A := (D - A == 1)),
    'L': (diff_L_A := (L - A == 1)),
    'R': (diff_R_A := (R - A == 1))
}
#print("Diffs):")
#print(diffs)


# Direction deltas
deltas = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}

# All zero-valued starts (offset +1 for padding)
zero_starts = [tuple(pos + 1) for pos in np.argwhere(A_original == 0)]
print("Zero starts (in padded matrix A):")
for start in zero_starts:
    print(tuple(int(x) for x in start))

# Notice we are getting the diffs in opposite direction
can_move_up = np.roll(diffs['D'], shift=1, axis=0)
can_move_down = np.roll(diffs['U'], shift=-1, axis=0)
can_move_left = np.roll(diffs['R'], shift=1, axis=1)
can_move_right = np.roll(diffs['L'], shift=-1, axis=1)

print("A")
print(A_original)


print("can_move_down")
can_move_down = can_move_down[:-2, 1:-1]
print(can_move_down.astype(int))

print("can_move_up")
can_move_up = can_move_up[2:, 1:-1]
print(can_move_up.astype(int))

print("can move left")
can_move_left = can_move_left[1:-1, 2:]
print(can_move_left.astype(int))

print("can move right")
can_move_right = can_move_right[1:-1, :-2]
print(can_move_right.astype(int))


can_move = {
    'U': can_move_up,
    'D': can_move_down,
    'L': can_move_left,
    'R': can_move_right
}

# From all A == 0 starts
with open("recursive_paths_from_0.txt", "w") as f:
    for start in zero_starts:
        all_paths = explore_paths(*start)
        for p, is_nine in all_paths:
            f.write(f"{(int(start[0]), int(start[1]))}: {p} (ends at 9: {is_nine})\n")
            if is_nine:
                print(f"{(int(start[0]), int(start[1]))}: {p} (ends at 9: {is_nine})\n")
