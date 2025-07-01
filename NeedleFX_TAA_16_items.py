import struct
import sys
import csv
import os

# TAA parameters and offsets
TARGET_OFFSETS = [0x0, 0x8, 0xC, 0x10, 0x14, 0x20, 0x24, 0x28, 0x29]  # TARGET_1 to TARGET_9 EXCLUDING 7
PARAM_NAMES = ["jitterscale", "sharpnesspower", "baseweight", "velocityVarianceBasedWeightBias",
               "velocityVarianceMin", "VelocityVarianceMax", "CharaStencilMask", "LiteMode"]
BASE_ADDRESS = 0xEE4
SLOT_OFFSET = 0x1390
NUM_SLOTS = 16
MIN_FILE_SIZE = 0x1347D + 1

def read_csv_values(csv_path):
    """Reads values from CSV."""
    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            headers = next(reader)
            print(f"CSV headers: {headers}")
            if len(headers) != 8 or headers != PARAM_NAMES:
                print(f"Error: Expected headers: {PARAM_NAMES}")
                return None
            row = next(reader, None)
            if not row:
                print("Error: CSV is empty")
                return None
            print(f"CSV data: {row}")
            values = []
            for i, val in enumerate(row):
                if i < 6:  # float
                    try:
                        values.append(float(val))
                    except ValueError:
                        print(f"Error: '{val}' in {PARAM_NAMES[i]} is not a number")
                        return None
                else:  # bool
                    val = val.lower()
                    if val not in ('true', 'false'):
                        print(f"Error: '{val}' in {PARAM_NAMES[i]} is not true/false")
                        return None
                    values.append(1 if val == 'true' else 0)
            print(f"Processed values: {values}")
            return values
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None

def write_values_to_file(file_path, values):
    """Writes values to file and verifies."""
    try:
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist!")
            return
        file_size = os.path.getsize(file_path)
        if file_size < MIN_FILE_SIZE:
            print(f"Error: {file_path} is too small (needs ≥ {MIN_FILE_SIZE} bytes, has {file_size})")
            return
        print(f"Size of {file_path}: {file_size} bytes")
        with open(file_path, 'r+b') as f:
            for slot in range(NUM_SLOTS):
                base = BASE_ADDRESS + slot * SLOT_OFFSET
                for i in range(8):  # 8 values
                    offset = TARGET_OFFSETS[i]
                    address = base + offset
                    f.seek(address)
                    if i < 6:  # float
                        f.write(struct.pack('<f', values[i]))
                    else:  # bool (1 byte)
                        f.write(struct.pack('B', values[i]))
                    f.flush()  # Force write
                    # Verify write
                    f.seek(address)
                    read_val = struct.unpack('<f' if i < 6 else 'B', f.read(4 if i < 6 else 1))[0]
                    print(f"{file_path}, slot {slot}, {PARAM_NAMES[i]} at {hex(address)}: wrote {values[i]}, read {read_val}")
                print(f"Slot {slot} in {file_path}: Wrote to {hex(base)}–{hex(base + 0x28)}")
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Drag CSV and files to cmd!")
        return
    csv_path = sys.argv[1]
    config_files = sys.argv[2:]

    if not csv_path.endswith('.csv'):
        print("First file must be CSV!")
        return
    if len(config_files) > 19:
        print("Maximum 19 files!")
        return

    values = read_csv_values(csv_path)
    if not values:
        return

    for file_path in config_files:
        write_values_to_file(file_path, values)
    print("Write completed!")

if __name__ == "__main__":
    main()