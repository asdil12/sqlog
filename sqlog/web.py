#!/usr/bin/python3

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

from flask import Flask, Markup, Response, render_template, request
from flask_httpauth import HTTPBasicAuth
import pymysql
import json
from io import TextIOWrapper

import sqlog
import sqlog.load
from sqlog.qso import QSO
from sqlog.sota import Summit
from sqlog.callsign import Callsign


sqlog.Config.load(os.environ.get('CONFIG', 'config.cfg'))

app = Flask(__name__)
auth = HTTPBasicAuth(realm='SQLog')

@auth.verify_password
def check_user_password(user, password):
	return sqlog.Config.get('web', 'user') and password == sqlog.Config.get('web', 'pass')

@app.context_processor
def utility_processor():
	def nav_active(endpoint):
		if isinstance(endpoint, str):
			active = (request.endpoint == endpoint)
		else:
			active = (request.endpoint in endpoint)
		return 'active' if active else ''
	def summit_link(summit, query_db=False):
		ref = summit.ref if isinstance(summit, Summit) else summit
		if query_db and not isinstance(summit, Summit) and ref:
			summit = Summit(ref)
		return Markup('<a title="%s" href="https://sotl.as/summits/%s">%s</a>') % (summit, ref, ref) if ref else ''
	def flag(callsign, sota=False):
		classes = 'flag fp fp-md fp-rounded'
		if isinstance(callsign, str):
			if sota:
				callsign = callsign.split('/')[0]
			callsign = Callsign(callsign)
		if callsign.roaming_country:
			roaming_country = Markup('<span class="abs"><span title="%s" class="%s fp-clip %s"></span></span>') % (callsign.roaming_country, classes, callsign.roaming_country.iso.lower())
			return Markup('%s<span title="%s" class="%s %s"></span>') % (roaming_country, callsign.country, classes, callsign.country.iso.lower())
		else:
			return Markup('<span title="%s" class="%s %s"></span>' % (callsign.country, classes, callsign.country.iso.lower()))
	def hide_decimal(f):
		if int(f) == f:
			return int(f)
		else:
			return f
	return {'nav_active': nav_active, 'summit_link': summit_link, 'flag': flag, 'hide_decimal': hide_decimal}

def sse(items):
	def _sees(items):
		for e in items:
			yield "data: %s\n\n" % json.dumps(e)
		yield "data: %s\n\n" % json.dumps({'close': True})
	return Response(_sees(items), mimetype='text/event-stream')


@app.route('/')
@auth.login_required
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
			cursor.execute("""SELECT qsos.*,
			                  ms.ref AS ms_ref, ms.name AS ms_name, ms.region AS ms_region, ms.association AS ms_association, ms.altitude AS ms_altitude, ms.lat AS ms_lat, ms.lon AS ms_lon,
			                  s.ref AS s_ref, s.name AS s_name, s.region AS s_region, s.association AS s_association, s.altitude AS s_altitude, s.lat AS s_lat, s.lon AS s_lon
			                  FROM qsos
			                  LEFT JOIN summits AS ms on my_sota_ref = ms.ref
			                  LEFT JOIN summits AS s on sota_ref = s.ref
							  %s
			                  ORDER BY datetime""" % query)
			def logitem(e):
				my_summit = Summit.from_joined_db(e, 'ms_') if e['ms_ref'] else None
				summit = Summit.from_joined_db(e, 's_') if e['s_ref'] else None
				return (QSO(e), my_summit, summit)
			log_items = map(logitem, cursor.fetchall())
			return render_template('logbook.html', log_items=log_items, s=s)
	finally:
		connection.close()

@app.route('/sota/summits')
@auth.login_required
def summits():
	connection = sqlog.mysql_connection()
	try:
		with connection.cursor() as cursor:
			cursor.execute("""SELECT COUNT(id) AS qsos, MAX(datetime) as last_activation, summits.ref, summits.name, region, association, altitude, summits.lat, summits.lon
			                  FROM qsos LEFT JOIN summits ON qsos.my_sota_ref = summits.ref
			                  WHERE ref IS NOT NULL
			                  GROUP BY my_sota_ref ORDER BY last_activation""")
			def summititem(e):
				summit = Summit.from_joined_db(e, '')
				return (summit, e['qsos'], e['last_activation'])
			summit_items = map(summititem, cursor.fetchall())
			return render_template('summits.html', summit_items=summit_items)
	finally:
		connection.close()

@app.route('/qso/<int:qso_id>')
@auth.login_required
def qso_show(qso_id):
	connection = sqlog.mysql_connection()
	try:
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM qsos WHERE id = '%s'", qso_id)
			qso = QSO(cursor.fetchone())
			my_summit = Summit(qso.my_sota_ref) if qso.my_sota_ref else None
			summit = Summit(qso.sota_ref) if qso.sota_ref else None
			return render_template('qso.html', qso=qso, my_summit=my_summit, summit=summit)
	except AttributeError:
		return "QSO not found", 404
	finally:
		connection.close()


@app.route('/qso/import', methods=['GET', 'POST'])
@auth.login_required
def qso_import():
	if request.method == 'POST':
		logfile = request.files["logfile"]
		logfp = TextIOWrapper(logfile, encoding='ascii')
		qsos = sqlog.load.read_fp(logfp, logfile.filename)
		imported_qsos = map(repr, sqlog.load.import_qsos(qsos))
	else:
		imported_qsos = []
	return render_template('qso_import.html', imported_qsos=imported_qsos)

@app.route('/sota/refresh')
@auth.login_required
def sota_refresh():
	if request.args.get('refresh') == '1':
		return sse(sqlog.sota.update_db())
	else:
		return render_template('sota_refresh.html')

@app.route('/map')
@auth.login_required
def qso_map():
	return render_template('map.html')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
