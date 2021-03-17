#!/usr/bin/python3

import os
import sys
import csv
import datetime
from dateutil.parser import parse as parsedate

import requests
import pymysql.cursors

import sqlog

def update_db(download=True):
	SUMMIT_DB_FILE = './summitslist.csv'
	if download:
		# download CSV
		url = sqlog.Config.get('sota', 'summit_db_url')
		os.makedirs(os.path.dirname(SUMMIT_DB_FILE), exist_ok=True)
		r = requests.head(url)
		try:
			file_last_updated = datetime.datetime.fromtimestamp(os.path.getmtime(SUMMIT_DB_FILE))
		except FileNotFoundError:
			file_last_updated = datetime.datetime.fromtimestamp(0)
		if 'last-modified' not in r.headers or parsedate(r.headers['last-modified']) > file_last_updated.replace(tzinfo=datetime.timezone.utc):
			r = requests.get(url, allow_redirects=True, stream=True)
			with open(SUMMIT_DB_FILE, 'wb') as f:
				yield 'Downloading summits '
				for chunk in r.iter_content(1024 * 150):
					yield '.'
					f.write(chunk)
				yield "\n"

	# import CSV into MySQL database
	connection = sqlog.mysql_connection()
	try:
		with connection.cursor() as cursor:
			f = open(SUMMIT_DB_FILE, 'r')
			f.readline()  # skip first line that looks like "SOTA Summits List (Date=29/06/2020)"
			yield 'Importing summits '
			summits = csv.DictReader(f)
			def _summits(n):
				global csv_empty
				i = 0
				for summit in summits:
					yield summit
					i += 1
					if i >= n:
						break
			cursor.execute("DELETE FROM summits")
			connection.commit()
			while True:
				try:
					cursor.executemany("""INSERT INTO summits (ref, name, region, association, altitude, lat, lon)
					                      VALUES (%(SummitCode)s, %(SummitName)s, %(RegionName)s, %(AssociationName)s, %(AltM)s, %(Latitude)s, %(Longitude)s)""", _summits(1000))
					yield '.'
				except StopIteration:
					break
			connection.commit()
			yield "\n"
	finally:
		connection.close()

class Summit(object):
	def __init__(self, ref, fetch_from_db=True, name=None, region=None, association=None, altitude=None, lat=None, lon=None):
		if fetch_from_db:
			connection = sqlog.mysql_connection()
			try:
				with connection.cursor() as cursor:
					cursor.execute("SELECT * FROM summits WHERE ref = %s", (ref,))
					result = cursor.fetchone()
					self.ref = ref
					self.name = result['name']
					self.region = result['region']
					self.association = result['association']
					self.altitude = result['altitude']
					self.lat = result['lat']
					self.lon = result['lon']
			finally:
				connection.close()
		else:
			self.ref = ref
			self.name = name
			self.region = region
			self.association = association
			self.altitude = altitude
			self.lat = lat
			self.lon = lon

	@classmethod
	def from_joined_db(cls, e, prefix):
		return cls(
			fetch_from_db = False,
			ref = e[prefix+'ref'],
			name = e[prefix+'name'],
			region = e[prefix+'region'],
			association = e[prefix+'association'],
			altitude = e[prefix+'altitude'],
			lat = e[prefix+'lat'],
			lon = e[prefix+'lon']
		)

	def __str__(self):
		return '%s (%im), %s, %s' % (self.name, self.altitude, self.region, self.association)

	def __repr__(self):
		return '<Summit: %s - %s>' % (self.ref, self.name)
