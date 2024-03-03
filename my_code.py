import random
import numpy

def shoelace_method(polygon):
    result = 0
    for i in range(0,len(polygon)):
        j = (i + 1) % len(polygon)
        result = result + (polygon[i][0] * polygon[j][1]) - (polygon[j][0] * polygon[i][1])
    result = abs(result) / 2
    return result

def print_polygon(polygon):
    area = str(shoelace_method(polygon))
    print(f"Area of polygon {polygon} is {area}.")

def calculate_error_from_polygons(polygon_a,polygon_b,polygon_c):
    area_a = shoelace_method(polygon_a)
    area_b = shoelace_method(polygon_b)
    area_c = shoelace_method(polygon_c)
    return calculate_error_from_areas(area_a,area_b,area_c)

def calculate_error_from_areas(area_a,area_b,area_c):
    avg = (area_a+area_b+area_c)/3
    return abs(avg - area_a) + abs(avg - area_b) + abs(avg - area_c)

def get_point_set(x_bounds,y_bounds,x_divisions = 10,y_divisions = 10):
    return [(x_bounds[0]+a*((x_bounds[1]-x_bounds[0])/x_divisions),
             y_bounds[0]+b*((y_bounds[1]-y_bounds[0])/y_divisions))
            for a in range(0,x_divisions)
            for b in range(0,y_divisions)]

def find_new_point_set(trial_points,trial_errors,x_divisions = 10, y_divisions = 10):
    min_error_index = trial_errors.index(min(trial_errors))
    min_error_point = trial_points[min_error_index]
    lower_xs = [p[0] for p in trial_points if p[0] < min_error_point[0]]
    upper_xs = [p[0] for p in trial_points if p[0] > min_error_point[0]]
    lower_ys = [p[1] for p in trial_points if p[1] < min_error_point[1]]
    upper_ys = [p[1] for p in trial_points if p[1] > min_error_point[1]]
    diff_x = trial_points[1][0]-trial_points[0][0]
    diff_y = trial_points[1][1]-trial_points[0][1]

    if len(lower_xs) == 0:
        lower_x = min_error_point[0]
    else:
        lower_x = max(lower_xs)

    if len(upper_xs) == 0:
        upper_x = min_error_point[0] + diff_x
    else:
        upper_x = min(upper_xs)

    if len(lower_ys) == 0:
        lower_y = min_error_point[0]
    else:
        lower_y = max(lower_ys)

    if len(upper_ys) == 0:
        upper_y = min_error_point[0] + diff_y
    else:
        upper_y = min(upper_ys)

    return get_point_set((lower_x,upper_x),(lower_y,upper_y),x_divisions,y_divisions)

def find_midpoint(offset,trials=None,error_tolerance=.0000000001):
    if not trials:
        trials = 10000

    #let's start with some sample points, then we'll improve upon these points.
    working_points = get_point_set((0,20),(0,10),20,10)
    trial_points = []
    trial_errors = []
    trial_weights = []

    for t in range(0,trials):
        for p in working_points:
            perform_trial(offset, p, trial_points, trial_errors, trial_weights)
        working_points = find_new_point_set(trial_points,trial_errors,4,4)
        if min(trial_errors) < error_tolerance:
            break

    min_error = min(trial_errors)
    optimal_point = trial_points[trial_errors.index(min_error)]
    print(f'Optimal point is: {optimal_point}')
    perform_trial(offset, optimal_point, trial_points, trial_errors, trial_weights)
    return optimal_point

def perform_trial(offset, cp, trial_points, trial_errors, trial_weights):
    if offset <= 10:
        perform_trial_0_10(offset, cp, trial_points, trial_errors, trial_weights)

def perform_trial_0_10(offset, cp, trial_points, trial_errors, trial_weights):
    #define the vertices of the cake.
    v1 = (0,10)
    v2 = (20,10)
    v3 = (0,0)
    v4 = (20,0)

    #define the points where the cuts will end on the edges, in relation
    #to the offset a from the basis cuts.
    c1 = (10+offset,10)
    c2 = (20-offset,0)
    c3 = (0,0+offset)

    polygon_a = [c3, v1, c1, cp]
    polygon_b = [c1, v2, v4, c2, cp]
    polygon_c = [c2, v3, c3, cp]
    area_a = shoelace_method(polygon_a)
    area_b = shoelace_method(polygon_b)
    area_c = shoelace_method(polygon_c)
    error = calculate_error_from_areas(area_a, area_b, area_c)
    trial_points.append(cp)
    trial_errors.append(error)
    trial_weights.append(1 / error)
    #print_polygon(polygon_a)
    #print_polygon(polygon_b)
    #print_polygon(polygon_c)
    #print()

#print_polygon([(0,0),(0,10),(10,10),(10,20/3)])
#print_polygon([(10,10),(20,10),(20,0),(10,20/3)])
#print_polygon([(20,0),(0,0),(10,20/3)])

midpoints = [find_midpoint(a/100,100000) for a in range(0,1001)]
reflection = [(20-p[0],p[1]) for p in midpoints]
reflection.reverse()
midpoints = midpoints + reflection
numpy.savetxt('midpoints.csv', midpoints, delimiter='\t')
midpoints_area = shoelace_method(midpoints)
print(f'The area contained by the midpoints is {midpoints_area}')