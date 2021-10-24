import sqlite3
from tools import get_database_path,create_connection
import tables

def create_table(conn,create_table_sql):
	""" create a table from the create_table_sql statement
	
	input:
	conn: Connection object
	create_table_sql: a CREATE TABLE statement
	
	return:
	"""
	try:
		c = conn.cursor()
		c.execute(create_table_sql)
	except Exception as e:
		print("Exception",e)


def parse_datasets_to_sql_database(conn,ferrets=None):
	from mustela_bh.tools import ferret_groups
	from mustela_bh.datasets import descriptions,parse_directory_structure,stimtypes

	"""
	populate sqlite database with ferrets,dates and timeseries information
	
	input:
	conn: Connection object
	ferrest: list of ferretNumbers for creating entries in database
	
	output:

	"""
	if ferrets is None:
		ferrets = ferret_groups.ferret_groups["pfc"]

	for ferret in ferrets:
		dates = parse_directory_structure.get_all_dates_for_ferret(ferret)
		birth_date = descriptions.all_descriptions[str(ferret)]["date_of_birth"]
		eo_date = descriptions.all_descriptions[str(ferret)]["date_of_eye_opening"]
		ref_date_dict = descriptions.all_descriptions[str(ferret)]["morphing_reference_date"]
		if isinstance(ref_date_dict,dict):
			ref_date = ref_date_dict[list(ref_date_dict.keys())[0]][0]
		else:
			ref_date = ref_date_dict

		ferret_tuple = (ferret,birth_date,ref_date,eo_date)
		# print("ferret_tuple",ferret_tuple)
		ferret_id = tables.create_ferret(conn, ferret_tuple)

		for date in dates:
			date_tuple = (date,ferret_id)
			# print("date_tuple",date_tuple)
			date_id = tables.create_dates(conn,date_tuple)

			datasets = parse_directory_structure.get_all_datasets_for_date(ferret,date)

			for dataset in datasets:
				ts = dataset.series_number
				area = dataset.desc["areal"][0]
				exp = dataset.desc["stim"]#stimtypes.stim_type.reverse_mapping[dataset.desc["stim"]]
				ref_ts = ref_date_dict[area][1]

				ts_tuple = (ts,area,exp,ref_ts,date_id,ferret_id)
				# print("ts_tuple",ts_tuple,ferret)
				tables.create_ts(conn,ts_tuple)



def populate_database():
	""" creates table and populates sqlite database from scratch """
	database_path = get_database_path()
	conn = create_connection(database_path)

	sql_create_projects_ferret = tables.sql_create_projects_ferret
	sql_create_projects_date = tables.sql_create_projects_date
	sql_create_projects_ts = tables.sql_create_projects_ts

	with conn:
		create_table(conn, sql_create_projects_ferret)
		create_table(conn, sql_create_projects_date)
		create_table(conn, sql_create_projects_ts)
		
		parse_datasets_to_sql_database(conn)



def update_database():
	""" updates individual tables in sqlite database """
	database_path = get_database_path()
	conn = create_connection(database_path)

	# order of tuple_new is tuple_old + id
	# examples from database
	ferret_new = (23,"2018-06-11","2018-07-11",2,"3000-07-10",1)
	date_new = None
	ts_new = None#(4,"v1","none_black",45,42,736)

	with conn:
		if ferret_new is not None:
			tables.update_ferrets(conn, ferret_new)

		if date_new is not None:
			tables.update_dates(conn, date_new)

		if ts_new is not None:
			print("update te")
			tables.update_ts(conn, ts_new)


def delete_entries_database():
	""" delete entries in individual tables in sqlite database """
	database_path = get_database_path()
	conn = create_connection(database_path)

	tables.delete_entry_in_table(conn, "ferrets", 1)
	conn.close()


if __name__=="__main__":
	populate_database()

	# update_database()

	# delete_entries_database()
