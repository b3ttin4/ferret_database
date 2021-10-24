import sqlite3
import re


def getSchema(conn):
	"""
	collects schema of database
	input:
	conn: connection object to sqlite database

	output:
	schema: list of schemas
	table_names: names of tables in database
	"""
	cur = conn.cursor()

	cur.execute("SELECT name FROM SQLITE_MASTER WHERE type='table' ORDER BY rootpage")
	table_names = cur.fetchall()
	

	cur.execute("SELECT sql FROM SQLITE_MASTER WHERE type='table' ORDER BY rootpage")
	table_structs = cur.fetchall()
	regex = re.compile(r"FOREIGN KEY \(\w+\) REFERENCES \w+ \(\w+\)")
	regex2 = re.compile(r"\w+ \(\w+\)")

	schema = []
	for (table_name,),(table_struct,) in zip(table_names,table_structs):
		cur.execute("PRAGMA table_info({})".format(table_name))
		rows = cur.fetchall()
		table_infos = []
		for row in rows:
			columnID,columnName,columnType,columnNotNull,columnDefault,columnPK = row
			table_infos.append([columnID,columnName,columnType,columnNotNull,\
								columnDefault,columnPK,"-","-"])
			for j,item in enumerate(table_infos[-1]):
				if item is None:
					table_infos[-1][j] = "-"

		table_struct = table_struct.replace("\n","")
		table_struct = table_struct.replace("\t","")
		matches = regex.findall(table_struct)
		for match in matches:
			m = match.split(" ")
			ref_table = m[4]
			ref_key = m[5].replace("(","").replace(")","")
			new_key = m[2].replace("(","").replace(")","")

			for table_info in table_infos:
				if new_key==table_info[1]:
					table_info[-2] = ref_table
					table_info[-1] = ref_key

		schema.append(table_infos)

	return schema,table_names

def printSchema(schema,table_names):
	"""
	print schema in table format
	input:
	schema: list of schema of all tables in database
	table_names: names of tables in database
	"""
	num_tables = len(schema)

	colLabels = ["ID","Name","Type","NotNull","Default","PK","FK","FK key"]
	hlines = ["---","---","---","---","---","---","---","---"]
	key_string = "| {:<5} | {:<15} | {:<10} | {:<10} | {:<10} | {:<5} | {:<10} | {:<10} |"

	# key_string = " {}, ".join(colLabels)
	# print("key_string",key_string)

	for (name,),table_schema in zip(table_names,schema):
		print("")
		print("Table: {}".format(name))
		print(key_string.format(*colLabels))
		print(key_string.format(*hlines))
		for row in table_schema:
			print(key_string.format(*row))
		


if __name__=="__main__":
	from mustela_bh.database.database import create_connection,get_database_path

	database_path = get_database_path()
	conn = create_connection(database_path)

	schema,table_names = getSchema(conn)
	printSchema(schema,table_names)