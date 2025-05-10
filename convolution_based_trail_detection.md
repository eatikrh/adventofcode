## 🚀 Alternative Solution: Convolution-Based Trail Detection (Matrix Propagation)

Instead of using graph traversal algorithms like DFS or BFS, we implemented a **matrix-based approach using convolution** to solve the hiking trail problem. This method is efficient and elegant, avoiding recursion or explicit stack management.

### 🧠 Idea

We simulate trail progression from altitude 0 to altitude 9 using a step-by-step propagation mechanism based on convolution. At each step, we determine which new cells are reachable by checking if they are adjacent to previously reachable cells **and** have the correct increasing altitude.

### 🔧 How It Works

1. **Start with cells of value 0**:
   ```python
   reachable = (A_original == 0).astype(np.uint8)
   ```

2. **Define a 4-neighbor convolution kernel**:
   ```python
   kernel = np.array([
       [0, 1, 0],
       [1, 0, 1],
       [0, 1, 0]
   ])
   ```

3. **Iteratively propagate reachability from 1 to 9**:
   ```python
   from scipy.ndimage import convolve

   for step in range(1, 10):
       mask = (A_original == step)
       neighbor_reach = convolve(reachable, kernel, mode='constant', cval=0)
       reachable = ((neighbor_reach > 0) & mask).astype(np.uint8)
   ```

4. **Extract final trail endpoints** (cells with value 9 that were reached in 10 steps):
   ```python
   endpoints = ((A_original == 9) & (reachable == 1))
   valid_coords = np.argwhere(endpoints)
   ```

### ✅ Benefits

- No recursion or graph traversal
- Fast and vectorized via NumPy/SciPy
- Easy to debug and extend
- Inspired by image processing techniques