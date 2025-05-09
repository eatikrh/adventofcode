import numpy as np

# Step 1: Define the original matrix A
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

# Step 2: Pad A with 10s on all sides
A = np.pad(A_original, pad_width=1, mode='constant', constant_values=10)

# Step 3: Create shifted matrices
U = np.roll(A, shift=-1, axis=0)
U[-1, :] = 0
D = np.roll(A, shift=1, axis=0)
D[0, :] = 0
L = np.roll(A, shift=-1, axis=1)
L[:, -1] = 0
R = np.roll(A, shift=1, axis=1)
R[:, 0] = 0

# Step 4: Compute directional difference matrices
diff_U_A = (U - A == 1).astype(int)
diff_D_A = (D - A == 1).astype(int)
diff_L_A = (L - A == 1).astype(int)
diff_R_A = (R - A == 1).astype(int)

direction_map = {
    'U': (-1, 0, diff_U_A),
    'D': (1, 0, diff_D_A),
    'L': (0, -1, diff_L_A),
    'R': (0, 1, diff_R_A)
}

# Step 5: Locate all A == 0 positions (account for +1 padding)
zero_starts = [tuple(pos + 1) for pos in np.argwhere(A_original == 0)]

# Step 6: Walk as far as possible from each A == 0 cell
def walk_path_as_far_as_possible(start_y, start_x):
    stack = [((start_y, start_x), "", set([(start_y, start_x)]))]
    best_path = ""
    max_value = A[start_y, start_x]

    while stack:
        (y, x), path, visited = stack.pop()

        if A[y, x] > max_value:
            max_value = A[y, x]
            best_path = path

        for dir_label, (dy, dx, diff_matrix) in direction_map.items():
            ny, nx = y + dy, x + dx
            if (
                0 <= ny < A.shape[0] and
                0 <= nx < A.shape[1] and
                diff_matrix[ny, nx] == 1 and
                (ny, nx) not in visited
            ):
                stack.append(((ny, nx), path + dir_label, visited | {(ny, nx)}))

    return best_path, max_value

# Step 7: Save all longest partial paths
with open("longest_partial_paths.txt", "w") as f:
    for start in zero_starts:
        path, peak = walk_path_as_far_as_possible(*start)
        if path:
            f.write(f"{start} -> peak {peak}: {path}\n")
