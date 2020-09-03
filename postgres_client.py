# postgres module
# intended to be used with remote database hosted on ElephantSQL
# for usage, please take a look at the comments at the bottom of this file

import psycopg2 as pg

class PGClient:
    """Postgres module that creates, updates, reads, and destroys records in the remote PostgreSQL database"""

    def __init__(self, dbname, user, password, host):
        """constructor. Should connect to db upon creation of object"""

        self._conn = None

        try:
            self._conn = pg.connect(dbname=dbname, user=user, password=password, host=host)
        except pg.Error as e:
            print('Error: ', e)
            print('Please check if database at https://www.elephantsql.com/ is still running. Program exiting...')
            raise(SystemExit)

        # create cursor after successfully connecting to DB
        self._cur = self._conn.cursor()

    def createRecord(self, student_id, name, house, points):
        """Creates a record in the database. Takes 4 separate fields,
        student_id: int, name: string, house: string, points: int"""
        success = False

        try:
            record = (student_id, name, house, points)
            sql = """INSERT INTO students(student_id, name, house, points)
                    VALUES(%s, %s, %s, %s)"""

            self._cur.execute(sql, record)
            self._conn.commit()
            success = True

        except pg.DatabaseError as e:
            print(e)
            print('Failed to upload to database')

        return success

    def fetchHouseRecords(self, house):
        """Reads house name and fetches all student records from house. Takes
        one argument, house: string"""
        payload = None

        try:
            # if house is 'All', then fetch all records from table
            if house == 'All':
                sql = """SELECT * FROM students"""
                self._cur.execute(sql)
            else:
                sql = """SELECT * 
                        FROM students
                        WHERE house = %s"""
                self._cur.execute(sql, (house,))
            payload = self._cur.fetchall()
            payload = sorted(payload, key=lambda t: t[0])   # sort by primary key

        except pg.DatabaseError as e:
            print(e)
            print("Failed to fetch from database")

        return payload

    def updateRecord(self, record):
        """Updates a single record. Uses record pk to select record.
        Takes a tuple argument, record = (pk, studnet_id, name, house, points).
        NOTE: Updated row is moved to the bottom of the table"""

        success = False

        # destructure record here since order of sql variables are
        # in a different order for the query
        pk, student_id, name, house, points = record

        try:
            sql = """UPDATE students 
                    SET name = %s,
                        student_id = %s,
                        house = %s,
                        points = %s
                    WHERE pk = %s"""
            self._cur.execute(sql, (name, student_id, house, points, pk)) # note: pk is placed at the end of the tuple
            self._conn.commit()
            success = True

        except pg.DatabaseError as e:
            print(e)
            print("Unable to update record in database")

        return success

    def deleteRecord(self, pk):
        """Deletes single record from database. Takes only pk: int, as argument. Note: this is not student_id"""
        try:
            sql = """DELETE FROM students
                    WHERE pk = %s"""
            self._cur.execute(sql, (pk,))
            self._conn.commit()

        except pg.DatabaseError as e:
            print(e)
            print("Unable to remove record from database")

    def __del__(self):
        """Destructor. Close out data base connection before destroying the object"""

        if self._conn:
            self._cur.close()
            self._conn.close()