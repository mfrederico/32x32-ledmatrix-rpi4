#!/bin/bash

# We will be using the "jq" command to parse json on the command line
# apt get install jq
# apt get install imagemagick

source /home/pi/led/settings.conf

curl -s "https://api.weatherapi.com/v1/current.json?key=${key}&q=${zip}&aqi=no" > /tmp/current-weather.json
mv /tmp/current-weather.json ${data}/current_weather.json

wget -q -O /tmp/current.png https:$(cat ${data}/current_weather.json | jq -r -c ".current .condition .icon")
convert -resize 32x32 /tmp/current.png ${data}/current-32x32.png
convert -resize 16x16 /tmp/current.png ${data}/current-16x16.png
convert -resize 8x8 /tmp/current.png ${data}/current-8x8.png
