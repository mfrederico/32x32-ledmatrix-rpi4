#!/bin/bash

# Make sure you get a weatherapi.com key and just stick it here like:
# key=yourapikeygoeshere
# zip=yourzipcodegoeshere
# data=wheretostoredatafiles /home/pi/data/

source /home/pi/weatherapi.key
curl -s "https://api.weatherapi.com/v1/current.json?key=${key}&q=${zip}&aqi=no" > ${data}/current_weather.json
wget -q -O ${data}/current.png https:$(cat ${data}/current_weather.json | jq -r -c ".current .condition .icon")
convert -resize 32x32 ${data}/current.png ${data}/current-32x32.png
convert -resize 16x16 ${data}/current.png ${data}/current-16x16.png
convert -resize 8x8 ${data}/current.png ${data}/current-8x8.png
