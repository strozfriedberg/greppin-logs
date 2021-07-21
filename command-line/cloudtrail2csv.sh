#!/usr/bin/env sh

if [ $# -lt 1 ]
then
    echo "::: ERROR: Must supply path to G-Zip compressed CloudTrail log file"
    exit 1
else
    FILEPATH="${1}"
    shift
fi

gunzip -c "${FILEPATH}" | \
    jq '.Records[] | [ .eventTime, .eventSource, .sourceIPAddress, .eventName, .eventType, .userAgent, (.resources | tostring) ] | @csv' | \
    tr -d '\\' | \
    sed -e 's/^"//g' -e 's/"$//g'
