# main.py
#
# Runs the image processing algorithm to count the amount of unburned char.

from core import *
import fuel_config
import os
import os.path

image_path = os.path.join("input", "photo2.png")

# fuel_config.py stores all configuration related to fuels
fuel = fuel_config.fuels["coffee husk"]

# tweak the configuration here if you need to
# example:
# fuel["PELLET_UPPER"] = 40

# Add masks to the image if needed
masks = []
masks.append(CircleMask(350.0, 240.0, 250.0, True))

# ***This needs to be updated for every image!***
#
# For now: use Photoshop/GIMP to measure the distance in pixels
# between two points in the image that you know the real distance
# of.
scale_factor = 59.5 / 480.0 # cm / px

run_analysis(image_path, scale_factor, fuel, masks)