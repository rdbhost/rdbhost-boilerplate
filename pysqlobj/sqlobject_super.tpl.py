#!/usr/bin/python
"""This Script was auto-generated for you to help you get started with the
rdbhost service and the SQLObject ORM. If you haven't installed it yet you can
get it at "https://{[{HOSTNAME}]}/downloads.hml".

The Example demonstrates how to make a connection the rdbhost service with
SQLObject, an Object Relational Manager, available at (http://sqlobject.org/). You may
need to checkout the latest version from http://svn.colorstudy.com/SQLObject/trunk/ that supports
the rdbhdb driver. A guide to installing from SVN is available at
http://sqlobject.org/DeveloperGuide.html .

It also demonstrates Error handling of different types of problems that may occur in your program, we
suggest playing around with adding/updating invalid data to see what happens.

You will be able to see the table sandbox.dvds in your database after running this
script at https://{[{HOSTNAME}]}/rdbadmin/

For Additional resources read the documentation that comes with SQLObject
and the documentation available on our website https://{[{HOSTNAME}]}/howpython.html
"""
from datetime import datetime
try:
    from rdbhdb import rdbhdb as db
    from rdbhdb.extensions import DictCursor
except ImportError:
    print "Couldn't import rdbhdb module"
    print "If you haven't installed it yet, you can obtain it at"
    print "https://{[{HOSTNAME}]}/downloads.html"
    exit(1)

try:
    import sqlobject.dberrors as sdbe
    from sqlobject import sqlhub, connectionForURI, SQLObject, StringCol, IntCol, FloatCol
    from sqlobject.main import SQLObjectNotFound
except ImportError:
    print "Couldn't import SQLObject"
    print "If you haven't installed it yet, you can obtain it at"
    print "http://sqlobject.org"
    exit(1)

# Your super role name from https://{[{HOSTNAME}]}/mbr/role_manager
SUPER_ROLE = '{[{SUPER_ROLE}]}'
# Your super role's authcode (keep this a secret!)
SUPER_AUTHCODE = '{[{SUPER_PASS}]}'

HOST = '{[{HOSTNAME}]}'

###############################################################################
###############################################################################

def setup_permissions():
    """Normally you wouldn't have this code in your applications, but we have it
    here to show you how permissions need to be granted for auth, preauth, etc.
    """
    # create a connection through our super role via db.connect
    try:
        super_connection = db.connect(SUPER_ROLE, authcode=SUPER_AUTHCODE, host='{[{HOSTNAME}]}')
    except db.OperationalError: # thrown if password or role don't match
        print 'Caught an exception while trying to log in, maybe your account does not exist yet?'
        #traceback.print_exc()
        exit()
    curs = super_connection.cursor(DictCursor)
    try:
        curs.execute('CREATE SCHEMA sandbox')
    except (db.ProgrammingError, db.OperationalError), e:
        pass
    super_connection.close()

def set_connection(role, authcode, host='{[{HOSTNAME}]}'):
    """Set the connection to be used by SQLObject, using our role and authcode"""
    try:
        sqlhub.processConnection = connectionForURI(
        'rdbhost://%s:%s@%s?schema=sandbox' % (role, authcode, host)
        )
    except AssertionError:
        print "Your Version of SQLObject doesn't seem to support our driver"
        print "Get the most recent version from http://sqlobject.org/DeveloperGuide.html"
        raise


class DVD(SQLObject):
    """Our DVD object which inherits SQLObject to make use of its ORM features"""
    class sqlmeta:
        # give our table a special name to put it in the sandbox schema
        table = 'sandbox.dvds_sqlobj'

    name = StringCol(alternateID=True, length=255)
    year = IntCol(default=datetime.now().year)
    rating = FloatCol()


if __name__ == '__main__':
    print 'This is a simple example on how to use SQLObject with rdbhost'
    print 'You can use the commands "help", "show", "exit", "add", "update"'
    print 'to interact with the database. Try adding some bad data to see how'
    print 'errors are handled'

    setup_permissions()
    set_connection(SUPER_ROLE, SUPER_AUTHCODE, HOST)
    # Create the table in the rdbhost database if it doesn't already exist
    try:
        DVD.dropTable()
    except sdbe.ProgrammingError, e:
        if e[0] != u'42P01': # table doesn't exist, thats okay though!
            raise
    DVD.createTable()
    # Create some DVDs, these are automatically saved
    DVD(name='Six Ways to Sunday', year=1997, rating=9.0)
    DVD(name='The Green Hornet',year=2011, rating=6.3)

    while True:
        iput = raw_input('>>')
        command = iput.split(' ', 1)[0]

        if command == 'help':
            print 'Following Commands are available'
            print 'help\t\tshow this help screen'
            print 'show\t\tdisplay the contents of sandbox.dvds'
            print 'add\t\tfollowed by "name, rating" adds a row to sandbox.dvds'
            print "update\t\tfollowed by 'name, rating' updates a movie's rating"
            print 'exit\t\texit program'
        elif command == 'show':
            dvds = DVD.select()
            print 'Name\t\trating'
            for dvd in dvds:
                print str(dvd)
        elif command == 'add':
            try:
                args = [tok.strip() for tok in iput.split(' ', 1)[1].split(',')]
                DVD(name=args[0], rating=float(args[1]))
            except IndexError, e:
                print 'Requires a name and rating i.e.'
                print '"add The Matrix, 9.0"'
        elif command == 'exit':
            break
        elif command == 'update':
            try:
                args = [tok.strip() for tok in iput.split(' ', 1)[1].split(',')]
                # Fetch the dvd with the auto-generated class method DVD.byName
                dvd = DVD.byName(args[0])
                dvd.rating = float(args[1])
            except SQLObjectNotFound, e:
                print 'No DVD named "%s"' % args[0]
            except IndexError, e:
                print 'Requires a name and rating i.e.'
                print '"add The Matrix, 9.0"'
        elif command:
            print '"%s" is not a recognized command, use "help" to list commands' % command
