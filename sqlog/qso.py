#!/usr/bin/python3

import datetime

from hamutils.adif.common import convert_freq_to_band

import sqlog.geo
import sqlog.sota


#TODO: get this at runtime from DB using MYSQL DESCRIBE command or something like that
fields = ('datetime', 'my_callsign', 'callsign', 'name', 'freq', 'band', 'mode', 'rst_rcvd', 'rst_sent', 'qsl', 'my_qth', 'my_sota_ref', 'my_gridsquare', 'my_lat', 'my_lon', 'qth', 'sota_ref', 'gridsquare', 'lat', 'lon', 'distance', 'remarks')

class QSO(object):
	def __init__(self, data={}, **kwdata):
		self.data = data
		self.data.update(kwdata)
		self.prepare_fields()

	@property
	def datetime(self):
		return self.data['datetime']

	@property
	def date(self):
		return self.data['datetime'].date()

	@property
	def time(self):
		return self.data['datetime'].time()

	@property
	def my_callsign(self):
		return self.data['my_callsign']

	@property
	def callsign(self):
		return self.data['callsign']

	@property
	def name(self):
		return self.data['name']

	@property
	def freq(self):
		return self.data['freq']

	@property
	def band(self):
		return self.data['band']

	@property
	def mode(self):
		return self.data['mode']

	@property
	def rst_rcvd(self):
		return self.data['rst_rcvd']

	@property
	def rst_sent(self):
		return self.data['rst_sent']

	@property
	def qsl(self):
		return self.data['qsl']

	@property
	def my_qth(self):
		return self.data['my_qth']

	@property
	def my_sota_ref(self):
		return self.data['my_sota_ref']

	@property
	def my_gridsquare(self):
		return self.data['my_gridsquare']

	@property
	def my_lat(self):
		return self.data['my_lat']

	@property
	def my_lon(self):
		return self.data['my_lon']

	@property
	def qth(self):
		return self.data['qth']

	@property
	def sota_ref(self):
		return self.data['sota_ref']

	@property
	def gridsquare(self):
		return self.data['gridsquare']

	@property
	def lat(self):
		return self.data['lat']

	@property
	def lon(self):
		return self.data['lon']

	@property
	def distance(self):
		return self.data['distance']

	@property
	def remarks(self):
		return self.data['remarks']

	def __repr__(self):
		return 'QSO(%s)' % ', '.join(['%s=%s' % (ks, self.data[k]) for k, ks in (('datetime', 'dt'), ('callsign', 'call'), ('my_sota_ref', 'sota')) if self.data[k]])

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
		if not self.data['my_gridsquare'] and (self.data['my_lat'] and self.data['my_lon']):
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

		# Get band from freq if not set
		if self.data['freq'] and not self.data['band']:
			self.data['band'] = convert_freq_to_band(self.data['freq'])

		# Ensure that some fields are uppercase
		def _ensure_uppercase_field(field):
			if self.data[field]:
				self.data[field] = self.data[field].upper()
		_ensure_uppercase_field('my_callsign')
		_ensure_uppercase_field('callsign')
		_ensure_uppercase_field('my_sota_ref')
		_ensure_uppercase_field('sota_ref')
		_ensure_uppercase_field('my_gridsquare')
		_ensure_uppercase_field('gridsquare')

	@classmethod
	def from_adi(cls, adi):
		d = {}
		#TODO: handle _intl fields
		d['datetime'] = adi['datetime_on']
		if 'station_callsign' in adi:
			d['my_callsign'] = adi['station_callsign']
		elif 'operator' in adi:
			d['my_callsign'] = adi['operator']
		d['callsign'] = adi['call']
		if 'name' in adi:
			d['name'] = adi['name']
		d['freq'] = float(adi['freq'])
		d['band'] = adi['band']
		d['mode'] = adi['mode']
		if 'rst_rcvd' in adi:
			d['rst_rcvd'] = adi['rst_rcvd']
		if 'rst_sent' in adi:
			d['rst_sent'] = adi['rst_sent']
		# ignore qsl from ADI
		# prepare_fields() will take care of my_qth if my_sota_ref is set
		if 'my_sota_ref' in adi:
			d['my_sota_ref'] = adi['my_sota_ref']
		if 'my_gridsquare' in adi:
			d['my_gridsquare'] = adi['my_gridsquare']
		if 'my_lat' in adi and 'my_lon' in adi:
			d['my_lat'] = float(adi['my_lat'])
			d['my_lon'] = float(adi['my_lat'])
		if 'qth' in adi:
			d['qth'] = adi['qth']
		if 'sota_ref' in adi:
			d['sota_ref'] = adi['sota_ref']
		if 'gridsquare' in adi:
			d['gridsquare'] = adi['gridsquare']
		if 'lat' in adi and 'lon' in adi:
			d['lat'] = float(adi['lat'])
			d['lon'] = float(adi['lat'])
		if 'comment' in adi:
			d['remarks'] = adi['comment']
		return cls(d)

	@classmethod
	def from_csv(cls, csv):
		d = {}
		assert csv['version'] == 'V2', 'Unexpected CSV version: "%s"' % csv['version']
		d['my_callsign'] = csv['my_callsign']
		d['my_sota_ref'] = csv['my_sota_ref']
		try:
			date = datetime.datetime.strptime(csv['date'], '%d/%m/%y').date()
		except ValueError:
			date = datetime.datetime.strptime(csv['date'], '%d/%m/%Y').date()
		time = datetime.datetime.strptime(csv['time'], '%H:%M').time()
		d['datetime'] = datetime.datetime.combine(date, time)
		freq = csv['freq'].upper().replace('MHZ', '')
		if 'KHZ' in freq:
			freq = float(freq.replace('KHZ', '')) / 1000
		elif 'GHZ' in freq:
			freq = float(freq.replace('GHZ', '')) * 1000
		else:
			freq = float(freq)
		d['freq'] = freq
		d['mode'] = csv['mode']
		d['callsign'] = csv['callsign']
		d['sota_ref'] = csv['sota_ref']
		d['remarks'] = csv['remarks']
		return cls(d)
