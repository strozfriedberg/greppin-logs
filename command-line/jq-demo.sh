#!/usr/bin/env sh

ll datasets/cloudtrail-log*

file datasets/cloudtrail-log.gz

gunzip -c datasets/cloudtrail-log.gz > datasets/cloudtrail-log.json

jq 'keys' datasets/cloudtrail-log.json

jq '.Records | type' datasets/cloudtrail-log.json

jq '.Records | length' datasets/cloudtrail-log.json

jq '.Records[0] | keys' datasets/cloudtrail-log.json

( echo "event_time,event_source,source_ip,event_name,event_type,user_agent,resources" && \
    jq '.Records[] | \
    [ .eventTime, .eventSource, .sourceIPAddress, .eventName, .eventType, .userAgent, (.resources | tostring) ] | \
    @csv' | \
    tr -d '\\' | \
    sed -e 's/^"//g' -e 's/"$//g' | \
    csvformat ) > datasets/cloudtrail-log.csv

head -n1 datasets/cloudtrail-log.csv | csvlook

csvstat datasets/cloudtrail-log.csv
