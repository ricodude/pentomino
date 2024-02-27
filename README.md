# Pentomino Solver

Solves tile placement puzzles for an MxN grid given specified tile definitions.

## Description

### Puzzles
A puzzle consists of:
- the grid to be filled;
- a list of squares that are pre-filled and hence out of bounds; and
- the tile definitions.

### Grid
The grid is specified as an x-y range - e.g. `(8, 8)` for an 8x8 grid.

### Pre-filled Squares
The pre-filled squares are specified as a list of x-y coordinates - e.g. `[(0, 3), (5, 2)]`.

### Tile Definitions
Each tile is defined as a list of tuples specifying the relative offsets of the
squares making up the tile, with (0, 0) assumed implicitly to be part of the
tile.

For example, an L-shaped tile with 5 squares could be defined as follows:
```python
l_tile_1 = [(0, 1), (0, 2), (0, 3), (1, 3)]
```

It could also be defined with any orientation or positioning around (0, 0),
providing that (0, 0) is (implicitly) part of the tile. For example:
```python
l_tile_2 = [(0, -1), (0, 1), (0, 2), (1, 2)]
```

The program will treat these as equivalent.

The tile definitions are then a list of tiles. The example provided in the code
is for the 12 pentominoes:
```python
TILE_DEFS = [
    [(0, 1), (0, 2), (0, 3), (0, 4)],
    [(1, 0), (0, 1), (1, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2), (1, 3)],
    [(1, 0), (-1, 1), (0, 1), (0, 2)],
    [(1, 0), (-2, 1), (-1, 1), (0, 1)],
    [(1, 0), (2, 0), (1, 1), (1, 2)],
    [(2, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 1), (0, 2), (1, 2), (2, 2)],
    [(0, 1), (1, 1), (1, 2), (2, 2)],
    [(-1, 1), (0, 1), (1, 1), (0, 2)],
    [(-2, 1), (-1, 1), (0, 1), (1, 1)],
    [(1, 0), (1, 1), (1, 2), (2, 2)],
]
```

## Running the Program

### Dependencies

* Numpy
* Jupyter - if you want to run the notebooks

Numpy is just used to make the code for placing the tiles simpler. I experimented 
a little with using it to improve performance - e.g. using np.sum() - but this 
had a negative effect, perhaps because the arrays are too small to justify the 
overhead.

### Running the program

You run the solver by executing the function `solve_puzzle()` in the `solve` module:
```python
xy_range = (3, 7)
filled_squares = [(3, 2)]
solutions = solve.solve_puzzle(xy_range, filled_squares, solve.TILE_DEFS)
```
You can then display the solutions using `solve.display_solution()`. This will 
need the set of tile orientations for the display, which is a little clunky:
```python
tile_orients = solve.tile_orientations(solve.TILE_DEFS, xy_range[0])
solve.display_solution(solutions[0], tile_orients, xy_range)
```
This displays a simple text output, labelling each tile with a different capital letter:
```
ECC
EEC
AEC
AEC
A B
ABB
ABB
```
__The display (but not the solver) will break if there are more than 26 tiles, in which case you'll have to 
figure out your own method.__

### Examples
There are a few Jupyter notebooks with examples:
- Another puzzle.ipynb (which is the above example)
- Pentomino puzzle.ipynb 
- Simple puzzle.ipynb
