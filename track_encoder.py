import json
import struct
import sys
import argparse
from lfs_object_types import get_object_index
from converters import meters_to_lfs_x, meters_to_lfs_y, meters_to_lfs_z, degrees_to_lfs_rotation

# Create the argument parser
parser = argparse.ArgumentParser(description="Process to decode .lyt tracks into json")

# Add the arguments
parser.add_argument('-i', '--input_file', type=str, required=True, help='.lyt file destination')
parser.add_argument('-o', '--output_file', type=str, required=True, help='Path where the output json should be saved')

# Parse the command line arguments
args = parser.parse_args()


def encode_data(obj):
	x = meters_to_lfs_x(obj['position']['x'])
	y = meters_to_lfs_y(obj['position']['y'])
	z = meters_to_lfs_z(obj['position']['z'])
	rotation = degrees_to_lfs_rotation(obj['rotation'])
	object_type = get_object_index(obj['type'])

	return struct.pack('<hhBBBB', x, y, z, 0, object_type, rotation)


def encode_header(data):
	signature = b'LFSLYT'
	version = 0
	revision = 252
	num_added_objects = len(data)
	laps = 1
	flags = 8

	print(f'{signature=}', f'{version=}', f'{revision=}', f'{num_added_objects=}', f'{laps=}', f'{flags=}')
	return struct.pack('6sBBHBB', signature, version, revision, num_added_objects, laps, flags)


if __name__ == "__main__":
	# python3 encoder.py AU1_FG2024_03.json
	track_file = sys.argv[1]
	file_name = 'AU1_testing_encoding_track'

	with open(args.input_file, "r") as f:
		data = json.loads(f.read())

		# Create the binary LFS layout file (.lyt)
		with open(args.output_file, "wb") as fb:
			encoded_header = encode_header(data)
			print(encoded_header)
			fb.write(encoded_header)

			for obj in data:
				encoded_object = encode_data(obj)
				fb.write(encoded_object)
