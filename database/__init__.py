import os
import sqlite3

def get_database_path():
	""" returns path for database """
	current_dir = os.getcwd()
	path = os.path.join(current_dir,\
				r"/ferret_database/database/data/ferret_database.db")
  if not os.path.exists(path):
    print("Error: Path to ferret_database.db not found.")
    return None
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
