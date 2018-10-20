'''
Downloads a static map image from a remote third-party server
'''

from PIL import Image

from requests import *

__author__ = "S7uXN37"
__license__ = "MIT"
__copyright__ = "Copyright 2018, Marc Himmelberger"

def get_map(x, y, size, maxPxSize, aspect=None):
	'''
	Download map from Tyler-StaticMap-API
	all arguments must be in degrees
	'''
	if aspect == None:
		aspect = (size[0] / size[1])

	for zoom in range(19,0,-1): #Start zoomed in, zoom out until px size is acceptable
		degPerPx = 0.01084 * pow(2, 7 - zoom) # based on measuring

		width = int(size[0] / degPerPx)
		height = int(width / aspect)

		if width * height < maxPxSize:
			break

	url = "https://tyler-demo.herokuapp.com/?lat={}&lon={}&zoom={}&width={}&height={}".format(y,x,zoom,width,height)
	print("Querying server: {}".format(url))
	resp = get(url, stream=True)
	if resp.status_code == 200:
		with open('.temp_map.png', 'wb') as f:
       			for block in resp:
        			f.write(block)
	print("Done!")
	return Image.open('.temp_map.png')
