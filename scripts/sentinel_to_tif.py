import sys
import os
from subprocess import run 
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("-c", "--clean", action="store_true")
parser.add_argument("-d", "--download", action="store_true")

args = parser.parse_args()

if args.clean:
    os.system("./scripts/clean.sh")

if args.download:
    os.system("./scripts/download.sh")

os.chdir("/home/vasil/mission-endurance/")
all_files = os.listdir("./data/PRODUCT_ZIP/")
zip_files = []
for name in all_files:
    extension = name.split(".")[-1]
    if extension == "zip":
        zip_files.append(name)

    
# pass zip filenames to converter from zip to .tif
tiff_image_filenames = []
for zip_name in zip_files:
    zip_name_no_ext = "".join(zip_name.split(".")[:-1])
    full_zip_path = os.path.join(os.path.join("./data/PRODUCT_ZIP", zip_name))
    os.system(f"python3 ./scripts/Sentinel-Scripts-master/sentinel_2/tiff-generator.py {full_zip_path}")
    tiff_name = f"./data/OUTPUT_TIF/{zip_name_no_ext}_PROCESSED/merged.tif" 
    tiff_image_filenames.append(tiff_name)

print(tiff_image_filenames)

