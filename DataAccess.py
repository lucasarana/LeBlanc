# -*- coding: utf-8 -*-
import traceback
import random
import psycopg2
import psycopg2.extras
from threading import Lock

import config
import NaixCommon.Errors

from NaixCommon.NaixLogger import NaixLogger

class DALeBlanc:
	
	@staticmethod
	def getUser(inParams):
		""" Lista los usuarios """
		print "GG";