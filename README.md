# Longest Uphill Paths in Matrix A
This is a solution for  https://adventofcode.com/2024/day/10

This project identifies all paths that start at cells with value `0` in a given matrix `A` and proceed through adjacent cells that are exactly `+1` greater at each step. It records the **longest such path** from each `0`-valued cell and reports the highest value reached.

## 🔍 Problem Description

Given a fixed 8×8 matrix `A`, we:
- Pad the matrix with a border of `10`s to avoid boundary issues.
- Construct four shifted versions of the matrix (up, down, left, right).
- Identify where a step in each direction results in a difference of exactly `+1`.
- From every `A == 0` cell, walk as far as possible by following `+1` steps.
- Save each valid path along with the peak value it reaches.

## 📁 Files

- `main.py`: The script that performs the computation.
- `longest_partial_paths.txt`: Output file listing each starting position, the longest path found from it, and the maximum value reached.

## 📦 Requirements

This project uses only Python's built-in libraries:
- `numpy`

Install it (if not already):

```bash
pip install numpy
