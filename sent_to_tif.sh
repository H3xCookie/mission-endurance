# ./clean.sh
# ./download.sh
# convert .safe format of sentinel_2 sats to .tif GeoTIFF
file=$(ls ./PRODUCT)
echo $file
# python3 ./Sentinel-Scripts-master/sentinel_2/tiff-generator.py ${file} 

# run the main script
python3 ./src/main.py ${file} 


