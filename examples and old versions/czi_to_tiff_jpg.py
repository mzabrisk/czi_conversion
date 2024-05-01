import numpy as np
import pathlib
from PIL import Image
from aicspylibczi import CziFile
from pathlib import Path
import os
import tifffile
from tqdm import tqdm

Image.MAX_IMAGE_PIXELS = None

# Path to directory containing the CZI files
# czi_dir = '/Users/mattzabriskie/Library/CloudStorage/Box-Box/MattZ_Work/Clinicians_PIs/LubdhaShah_ViolaRieke/cervical_fus_goat_research/Data/Histology/scanned_slides/2023.08.08'
czi_dir = '/Users/mattzabriskie/Desktop/czi_conversion/czi_files'

# create directory to save tiff files
tiff_dir = os.path.join(czi_dir, 'tiff_files')
os.makedirs(tiff_dir, exist_ok=True)

# create directory to save jpg files
jpg_dir = os.path.join(czi_dir, 'jpg_files')
os.makedirs(jpg_dir, exist_ok=True)

# Get all files in directory ending with '.czi'
czi_files = [file for file in os.listdir(czi_dir) if file.endswith('.czi')]

# Loop over all files in the directory
for filename in tqdm(czi_files, desc="Converting files"):

    # check to see if the CZI has already been converted to TIFF
    if os.path.isfile(os.path.splitext(os.path.join(tiff_dir, filename))[0] + ".tiff"):
                print("A TIFF file already exists for %s" % filename)

    # if no TIFF, create TIFF from CZI
    else:
        # Construct the full file path
        czi_file = os.path.join(czi_dir, filename)
        print(filename)

        try:
            # Try to read the CZI file
            czi = CziFile(pathlib.Path(czi_file))

            czi_data = czi.read_mosaic(C=0, scale_factor=1)

        except Exception as e:
            print(f"File {filename} raised an error during processing: {str(e)}. Continuing with next file.")        
            continue
            
        # Construct the output file path (change the extension to .tiff)
        tiff_file = os.path.join(tiff_dir, os.path.splitext(filename)[0] + '.tiff')
        
        # Save as a TIFF file
        tifffile.imsave(tiff_file, czi_data)

    # check to see if the TIFF has already been converted to JPG
    if os.path.isfile(os.path.splitext(os.path.join(tiff_dir, filename))[0] + ".jpg"):
                print("A JPG file already exists for %s" % filename)

    # if no JPG, create JPG from TIFF
    else:
        # construct jpeg outfile path
        jpg_file = os.path.join(jpg_dir, os.path.splitext(filename)[0] + '.jpg')
        try:
            im = Image.open(os.path.join(tiff_dir, os.path.splitext(filename)[0] + '.tiff'))
            print("Generating jpeg for %s" % filename)
            im.thumbnail(im.size)
            im.save(jpg_file, "JPEG", quality=50)
        except Exception as e:
                print(e)

print("All CZI files have been converted to TIFF.")
print("All TIFF files have been converted to JPG.")
