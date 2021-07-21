#!/usr/bin/env sh

ll datasets/cloudtrail-logs/ | wc -l

du -c datasets/cloudtrail-logs/

find datasets/cloudtrail-logs/ -iregex '.*\.gz' -type f | \
    parallel --jobs 500% ./cloudtrail2csv.sh {} >> datasets/all-cloudtrail-logs.csv
