import os
import re

def convert_size_to_bytes(size_str):
    size_str = size_str.strip().lower()
    size_match = re.match(r'^(\d+(?:\.\d+)?)\s*([kmgtp]?b)$', size_str)
    if size_match:
        size, unit = size_match.groups()
        size = float(size)
        units = {
            'b': 1,
            'kb': 1024,
            'mb': 1024**2,
            'gb': 1024**3,
            'tb': 1024**4,
            'pb': 1024**5,
        }
        return int(size * units.get(unit, 1))
    else:
        raise ValueError("Invalid size format. Please use formats like '1MB', '3.5MB', '100kB'.")

def slice_file(input_file, output_directory, slice_size=None, num_slices=None):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(input_file, 'rb') as infile:
        file_extension = os.path.splitext(input_file)[1]
        file_type = file_extension.strip('.') if file_extension else 'bin'
        data = infile.read()
        file_size = len(data)

    if slice_size is not None:
        slice_size = convert_size_to_bytes(slice_size)
        slice_number = 1
        start = 0
        while start < file_size:
            end = min(start + slice_size, file_size)
            slice_data = data[start:end]
            output_file = os.path.join(output_directory, f'slice_{slice_number}.bin')
            with open(output_file, 'wb') as outfile:
                outfile.write(slice_data)
            start = end
            slice_number += 1

    elif num_slices is not None:
        slice_size = file_size // num_slices
        start = 0
        for slice_number in range(1, num_slices + 1):
            end = start + slice_size
            if slice_number == num_slices:
                end = file_size  # Make sure the last slice includes any remaining data
            slice_data = data[start:end]
            output_file = os.path.join(output_directory, f'slice_{slice_number}.bin')
            with open(output_file, 'wb') as outfile:
                outfile.write(slice_data)
            start = end

def join_sliced_files(input_directory, output_file, remove_sliced_files=False):
    file_list = sorted(os.listdir(input_directory), key=lambda x: int(re.search(r'\d+', x).group()))
    with open(output_file, 'wb') as outfile:
        for filename in file_list:
            file_path = os.path.join(input_directory, filename)
            with open(file_path, 'rb') as infile:
                data = infile.read()
                outfile.write(data)

    if remove_sliced_files:
        for filename in os.listdir(input_directory):
            file_path = os.path.join(input_directory, filename)
            os.remove(file_path)


# # Example usage:
# input_file = 'test/test.mp4'  # Input file of any type
# output_directory = 'test/sliced_files'  # Directory to store sliced files
# slice_size = None  # You can specify size as '1MB', '3.5MB', '100kB', etc.
# num_slices = 10
# 
# slice_file(input_file, output_directory, slice_size, num_slices)
# 
# # Rejoin the sliced files and remove them after joining
# output_file = 'test/test_out.mp4'  # Output file with the same file type
# join_sliced_files(output_directory, output_file, remove_sliced_files=False)
