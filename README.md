# Longest Uphill Paths in Matrix A — Advent of Code 2024, Day 10

This repository contains multiple approaches to solve [Advent of Code 2024 - Day 10](https://adventofcode.com/2024/day/10), which involves analyzing topographic trail maps and identifying valid uphill paths.

## 🔍 Problem Summary

Given a fixed 8×8 matrix `A`, identify all paths that:

- Start at a cell with value `0`
- Proceed step-by-step through adjacent (up, down, left, right) cells
- Only move to a neighbor with a value exactly `+1`
- Optionally reach a cell with value `9` after exactly 10 steps (Part 1)
- Count the total number of distinct valid trails starting from each trailhead (Part 2)

## 🧠 Implemented Solution Methods

### `kernel_solution.py` (💡 Fastest – Matrix Convolution-Based)

- Uses `numpy` and `scipy.ndimage.convolve` to simulate flow from value `0` to `9`
- Efficient trailhead scoring without recursion or traversal
- Ideal for large-scale or performance-sensitive versions of the problem

### `dfg_solution.py` (📊 Deterministic Finite Graph Walk)

- Uses a graph traversal model, exploring valid trail steps with control over path depth
- Suitable for counting exact-length paths and precise path enumeration

### `hoofit.py` (🧵 Recursive Exploration)

- Recursively explores all valid trails starting at each `0`-cell
- Records each path that reaches a `9` in 10 steps
- Also computes trailhead **ratings**: number of distinct valid trails starting from each `0`

## 📁 Files

- `dfg_solution.py` – Iterative DFS/graph-based approach
- `hoofit.py` – Recursive path enumeration and rating calculation
- `kernel_solution.py` – Matrix convolution approach using NumPy + SciPy
- `requirements.txt` – Python dependencies (`numpy`, `scipy`)
- `README.md` – You're reading it
- `.gitignore` – Excludes IDE config and Python artifacts

## 📦 Requirements

Install required packages with:

```bash
pip install -r requirements.txt
