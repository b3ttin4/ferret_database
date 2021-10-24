sql_create_projects_ferret = """ CREATE TABLE IF NOT EXISTS ferrets (
									id integer PRIMARY KEY,
									ferretNumber integer NOT NULL,
									birth_date text,
									ref_date text,
de									eo_date text
								); """

sql_create_projects_date = """ CREATE TABLE IF NOT EXISTS dates (
									id integer PRIMARY KEY,
									date_exp text NOT NULL,
									ferret_id integer NOT NULL,
									FOREIGN KEY (ferret_id) REFERENCES ferrets (id)
								); """


sql_create_projects_ts = """ CREATE TABLE IF NOT EXISTS timeseries (
									id integer PRIMARY KEY,
									ts integer NOT NULL,
									area text,
									exp text,
									ref_ts integer,
									date_id integer NOT NULL,
									ferret_id integer NOT NULL,
									FOREIGN KEY (ferret_id) REFERENCES ferrets (id)
									FOREIGN KEY (date_id) REFERENCES dates (id)
								); """


def create_ferret(conn, ferret):
	"""
	Create a new ferret into the ferrets table

	input:
	conn: Connection to sqlite database
	ferret:

	:return: ferret id
	"""
	sql = ''' INSERT INTO ferrets(ferretNumber,birth_date,ref_date,eo_date)
	          VALUES(?,?,?,?) '''
	cur = conn.cursor()
	cur.execute(sql, ferret)
	conn.commit()
	return cur.lastrowid #get back generated id


def update_ferrets(conn, ferret):
	""" update ferretNumber,birth_date,ref_date,ref_ts,eo_date
	input:
	conn: Connection to sqlite database
	ferret: tuple of ferret parameters

	output:
	ferret_id
	"""
	sql = """ UPDATE ferrets
				SET ferretNumber = ? ,
					birth_date = ? ,
					ref_date = ? ,
					eo_date = ?
				WHERE id = ?"""
	cur = conn.cursor()
	cur.execute(sql, ferret)
	conn.commit()


def create_dates(conn, date):
	"""
	Create a new date into the dates table

	input:
	conn: Connection to sqlite database
	date:

	:return: date id
	"""
	sql = ''' INSERT INTO dates(date_exp,ferret_id)
	          VALUES(?,?) '''
	cur = conn.cursor()
	cur.execute(sql, date)
	conn.commit()
	return cur.lastrowid #get back generated id

def update_dates(conn, date):
	""" update date_exp,ferret_id
	input:
	conn: Connection to sqlite database
	date: tuple of date parameters

	output:
	date_id
	"""
	sql = """ UPDATE dates
				SET date_exp = ? ,
					ferret_id = ?
				WHERE id = ?"""
	cur = conn.cursor()
	cur.execute(sql, date)
	conn.commit()


def create_ts(conn, timeser):
	"""
	Create a new timeseries into the timeseries table

	input:
	conn: Connection to sqlite database 
	timeser:

	:return: timeser id
	"""
	sql = ''' INSERT INTO timeseries(ts,area,exp,ref_ts,date_id,ferret_id)
	          VALUES(?,?,?,?,?,?) '''
	cur = conn.cursor()
	cur.execute(sql, timeser)
	conn.commit()
	return cur.lastrowid #get back generated id


def update_ts(conn, timeser):
	""" update ts,area,exp,date_id,ferret_id
	input:
	conn: Connection to sqlite database
	timeser: tuple of timeser parameters

	output:
	timeser_id
	"""
	sql = """ UPDATE timeseries
				SET ts = ? ,
					area = ? ,
					exp = ? ,
					ref_ts = ? ,
					date_id = ? ,
					ferret_id = ?
				WHERE id = ?"""
	cur = conn.cursor()
	cur.execute(sql, timeser)
	conn.commit()


def delete_entry_in_table(conn, table_name, id):
	""" delete table entry by id
	input:
	conn: Connection to sqlite database
	table_name: table name (ferrets, dates, timeseries)
	id: id of entry

	output:
	"""
	sql = 'DELETE FROM {} WHERE id=?'.format(table_name)
	cur = conn.cursor()
	cur.execute(sql, (id,))
	conn.commit()


def delete_all_entries_in_table(conn, table_name):
	""" delete all table entry
	input:
	conn: Connection to sqlite database
	table_name: table name (ferrets, dates, timeseries)

	output:
	"""
	sql = 'DELETE FROM {}'.format(table_name)
	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()