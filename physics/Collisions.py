from visualizer.Vector2 import Vector2

def orientation(a : Vector2, b : Vector2, c : Vector2):
    """Returns the orientation of the ordered triplet (p, q, r).
    0 -> p, q and r are collinear
    1 -> Clockwise
    2 -> Counterclockwise"""
    val = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)
    
    if val > 0:
        return 1
    else:
        return -1

def lines_intersect(p1 : Vector2, q1 : Vector2, p2 : Vector2, q2 : Vector2):
    """Returns True if the line segments p1q1 and p2q2 intersect"""
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True
    else:
        return False

def distance_btwn_points_sq(p1 : Vector2, p2 : Vector2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    return dx**2 + dy**2