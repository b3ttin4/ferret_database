import sqlite3
import re

import tables,gen_database

def select_all_ferrets(conn):
	"""
	Query all rows in the ferrets table

	input:
	conn: the Connection object

	return:
	ferrets: list of all ferrets
	"""
	cur = conn.cursor()
	cur.execute("SELECT ferretNumber from ferrets")
	ferrets = cur.fetchall()
	return ferrets

def select_all_timeseries_for_key(conn,key,value,output_keys=None,ferret_subset=None,info_per_day=False):
	""" select all timeseries for given key
	
	input:
	conn: Connection for database
	key: str, "area", "exp"
	value: specific value of key
	output_keys: list of keys to output
	info_per_day: bool, if True return only one timeseries per day and ferret

	output:
	datasets: list of ferretNumber,date,ts in given area
	"""
	ferrets = select_all_ferrets(conn)

	cur = conn.cursor()
	params_str = ""
	if output_keys is not None:
		params_str = ","+",".join(output_keys)
		print("params_str",params_str,value)
	if info_per_day:
		cur.execute("SELECT DISTINCT ferret_id,date_id{} from timeseries WHERE {} = ? ORDER BY ferret_id".format(params_str,key),(value,))
	else:
		cur.execute("SELECT ferret_id,date_id,ts{} from timeseries WHERE {} = ? ORDER BY ferret_id".format(params_str,key),(value,))



	timeseries = cur.fetchall()
	print("timeseries",timeseries)

	datasets = []
	for row in timeseries:
		ferret_id,date_id = row[:2]
		
		cur.execute("SELECT ferretNumber from ferrets WHERE id=?",(ferret_id,))
		ferretNumber = cur.fetchone()[0]

		if (ferret_subset is not None and ferretNumber not in ferret_subset):
			continue

		cur.execute("SELECT date_exp from dates WHERE id=?",(date_id,))
		date = cur.fetchone()[0]

		dataset = [ferretNumber,date] + list(row[2:])
		datasets.append(dataset)

	return datasets



if __name__=="__main__":
	from tools import create_connection,get_database_path

	database_path = get_database_path()
	conn = create_connection(database_path)

	ts = select_all_timeseries_for_key(conn,"exp","none_black",output_keys=["area","ts"],\
										info_per_day=False)





	conn.close()
