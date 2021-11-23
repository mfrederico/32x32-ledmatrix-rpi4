#!/bin/bash
cd /home/pi/led/
ls settings.conf
pwd
source settings.conf
php wiring.php > mymatrix.py
sudo python3 clock.py ${data} > output.txt
