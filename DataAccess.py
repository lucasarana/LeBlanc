# -*- coding: utf-8 -*-
import traceback
import random

# import psycopg2
# import psycopg2.extras

import MySQLdb
# import mysql.connector
# from mysql.connector import errorcode

from threading import Lock

import config
import tableDefinitions

from NaixCommon import Utils
from NaixCommon import simplejson

import NaixCommon.Errors

from NaixCommon.NaixLogger import NaixLogger

class DALeBlanc:

	@staticmethod
	def get(inParams, tableName, extraParams={}, overridePrivate=False):
		""" Get data from database. Generic for all services... """

		# Buscamos las tablas
		table    = getattr(getattr(tableDefinitions, 'tables'), tableName)
		database = config.database[table['database']]

		fields = []

		# Agregamos las claves de los fields
		for key, field in table['fields'].iteritems():
			if overridePrivate is True or field['private'] is False:
				fields.append(key) 

		sql = "SELECT %s FROM %s" % (', '.join(fields), tableName)

		where = False

		for key, param in inParams.iteritems():

			if key in table['key'] or key in table['search_fields']:

				if key in table['search_fields'] and key not in table['key']:
					cond = 'LIKE'
				else:
					cond = '='

				if param is not None and where is False:
					sql += " WHERE %(key)s %(cond)s %%(%(key)s)s" % ({'key': key, 'cond': cond })
					where = True
				elif param is not None:
					sql += " AND %(key)s %(cond)s %%(%(key)s)s" % ({'key':key, 'cond': cond })

		if type(extraParams) == 'dict' and len(extraParams > 0):
			for key, param in extraParams.iteritems():
				sql += " %s %s" % (key, param)

		result = DALeBlanc.query(database, sql, inParams)
		result = filter(None, result)

		return result

	@staticmethod
	def set(inParams, tableName):
		""" Insert data, Generic for all services... """

		# Buscamos las tablas
		table    = getattr(getattr(tableDefinitions, 'tables'), tableName)
		database = config.database[table['database']]

		fields = []
		fieldsValue = [] 

		# Agregamos las claves de los fields
		for key, field in table['fields'].iteritems():
			if key in inParams:
				fields.append(key) 
				fieldsValue.append("%%(%s)s" % key)

		sql  = "INSERT INTO %s (%s)" % ( tableName, ', '.join(fields) )
		sql += " VALUES (%s)" % (', '.join(fieldsValue))

		result = DALeBlanc.query(database, sql, inParams)

		return result

	@staticmethod
	def update(inParams, tableName, updateKey=False):
		""" Actualizamos un registro """ 

		# Buscamos las tablas
		table    = getattr(getattr(tableDefinitions, 'tables'), tableName)
		database = config.database[table['database']]

		fields = []

		prevRow = DALeBlanc.get(inParams, tableName, overridePrivate=True)

		where = None

		# Recopilamos las claves y las asignamos al where
		for key in table['key']:
			if key in prevRow[0] and inParams[key] == prevRow[0][key]:
				if key in inParams and inParams[key] is not None and where is None:
					where = ' WHERE %s = %%(%s)s' % (key, key)
				elif key in inParams and inParams[key] is not None: # Rancid!!
					where += ' AND  %s = %%(%s)s' % (key, key)

		for key, param in inParams.iteritems():
			if key in prevRow[0] and param != prevRow[0][key]:
				fields.append( '%s = %%(%s)s' % (key, key) )

		if len(fields) > 0:
			
			sql = 'UPDATE %s SET %s %s' % (tableName, ', '.join(fields), where)
			result = DALeBlanc.query(database, sql, inParams)

			return result			
		else:
			return False

	@staticmethod
	def delete(inParams, tableName):

		# Buscamos las tablas
		table    = getattr(getattr(tableDefinitions, 'tables'), tableName)
		database = config.database[table['database']]

		where = None
		
		# Recopilamos las claves y las asignamos al where
		for key in table['key']:
			if key in inParams and inParams[key] is not None and where is None:
				where = ' WHERE %s = %%(%s)s' % (key, key)
			elif key in inParams and inParams[key] is not None: # Rancid!!
				where += ' AND  %s = %%(%s)s' % (key, key)

		sql = 'DELETE FROM %s %s' % (tableName, where)
		result = DALeBlanc.query(database, sql, inParams)
		return result			
		
	@staticmethod
	def query(database, query, params): 

		conn = MySQLdb.connect(*database) # Conectar a la base de datos 
		cursor = conn.cursor()         # Crear un cursor 
		result = cursor.execute(query, params)          # Ejecutar una consulta 
	 
		if query.upper().startswith('SELECT'): 
			# data = cursor.fetchall()   # Traer los resultados de un select 
			columns = cursor.description 
			data = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]	        
		elif query.upper().startswith('INSERT INTO'):
			conn.commit()              # Hacer efectiva la escritura de datos 
			data = cursor.lastrowid
		elif query.upper().startswith('UPDATE') or query.upper().startswith('DELETE'):
			conn.commit()
			data = cursor.rowcount
		else: 
			conn.commit()              # Hacer efectiva la escritura de datos 
			data = None

		cursor.close()                 # Cerrar el cursor 
		conn.close()                   # Cerrar la conexión 

		return data