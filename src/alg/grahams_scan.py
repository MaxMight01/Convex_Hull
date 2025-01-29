import numpy as np

def is_right_turn(p, q, r):
    my_array = np.array([[1, p[0], p[1]],
                      [1, q[0], q[1]],
                      [1, r[0], r[1]]])
    det = np.linalg.det(my_array)
    if det >= 0:
        return False
    return True

def x_value(point):
    return point[0]

def ConvexHull(point_list):
    point_list = sorted(point_list, key = x_value)
    if len(point_list) > 1:
        upper_hull = [point_list[0], point_list[1]]
        for i in range(2, len(point_list)):
            upper_hull.append(point_list[i])
            while len(upper_hull) > 2 and not is_right_turn(upper_hull[-3], upper_hull[-2], upper_hull[-1]):
                del upper_hull[-2]

        lower_hull = [point_list[-1], point_list[-2]]
        for j in range(len(point_list)-3, -1, -1):
            lower_hull.append(point_list[j])
            while len(lower_hull) > 2 and not is_right_turn(lower_hull[-3], lower_hull[-2], lower_hull[-1]):
                del lower_hull[-2]

        # del lower_hull[-1]
        del lower_hull[0]

    else:
        upper_hull = point_list
        lower_hull = []    
    
    return upper_hull + lower_hull