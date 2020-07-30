#!/usr/bin/python3

from math import sin, cos, sqrt, atan2, radians


def distance(lat1, lon1, lat2, lon2):
	# approximate radius of earth in km
	R = 6373.0

	lat1 = radians(lat1)
	lon1 = radians(lon1)
	lat2 = radians(lat2)
	lon2 = radians(lon2)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	return R * c

def gridsquare(lat, lon):
	precision = 3

	A = ord("A")
	a = divmod(lon + 180, 20)
	b = divmod(lat + 90, 10)
	maiden = chr(A + int(a[0])) + chr(A + int(b[0]))
	lon = a[1] / 2.0
	lat = b[1]
	i = 1
	while i < precision:
		i += 1
		a = divmod(lon, 1)
		b = divmod(lat, 1)
		if not (i % 2):
			maiden += str(int(a[0])) + str(int(b[0]))
			lon = 24 * a[1]
			lat = 24 * b[1]
		else:
			maiden += chr(A + int(a[0])) + chr(A + int(b[0]))
			lon = 10 * a[1]
			lat = 10 * b[1]

	if len(maiden) >= 6:
		maiden = maiden[:4] + maiden[4:6].lower() + maiden[6:]

	return maiden

def location(maiden):
	if not isinstance(maiden, str):
		raise TypeError("Maidenhead locator must be a string")

	maiden = maiden.strip().upper()

	N = len(maiden)
	if not 8 >= N >= 2 and N % 2 == 0:
		raise ValueError("Maidenhead locator requires 2-8 characters, even number of characters")

	Oa = ord("A")
	lon = -180.0
	lat = -90.0
	# %% first pair
	lon += (ord(maiden[0]) - Oa) * 20
	lat += (ord(maiden[1]) - Oa) * 10
	# %% second pair
	if N >= 4:
		lon += int(maiden[2]) * 2
		lat += int(maiden[3]) * 1
	# %%
	if N >= 6:
		lon += (ord(maiden[4]) - Oa) * 5.0 / 60
		lat += (ord(maiden[5]) - Oa) * 2.5 / 60
	# %%
	if N >= 8:
		lon += int(maiden[6]) * 5.0 / 600
		lat += int(maiden[7]) * 2.5 / 600

	return lat, lon
