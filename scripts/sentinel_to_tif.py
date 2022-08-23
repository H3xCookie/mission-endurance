import sys
import os
from subprocess import run 
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--deep_clean", action="store_true")
parser.add_argument("--clean", action="store_true")

args = parser.parse_args()

if args.deep_clean:
    if input("do u really want to delete everything!!! y/n").lower() == "y":
        os.system("./scripts/deep_clean.sh")
        # download .zip files to the ./data/PRODUCT_ZIP folder
        os.system("./scripts/download.sh")

if args.clean:
    os.system("./scripts/clean.sh")

os.chdir("/home/vasil/mission-endurance/")
all_files = os.listdir("./data/PRODUCT_ZIP/")
zip_files = []
for name in all_files:
    extension = name.split(".")[-1]
    if extension == "zip":
        zip_files.append(name)
    
# convert .zip files to ./data/OUTPUT_TIF/<path>_PROCESSED/merged.tif
tiff_image_filenames = []
for zip_name in zip_files:
    zip_name_no_ext = "".join(zip_name.split(".")[:-1])
    full_zip_path = os.path.join(os.path.join("./data/PRODUCT_ZIP", zip_name))
    os.system(f"python3 ./scripts/Sentinel-Scripts-master/sentinel_2/tiff-generator.py {full_zip_path}")
    tiff_name = f"./data/OUTPUT_TIF/{zip_name_no_ext}_PROCESSED/merged.tif" 
    os.system(f"rm -r ./data/OUTPUT_TIF/{zip_name_no_ext}.SAFE")
    os.system(f"rm -r ./data/OUTPUT_TIF/{zip_name_no_ext}_PROCESSED/IMAGE_DATA/")

    tiff_image_filenames.append(tiff_name)

print("tif filenames: ")
print(tiff_image_filenames)

