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
parser.add_argument('--save', dest='save', action='store_const', const=True, default=False, help='Save the finished map; disables zoom')
parser.add_argument('--images', dest='images', action='store_const', const=True, default=False, help='Show images when possible')
parser.add_argument('--no-mask', dest='masking', action='store_const', const=False, default=True, help='Leave images rectangular')
args = parser.parse_args()

DRAW_IMAGES = args.images
DRAW_LABELS = args.draw_labels
DRAW_COASTLINES = args.draw_coast
SAVE_MAP = args.save
MASK_CIRCLE = args.masking

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
from read_data import images, masked_images, locations, filenames
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

print(G + "Done!" + W)

if DRAW_COASTLINES:
	ax.coastlines(resolution='10m', color='black', linewidth=1)

y = [l[0] for l in locations]
x = [l[1] for l in locations]

# Draw labels
if DRAW_LABELS:
	for l,f in zip(locations, filenames):
		plt.text(l[1], l[0], f, transform=ccrs.Geodetic())

if DRAW_IMAGES:
	# get width of are to display in data coordinates
	w = [proj.transform_point(l[0], l[1], ccrs.Geodetic())[1] for l in locations]
	width_data = max(w) - min(w)
	# estimate a should-be pixel width
	width_px = 400.0
	# calculate radius of images so they are approx. size_px wide
	size_px = 30
	delta = size_px / width_px * width_data / 2
	# draw images
	print(B + "Drawing images..." + W)
	for i,l in zip(masked_images if MASK_CIRCLE else images, locations):
		pos = proj.transform_point(l[1], l[0], ccrs.Geodetic())
		plt.imshow(i, extent=[pos[0]-delta,pos[0]+delta,pos[1]-delta,pos[1]+delta], zorder=10)
	print(G + "Done!" + W)

plt.plot(x,y, '-o', transform=ccrs.Geodetic())

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
