from instagram.client import InstagramAPI
import hmac
from hashlib import sha256
import re
import csv
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import time


access_token = raw_input("Enter Access Token: ")
client_id = raw_input("Enter Client Id: ")
client_secret= raw_input("Enter Client Secret: ")

ips = raw_input("Enter IP: ")
signature = hmac.new(client_secret, ips, sha256).hexdigest()
header = '|'.join([ips, signature])

j = 0
i = 0

timestr = time.strftime("%Y%m%d-%H%M%S")
tags = raw_input("Enter Tag that you want to Map: ")
api = InstagramAPI(access_token = access_token,client_secret=client_secret,client_ips=ips)
print api.tag(tags).media_count

lats, lons = [], []

while i < 4:
	m = api.tag_recent_media(count=40,tag_name=tags,max_tag=j)
	match = re.search(r'max_tag_id=(\d+)',m[1])
	j=match.group(1)
	for k in m[0]:
		try:
			a = str(k.location.point.latitude) + ',' + str(k.location.point.longitude)
			print a
			lats.append(k.location.point.latitude)
			lons.append(k.location.point.longitude)
		except Exception,e:
			continue
	i = i + 1

map = Basemap(projection='robin', resolution = 'l', area_thresh = 1000.0,
              lat_0=-90, lon_0=90)
map.drawcoastlines()
map.drawcountries()
map.fillcontinents(color = 'gray')
map.drawmapboundary()
map.drawmeridians(np.arange(0, 360, 30))
map.drawparallels(np.arange(-90, 90, 30))
 
x,y = map(lons, lats)
map.plot(x, y, 'ro', markersize=6)
 
plt.show()
