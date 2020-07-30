#!/usr/bin/python3

import sqlog.geo
import sqlog.sota


#TODO: get this at runtime from DB using MYSQL DESCRIBE command or something like that
fields = ('datetime', 'my_callsign', 'callsign', 'name', 'freq', 'band', 'mode', 'rst_rcvd', 'rst_sent', 'qsl', 'my_qth', 'my_sota_ref', 'my_gridsquare', 'my_lat', 'my_lon', 'qth', 'sota_ref', 'gridsquare', 'lat', 'lon', 'distance', 'remarks')

class QSO(object):
	def __init__(self, **data):
		self.data = data
		self.prepare_fields()

	def prepare_fields(self):
		d = self.data
		self.data = {}
		for field in fields:
			self.data[field] = d.get(field, None)

		if self.data['my_sota_ref'] and not (self.data['my_lat'] and self.data['my_lon'] and self.data['my_qth']):
			my_summit = sqlog.sota.Summit(self.data['my_sota_ref'])
			# Set coordinates based on SOTA
			if not (self.data['my_lat'] and self.data['my_lon']):
				self.data['my_lat'] = my_summit.lat
				self.data['my_lon'] = my_summit.lon
			# Set QTH based on SOTA
			if not self.data['my_qth']:
				self.data['my_qth'] = str(my_summit)

		if self.data['sota_ref'] and not (self.data['lat'] and self.data['lon'] and self.data['qth']):
			summit = sqlog.sota.Summit(self.data['sota_ref'])
			# Set coordinates based on SOTA
			if not (self.data['lat'] and self.data['lon']):
				self.data['lat'] = summit.lat
				self.data['lon'] = summit.lon
			# Set QTH based on SOTA
			if not self.data['qth']:
				self.data['qth'] = str(summit)

		# Set locator based on coordinates
		if not self.data['my_gridsquare'] and (self.data['lat'] and self.data['lon']):
			self.data['my_gridsquare'] = sqlog.geo.gridsquare(self.data['my_lat'], self.data['my_lon'])
		if not self.data['gridsquare'] and (self.data['lat'] and self.data['lon']):
			self.data['gridsquare'] = sqlog.geo.gridsquare(self.data['lat'], self.data['lon'])

		# Set coordinates based on locator
		if self.data['my_gridsquare'] and not (self.data['my_lat'] and self.data['my_lon']):
			self.data['my_lat'], self.data['my_lon'] = sqlog.geo.location(self.data['my_gridsquare'])
		if self.data['gridsquare'] and not (self.data['lat'] and self.data['lon']):
			self.data['lat'], self.data['lon'] = sqlog.geo.location(self.data['gridsquare'])

		# Set distance based on coordinates
		if isinstance(self.data['my_lat'], float) and isinstance(self.data['my_lon'], float) and isinstance(self.data['lat'], float) and isinstance(self.data['lon'], float):
			if not isinstance(self.data['distance'], float):
				self.data['distance'] = sqlog.geo.distance(self.data['my_lat'], self.data['my_lon'], self.data['lat'], self.data['lon'])

	@classmethod
	def from_adi(cls, adi):
		a = adi
		d = {}
		#TODO: handle _intl fields
		d['datetime'] = a['datetime_on']
		if 'operator' in a:
			d['my_callsign'] = a['operator']
		d['callsign'] = a['call']
		if 'name' in a:
			d['name'] = a['name']
		d['freq'] = float(a['freq'])
		d['band'] = a['band']
		d['mode'] = a['mode']
		if 'rst_rcvd' in a:
			d['rst_rcvd'] = a['rst_rcvd']
		if 'rst_sent' in a:
			d['rst_sent'] = a['rst_sent']
		# ignore qsl from ADI
		# prepare_fields() will take care of my_qth if my_sota_ref is set
		if 'my_sota_ref' in a:
			d['my_sota_ref'] = a['my_sota_ref']
		if 'my_gridsquare' in a:
			d['my_gridsquare'] = a['my_gridsquare']
		if 'my_lat' in a and 'my_lon' in a:
			d['my_lat'] = float(a['my_lat'])
			d['my_lon'] = float(a['my_lat'])
		if 'qth' in a:
			d['qth'] = a['qth']
		if 'sota_ref' in a:
			d['sota_ref'] = a['sota_ref']
		if 'gridsquare' in a:
			d['gridsquare'] = a['gridsquare']
		if 'lat' in a and 'lon' in a:
			d['lat'] = float(a['lat'])
			d['lon'] = float(a['lat'])
		if 'comment' in a:
			d['remarks'] = a['comment']
		return cls(**d)
