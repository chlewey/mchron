
from PyPDF2 import PdfFileWriter
#from ConfigParser import ConfigParser
import sitrad
import os,time

from config import mcConfig

CONFIGFILE = 'mchron.cfg'

def getdb(config):
	section = 'Database'
	maker = config.xget(section,'maker')
	if maker is None:
		raise 'No database maker provided'
	if maker=='sitrad':
		dbfile = config.xget(section,'source','datos.db')
		path = config.xget(section,'path','.')
		if path not in ['.','']:
			dbfile = path.rstrip('/')+'/'+dbfile
		return sitrad.database(dbfile)
	raise 'No configuration for a "{}" database'.format(maker)
	

sitradtrans = {
    'status': 'status',
	'datacad': 'date',
	'modelo': 'model',
	'descricao': 'description'
}

sitradconvs = {
	'datacad': 'date',
}
def sitradconv(value,key=None):
	if key in sitradconvs.keys():
		ckey = sitradconvs[key]
		if ckey == 'date':
			return time.ctime(sitrad.data2time(value))
		pass
	return value

def main():
	""" Read the configuration file """
	with mcConfig(CONFIGFILE) as config:
		ltime = config.xget('Run','time')
		ntime = time.time()
		if ltime is not None:
			print 'Last time was {}.'.format(ltime)
			otime = time.mktime(time.strptime(ltime))
		else:
			print 'Never run before.'
			otime = ntime - 30*24*60*60
		print 'Current time is {}.'.format(time.ctime(ntime))
		if ntime - otime < 86400:
			otime = (int(ntime/3600)-24)*3600
		print 'Reading since {}.'.format(time.ctime(otime))
		ttime = otime - 30*24*60*60
		stime = sitrad.time2data(ttime)

		""" Read the database """
		d = {}
		with getdb(config) as db:
			for table in db.tables():
				if table=='empresa':
					a,e = db.query(table)
					empresa = e[0][0]
					r = config.check('Site','name',empresa,True)
					d[table] = empresa
				elif table in ['modulo_io_cfg']:
					a,e = db.query(table)
					d[table] = [dict(zip(a,q)) for q in e]
				elif table == 'instrumentos':
					a,e = db.query(table)
					dd =  dict(zip([q[0] for q in e],[dict(zip(a[1:],q[1:])) for q in e]))
					d[table] = dd
					[config.check('Site','instrument-{}'.format(x),dd[x]['descricao'],True) for x in dd.keys()]
					for x in dd.keys():
						for k in dd[x].keys():
							if k in sitradtrans.keys():
								config.check('Instrument {}'.format(x), sitradtrans[k], sitradconv(dd[x][k],k))
				elif table=='rel_alarmes':
					a,e = db.query(table,where="dataInicio>{0} OR dataFim>{0}".format(stime))
					dd = [dict(zip(a,q)) for q in e]
					d[table] = dd
					larms = {}
					for l in e:
						if l[0] not in larms.keys():
							larms[l[0]] = set()
						larms[l[0]].add(l[1])
					z = [config.check('Instrument {}'.format(x), 'alarms', (';\n'.join(larms[x])).encode('utf8')) for x in larms.keys()]
					print table,z
				else:
					a,e = db.query(table,where="data>{0}".format(stime))
					if len(e):
						dd = [dict(zip(a,q)) for q in e]
						d[table] = dd
						y = set([x[0] for x in e])
						z = [config.check(table,x,False) for x in a]
						for x in y:
							config.check('Instrument {}'.format(x), 'type', table)
							for i in range(len(a)):
								if z[i]:
									config.check(table,a[i],z[i])
						config.xset(table,'instruments',','.join([str(x) for x in y]))
						print table,y,z
			
		""" Form the document """
	
		""" Email the document """
	
		""" Saving configuration """
		#cput(config,'Run','date',date)
		config.xset('Run','time',time.ctime(ntime))
		with open(CONFIGFILE,'w') as file:
			config.write(file)


if __name__ == "__main__":
	main()
            

