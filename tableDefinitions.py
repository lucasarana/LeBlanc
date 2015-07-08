class tables:
	#probando eeeeee
	salts = {
		'database': 'LeBlanc',
		'name': 'salts',
		'auto_increment': ['salt_id'],
		'key': ['salt', 'valid'], 
		'fields': {
			'salt_id': {'type': 'INTEGER', 'maxlength':11, 'notnull': False, 'private': True },
			'salt': {'type': 'VARCHAR', 'maxlength':12, 'notnull': True, 'private': False },
			'valid': {'type': 'TINYINT', 'maxlength':1, 'notnull': True, 'private': False },
			'date_lastupdate': {'type': 'TIMESTAMP', 'maxlength':None, 'notnull': False, 'private': False },
		},
		'search_fields': ['user_id', 'user_name','user_email'],	
	}

	clients = {
		'database': 'LeBlanc',
		'name': 'clients',
		'auto_increment': ['client_id'],
		'key': ['client_name', 'client_email'], 
		'fields': {
			'client_id': {'type': 'INTEGER', 'maxlength':12, 'notnull': False, 'private': True },
			'client_name': {'type': 'VARCHAR', 'maxlength':120, 'notnull': True, 'private': False },
			'client_description': {'type': 'VARCHAR', 'maxlength':255, 'notnull': True, 'private': False },
			'client_email': {'type': 'VARCHAR', 'maxlength':120, 'notnull': True, 'private': False },
			'client_password': {'type': 'VARCHAR', 'maxlength':32, 'notnull': True, 'private': True },
			'client_salt': {'type': 'VARCHAR', 'maxlength':12, 'notnull': False, 'private': True },
			'client_status': {'type': 'VARCHAR', 'maxlength':1, 'notnull': False, 'private': False, 'default': 'P' },			
			'date_created': {'type': 'TIMESTAMP', 'maxlength':None, 'notnull': False, 'private': False, 'default': 'TIMESTAMP' },
		},
		'search_fields': ['client_id', 'client_name','client_email'],
	}

	users = {
		'database': 'LeBlanc',
		'name': 'users',
		'auto_increment': ['user_id'],
		'key': ['user_name', 'user_email'], 
		'fields': {
			'user_id': {'type': 'INTEGER', 'maxlength':12, 'notnull': False, 'private': True },
			'client_id': {'type': 'INTEGER', 'maxlength':12, 'notnull': False, 'private': True },
			'user_name': {'type': 'VARCHAR', 'maxlength':32, 'notnull': True, 'private': False },
			'user_description': {'type': 'VARCHAR', 'maxlength':64, 'notnull': True, 'private': False },
			'user_email': {'type': 'VARCHAR', 'maxlength':120, 'notnull': True, 'private': False },
			'user_password': {'type': 'VARCHAR', 'maxlength':32, 'notnull': True, 'private': True },
			'user_salt': {'type': 'VARCHAR', 'maxlength':12, 'notnull': False, 'private': True },
			'user_status': {'type': 'TINYINT', 'maxlength':1, 'notnull': False, 'private': False, 'default': 'P' },
			'date_created': {'type': 'TIMESTAMP', 'maxlength':None, 'notnull': False, 'private': False },
		},
		'search_fields': ['user_id', 'user_name','user_email','user_status'],
	}

