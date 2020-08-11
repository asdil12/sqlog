#!/usr/bin/python3

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

from flask import Flask, Markup, render_template, request
import pymysql

import sqlog
import sqlog.qso
import sqlog.sota
from sqlog.callsign import Callsign


sqlog.Config.load(os.environ.get('CONFIG', 'config.cfg'))

app = Flask(__name__)

@app.context_processor
def utility_processor():
	def nav_active(endpoint):
		if isinstance(endpoint, str):
			active = (request.endpoint == endpoint)
		else:
			active = (request.endpoint in endpoint)
		return 'active' if active else ''
	def summit_link(ref):
		return Markup('<a href="https://sotl.as/summits/%s">%s</a>' % (ref,ref)) if ref else ref
		#TODO: this is too slow:
		#return Markup('<a href="https://sotl.as/summits/%s" title="%s">%s</a>' % (ref, sqlog.sota.Summit(ref), ref)) if ref else ref
	def flag(callsign, sota=False):
		#FIXME: html escaping
		classes = 'flag fp fp-md fp-rounded'
		if isinstance(callsign, str):
			if sota:
				callsign = callsign.split('/')[0]
			callsign = Callsign(callsign)
		if callsign.roaming_country:
			roaming_country = '<span class="abs"><span title="%s" class="%s fp-clip %s"></span></span>' % (callsign.roaming_country, classes, callsign.roaming_country.iso.lower())
			return Markup('%s<span title="%s" class="%s %s"></span>' % (roaming_country, callsign.country, classes, callsign.country.iso.lower()))
		else:
			return Markup('<span title="%s" class="%s %s"></span>' % (callsign.country, classes, callsign.country.iso.lower()))
	return {'nav_active': nav_active, 'summit_link': summit_link, 'flag': flag}

@app.route('/')
def logbook():
	connection = sqlog.mysql_connection()
	try:
		with connection.cursor() as cursor:
			s = request.args.get('s', '')
			if not s:
				query = ''
			elif not (' ' in s or '=' in s):
				s = s.upper()
				c = pymysql.escape_string(s)
				query = 'WHERE callsign = "%s" OR callsign LIKE "%%/%s/%%" OR callsign LIKE "%%/%s" OR callsign LIKE "%s/%%"' % (c,c,c,c)
			else:
				query = 'WHERE %s' % s #FIXME: escape somehow?
			cursor.execute('SELECT * FROM qsos %s ORDER BY datetime' % query)
			qsos = map(sqlog.qso.QSO, cursor.fetchall())
			return render_template('logbook.html', qsos=qsos, s=s)
	finally:
		connection.close()

@app.route('/sota/summits')
def summits():
	connection = sqlog.mysql_connection()
	try:
		with connection.cursor() as cursor:
			cursor.execute("""SELECT my_sota_ref, COUNT(id) AS qsos, MAX(datetime) as last_activation, summits.name, region, association, altitude
			                  FROM qsos LEFT JOIN summits ON qsos.my_sota_ref = summits.ref
			                  GROUP BY my_sota_ref ORDER BY last_activation""")
			return render_template('summits.html', summits=cursor.fetchall())
	finally:
		connection.close()


if __name__ == '__main__':
	app.run(debug=True)
