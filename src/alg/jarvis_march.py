import numpy as np

def is_to_the_right(p, q, r):
    my_array = np.array([[1, p[0], p[1]],
                      [1, q[0], q[1]],
                      [1, r[0], r[1]]])
    det = np.linalg.det(my_array)
    if det <= 0:
        return False
    return True

def ConvexHull(point_list):
    edges = []
    for p in point_list:
        for q in point_list:
            if p != q:
                valid = True
                for r in point_list:
                    if r != p and r != q:
                        if not is_to_the_right(p, q, r):
                            valid = False
                            break
                if valid:
                    edges.append([p, q])
    return edges
    
