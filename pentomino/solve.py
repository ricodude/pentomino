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
    """Rebase the tile coords so that lowest square on y-axis is at y=0 and
    lowest square on x-axis with (new) y=0 has x=0"""
    new_tile = sorted(tile, key=square_key)
    base = new_tile[0]
    return [(square[0] - base[0], square[1] - base[1]) for square in new_tile]


def enrich_config(tile_config, x_range):
    """Return a dictionary with the tile config (placement) details enriched
    with useful info for placing the tile"""
    tile_dict = {
        'xy_config': tile_config,
        'adds': [square[0] + x_range * square[1] for square in tile_config],
    }

    all_x = [square[0] for square in tile_config]
    min_x = min(all_x)
    if min_x < 0:
        tile_dict['min_x'] = min_x
    max_x = max(all_x)
    if max_x > 0:
        tile_dict['max_x'] = max_x
    max_y = max([square[1] for square in tile_config])
    if max_y > 0:
        tile_dict['max_y'] = max_y

    return tile_dict


def tile_configs(tile_defs, x_range):
    """Use the tile definitions to create & return all possible configs
    (placements) for each tile"""
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
    enriched_configs = [[enrich_config(config, x_range) for config in configs] \
                        for configs in all_configs]
    return enriched_configs
