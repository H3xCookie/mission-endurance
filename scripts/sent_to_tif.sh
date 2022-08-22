#!/bin/bash

if [ "$1" = "clean" ]; then 
    ./scripts/clean.sh
fi
./scripts/download.sh
# unzip product.zip
zip_file=$(ls ./data/PRODUCT_ZIP/*.zip)
unzip -q ${zip_file} -d ./data/PRODUCT_ZIP/
safe_file=$(echo ./PRODUCT_ZIP/*.SAFE)
echo $safe_file
# convert .safe format of sentinel_2 sats to .tif GeoTIFF

python3 ./scripts/Sentinel-Scripts-master/sentinel_2/tiff-generator.py ${safe_file}
