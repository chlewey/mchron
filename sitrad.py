
import sqlite3,debug,json,time,config
from mytime import *

latest = 25568.0
instrumentos = {}
empresa = ''

class database:
	def __init__(self,dfile):
		self.db = sqlite3.connect(dfile)
		self.db.text_factory = bytes

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		pass

	def adjust(self,x):
		if x==b'0': return False
		if x==b'1': return True
		if type(x)==type(b''): return x.decode('latin-1')
		return x
		
	def query(self,query,limit=1000):
		tab = self.db.cursor()
		try:
			tab.execute(query)
		except:
			debug.err(query)
			exit()
		res = [[self.adjust(item) for item in row] for row in tab.fetchmany(limit)]
		kis = [str(i[0]) for i in tab.description]
		return (kis,res)

	def select(self,table,limit=1000,where=None,order=None,desc=False):
		query = "SELECT * FROM "+table
		if where: query+= " WHERE "+where
		if order: query+= " ORDER BY "+order
		if desc: query+= " DESC"
		tab = self.db.cursor()
		try:
			tab.execute(query)
		except:
			debug.err(query)
			exit()
		res = [[self.adjust(item) for item in row] for row in tab.fetchmany(limit)]
		kis = [str(i[0]) for i in tab.description]
		return (kis,res)
		
	def tables(self):
		k,r = self.select('sqlite_master',where="type='table'")
		return [i[1] for i in r]

	def run(self,d):
		assert type(d)==dict
		ntime = d['time'][0]
	#	d['time'][1]-= 31*24*60*60
		ttime = d['time'][1]
		stime = time2data(ttime)

		for table in self.tables():
			if table=='empresa':
				a,e = self.select(table)
				empresa = e[0][0]
				if empresa is None: continue
				r = config.check('Site','name',empresa.encode('UTF-8'),True)
				r = config.check('Report','title',empresa.encode('UTF-8'))
				d[table] = empresa
			elif table in ['modulo_io_cfg']:
				a,e = self.select(table)
				d[table] = [dict(zip(a,q)) for q in e]
			elif table == 'instrumentos':
				a,e = self.select(table)
				dd = dict([[q[0],dict(translate(zip(a[1:],q[1:])))] for q in e])
				d[table] = dd
				[config.check('Site','instrument-{}'.format(x),dd[x]['description'].encode('UTF-8'),True) for x in dd.keys()]
				[config.check('Figure {}'.format(x),'description',dd[x]['description'].encode('UTF-8')) for x in dd.keys()]
				for x in dd.keys():
					for k in dd[x].keys():
						if k in ['status','date','model']:
							config.check('Instrument {}'.format(x), k, dd[x][k])
						elif k=='description':
							config.check('Instrument {}'.format(x), k, dd[x][k].encode('UTF-8'))
				config.checklist('Report','figures',['Figure {}'.format(x) for x in dd.keys()])
			elif table=='rel_alarmes':
				a,e = self.select(table,where="dataInicio>{0} OR dataFim>{0}".format(stime))
				dd = [dict(zip(a,q)) for q in e]
				d[table] = dd
				larms = {}
				for l in e:
					if l[0] not in larms.keys():
						larms[l[0]] = set()
					larms[l[0]].add(l[1].encode('utf8'))
				z = [config.checklist('Instrument {}'.format(x), 'alarms', larms[x]) for x in larms.keys()]
			else:
				u,v = self.query('SELECT id,COUNT(*) AS n FROM {} WHERE data>{} GROUP BY id;'.format(table,stime))
				if not len(v):
					continue
				for i,n in v:
					d['data'][i] = {}
					d['keys'][i] = []
					config.check('Instrument {}'.format(i), 'type', table)
					a,e = self.select(table,limit=n,where="data>{0} AND id={1}".format(stime,i),order='data')
					g = a.index('data')
					common, flags, keys = [], [], {}
					j = 0
					for x in a:
						y = translate(x)
						keys[y] = (j,x)
						if y in ['temperature', 'VoltR', 'humidity', 'temp_dry', 'temp_wet', 'tension']:
							common.append(y)
						else:
							flags.append(y)
						j+= 1
					meters = config.checklist(table, 'meters', common) or [];
					config.checklist(table, 'flags', flags);
					for j in range(len(meters)):
						met = meters[j]
						d['data'][i][met] = [(q[g],translatev(keys[met][1],q[keys[met][0]])) for q in e]
						d['keys'][i].append(met)

					config.checklist('Instrument {}'.format(i), 'meters', meters, True)
					ii = ';\n{:03}.'.format(i)
					config.check('Figure {}'.format(i), 'meters', ii[2:]+ii.join(common))
		return d

	def check(self):
		d = self.getall()
		r = {}
		global instrumentos, empresa
		if d['empresa'] != empresa:
			r['empresa'] = d['empresa']
			empresa =  d['empresa']
		ii = {}
		for i,inst in d['instrumentos'].items():
			if i not in instrumentos.keys() or inst!=instrumentos[i]:
				instrumentos[i] = inst
				ii[i] = inst
		if ii:
			r['instrumentos'] = tuplist_json(ii)

		if d['rel_alarmes']:
			r['alarmas'] = tuplist_json(d['rel_alarmes'])

		for k,a in d.items():
			if k[-1:] != '*': continue
			m = d[k[:-1]]
			if m:
				r['ud_'+k[:-1]] = tuplist_json(m)

		return r
		if 1:
			for i in d[k[:-1]]:
				idt = i['data']
				while idt in u: idt+= md
				u.append(idt)
				v[idt] = [(b,i[b]) for b in a]
				o.add(i['id'])

		return r
	
		u = []
		v = {}
		o = set([])
		md = 0.00000001
		
		for k in d.keys():
			if k[-1:]=='*':
				a = d[k]
				for i in d[k[:-1]]:
					idt = i['data']
					while idt in u: idt+= md
					u.append(idt)
					v[idt] = [(b,i[b]) for b in a]
					o.add(i['id'])
		a = ['id','dataInicio','dataFim','descricao']
		for i in d['rel_alarmes']:
			idt = i['dataInicio']
			while idt in u: idt+= md
			u.append(idt)
			v[idt] = [(b,i[b]) for b in a]
			o.add(i['id'])
		u.sort()
		debug.out(d['instrumentos'])
		r = dict([['inst-{:03}'.format(i),d['instrumentos'][i]] for i in o])
		c = 0
		for w in u:
			c+= 1
			r['update-{:03}'.format(c)] = dict(v[w])
		global latest
		return r

def check(dbf = r'C:\ProgramData\Full Gauge\Sitrad\datos.db',tick=0.0):
	global latest
	l = time2data(tick)
	if l>latest:
		latest = l
	with sitradDB(dbf) as db:
		return db.check()
	return {}

def tuplist_json(x):
	if type(x)==type({}):
		a = list(x.keys())
		a.sort()
		return '{'+','.join(['"{!s}":{}'.format(b,tuplist_json(x[b])) for b in a])+'}'
	if type(x)==type([]) and type(x[0])==type((1,2)):
		return '{'+','.join(['"{!s}":{}'.format(y[0],tuplist_json(y[1])) for y in x])+'}'
	if type(x)==type([]):
		return '['+','.join([tuplist_json(y) for y in x])+']'
	return json.dumps(x)

def decimate(v):
	if not v:
		return 0
	return v/10.0

translations = {
	'temperatura':('temperature',decimate),
	'temperatura1':('temp_dry',decimate),
	'temperatura2':('temp_wet',decimate),
	'TemperaturaSec':('temp_dry',decimate),
	'TemperaturaHum':('temp_wet',decimate),
	'umidade':('humidity',decimate),
	'Umidade':('humidity',decimate),
	'tensao':('tension',decimate),
	'data':('time',data2time,True),
	'dataInicio':('time_beg',data2time,True),
	'dataFim':('time_end',data2time,True),
	'periodo':('period',None),
	'estagio':('stage',None),
	'endereco':('address',None),
	'descricao':('description',None),
	'datacad':('date',data2asc),
	'alarme1L':('alarm1L',decimate),
	'alarme1H':('alarm1H',decimate),
	'alarme2L':('alarm2L',decimate),
	'alarme2H':('alarm2H',decimate),
	'alarme3L':('alarm3L',decimate),
	'alarme3H':('alarm3H',decimate),
	'alarme4L':('alarm4L',decimate),
	'alarme4H':('alarm4H',decimate),
	'alarme5L':('alarm5L',decimate),
	'alarme5H':('alarm5H',decimate),
	'alarme6L':('alarm6L',decimate),
	'alarme6H':('alarm6H',decimate),
	'voltr': ('volt_R',None),
	'volts': ('volt_S',None),
	'voltt': ('volt_T',None),
	'modelo':('model',None),
	'tipo':('type',None),
	}

def translatev(k,v):
	global translations
	if k in translations.keys() and translations[k][1]:
		return translations[k][1](v)
	return v

def translate(x):
	global translations,latest
	if type(x)==type(''):
		if x in translations.keys():
			return translations[x][0]
		return x
	if type(x)==type((0,1)):
		if x[0] in translations.keys():
			y = translations[x[0]]
			name = y[0]
			if y[1]:
				return (name,y[1](x[1]))
			return (name,x[1])
		return x
	r = []
	for a,b in x:
		if a in translations.keys():
			y = translations[a]
			if not y: continue
			name = y[0]
			if not name: name = a
			if y[1]:
				r.append((name,y[1](b)))
			else:
				r.append((name,b))
			if len(y)>2 and b>latest:
				latest = b
		else:
			r.append((a,b))
	return r

