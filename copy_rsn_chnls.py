import os
import shutil
import sys
from glob import glob


def file_is_locked(filepath):
    """Check if a file is locked by trying to open it in append mode."""
    try:
        with open(filepath, 'ab') as _:
            return False
    except IOError:
        return True


def move_files(source_dir, dest_base_dir):
    # Loop through all files in the source directory
    dirs_list = [name for name in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, name))]
    print(dirs_list)
    for dirfilename in dirs_list:
        print(dirfilename)

        ptrn = os.path.join(source_dir, dirfilename, "*.ts")
        print(ptrn)
        print(glob(ptrn))
        for filename in glob(os.path.join(source_dir, dirfilename, "*.ts")):
            print(filename)
            src_file_path = os.path.join(source_dir, filename)

            # Skip the file if it's locked/being written to
            if file_is_locked(src_file_path):
                print(f"File is currently in use or locked: {filename}")
                continue

            # Extract details from the file name
            parts = os.path.basename(filename).split("__")[0].split('_')
            channel_name = parts[0]

            year = parts[1]
            month = parts[2]
            day = parts[3]

            # Construct the destination directory path
            print(dest_base_dir)
            dest_dir = os.path.join(dest_base_dir, year, f"{year}_{month}", f"{year}_{month}_{day}", channel_name)
            print(dest_dir)

            # Ensure the destination directory exists
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            # Construct the destination file path

            dest_file_path = os.path.join(dest_dir, os.path.basename(filename))

            try:
                # Move the file
                print(f"Moving {filename} to {dest_file_path}")
                shutil.move(src_file_path, dest_file_path)
            except Exception as e:
                # This block executes if an error occurred in the try block
                print(f"With {filename} an error occurred: {e}")


def main():
    # Check if the correct number of arguments are passed
    if len(sys.argv) != 3:
        print("Usage: python script.py <source_dir> <dest_base_dir>")
        sys.exit(1)

    # Assign command-line arguments to variables
    source_dir = sys.argv[1]
    dest_base_dir = sys.argv[2]

    # Define the source and destination base directories
    # source_dir = 'Z:\\rec'
    # dest_base_dir = 'Z:\\RussiaContentRecords'

    move_files(source_dir, dest_base_dir)


if __name__ == "__main__":
    main()
