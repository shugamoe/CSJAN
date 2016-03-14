#!/bin/bash  
 
# Bash script for installing most modules for Whiteboard.
 
apt-get update
pip install Django==1.8.8
python3 –m pip install django-haystack
pip install --user Whoosh
apt-get build-dep python-matplotlib
apt-get install python3-matplotlib
python3 -m pip install --user selenium
python3 -m pip install --user bs4
