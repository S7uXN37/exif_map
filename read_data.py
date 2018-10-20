'''
Reads all images from 'data/' including their geo location.
Data is accessible after importing in 'images', 'locations' and 'filenames'.
All elements at the same index in these lists correspond to each other.
'''

from PIL import Image
import glob

import exifread as ef

__author__ = "S7uXN37"
__license__ = "MIT"
__copyright__ = "Copyright 2018, Marc Himmelberger"

def to_degrees(data):
    degrees = float(data.values[0].num) / float(data.values[0].den)
    minutes = float(data.values[1].num) / float(data.values[1].den)
    seconds = float(data.values[2].num) / float(data.values[2].den)
    return d + (minutes + (seconds / 60.0) / 60.0)

def getGPS(filename):
    with open(filename, 'rb') as f:
        tags = ef.process_file(f)

        latitude = tags.get('GPS GPSLatitude')
        latitude_ref = tags.get('GPS GPSLatitudeRef')
        longitude = tags.get('GPS GPSLongitude')
        longitude_ref = tags.get('GPS GPSLongitudeRef')

        if latitude and longitude:
            lat_value = to_degrees(latitude)
            lon_value = to_degrees(longitude)
            if latitude_ref.values != 'N':
                lat_value = -lat_value
            if longitude_ref.values != 'E':
                lon_value = -lon_value
        else:
            print('Exif data in "{}" not found; skipping...'.format(filename))
            return None
        return [lat_value, lon_value]
    raise Exception('File could not be read')

images = []
locations = []
filenames = sorted(glob.glob('data_city/*.jpg'))
skipped = []
for filename in filenames:
    im = Image.open(filename)
    gps = getGPS(filename)
    if gps:
        images.append(im)
        locations.append(gps)
    else:
        skipped.append(filename)
# Clean up filenames
for s in skipped:
    del(filenames[filenames.index(s)])
