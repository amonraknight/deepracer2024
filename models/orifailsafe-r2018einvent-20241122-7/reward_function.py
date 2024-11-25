import math

# static

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
# Must update if the env changes.
TOP_SPEED = 4.0  
IS_CLOCKWISE = False
INTERVAL_TO_TARGET_WAY_POINT = 10
STEP_VALUE = 0.1

previous_progress = 0

def get_direction_in_degree(next_point, prev_point):
	'''
	The speed in the direction of the waypoints.
	'''
	# Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
	track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
	# Convert to degree (-180, 180)
	return math.degrees(track_direction)
	
def get_speed_in_direction(target_direction, heading, speed):
	direction_diff = abs(target_direction - heading)
	if direction_diff > 180:
		direction_diff = 360 - direction_diff
	speed_bonus = math.cos(math.radians(direction_diff)) * speed / TOP_SPEED
	return speed_bonus
	

def reward_function(params):
	'''
	1. Don't run off the track.
	2. Base reward when keeping all wheels on track and not heading towards the opposite way.
	3. Encourage the agent to have a high speed towards a far side way point.
	4. Every step values.
	5. Give as much rewards as the progress made.
	'''
	
	# Read input variables
	x = params['x']
	y = params['y']
	# waypoints = params['waypoints']
	waypoints = OPTIMIZED_WAYPOINTS
	closest_waypoints = params['closest_waypoints']
	heading = params['heading']
	speed = params['speed']
	is_offtrack = params['is_offtrack']
	all_wheels_on_track = params['all_wheels_on_track']
	is_reversed = params['is_reversed'] # if the agent is driving on clock-wise (True) or counter clock-wise (False).
	steps = params['steps']
	progress = params['progress']
	
	reward = 0.0
	# 1. Don't terminate off track.
	if is_offtrack:
		print('Vehicle is off track!')
		return -10.0
		
	# 2. Base reward when keeping all wheels on track and not heading towards the opposite way.
	if all_wheels_on_track and ((IS_CLOCKWISE and is_reversed) or (not IS_CLOCKWISE and not is_reversed)):
		reward += 0.01
	else:
		if not all_wheels_on_track:
			print('The vehicle is having a wheel off track.')
			
		if (IS_CLOCKWISE and not is_reversed) or (not IS_CLOCKWISE and is_reversed):
			print('The vehicle is heading backword.')
		
	# 3. Encourage the agent to have a high speed towards a far side way point. 
	target_way_point_idx = (closest_waypoints[1] + INTERVAL_TO_TARGET_WAY_POINT) % len(waypoints)
	target_way_point = waypoints[target_way_point_idx]
	
	target_direction = get_direction_in_degree(target_way_point, [x, y])
	speed_bonus = get_speed_in_direction(target_direction, heading, speed)
	print('The speed bonus is %f.' % speed_bonus)
	reward += speed_bonus
	
	# 4. Every step values.
	reward -= STEP_VALUE
	
	# 5. Give as much rewards as the progress made.
	global previous_progress
	progress_bonus = progress - previous_progress
	if progress_bonus > 0:
		progress_bonus = progress_bonus / 5
		reward += progress_bonus
	previous_progress = progress
	
	return float(reward)