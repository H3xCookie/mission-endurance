#!/bin/bash

start_time="2022-07-01T00:00:00.000Z"
end_time="2022-08-01T00:00:00.000Z"
location="43.7,27.1:43.8,27.2"
password="monke"

# echo "./dhusget.sh -m Sentinel-2 -S $start_time -E $end_time -c"
./dhusget.sh -u vaskonikolov2003 -p $password -m Sentinel-2 -S $start_time -E $end_time -c $location
