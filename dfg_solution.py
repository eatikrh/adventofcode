import numpy as np

# Original matrix from the Day 10 question
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

rows, cols = A_original.shape
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

# Find all trailheads (cells with value 0)
trailheads = [(i, j) for i in range(rows) for j in range(cols) if A_original[i, j] == 0]

# Perform a non-recursive DFS to find trails of exact length 10 with increasing height by 1 each step
target_length = 10
valid_trails = []

for head in trailheads:
  stack = [(head, [head])]
  while stack:
    (x, y), path = stack.pop()
    if len(path) == target_length and A_original[x, y] == 9:
      valid_trails.append(path)
      continue
    if len(path) >= target_length:
      continue
    for dx, dy in directions:
      nx, ny = x + dx, y + dy
      if 0 <= nx < rows and 0 <= ny < cols:
        if (nx, ny) not in path and A_original[nx, ny] == A_original[x, y] + 1:
          stack.append(((nx, ny), path + [(nx, ny)]))


print(len(valid_trails))


for trail in valid_trails:
  print(trail)


count = 0
for path in valid_trails:
  start_row, start_col = path[0]
  end_row, end_col = path[-1]
  if A_original[start_row, start_col] == 0 and A_original[end_row, end_col] == 9:
    count += 1

print(f"{count} trails start at 0 and end at 9.")

# Extract all end coordinates
endpoints = [path[-1] for path in valid_trails]
unique_endpoints = set(endpoints)

all_starts = [path[0] for path in valid_trails]
zero_starts = set(all_starts)

print(f" unique_endpoints {unique_endpoints} count={len(unique_endpoints)}")
print(f" zero_starts {zero_starts} count={len(zero_starts)}")
trailhead_scores = {}

paths = valid_trails

for start in zero_starts:
  endings = set()
  for end_coord in unique_endpoints:
    endings.add(tuple(end_coord))
    print(f"{(int(start[0]), int(start[1]))}")

  score = len(endings)
  trailhead_scores[start] = score

print(f"endings: {endings}")

# Display results
print("\nTrailhead Scores:")
total = 0
for k in sorted(trailhead_scores):
  print(f"{k}: {trailhead_scores[k]}")
  total += trailhead_scores[k]

print(f"\nSum of all trailhead scores: {total}")

