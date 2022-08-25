#!/bin/bash

start_time="2022-07-01T00:00:00.000Z"
end_time="2022-08-01T00:00:00.000Z"
location="28.2,43.5:27.9,43.7"
password=$(sudo cat ./.sentinel_api_password)
xml_file="./api_search_results/OSquery-result.xml"
csv_file="./api_search_results/products-list.csv"
n_photos=10
# get number of results
./scripts/dhusget.sh -u vaskonikolov2003 -p $password \
    -m Sentinel-2 -S $start_time -E $end_time -c $location -F 'cloudcoverpercentage:[0 TO 10]'\
    -l $n_photos -q $xml_file -C $csv_file \

n_results=$(wc -l < ./api_search_results/products-list.csv)
echo "num of results is"
echo $n_results
if [ $n_results -lt 1 ]; then
    echo "there are no results found"
    echo "num of results"
    echo $n_results
    exit -1
fi

# # echo "./dhusget.sh -m Sentinel-2 -S $start_time -E $end_time -c"
# ./scripts/dhusget.sh -u vaskonikolov2003 -p $password \
#     -m Sentinel-2 -S $start_time -E $end_time -c $location -F 'cloudcoverpercentage:[0 TO 10]'\
#     -l $n_photos -q $xml_file -C $csv_file \
#     -o product -O ./data/PRODUCT_ZIP/ -D

# # autoremove useless files
# rm -r ./logs
# rm ./failed_MD5_check_list.txt
