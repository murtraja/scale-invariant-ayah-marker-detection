import numpy as np

def process_result_points(located_points, given_pts=[]):
    points_count = len(located_points)
    print ("length of located points", points_count)
    if points_count == 0:
        return []
    actual_pts = given_pts[:]
    if len(actual_pts) == 0:
        actual_pts.append(located_points[0])
    # distance_min = 10000
    for pt in located_points:
        a = pt[0]
        b = pt[1]
        distance = min([(a-x)**2+(b-y)**2 for (x,y) in actual_pts])
        
        # print("distance", distance)
        if distance < 100:
            # print("skipping", pt)
            continue
        actual_pts.append(pt)
    return actual_pts