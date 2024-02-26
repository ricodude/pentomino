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


def square_key(square):
    return square[1], square[0]


def rotate_tile(tile):
    """Rotate tile 90 degrees clockwise"""
    return [(square[1], -square[0]) for square in tile]


def flip_tile(tile):
    """Flip tile around y-axis"""
    return [(-square[0], square[1]) for square in tile]


def rebase_tile(tile):
    """Rebase the tile coords so that lowest square on y-axis is at y=0 and lowest square on x-axis
    with (new) y=0 has x=0"""
    new_tile = sorted(tile, key=square_key)
    base = new_tile[0]
    return [(square[0] - base[0], square[1] - base[1]) for square in new_tile]


def tile_configs(tile_defs):
    tiles = [[(0, 0)] + tile for tile in tile_defs]
    all_configs = []
    for tile in tiles:
        this_tile_configs = []
        flipped = False
        new_config = tile
        while True:
            new_config = rebase_tile(new_config)
            if new_config not in this_tile_configs:
                this_tile_configs.append(new_config)
                new_config = rotate_tile(new_config)
            else:
                if not flipped:
                    new_config = flip_tile(new_config)
                    flipped = True
                else:
                    break
        all_configs.append(this_tile_configs)
    return all_configs
