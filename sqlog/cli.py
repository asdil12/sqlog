#!/usr/bin/python3

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import argparse

import sqlog
import sqlog.load


parser = argparse.ArgumentParser(description='SQLog Amateur Radio Logbook CLI.')
subparsers = parser.add_subparsers(dest='command', help='command')
subparsers.required = True

parser.add_argument('-c', dest='config', default='config.cfg', help='Config file')

h = 'Import QSOs from file'
parser_import = subparsers.add_parser('import', description=h, help=h)
parser_import.add_argument('file', help='ADIF/CSV file')

h = 'Refresh SOTA summits database'
parser_sota = subparsers.add_parser('sotarefresh', description=h, help=h)
parser_sota.add_argument('-D', '--no-download', action='store_true', help='Only import the already downloaded summits CSV into the DB')

args = parser.parse_args()


sqlog.Config.load(args.config)

if args.command == 'import':
	if args.file.endswith('csv'):
		qsos = sqlog.load.read_csv(args.file)
	else:
		qsos = sqlog.load.read_adi(args.file)
	for qso in sqlog.load.import_qsos(qsos):
		print(repr(qso))
elif args.command == 'sotarefresh':
	for s in sqlog.sota.update_db(not args.no_download):
		sys.stdout.write(s)
		sys.stdout.flush()
