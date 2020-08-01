#!/usr/bin/python3

import sqlog
import sqlog.qso

import csv
import hamutils.adif


def import_qsos(qsos):
	connection = sqlog.mysql_connection()
	try:
		with connection.cursor() as cursor:
			field_keys = ', '.join(map(lambda f: '`%s`' % f, sqlog.qso.fields))
			field_values = ', '.join(map(lambda f: '%%(%s)s' % f, sqlog.qso.fields))
			for qso in qsos:
				print(repr(qso))
				cursor.execute('INSERT INTO qsos (%s) VALUES (%s)' % (field_keys, field_values), qso.data)
				connection.commit()
	except:
		print(qso.data)
		raise
	finally:
		connection.close()


def read_adi(filename):
	with open(filename, 'r', encoding="ascii") as f:
		for qso in hamutils.adif.ADIReader(f):
			yield sqlog.qso.QSO.from_adi(qso)

def read_csv(filename):
	with open(filename, 'r', encoding="ascii") as f:
		fields = ('version', 'my_callsign', 'my_sota_ref', 'date', 'time', 'freq', 'mode', 'callsign', 'sota_ref', 'remarks')
		for qso in csv.DictReader(f, fields):
			if qso['version'] == 'Version':
				# try to be smart and skip header
				continue
			yield sqlog.qso.QSO.from_csv(qso)
