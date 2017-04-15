def match_hood(geotag, hoods):
    if geotag is None:
        return None

    for hood in hoods:
        name = hood['label']
        vertices = hood['polygon']
        if point_inside_polygon(geotag, vertices):
            return name

    return False


def point_inside_polygon(point, vertices):
    inside = False
    num_vertices = len(vertices)
    x, y = point
    xj, yj = vertices[num_vertices - 1]
    for n in range(num_vertices):
        xi, yi = vertices[n]
        between_y = (yi > y) != (yj > y)
        if between_y:
            x_interp = ((y - yi)/(yj - yi))*(xj - xi) + xi
            if x < x_interp:
                inside = not inside
        xj, yj = xi, yi

    return inside
