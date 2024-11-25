import math

# static
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
	waypoints = params['waypoints']
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
		reward += 0.1
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