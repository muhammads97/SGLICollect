def inside_polygon(px: list[float], py: list[float], x: float, y: float):
    counter = 0
    p1x = px[0]
    p1y = py[0]
    n = len(px)
    i = 1
    while (i < n):
        p2x = px[i % n]
        p2y = py[i % n]
        if (y > min(p1y, p2y)):
            if (y <= max(p1y, p2y)):
                if (x <= max(p1x, p2x)):
                    if (p1y != p2y):
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if (p1x == p2x or x <= xinters):
                            counter += 1
        p1x = p2x
        p1y = p2y
        i += 1

    if (counter % 2 == 0):
        return 0
    else:
        return 1

def distance(coord1, coord2):
    return ((coord1[0]-coord2[0])**2 + (coord1[1]-coord2[1])**2)**0.5


def min_distance(point, polygon):
    return min(distance(point, coord) for coord in polygon)