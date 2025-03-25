
def lfs_rotation_to_degrees(rotation):
	return round(rotation * 360 / 256 - 180, 1)

def lfs_x_to_meters(x):
	return round(x / 16, 2)

def lfs_y_to_meters(y):
	return round(y / 16, 2)

def lfs_z_to_meters(z):
	return round(z / 4, 2)

def meters_to_lfs_x(meters):
	return int(meters * 16)

def meters_to_lfs_y(meters):
	return int(meters * 16)

def meters_to_lfs_z(meters):
	return int(meters * 4)

def degrees_to_lfs_rotation(degrees):
	return int((degrees + 180) * 256 / 360)

