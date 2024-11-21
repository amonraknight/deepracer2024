'''
20241121
Falk Tandetzky + yang0369
https://github.com/falktan/deepracer
https://github.com/yang0369/AWS_DeepRacer
'''

import math

OPTIMIZED_WAYPOINTS = [
        [3.06664, 0.69989],
        [3.21372, 0.69357],
        [3.36169, 0.6893],
        [3.51032, 0.68657],
        [3.65944, 0.68518],
        [3.80869, 0.68499],
        [3.9577, 0.68593],
        [4.10629, 0.688],
        [4.25437, 0.69122],
        [4.40189, 0.69562],
        [4.54878, 0.70129],
        [4.69495, 0.7083],
        [4.84035, 0.71677],
        [4.9849, 0.7268],
        [5.12852, 0.73849],
        [5.27111, 0.75197],
        [5.41256, 0.76741],
        [5.55265, 0.78511],
        [5.69115, 0.80542],
        [5.82783, 0.82863],
        [5.96225, 0.85532],
        [6.09384, 0.88621],
        [6.22194, 0.92207],
        [6.34568, 0.96381],
        [6.46387, 1.01256],
        [6.57482, 1.06969],
        [6.67653, 1.13638],
        [6.76588, 1.21406],
        [6.83839, 1.3035],
        [6.8965, 1.40041],
        [6.94112, 1.50274],
        [6.96947, 1.60974],
        [6.97707, 1.71948],
        [6.96702, 1.82873],
        [6.94149, 1.93565],
        [6.90175, 2.03894],
        [6.84699, 2.13674],
        [6.77532, 2.22592],
        [6.69013, 2.30621],
        [6.59411, 2.37815],
        [6.48935, 2.44258],
        [6.37761, 2.50053],
        [6.26056, 2.55329],
        [6.13955, 2.60203],
        [6.01585, 2.648],
        [5.89082, 2.69257],
        [5.76067, 2.73919],
        [5.63058, 2.78629],
        [5.5006, 2.83412],
        [5.37081, 2.88295],
        [5.2413, 2.93305],
        [5.11223, 2.98473],
        [4.9838, 3.03838],
        [4.85635, 3.09451],
        [4.73023, 3.15374],
        [4.60596, 3.21695],
        [4.48296, 3.2828],
        [4.36104, 3.35081],
        [4.24006, 3.42061],
        [4.11988, 3.49191],
        [4.00046, 3.56448],
        [3.88179, 3.63809],
        [3.76397, 3.71247],
        [3.64724, 3.7873],
        [3.53105, 3.86073],
        [3.41419, 3.93239],
        [3.29624, 4.00105],
        [3.17677, 4.06545],
        [3.0554, 4.12417],
        [2.93169, 4.17515],
        [2.80549, 4.21581],
        [2.67785, 4.24822],
        [2.5493, 4.27301],
        [2.42021, 4.29067],
        [2.29093, 4.30153],
        [2.16175, 4.30562],
        [2.03303, 4.30283],
        [1.90519, 4.29292],
        [1.7788, 4.27535],
        [1.65459, 4.24957],
        [1.53376, 4.21418],
        [1.41797, 4.16786],
        [1.30974, 4.10893],
        [1.21287, 4.03538],
        [1.13093, 3.94692],
        [1.06435, 3.84609],
        [1.01121, 3.73603],
        [0.96999, 3.61869],
        [0.93956, 3.49541],
        [0.91891, 3.36729],
        [0.90708, 3.23527],
        [0.90334, 3.10018],
        [0.90681, 2.9629],
        [0.91698, 2.82419],
        [0.93341, 2.68483],
        [0.95571, 2.54557],
        [0.98342, 2.40706],
        [1.01626, 2.26986],
        [1.05392, 2.13444],
        [1.09624, 2.00121],
        [1.14311, 1.87057],
        [1.19482, 1.7431],
        [1.25158, 1.61938],
        [1.31382, 1.50015],
        [1.38221, 1.38643],
        [1.45757, 1.27943],
        [1.54096, 1.18072],
        [1.63386, 1.09253],
        [1.7384, 1.01844],
        [1.85098, 0.955],
        [1.97002, 0.90067],
        [2.09459, 0.85453],
        [2.2239, 0.81579],
        [2.35729, 0.78373],
        [2.49419, 0.75767],
        [2.63406, 0.73695],
        [2.77639, 0.72086],
        [2.92074, 0.70874],
        [3.06664, 0.69989]
    ]

RADIUS_FACTOR = 0.3

def dist(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


# thanks to https://stackoverflow.com/questions/20924085/python-conversion-between-coordinates
def rect(r, theta):
    """
    theta in degrees

    returns tuple; (float, float); (x,y)
    """

    x = r * math.cos(math.radians(theta))
    y = r * math.sin(math.radians(theta))
    return x, y


# thanks to https://stackoverflow.com/questions/20924085/python-conversion-between-coordinates
def polar(x, y):
    """
    returns r, theta(degrees)
    """

    r = (x ** 2 + y ** 2) ** .5
    theta = math.degrees(math.atan2(y,x))
    return r, theta


def angle_mod_360(angle):
    """
    Maps an angle to the interval -180, +180.

    Examples:
    angle_mod_360(362) == 2
    angle_mod_360(270) == -90

    :param angle: angle in degree
    :return: angle in degree. Between -180 and +180
    """

    n = math.floor(angle/360.0)

    angle_between_0_and_360 = angle - n*360.0

    if angle_between_0_and_360 <= 180.0:
        return angle_between_0_and_360
    else:
        return angle_between_0_and_360 - 360


def get_waypoints_ordered_in_driving_direction(params):
    # waypoints are always provided in counter clock wise order
    if params['is_reversed']: # driving clock wise.
        # return list(reversed(params['waypoints']))
        return list(reversed(OPTIMIZED_WAYPOINTS))
    else: # driving counter clock wise.
        # return params['waypoints']
        return OPTIMIZED_WAYPOINTS


def up_sample(waypoints, factor):
    """
    Adds extra waypoints in between provided waypoints

    :param waypoints:
    :param factor: integer. E.g. 3 means that the resulting list has 3 times as many points.
    :return:
    """
    p = waypoints
    n = len(p)

    return [[i / factor * p[(j+1) % n][0] + (1 - i / factor) * p[j][0],
             i / factor * p[(j+1) % n][1] + (1 - i / factor) * p[j][1]] for j in range(n) for i in range(factor)]


def get_target_point(params):
    waypoints = up_sample(get_waypoints_ordered_in_driving_direction(params), 20)

    car = [params['x'], params['y']]

    distances = [dist(p, car) for p in waypoints]
    min_dist = min(distances)
    i_closest = distances.index(min_dist)

    n = len(waypoints)

    waypoints_starting_with_closest = [waypoints[(i+i_closest) % n] for i in range(n)]

    r = params['track_width'] * RADIUS_FACTOR

    is_inside = [dist(p, car) < r for p in waypoints_starting_with_closest]
    i_first_outside = is_inside.index(False)

    if i_first_outside < 0:  # this can only happen if we choose r as big as the entire track
        return waypoints[i_closest]

    return waypoints_starting_with_closest[i_first_outside]


def get_target_steering_degree(params):
    tx, ty = get_target_point(params)
    car_x = params['x']
    car_y = params['y']
    dx = tx-car_x
    dy = ty-car_y
    heading = params['heading']
    print('x: %f, y: %f, tx: %f, ty: %f' % (car_x, car_y, tx, ty))

    _, target_angle = polar(dx, dy)

    steering_angle = target_angle - heading

    return angle_mod_360(steering_angle)


def score_steer_to_point_ahead(params):
    best_stearing_angle = get_target_steering_degree(params)
    steering_angle = params['steering_angle']

    error = (steering_angle - best_stearing_angle) / 60.0  # 60 degree is already really bad

    score = 1.0 - abs(error)

    return max(score, 0.01)  # optimizer is rumored to struggle with negative numbers and numbers too close to zero


def reward_function(params):
    reward = score_steer_to_point_ahead(params)
    print('reward: %f' % reward)
    return float(reward)