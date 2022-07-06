def fix_vec2d_polygon(polygon,
                      offset: tuple[float, float] = (0, 0)) -> list[tuple[float, float]]:
    """
    Salut toi

    polygon is a list of pymunk vec2d. I disabled it because pycharm don't recognize type for this shitty pymunk.

    OFFSET WILL BE ADDED
    """

    fixed_polygon = []
    for point in polygon:
        fixed_polygon.append((point[0]+offset[0], point[1]+offset[1]))

    return fixed_polygon
