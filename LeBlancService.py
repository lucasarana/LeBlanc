# -*- coding: utf-8 -*-

from decimal  import Decimal
from datetime import datetime, tzinfo

import traceback

import NaixCommon
import json
import config
import tableDefinitions

from NaixCommon.ValueObjects import VO_Message

from NaixCommon import Utils
from NaixCommon import simplejson

# from NaixCommon.Utils import InParams, InParam, Validate, MANDATORY, OPTIONAL
from NaixCommon.NaixLogger import NaixLogger

from DataAccess import DALeBlanc

import hashlib

LEBLANC_VERSION = "ALPHA"

class LeBlancServices:

	@staticmethod
	def validateParams(paramsGet, method, table):
		""" Se valida que los parametros de entrada esten la deficinicon de la tabla en cuestion """

		# Buscamos las tablas
		tables = getattr(tableDefinitions, 'tables')
		table  = getattr(tables, table)

		fields = table['fields']

		if method is 'update':

			keyInput = []

			# Validamos que una de las claves exista
			for key in table['key']:
				if key in paramsGet and paramsGet[key] is not None:
					keyInput.append(key)

			if len(keyInput) == 0:
				return { 'valid': False, 'error': NaixCommon.Errors.KEY_MISSING() }

		if method is 'delete':

			keyInput = []

			# Validamos que una de las claves exista
			for key in table['key']:
				if key in paramsGet and paramsGet[key] is None:
					return { 'valid': False, 'error': NaixCommon.Errors.KEY_MISSING() }

		# Validamos si los campos enviados son validos en la definicion de la tabla
		for key, param in paramsGet.iteritems():

			notnull   = table['fields'][key]['notnull']
			maxlength = table['fields'][key]['maxlength']

			if param is not None:

				# elif method is 'get':
					# Validamos ...

				# elif method is 'set':
					# return simplejson.dumps(NaixCommon.Errors.INPUT_PARAM_VIOLATION(), default=str)

				# Validacion Generica
				if key not in fields or len(param) > int(maxlength):
					# Validamos que los campos ingresados sean validos tanto en longitud como que exista la definicion de la tabla
					return { 'valid': False, 'error': NaixCommon.Errors.INPUT_PARAM_VIOLATION() }

			else:
				
				if method is 'set':
					# Validamos que todos los campos NotNull esten presentes y no sean None.
					if notnull:
						return { 'valid': False, 'error': NaixCommon.Errors.INPUT_PARAM_MISSING() }

		return { 'valid': True }

	@staticmethod
	def mergeParams(paramsGet, reName=None, extraParams=None):
		""" Renombra los parametros de entrada segun un diccionario de relacion dado. 
		Tambien se separa los parametros agregados como los order by. """

		params_remove = []
		params_add = {}	

		for param in paramsGet:
			if param in extraParams:
				extraParams[param] = paramsGet[param]
				params_remove.append(param)
			elif param in reName:
				params_add[reName[param]] = paramsGet[param]
				params_remove.append(param)

		for param in params_remove:
			if param in paramsGet:
				del paramsGet[param]

		for param in params_add:
			paramsGet[param] = params_add[param]

		return {'paramsGet': paramsGet, 'extraParams': extraParams}

	# ++++++++++ User Service ++++++++++ #
	
	@staticmethod
	def getUser(handler):

		# Los ar'gumentos se tratan con el handler.get_argument('argument_name')
		# La IP se obtiene del comando handler.request.remote_ip
		paramsGet = {
			'id': handler.get_argument('id', None),
			'name': handler.get_argument('name', None),
			'byClient': handler.get_argument('byClient', None),
			'order_by': handler.get_argument('order_by', None),
			'limit': handler.get_argument('limit', None)
		}

		# En el caso de recibir parametros con diferentes nombres a los de la base.
		reName = {'name':'user_name', 'id':'user_id', 'byClient':'client_id'}

		# Extra Params, son todo aquel input que no sea un campo en la base de datos.
		extraParams = {'order_by': None, 'limit': None }

		# Mergeamos los params, con los extra params y renombramos lo campos que se tiene que renombrar
		params = LeBlancServices.mergeParams(paramsGet, reName, extraParams)

		# Validamos los input params
		validate = LeBlancServices.validateParams(params['paramsGet'], 'get', 'users')

		if validate['valid']:
			result = DALeBlanc.get(params['paramsGet'], 'users', params['extraParams'])

			if result:
				return simplejson.dumps({'status':'SUCCESS', 'code': 200, 'data': result}, default=str)
		else:
			return validate

	@staticmethod
	def createUser(handler):

		# Los argumentos se tratan con el handler.get_argument('argument_name')
		# La IP se obtiene del comando handler.request.remote_ip
		paramsGet = {
			'user_name': handler.get_argument('user_name', None),
			'user_description': handler.get_argument('user_description', None),
			'user_email': handler.get_argument('user_email', None),
			'user_password': handler.get_argument('user_password', None),
			'client_id': handler.get_argument('client_id', None),
		}

		if paramsGet['user_password'] is not None:
			# Buscamos el HASH
			salt = DALeBlanc.get({'valid':True}, 'salts', {'limit': 1})
			paramsGet['user_salt'] = salt[0]['salt']

			# Hasheamos el password
			password = hashlib.md5(paramsGet['user_password'] + paramsGet['user_salt']).hexdigest()
			paramsGet['user_password'] = password

		# Validamos los input params
		validate = LeBlancServices.validateParams(paramsGet, 'set', 'users')

		# Ejecutamos la query
		if validate['valid']:

			# Validamos que los datos a ingresar no existan.
			currentRow = DALeBlanc.get(paramsGet, 'users')

			if len(currentRow) > 0:
				return simplejson.dumps(NaixCommon.Errors.REGISTER_DUPLICATE(), default=str)

			result = DALeBlanc.set(paramsGet, 'users')

			if result:
				return simplejson.dumps({'status':'SUCCESS', 'code': 201, 'data': result}, default=str)
		else:
			return simplejson.dumps( validate['error'], default=str )

	@staticmethod
	def updateUser(handler):

		# Los argumentos se tratan con el handler.get_argument('argument_name')
		# La IP se obtiene del comando handler.request.remote_ip
		paramsGet = {
			'user_name': handler.get_argument('user_name', None),
			'user_description': handler.get_argument('user_description', None),
			'user_email': handler.get_argument('user_email', None),
			'user_password': handler.get_argument('user_password', None),
			'client_id': handler.get_argument('client_id', None),
		}

		# Hasheamos el password si esta
		if paramsGet['user_password'] is not None:
			# Buscamos el HASH
			salt = DALeBlanc.get({'valid':True}, 'salts', {'limit': 1})
			paramsGet['user_salt'] = salt[0]['salt']

			# Lo Hasheamos
			password = hashlib.md5(paramsGet['user_password'] + paramsGet['user_salt']).hexdigest()
			paramsGet['user_password'] = password

		# Validamos los input params
		validate = LeBlancServices.validateParams(paramsGet, 'update', 'users')

		# Ejecutamos la query
		if validate['valid']:

			# Validamos que los datos a ingresar no existan.
			currentRow = DALeBlanc.get(paramsGet, 'users')

			if len(currentRow) <= 0:
				return simplejson.dumps(NaixCommon.Errors.REGISTER_MISSING(), default=str)

			# Hacemos que los None se remplacen por el valor anterior
			toRemove = []

			for key, param in paramsGet.iteritems():
				if param is None:
					toRemove.append(key)
				elif param == 'Null':
					paramsGet[key] = None

			if len(toRemove) > 0:
				for param in toRemove:
					del paramsGet[param]

			result = DALeBlanc.update(paramsGet, 'users')

			if result:
				return simplejson.dumps({'status':'SUCCESS', 'code': 201, 'description': 'Transaction update %s register\'s' % result}, default=str)
			else:
				return simplejson.dumps({'status':'NOTICE', 'code': 300, 'description': 'Nothing to Update'}, default=str)
		else:
			return validate['error']

	@staticmethod
	def deleteUser(handler):
		""" Para eliminar un usuario es necesario proporcionar todas las claves """

		# Los argumentos se tratan con el handler.get_argument('argument_name')
		# La IP se obtiene del comando handler.request.remote_ip
		paramsGet = {
			'user_name': handler.get_argument('user_name', None),
			'user_email': handler.get_argument('user_email', None),
		}

		# Validamos los input params
		validate = LeBlancServices.validateParams(paramsGet, 'delete', 'users')

		# Ejecutamos la query
		if validate['valid']:

			# Verificamos que el registro exista antes de eliminarlo.
			currentRow = DALeBlanc.get(paramsGet, 'users')

			if len(currentRow) <= 0:
				return simplejson.dumps(NaixCommon.Errors.REGISTER_MISSING(), default=str)

			result = DALeBlanc.delete(paramsGet, 'users')

			if result:
				return simplejson.dumps({'status':'SUCCESS', 'code': 201, 'description': 'Transaction delete %s register\'s' % result}, default=str)
			else:
				return simplejson.dumps({'status':'NOTICE', 'code': 300, 'description': 'Nothing to delete'}, default=str)

		else:
			return validate['error']

	# ---------- User Service ---------- #