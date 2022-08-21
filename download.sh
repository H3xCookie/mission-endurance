#!/bin/bash

start_time="2022-07-01T00:00:00.000Z"
end_time="2022-08-01T00:00:00.000Z"
location="28.2,43.5:27.9,43.7"
password=$(sudo cat .sentinel_api_password)
xml_file="./api_search_results/OSquery-result.xml"
csv_file="./api_search_results/products-list.csv"

# echo "./dhusget.sh -m Sentinel-2 -S $start_time -E $end_time -c"
./dhusget.sh -u vaskonikolov2003 -p $password \
    -m Sentinel-2 -S $start_time -E $end_time -c $location \
    -l 1 -q $xml_file -C $csv_file \
    -o all -D
