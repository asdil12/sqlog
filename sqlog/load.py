#!/usr/bin/python3

import sqlog
import sqlog.qso

import hamutils.adif


def import_qsos(qsos):
	connection = sqlog.mysql_connection()
	try:
		with connection.cursor() as cursor:
			field_keys = ', '.join(map(lambda f: '`%s`' % f, sqlog.qso.fields))
			field_values = ', '.join(map(lambda f: '%%(%s)s' % f, sqlog.qso.fields))
			for qso in qsos:
				cursor.execute('INSERT INTO qsos (%s) VALUES (%s)' % (field_keys, field_values), qso.data)
				connection.commit()
	finally:
		connection.close()


def read_adi(filename):
	with open(filename, 'r', encoding="ascii") as f:
		adi = hamutils.adif.ADIReader(f)
		for qso in adi:
			yield sqlog.qso.QSO.from_adi(qso)
