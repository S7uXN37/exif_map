#!/usr/bin/env python3
'''
Generates a map displaying the locations of all images in 'data/'
'''

__author__ = "S7uXN37"
__license__ = "MIT"
__copyright__ = "Copyright 2018, Marc Himmelberger"

import argparse

parser = argparse.ArgumentParser(description='Creates map showing images in \'data/\'')
parser.add_argument('--coast', dest='draw_coast', action='store_const', const=True, default=False, help='Draw coastlines')
parser.add_argument('--labels', dest='draw_labels', action='store_const', const=True, default=False, help='Draw labels for each image')
parser.add_argument('--no-save', dest='save', action='store_const', const=False, default=True, help='Don\'t save the finished map')
args = parser.parse_args()

DRAW_LABELS = args.draw_labels
DRAW_COASTLINES = args.draw_coast
SAVE_MAP = args.save

# Console colors
W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green
O = '\033[33m'  # orange
B = '\033[34m'  # blue
P = '\033[35m'  # purple
C = '\033[36m'  # cyan
GR = '\033[37m' # gray


print(B + "Loading images..." + W)
from read_data import images, locations, filenames
print(G + "Done!" + W)

from tyler_map import *

print(B + "Initialising..." + W)
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

fig = plt.figure(figsize=(10, 6))

#avgX = 0.0
#avgY = 0.0
#for l in locations:
#	avgX += l[0]
#	avgY += l[1]
#avgX /= len(locations)
#avgY /= len(locations)

proj = ccrs.Mercator() # central_longitude=avgY, latitude_true_scale=avgX)
ax = plt.axes(projection=proj)

if DRAW_COASTLINES:
	ax.coastlines(resolution='10m', color='black', linewidth=1)

y = [l[0] for l in locations]
x = [l[1] for l in locations]
plt.plot(x,y, '-o', transform=ccrs.Geodetic())

# Draw labels
if DRAW_LABELS:
	for l in locations:
		plt.text(l[1], l[0], filenames[locations.index(l)], transform=ccrs.Geodetic())

# Get data size
xmin, xmax, ymin, ymax = plt.axis()

# Transform to coordinates
lonMin, latMin = ccrs.Geodetic().transform_point(xmin, ymin, proj)
lonMax, latMax = ccrs.Geodetic().transform_point(xmax, ymax, proj)

# calculate Midpoint and size of map
lonMid = (lonMin + lonMax) / 2
latMid = (latMin + latMax) / 2
size = (abs(lonMax-lonMin), abs(latMax-latMin))

# Get display size
bbox = ax.get_window_extent()
pxSize = abs(bbox.x0-bbox.x1) * abs(bbox.y0-bbox.y1)

aspect = abs(xmax-xmin) / abs(ymax-ymin)
map = get_map(lonMid, latMid, size, pxSize, aspect=aspect)

print(G + "Displaying..." + W)
try:
	plt.imshow(map, extent=[xmin, xmax, ymin, ymax], interpolation="bilinear")
	if SAVE_MAP:
		plt.savefig("map.png")
	plt.show()
except KeyboardInterrupt:
	print()
except Exception as e:
	print(e)
finally:
	print(B + "Cleaning up!" + W)
	from os import system
	system("rm .temp_map.png")
	quit()
