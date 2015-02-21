# -*- coding: utf-8 -*-

from decimal  import Decimal
from datetime import datetime, tzinfo

import NaixCommon
import json

from NaixCommon.ValueObjects import VO_Message

from NaixCommon import Utils
from NaixCommon import simplejson

# from NaixCommon.Utils import InParams, InParam, Validate, MANDATORY, OPTIONAL
from NaixCommon.NaixLogger import NaixLogger

from DataAccess import DALeBlanc

LEBLANC_VERSION = "ALPHA"

class LeBlancServices:

	@staticmethod
	def getUser(handler):

		# Los argumentos se tratan con el handler.get_argument('argument_name')
		# La IP se obtiene del comando handler.request.remote_ip
		exception = NaixCommon.Errors.BAD_REQUEST()

		paramsGet = {
			'byName': handler.get_argument('byName', None),
			'byId': handler.get_argument('byId', None),
			'orderBy': handler.get_argument('orderBy', None),
			'limitBy': handler.get_argument('limitBy', None)
		}

		if paramsGet['byName'] or paramsGet['byId']:
			retult = DALeBlanc.getUser(paramsGet)
		else:
			return simplejson.dumps(exception, default=str)

		# pars = validate_pars(inParams, paramsGet)