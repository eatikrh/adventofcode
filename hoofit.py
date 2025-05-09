import numpy as np
import pandas as pd

def explore_paths(y, x, path="", visited=None):
    if visited is None:
        visited = set()
    visited.add((y, x))

    current_value = A[y, x]
    paths = []

    #print(f"start: x={x}, y={y}, Value={current_value}, path={path} ")
    moved = False
    for dir in ['U', 'R', 'D', 'L']:
        dy, dx = deltas[dir]
        ny, nx = y + dy, x + dx

        if (
            0 <= ny < A.shape[0]
            and 0 <= nx < A.shape[1]
            and 0 <= y < can_move[dir].shape[0]
            and 0 <= x < can_move[dir].shape[1]
            and can_move[dir][y, x] == 1
            and (ny, nx) not in visited
        ):
            moved = True
            #print(f"moved={moved}, ny={ny}, ny={ny}, Value={A[ny, nx]}, path={path} ")
            new_paths = explore_paths(ny, nx, path + dir, visited.copy())
            paths.extend(new_paths)

    if not moved:
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
