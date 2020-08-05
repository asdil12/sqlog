#!/usr/bin/python3

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

from flask import Flask, render_template, request
import pymysql

import sqlog
import sqlog.qso


sqlog.Config.load(os.environ.get('CONFIG', 'config.cfg'))

app = Flask(__name__)


@app.route('/')
def logbook():
	connection = sqlog.mysql_connection()
	try:
		with connection.cursor() as cursor:
			s = request.args.get('s', '')
			"""
			if not s:
				query = ''
			elif ' ' in s or '=' in s:
				query = 'WHERE %s' % s
			elif '/' in query:
				query = 'WHERE callsign = "%s"' % s #FIXME: escapt
			else:
			"""
			if not s:
				query = ''
			elif not (' ' in s or '=' in s):
				s = s.upper()
				c = pymysql.escape_string(s)
				query = 'WHERE callsign = "%s" OR callsign LIKE "%%/%s/%%" OR callsign LIKE "%%/%s" OR callsign LIKE "%s/%%"' % (c,c,c,c)
			cursor.execute('SELECT * FROM qsos %s ORDER BY datetime' % query)
			qsos = map(sqlog.qso.QSO, cursor.fetchall())
			return render_template('logbook.html', qsos=qsos, s=s)
	finally:
		connection.close()


if __name__ == '__main__':
	app.run(debug=True)
