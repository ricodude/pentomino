"""Module for solving Pentomino problems in an 8x8 puzzle.

(The code is more general and could be used to solve problems for other tile
shapes in an M x N puzzle)"""

from collections import deque
import string

import numpy as np

# Pentomino tile defs in relative x-y terms. All tiles are assumed to have an
# implicit (0, 0) square
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


# All these functions are for setting up the tile orientations in advance
def square_key(square):
    return square[1], square[0]


def rotate_tile(tile):
    """Rotate tile 90 degrees clockwise"""
    return [(square[1], -square[0]) for square in tile]


def flip_tile(tile):
    """Flip tile around y-axis"""
    return [(-square[0], square[1]) for square in tile]


def rebase_tile(tile):
    """Rebase the tile coords so that lowest square on y-axis is at y=0 and
    lowest square on x-axis with (new) y=0 has x=0"""
    new_tile = sorted(tile, key=square_key)
    base = new_tile[0]
    return [(square[0] - base[0], square[1] - base[1]) for square in new_tile]


def enrich_tile(tile, x_range):
    """Return a dictionary with the tile details enriched with useful info for
    placing"""
    tile_dict = {
        'xy_config': tile,
        'adds': np.array([square[0] + x_range * square[1] for square in tile]),
    }

    all_x = [square[0] for square in tile]
    min_x = min(all_x)
    if min_x < 0:
        tile_dict['min_x'] = min_x
    max_x = max(all_x)
    if max_x > 0:
        tile_dict['max_x'] = max_x
    max_y = max([square[1] for square in tile])
    if max_y > 0:
        tile_dict['max_y'] = max_y

    return tile_dict


def tile_orientations(tile_defs, x_range):
    """Use the tile definitions to create & return all possible orientations
    for each tile"""
    tiles = [[(0, 0)] + tile for tile in tile_defs]
    all_orientations = []
    for tile in tiles:
        orientations = []
        flipped = False
        new_orientation = tile
        while True:
            new_orientation = rebase_tile(new_orientation)
            if new_orientation not in orientations:
                orientations.append(new_orientation)
                new_orientation = rotate_tile(new_orientation)
            else:
                if not flipped:
                    new_orientation = flip_tile(new_orientation)
                    flipped = True
                else:
                    break
        all_orientations.append(orientations)
    enriched_tiles = [[enrich_tile(orient, x_range) for orient in
                       orientations] for orientations in all_orientations]
    return enriched_tiles


# All these functions are (mostly) for solving the problem given the pre-built
# tile orientations
def square_pos(square, xy_range):
    """Return the index of the square given the range"""
    return square[0] + square[1] * xy_range[0]


def square_xy(pos, xy_range):
    """Return the xy coords of the square given the range"""
    return pos % xy_range[0], int(pos / xy_range[0])


def get_next_tile(tile, tile_orients, remaining_tiles):
    """Tile here refers to (tile_num, orient_num):
    - if tile is None, return first orientation of first of the remaining tiles,
      or None if there are no remaining tiles;
    - if tile is not None, look for next orientation for this tile and return
      that;
    - if there are no more orientations for the tile, replace it and return
      first orientation for next tile;
    - if there are no more tiles, return None."""
    if tile is None:
        if len(remaining_tiles) == 0:
            return None
        new_tile_num = remaining_tiles.popleft()
        return new_tile_num, 0

    tile_num = tile[0]
    next_orient_num = tile[1] + 1
    if next_orient_num < len(tile_orients[tile_num]):
        return tile_num, next_orient_num

    if len(remaining_tiles) == 0 or \
            tile_num > remaining_tiles[len(remaining_tiles) - 1]:
        remaining_tiles.append(tile_num)
        return None

    num_rotations = 0
    while tile_num > remaining_tiles[0]:
        remaining_tiles.rotate(-1)
        num_rotations += 1
    new_tile_num = remaining_tiles.popleft()
    remaining_tiles.appendleft(tile_num)
    remaining_tiles.rotate(num_rotations)
    temp_list = list(remaining_tiles)
    if sorted(temp_list) != temp_list:
        print('Problem')
    return new_tile_num, 0


def backtrack(placed_tiles, tile_orients, squares, remaining_tiles):
    """Remove the last placed tile and return it together with the position it
    was placed in"""
    if len(placed_tiles) == 0:
        return 0, None
    pos, tile = placed_tiles.pop()
    tile_squares = tile_orients[tile[0]][tile[1]]['adds'] + pos
    squares[tile_squares] = 0
    next_tile = get_next_tile(tile, tile_orients, remaining_tiles)
    if next_tile is None:
        return backtrack(placed_tiles, tile_orients, squares, remaining_tiles)
    return pos, next_tile


def place_tile(tile, tile_orients, pos, xy_range, squares, placed_tiles):
    """Try to place the tile in the specified position. If it succeeds, return
    the new position for next empty square and None. Otherwise return the
    current position and current tile."""
    tile_details = tile_orients[tile[0]][tile[1]]

    # Check the tile fits within the xy range
    x, y = square_xy(pos, xy_range)
    if 'min_x' in tile_details:
        if x + tile_details['min_x'] < 0:
            return pos, tile
    if 'max_x' in tile_details:
        if x + tile_details['max_x'] >= xy_range[0]:
            return pos, tile
    if 'max_y' in tile_details:
        if y + tile_details['max_y'] >= xy_range[1]:
            return pos, tile

    tile_squares = tile_details['adds'] + pos

    # Check all squares that would be covered by the tile are empty
    if sum(squares[tile_squares]) > 0:
        return pos, tile

    squares[tile_squares] = 1
    placed_tiles.append((pos, tile))
    while pos < len(squares) and squares[pos] > 0:
        pos += 1
    return pos, None


def solve_puzzle(xy_range, filled_squares, tile_defs):
    """Solve the puzzle with the given x-y range, filled squares and defined
    tiles"""
    # Check the filled squares are inside the range
    for square in filled_squares:
        if (square[0] < 0) or (square[0] >= xy_range[0]) \
                or (square[1] < 0) or (square[1] >= xy_range[1]):
            raise ValueError(f'Square outside range: {square}')

    # Initialise the squares to unfilled (0)
    squares = np.zeros(xy_range[0] * xy_range[1], dtype=np.int8)

    # Set the specified squares to filled (1)
    for square in filled_squares:
        squares[square_pos(square, xy_range)] = 1

    # Determine all orientations for the tiles
    tile_orients = tile_orientations(tile_defs, xy_range[0])

    # Variables carrying state for the algorithm:
    # - squares: array of squares (0 = empty, 1 = filled),
    # - pos: next square to be filled,
    # - placed_tiles: deque of tuples (pos, tile), where orient is tuple
    #   (tile_num, orient_num) - filled / emptied from right,
    # - remaining_tiles: deque of tile_num's - emptied / filled from left,
    # - solutions: list of solutions discovered, where each solution is a
    #   list of tuples (pos, tile) as per placed_tiles above.
    pos = 0
    placed_tiles = deque()
    remaining_tiles = deque(range(len(tile_orients)))
    solutions = []

    curr_tile = None
    while True:
        curr_tile = get_next_tile(curr_tile, tile_orients, remaining_tiles)
        if curr_tile is None:
            pos, curr_tile = backtrack(placed_tiles, tile_orients, squares,
                                       remaining_tiles)
            if curr_tile is None:
                print('Tried everything')
                return solutions
        pos, curr_tile = place_tile(curr_tile, tile_orients, pos, xy_range,
                                    squares, placed_tiles)
        if pos == len(squares):
            solution = list(placed_tiles)
            solutions.append(solution)
            pos, curr_tile = backtrack(placed_tiles, tile_orients, squares,
                                       remaining_tiles)


# Simple display using capital letters. Obviously will break if there are more
# than 26 tiles
LABELS = list(string.ascii_uppercase)


def display_solution(solution, tile_orients, xy_range):
    """Display solution as text. NB: Bottom left is (0, 0)"""
    chars = [' '] * xy_range[0] * xy_range[1]
    for pos, (tile_num, config_num) in solution:
        label = LABELS[tile_num]
        for char_pos in tile_orients[tile_num][config_num]['adds'] + pos:
            chars[char_pos] = label

    solution_str = ''.join(chars)

    for y in reversed(range(xy_range[1])):
        print(solution_str[y * xy_range[0]:(y + 1) * xy_range[0]])
