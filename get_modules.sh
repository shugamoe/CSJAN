#!/bin/bash  
 
# Bash script for installing most modules for Whiteboard.
 
sudo apt-get update
sudo python3 -m pip install Django==1.8.8
sudo python3 -m pip install django-haystack
sudo python3 -m pip install Whoosh
sudo apt-get install python3-matplotlib
sudo python3 -m pip install selenium
sudo python3 -m pip install bs4
cd pdfminer-master
python2 setup.py install
cd ../