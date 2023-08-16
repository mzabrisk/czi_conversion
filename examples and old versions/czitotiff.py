import os
import czifile
import tifffile
from tqdm import tqdm

# Path to directory containing the CZI files
czi_dir = '/Users/mattzabriskie/Desktop/czi_file/czi_files'

# Directory to save the TIFF files
# creates subfolder within directory 'TIFF files'
tiff_dir = os.path.join(czi_dir, 'TIFF files')
os.makedirs(tiff_dir, exist_ok=True)

# Get all files in directory ending with '.czi'
czi_files = [file for file in os.listdir(czi_dir) if file.endswith('.czi')]

# Loop over all files in the directory
for filename in tqdm(czi_files, desc="Converting files"):
    # Construct the full file path
    czi_file = os.path.join(czi_dir, filename)

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

print("All CZI files have been converted to TIFF.")
