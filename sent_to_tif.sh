# ./clean.sh
# ./download.sh
file=$(ls ./PRODUCT)
echo $file
python3 ./Sentinel-Scripts-master/sentinel_2/tiff-generator.py ${file} 

