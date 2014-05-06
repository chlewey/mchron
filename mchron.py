# -*- coding: UTF-8 -*-

import sitrad,emailer,myreport
import os

from mytime import *
from myreport import report
import config

CONFIGFILE = 'mchron.cfg'

EMAILMSG = """
Este es un correo automámatico generado por el
sistema de la Oruga Amarilla como reporte de
actividad.

Sitio: {}
Generado el {}, a las {}

Período del {}, a las {}.
         al {}, a las {}.
"""

def getdb():
	section = 'Database'
	maker = config.get(section,'maker')
	if maker is None:
		raise 'No database maker provided'
	if maker=='sitrad':
		dbfile = config.get(section,'source','datos.db')
		path = config.get(section,'path','C:\\Documents and Settings\\All Users\\Application Data\\Full Gauge\\Sitrad')
		if path not in ['.','']:
			dbfile = path.rstrip('/')+'/'+dbfile
		return sitrad.database(dbfile)
	raise 'No configuration for a "{}" database'.format(maker)

def main(debug=False):
	""" Read the configuration file """
	config.init(CONFIGFILE)
	ltime = config.get('Run','time')
	ntime = now()
	if ltime is not None:
		print 'Last time was {}.'.format(ltime)
		otime = asc2time(ltime)
	else:
		print 'Never run before.'
		otime = ntime - 30*24*60*60
	print 'Current time is {}.'.format(time2asc(ntime))
	if ntime - otime < 86400:
		otime = (int(ntime/3600)-24)*3600
	print 'Reading since {}.'.format(time2asc(otime))

	""" Read the database """
	d = {'time': [ntime,otime], 'data': {}, 'keys': {}}
	with getdb() as db:
		d = db.run(d)

	""" Form the document """
	docfn = "{}_{}.pdf".format(
		config.get('Report','namebase','report'),
		time2fmt('%Y-%m-%d(%I%p)',ntime))
	print docfn
	#try:
	report(docfn,d)
	#except Exception, exc:
	#	config.close()
	#	raise exc

	""" Email the document """
	txt = EMAILMSG.format(
		config.get('Site','name'),
		time2esk(ntime),
		time2hms(ntime),
		time2esk(conf2time('Run','from',otime)),
		time2hms(conf2time('Run','from',otime)),
		time2esk(conf2time('Run','to',ntime)),
		time2hms(conf2time('Run','to',ntime))
		)
	if debug:
                emailer.nsend(txt)
        else:
        	emailer.send(txt,[docfn])

	""" Saving configuration """
	config.set('Run','time',time2asc(ntime))
	config.close()

if __name__ == "__main__":
        from sys import argv
	main('debug' in argv)
