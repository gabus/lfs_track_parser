import json
import struct
import sys
import argparse
from lfs_object_types import OBJECT_TYPES
from converters import lfs_x_to_meters, lfs_y_to_meters, lfs_z_to_meters, lfs_rotation_to_degrees

# Create the argument parser
parser = argparse.ArgumentParser(description="Process to encode json objects into .lyt track")

# Add the arguments
parser.add_argument('-i', '--input_file', type=str, required=True, help='json objects file destination')
parser.add_argument('-o', '--output_file', type=str, required=True, help='Path where the .lyt should be saved')

# Parse the command line arguments
args = parser.parse_args()

def parse_header(data):
	"""
		HEADER BLOCK :
			6     char    0       LFSLYT              : do not read file if no match
			1     byte    6       version             : do not read file if > 0
			1     byte    7       revision            : do not read file if > 252
			1     word    8       num added objects   : number of OBJECT BLOCKS
			1     byte    10      laps                : number
			1     byte    11      flags               : 7 in new files  - see NOTE4
		"""

	b_lfslyt = struct.unpack('6s', data[0:6])
	signature = b''.join(b_lfslyt).decode('utf-8')  # LFSLYT signature
	# version = struct.unpack('B', data[6:7])[0]  # version
	# revision = struct.unpack('B', data[7:8])[0]  # revision
	# b_number_of_objects = struct.unpack('H', data[8:10])
	# s_number_of_objects = ''.join(map(str, b_number_of_objects)) # number of objects
	# laps = struct.unpack('B', data[10:11])  # laps
	# flags = struct.unpack('B', data[11:12])  # flags

	version, revision, objects_count, laps, flags = struct.unpack('BBHBB', data[6:12])
	return {
		'signature': signature,
		'version': version,
		'revision': revision,
		'objects_count': objects_count,
		'laps': laps,
		'flags': flags,
	}


def decode_entry(data):
	"""
	OBJECT BLOCK :
		1     short   0       X                   : position (1 metre = 16)
		1     short   2       Y                   : position (1 metre = 16)
		1     byte    4       Zbyte               : height (1m = 4) - see NOTE3
		1     byte    5       Flags               : various         - see NOTE1
		1     byte    6       Index               : object index    - see NOTE1/5
		1     byte    7       Heading             : heading         - see NOTE2
	"""

	# Unpack position (float), rotation (float), type (int), attributes (int)
	unpacked_data = struct.unpack('<hhBBBB', data[:8])
	x, y, z, flag, object_type, rotation = unpacked_data

	if object_type not in OBJECT_TYPES:
		raise ValueError(f"Unknown object type: {object_type}")

	return {
		'position': {'x': lfs_x_to_meters(x), 'y': lfs_y_to_meters(y), 'z': lfs_z_to_meters(z)},
		'rotation': lfs_rotation_to_degrees(rotation),
		'type': OBJECT_TYPES[object_type],
	}




# Define a function to decode the entire data stream
def decode_data(data):
	entries = []
	header_offset = 12  # Skip the header
	entry_size = 8  # Size of each individual entry in bytes

	header = parse_header(data[:header_offset])

	for i in range(header_offset, len(data), entry_size):
		entry_data = data[i:i + entry_size]
		decoded_entry = decode_entry(entry_data)
		entries.append(decoded_entry)

	return header, entries


if __name__ == "__main__":
	# python3 qwen2_decoder.py AU1_FG2024_03.lyt
	track_file = sys.argv[1]

	with open(args.input_file, "rb") as fb:
		data = fb.read()

		header, decoded_entries = decode_data(data)
		print(header)

		with open(args.output_file, "w") as f:
			f.write(json.dumps(decoded_entries, indent=4))
