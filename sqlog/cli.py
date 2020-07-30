#!/usr/bin/python3

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import sqlog
import sqlog.load

sqlog.Config.load('config.cfg')

qsos = sqlog.load.read_adi(sys.argv[1])
sqlog.load.import_qsos(qsos)
