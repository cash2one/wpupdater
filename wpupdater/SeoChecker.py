import MySQLdb
import sys

class Database:

    def __init__(self, *args, **kwargs):
        self.host = kwargs.get('host')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.dbname = kwargs.get('dbname')
        self.connect()

    def connect(self):
        try:
            self.connection = MySQLdb.connect(user=self.username,passwd=self.password,host=self.host,db=self.dbname)
        except MySQLdb.MySQLError as e:
            print "Error while connecting to database %s"%e
            sys.exit(1)

class Domain:

    def __init__(self, db_conn, sql):
        self.db_conn = db_conn
        self.sql = sql

    def get_wp_list(self):
        c = self.db_conn.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        c.execute(self.sql)
        result = c.fetchall()
        return result

