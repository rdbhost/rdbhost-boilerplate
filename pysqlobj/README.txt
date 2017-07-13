

RDBHOST VIA SQLOBJECT
=========================

The popular SQLObject ORM will work with Rdbhost databases.

Neither SQLObject nor the Rdbhdb module are bundled, and should
be installed separately, prior to trying these scripts.  They are
both on Pypi, so try:

easy_install rdbhdb
easy_install sqlobject
 - or -
pip install rdbhdb
pip install sqlobject


The included script implements a simple DVD database.  It uses
the Super database role exclusively, and
assumes the user can be trusted not to maliciously recode the
script.

There is no Preauth mode script, as SQLObject does its own
parameter interpolation, and does not work well with white-listing.


Enjoy.

David Keeney
dkeeney@rdbhost.com