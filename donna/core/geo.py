def is_point_inside_polygon(point, vertices):
    # Uses the ray-casting algorithm
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
