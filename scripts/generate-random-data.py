BEGIN = """
{ 
	"frames": [
"""

FRAME_TEMPLATE = """
			{	"time": %(frame_time)f,
				"accelerometer": {
					"x": %(accel_x)f,
					"y": %(accel_y)f,
					"z": %(accel_z)f
				},
				"gyroscope": {
					"x": %(gyro_x)f,
					"y": %(gyro_y)f,
					"z": %(gyro_z)f
				},
				"location": {
					"latitude": %(loc_lat)f,
					"longitude": %(loc_long)f
				},
				"velocity": %(velocity)f
			},
"""

END = """
		],
	"slow-motion-bracket": {
		"startTime": 30.00,
		"endTime": 50.00
	}
}
"""

NUMBER_OF_FRAMES = 1000
MS_FRAMES = 1000

import random

print BEGIN

frame_time = 0.0
for frame_counter in range(NUMBER_OF_FRAMES):
	accel_x = random.random() * 180
	accel_y = random.random() * 180
	accel_z = random.random() * 180
	gyro_x = random.random() * 10
	gyro_y = random.random() * 10
	gyro_z = random.random() * 10
	loc_lat = random.random() * 10
	loc_long = random.random() * 10
	velocity = random.random() * 32
	print FRAME_TEMPLATE % locals()

	# finally increment time
	frame_time += (MS_FRAMES / 1000)

print END