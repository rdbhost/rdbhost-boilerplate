#!/usr/bin/python
"""This Script was auto-generated for you to help you get started with the
rdbhost service and the rdbhdb API. If you haven't installed it yet you can
get it at "https://{[{HOSTNAME}]}/downloads.hml". Once It is installed you can
execute this script via the python interpreter

The Example demonstrates how to make a connection the rdbhost service via the
API described in http://www.python.org/dev/peps/pep-0249/ .It also demonstrates
Error handling of different types of problems that may occur in your program, we
suggest playing around with adding/updating invalid data to see what happens.

You will be able to see the table sandbox.dvds in your database after running this
script at https://{[{HOSTNAME}]}/rdbadmin/

For Additional resources read the documentation that comes with the rdbhdb module
and the documentation available on our website https://{[{HOSTNAME}]}/howpython.html
"""
import traceback
try:
    from rdbhdb import rdbhdb as db
    from rdbhdb.extensions import DictCursor

except ImportError:
    print "Couldn't import rdbhdb module"
    print "If you haven't installed it yet, you can obtain it at"
    print "https://{[{HOSTNAME}]}/downloads.html"
    exit(1)


# Your super role name from https://{[{HOSTNAME}]}/mbr/role_manager
SUPER_ROLE = '{[{SUPER_ROLE}]}'
# Your super role's authcode (keep this a secret!)
SUPER_AUTHCODE = '{[{SUPER_PASS}]}'

HOST = '{[{HOSTNAME}]}'

class BasicDatabaseConnector(object):
    """A Simple Object that will connect to the rdbhost server on initialization
    and create a simple DVD-based example table and allow you to interact with it
    in order to demonstrate the rdbhdb API
    """
    def __init__(self):
        """Initialize the database connector by connecting to rdbhost with your
        account and authcode, and create an example table
        """
        # create a connection through our super role via db.connect
        try:
            self.connection = db.connect(SUPER_ROLE, authcode=SUPER_AUTHCODE, host=HOST)
        except db.OperationalError: # thrown if password or role don't match
            print 'Caught an exception while trying to log in, maybe your account does not exist yet?'
            exit()
            
        # get a DictCursor as our cursor (which returns queries as column-name dicts)
        self.cursor = self.connection.cursor(DictCursor)
        
        self.setup_tables()
        
    def setup_tables(self):
        """Drop and then Create a schema and table to use with the examples"""
        try:
            self.cursor.execute('CREATE SCHEMA sandbox')
            self.cursor.execute("DROP TABLE sandbox.dvds_rdbhdb_super;")
        except (db.ProgrammingError, db.OperationalError), e:
            # sandbox may not exist
            pass #raise

        try:
            self.cursor.execute(
            """CREATE TABLE sandbox.dvds_rdbhdb_super(
                id          SERIAL PRIMARY KEY,
                name        varchar(40) NOT NULL,
                rating      float,
                UNIQUE(name)
                );
            """ )
        except db.ProgrammingError, e:
            if e[0] != '42P07':
                raise

    def add_dvd(self, name, rating):
        """Add a 'dvd' to the database"""
        try:
            self.cursor.execute(
                """INSERT INTO sandbox.dvds_rdbhdb_super (name, rating)
                VALUES (%s, %s);""" , 
                (name, rating)
            )
        # catch the most broad type of error
        except (db.DataError, db.IntegrityError), e:
            if e[0] == '22P02':
                print 'Cannot add %s because its not a valid float' % rating
            elif e[0] == '23505':
                print 'Cannot add %s because of UNIQUE constraint on "name"' % name
            else:
                print 'Caught Error while trying to add (%s, %s)' % (name, rating)
            #traceback.print_exc()
            
    
    def update_rating(self, name, rating):
        """Update a Movie's rating given its' name"""
        try:
            self.cursor.execute(
            """UPDATE sandbox.dvds_rdbhdb_super
                SET rating = %s
                WHERE name LIKE %s
                """, 
                (rating, name)
            )
        except (db.DataError, db.IntegrityError), e:
            if e[0] == '22P02':
                print 'Cannot add %s because its not a valid float' % rating
            else:
                print 'Caught Error while trying to update %s to %s' % (name, rating)
            #traceback.print_exc()
    
    def get_all_dvds(self):
        """Return all DVDs as a list of dictionaries with column name : value entries"""
        self.cursor.execute(
        """SELECT *
            FROM sandbox.dvds_rdbhdb_super
        """,
         (id,)
        )
        dvds = self.cursor.fetchall()
        if dvds:
            return dvds
        else:
            return []
    
    def close(self):
        """Tell rdbhost that this session has expired"""
        self.connection.close()

# Execute the script to allow you to interact with the Database
if __name__ == '__main__':

    print 'This is a simple example on how to use the rdbhdb API'
    print 'You can use the commands "help", "show", "exit", "add", "update"'
    print 'to interact with the database. Try adding some bad data to see how'
    print 'errors are handled'
    
    # Create a database and fill it with some data
    myDB = BasicDatabaseConnector()
    if not myDB.get_all_dvds():
        myDB.add_dvd('Six Ways to Sunday', 9.0)
        myDB.add_dvd('The Green Hornet', 6.3)
    
    def inputHelp(cmd):
        print 'Requires a name and rating i.e.'
        print cmd+' The Matrix, 9.0'

    while True:
        iput = raw_input('>>')
        command = iput.split(' ', 1)[0]
        
        if command == 'help':
            print 'Following Commands are available'
            print 'help\t\tshow this help screen'
            print 'show\t\tdisplay the contents of sandbox.dvds'
            print 'add\t\tfollowed by "name, rating" adds a row to sandbox.dvds'
            print "update\t\tfollowed by 'name, rating' updates a movie's rating"
            print 'exit\t\texit program and close connection'
        elif command == 'show':
            dvds = myDB.get_all_dvds()
            print 'Name\t\trating'
            for dvd in dvds:
                print '%s\t\t%s' % (dvd['name'], dvd['rating'])
        elif command == 'add':
            try:
                args = [tok.strip() for tok in iput.split(' ', 1)[1].split(',')]
                myDB.add_dvd(args[0], args[1])
            except IndexError, e:
                inputHelp('add')
        elif command == 'exit':
            myDB.close()
            break
        elif command == 'update':
            try:
                args = [tok.strip() for tok in iput.split(' ', 1)[1].split(',')]
                myDB.update_rating(args[0], args[1])
            except IndexError, e:
                inputHelp('update')
        elif command:
            print '"%s" is not a recognized command, use "help" to list commands' % command
