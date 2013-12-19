# -*- coding: UTF-8 -*-

import sitrad,emailer,myreport
import os

from mytime import *
from myreport import report
from config import mcConfig

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

def getdb(config):
	section = 'Database'
	maker = config.xget(section,'maker')
	if maker is None:
		raise 'No database maker provided'
	if maker=='sitrad':
		dbfile = config.xget(section,'source','datos.db')
		path = config.xget(section,'path','C:\\Documents and Settings\\All Users\\Application Data\\Full Gauge\\Sitrad')
		if path not in ['.','']:
			dbfile = path.rstrip('/')+'/'+dbfile
		return sitrad.database(dbfile)
	raise 'No configuration for a "{}" database'.format(maker)

def main():
	""" Read the configuration file """
	with mcConfig(CONFIGFILE) as config:
		ltime = config.xget('Run','time')
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
		with getdb(config) as db:
			d = db.run(config,d)

		""" Form the document """
		docfn = "{}_{}.pdf".format(
			config.xget('Report','namebase','report'),
			time2ymd(ntime))
		report(docfn,config,d)

		""" Email the document """
		emailer.nsend(config,EMAILMSG.format(
			config.xget('Site','name'),
			time2esk(ntime),
			time2hms(ntime),
			time2esk(conf2time(config,'Run','from',otime)),
			time2hms(conf2time(config,'Run','from',otime)),
			time2esk(conf2time(config,'Run','to',ntime)),
			time2hms(conf2time(config,'Run','to',ntime))
			),
			[docfn])

		""" Saving configuration """
		config.xset('Run','time',time2asc(ntime))


if __name__ == "__main__":
	main()
