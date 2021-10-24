import os
import sqlite3

def get_database_path():
	""" returns path for database """
	home_path = os.environ["HOME"]
	if os.environ["USER"]=="bettina":
		path = os.path.join(home_path,\
				r"physics/code/smithlab/Python_Scripts/mustela_bh/database/database/data/ferret_database.db")
	elif os.environ["USER"]=="heinb":
		path = os.path.join(home_path,\
				r"code/Python Scripts/mustela_bh/database/database/data/ferret_database.db")
	return path


def create_connection(db_file):
	""" create a database connection to a sqlite database
	
	input: 
	db_file: database file

	output:
	Connection object or None
	"""
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		print(sqlite3.version)
	except Exception as e:
		print("Exception",e)

	return conn