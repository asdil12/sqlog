#!/usr/bin/python3

import os
import configparser
import pymysql.cursors

class Config(object):
	_object = None

	def __init__(self, configfile):
		assert os.path.exists(configfile), "Configfile '%s' not found" % configfile
		self.config = configparser.ConfigParser()
		self.config.read(configfile)

	@classmethod
	def get(cls, section, key):
		return cls._object.config[section][key]

	@classmethod
	def load(cls, configfile):
		cls._object = cls(configfile)

	@classmethod
	def instance(cls):
		assert cls._object, "Config used before initialisation"
		return cls._object


def mysql_connection():
	c = Config.instance()
	connection = pymysql.connect(
		host=c.get('mysql', 'host'),
		user=c.get('mysql', 'user'),
		password=c.get('mysql', 'pass'),
		db=c.get('mysql', 'db'),
		charset='utf8mb4',
		cursorclass=pymysql.cursors.DictCursor
	)
	return connection
