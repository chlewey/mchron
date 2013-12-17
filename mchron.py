
import sqlite3,debug,sitrad

dfile = 'datos.db'
with sitrad.sitradDB(dfile) as db:
	print db.check()
