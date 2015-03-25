class tables:
	
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

	users = {
		'database': 'LeBlanc',
		'name': 'users',
		'auto_increment': ['user_id'],
		'key': ['user_name', 'user_email'], 
		'fields': {
			'user_id': {'type': 'INTEGER', 'maxlength':12, 'notnull': False, 'private': True },
			'client_id': {'type': 'INTEGER', 'maxlength':12, 'notnull': False, 'private': True },
			'user_name': {'type': 'TINYINT', 'maxlength':32, 'notnull': True, 'private': False },
			'user_description': {'type': 'TINYINT', 'maxlength':64, 'notnull': True, 'private': False },
			'user_email': {'type': 'TINYINT', 'maxlength':120, 'notnull': True, 'private': False },
			'user_password': {'type': 'TINYINT', 'maxlength':32, 'notnull': True, 'private': True },
			'user_salt': {'type': 'TINYINT', 'maxlength':12, 'notnull': False, 'private': True },
			'date_created': {'type': 'TIMESTAMP', 'maxlength':None, 'notnull': False, 'private': False },
		},
		'search_fields': ['user_id', 'user_name','user_email'],
	}

