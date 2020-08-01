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
		if parsedate(r.headers['last-modified']) > file_last_updated.replace(tzinfo=datetime.timezone.utc):
			sys.stdout.flush()
			r = requests.get(url, allow_redirects=True, stream=True)
			with open(SUMMIT_DB_FILE, 'wb') as f:
				print('Downloading summits ', end='')
				for chunk in r.iter_content(1024 * 1024):
					sys.stdout.write('.')
					sys.stdout.flush()
					f.write(chunk)
				sys.stdout.write("\n")

	# import CSV into MySQL database
	connection = sqlog.mysql_connection()
	try:
		with connection.cursor() as cursor:
			def _summits():
				f = open(SUMMIT_DB_FILE, 'r')
				f.readline()  # skip first line that looks like "SOTA Summits List (Date=29/06/2020)"
				print('Importing summits ', end='')
				sys.stdout.flush()
				i = 0
				for summit in csv.DictReader(f):
					i += 1
					if i % 1000 == 0:
						sys.stdout.write('.')
						sys.stdout.flush()
					yield summit
			cursor.execute("DELETE FROM summits")
			connection.commit()
			cursor.executemany("""INSERT INTO summits (ref, name, region, association, altitude, lat, lon)
			                      VALUES (%(SummitCode)s, %(SummitName)s, %(RegionName)s, %(AssociationName)s, %(AltM)s, %(Latitude)s, %(Longitude)s)""", _summits())
			connection.commit()
			sys.stdout.write("\n")
	finally:
		connection.close()

class Summit(object):
	def __init__(self, ref):
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

	def __str__(self):
		return '%s (%im), %s, %s' % (self.name, self.altitude, self.region, self.association)

	def __repr__(self):
		return '<Summit: %s - %s>' % (self.ref, self.name)
