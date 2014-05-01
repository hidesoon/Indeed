import warnings
try:
    import MySQLdb as mdb 
except ImportError:
    warnings.warn("MySQLdb not found, database functionality disabled.")


class Database:
	# would be nice to be able store password somewhere else
    def __init__(self, user, password, database, h = 'localhost'):
        self.h = h
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        self.connection = mdb.connect(self.h, self.user, self.password, self.database)


    def into_db(self, commands):
	    # commands should be tuple of different commands
	    # will add ability to make this sort of structure
	    # this sort of thing will be dangerous without some filtering/checking
	    # be very careful about funky tuple nonsense, if only one command, then need a comma randomly
        with self.connection:
            cur = self.connection.cursor()
            for s in commands:	
                cur.execute(s)
                print "Executing: "+ s 


    def from_db(self, command, q = 'all'):
        with self.connection:
            cur = self.connection.cursor()
            cur.execute(command)   	
            if q == 'all':
                rows = cur.fetchall()	
                return rows
            else:
                return (cur.fetchone() for i in range(cur.rowcount))



        

