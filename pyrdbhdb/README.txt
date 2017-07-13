

RDBHDB MODULE FOR RDBHOST
=========================


The Rdbhdb module provides a DB API 2 module for accessing Rdbhost
databases from any Python application with internet access.

The Rdbhdb module is not bundled, and should be installed
separately, prior to trying these scripts.  It is on Pypi, so try:

easy_install rdbhdb
 - or -
pip install rdbhdb



The included scripts implement a simple DVD database.  The first
'rdbhdb_super.py' uses the Super database role exclusively, and
assumes the user can be trusted not to maliciously recode the
script.

The second script 'rdbhdb_orole_setup.py' uses both Super and
Preauth roles.  The Super role sets up the schema and tables, and
the Preauth role trains the white-list.  You should enable
Training Mode from the website profile page before running this,
and (IMPORTANT!) disable Training Mode afterwards.

Be sure to exercise every command during this session, as that
is how the server white-list learns which SQL queries are
permissible.

The third script 'rdbhdb_orole.py' uses the Preauth role only,
and can be used by untrusted users, assuming Training Mode has
been turned off at the end of the 'rdbhdb_orole_setup.py' session.
Editing malicious SQL queries into this script would be harmless, as
the trained white-list filter will block non-white-listed Preauth
queries.


Enjoy.

David Keeney
dkeeney@rdbhost.com