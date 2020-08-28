#!/usr/bin/python3

import datetime
from enum import IntEnum

from hamutils.adif.common import convert_freq_to_band

import sqlog.geo
import sqlog.sota
from sqlog.callsign import Callsign

fields = ('id', 'datetime', 'my_callsign', 'callsign', 'name', 'freq', 'band', 'mode', 'rst_rcvd', 'rst_sent', 'qsl', 'my_qth', 'my_sota_ref', 'my_gridsquare', 'my_lat', 'my_lon', 'my_geoaccuracy', 'qth', 'sota_ref', 'gridsquare', 'lat', 'lon', 'geoaccuracy', 'distance', 'remarks')

class GeoAccuracy(IntEnum):
	USER = 10
	SOTA = 20
	GRID = 50
	CALL = 40

class QSO(object):
	def __init__(self, data={}, **kwdata):
		d = data.copy()
		d.update(kwdata)

		self.id = d.get('id', None)
		self.datetime = d.get('datetime', None)
		self.my_callsign = d.get('my_callsign', None)
		self.callsign = d.get('callsign', None)
		self.name = d.get('name', None)
		self.freq = d.get('freq', None)
		self.band = d.get('band', None)
		self.mode = d.get('mode', None)
		self.rst_rcvd = d.get('rst_rcvd', None)
		self.rst_sent = d.get('rst_sent', None)
		self.qsl = d.get('qsl', None)
		self.my_qth = d.get('my_qth', None)
		self.my_sota_ref = d.get('my_sota_ref', None)
		self.my_gridsquare = d.get('my_gridsquare', None)
		self.my_lat = d.get('my_lat', None)
		self.my_lon = d.get('my_lon', None)
		self.my_geoaccuracy = d.get('my_geoaccuracy', None)
		self.qth = d.get('qth', None)
		self.sota_ref = d.get('sota_ref', None)
		self.gridsquare = d.get('gridsquare', None)
		self.lat = d.get('lat', None)
		self.lon = d.get('lon', None)
		self.geoaccuracy = d.get('geoaccuracy', None)
		self.distance = d.get('distance', None)
		self.remarks = d.get('remarks', None)

		# Create Callsign objects
		self.my_callsign = Callsign(self.my_callsign)
		self.callsign = Callsign(self.callsign)

		# Create GeoAccuracy objects
		if not isinstance(self.my_geoaccuracy, GeoAccuracy):
			self.my_geoaccuracy = GeoAccuracy[self.my_geoaccuracy] if self.my_geoaccuracy else None
		if not isinstance(self.geoaccuracy, GeoAccuracy):
			self.geoaccuracy = GeoAccuracy[self.geoaccuracy] if self.geoaccuracy else None

		if not self.my_geoaccuracy and self.my_pos:
			self.my_geoaccuracy = GeoAccuracy.USER
		if not self.geoaccuracy and self.pos:
			self.geoaccuracy = GeoAccuracy.USER

		if self.my_sota_ref and not (self.my_pos and self.my_qth):
			my_summit = sqlog.sota.Summit(self.my_sota_ref)
			# Set coordinates based on SOTA
			if not self.pos:
				self.my_lat = my_summit.lat
				self.my_lon = my_summit.lon
				self.my_geoaccuracy = GeoAccuracy.SOTA
			# Set QTH based on SOTA
			if not self.my_qth:
				self.my_qth = str(my_summit)

		if self.sota_ref and not (self.pos and self.qth):
			summit = sqlog.sota.Summit(self.sota_ref)
			# Set coordinates based on SOTA
			if not self.pos:
				self.lat = summit.lat
				self.lon = summit.lon
				self.geoaccuracy = GeoAccuracy.SOTA
			# Set QTH based on SOTA
			if not self.qth:
				self.qth = str(summit)

		# Set locator based on coordinates
		if not self.my_gridsquare and self.my_pos:
			self.my_gridsquare = sqlog.geo.gridsquare(self.my_lat, self.my_lon)
		if not self.gridsquare and self.pos:
			self.gridsquare = sqlog.geo.gridsquare(self.lat, self.lon)

		# Set coordinates based on locator
		if self.my_gridsquare and not self.my_pos:
			self.my_lat, self.my_lon = sqlog.geo.location(self.my_gridsquare)
			self.my_geoaccuracy = GeoAccuracy.GRID
		if self.gridsquare and not self.pos:
			self.lat, self.lon = sqlog.geo.location(self.gridsquare)
			self.geoaccuracy = GeoAccuracy.GRID

		# Set coordinates based on Callsign
		if not self.my_pos:
			country = self.my_callsign.roaming_country if self.my_callsign.roaming_country else self.my_callsign.country
			self.my_lat = country.lat
			self.my_lon = country.lon
			self.my_geoaccuracy = GeoAccuracy.CALL
		if not self.pos:
			country = self.callsign.roaming_country if self.callsign.roaming_country else self.callsign.country
			self.lat = country.lat
			self.lon = country.lon
			self.geoaccuracy = GeoAccuracy.CALL

		# Set distance based on coordinates if geoaccuracy is sufficient
		if self.my_geoaccuracy >= GeoAccuracy.GRID and self.geoaccuracy >= GeoAccuracy.GRID:
			if self.my_pos and pos:
				if not isinstance(self.distance, float):
					self.distance = sqlog.geo.distance(self.my_lat, self.my_lon, self.lat, self.lon)

		# Get band from freq if not set
		if self.freq and not self.band:
			self.band = convert_freq_to_band(self.freq)

		# Ensure that some fields are uppercase
		self.my_sota_ref = self.my_sota_ref.upper() if self.my_sota_ref else self.my_sota_ref
		self.sota_ref = self.sota_ref.upper() if self.sota_ref else self.sota_ref
		self.my_gridsquare = self.my_gridsquare.upper() if self.my_gridsquare else self.my_gridsquare
		self.gridsquare = self.gridsquare.upper() if self.gridsquare else self.gridsquare

	@property
	def data(self):
		d = {}
		for field in fields:
			d[field] = getattr(self, field)
			if field == 'my_geoaccuracy' or field == 'geoaccuracy':
				d[field] = d[field].name if d[field] else None
		return d

	@property
	def date(self):
		return self.datetime.date()

	@property
	def time(self):
		return self.datetime.time()

	@property
	def my_pos(self):
		return (self.my_lat, self.my_lat) if (isinstance(self.my_lat, float) and isinstance(self.my_lon, float)) else None

	@property
	def pos(self):
		return (self.lat, self.lat) if (isinstance(self.lat, float) and isinstance(self.lon, float)) else None

	def __repr__(self):
		return 'QSO(%s)' % ', '.join(['%s=%s' % (ks, getattr(self, k)) for k, ks in (('datetime', 'dt'), ('callsign', 'call'), ('my_sota_ref', 'sota')) if getattr(self, k)])

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
