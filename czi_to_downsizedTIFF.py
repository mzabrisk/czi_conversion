import os
import czifile
import tifffile
from tqdm import tqdm
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

# Path to directory containing the CZI files
czi_dir = input("what is file locations?")

# Directory to save the TIFF files
# creates subfolder within directory 'TIFF files'
tiff_dir = os.path.join(czi_dir, 'tiff_files')
os.makedirs(tiff_dir, exist_ok=True)

max_width = 10000  # Maximum width after downsampling
max_height = 10000  # Maximum height after downsampling

max_file_size = 1000000000

# Get all files in directory ending with '.czi'
czi_files = [file for file in os.listdir(czi_dir) if file.endswith('.czi')]


# Loop over all files in the directory
for filename in tqdm(czi_files, desc="Converting files"):
    # Construct the full file path
    czi_file = os.path.join(czi_dir, filename)

    # check to see if file size < 1GB
    file_size = os.path.getsize(czi_file)

    # if file is small enough, proceed with conversion and downsampling
    if file_size < max_file_size:

        try:
            # Try to read the CZI file
            with czifile.CziFile(czi_file) as czi:
                img_data = czi.asarray()

        except Exception as e:
            print(f"File {filename} raised an error during processing: {str(e)}. Continuing with next file.")        
            continue
            
        # Construct the output file path (change the extension to .tiff)
        tiff_file = os.path.join(tiff_dir, os.path.splitext(filename)[0] + '.tiff')
        
        # Save as a TIFF file
        tifffile.imsave(tiff_file, img_data)

        try:
        #downsample and save over original tiff file
            with Image.open(tiff_file) as img:
                # Resize the image while preserving aspect ratio
                img.thumbnail((max_width, max_height))
                # Save the resized image
                img.save(tiff_file)
            
            print(f"Successfully downsampled {filename}.")
        
        except Exception as e:
            print(f"An error occurred while processing {filename}: {e}. Continuing with next file.")
    
    # if file is too large, skip.
    else:
        print(f"{filename} exceeds max file size. Skipping.")

print("All CZI files have been converted to TIFF and downsampled.")
