#!/usr/bin/python3

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import argparse

from flask import Flask, render_template

import sqlog
import sqlog.qso


sqlog.Config.load(os.environ.get('CONFIG', 'config.cfg'))

app = Flask(__name__)

@app.route('/')
def logbook():
	connection = sqlog.mysql_connection()
	try:
		with connection.cursor() as cursor:
			cursor.execute('SELECT * FROM qsos')
			qsos = map(sqlog.qso.QSO, cursor.fetchall())
			return render_template('logbook.html', qsos=qsos)
	finally:
		connection.close()


if __name__ == '__main__':
	app.run(debug=True)
