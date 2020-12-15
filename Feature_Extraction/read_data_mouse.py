import pandas as pd
import numpy as np

def velocity(array):
	array = np.array(array)
	return np.sum(np.abs(array[1:] - array[0:-1])) / len(array)

def read_data_mouse(segment_size=10):

	# STEP A: Read raw data
	data = pd.read_csv('2020_12_06.csv', delimiter=',')

	# Date,Time,Action,PosX,PosY,Button
	times = list(data['Time'])
	x, y, b = data['PosX'], data['PosY'], data['Button']
	times_seconds = []
	day_start = data['Date'][0]
	for i, t in enumerate(times):
		split = t.split(':')
		if len(split)==3:
			seconds = float(split[0]) * 3600 + float(split[1]) * 60 + float(split[2].replace(',', '.'))
			times_seconds.append(seconds)
		else:
			return
			print('Problem Reading Data')


	# STEP B: Get features
	start = times_seconds[0]
	features = []
	segment_centers = []
	while start + segment_size < times_seconds[-1]:
		end = start + segment_size

		cur_x = [ix for i, ix in enumerate(x) if times_seconds[i] >=start and times_seconds[i] <= end]
		cur_y = [iy for i, iy in enumerate(y) if times_seconds[i] >=start and times_seconds[i] <= end]
		cur_b = [ib for i, ib in enumerate(b) if times_seconds[i] >=start and times_seconds[i] <= end]

		velocity_x = velocity(cur_x)
		velocity_y = velocity(cur_y)

		features.append([velocity_x, velocity_y])
		segment_centers.append(start + segment_size / 2)

		start += segment_size

	features = np.array(features)
	return features, segment_centers, day_start

f, t, start = read_data_mouse()
print(f)
print(t)