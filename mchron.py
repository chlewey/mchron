
#from PyPDF2 import PdfFileWriter
#from ConfigParser import ConfigParser
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import sitrad
import os,time,emailer

from config import mcConfig

CONFIGFILE = 'mchron.cfg'

def getdb(config):
	section = 'Database'
	maker = config.xget(section,'maker','sitrad')
	if maker is None:
		raise 'No database maker provided'
	if maker=='sitrad':
		dbfile = config.xget(section,'source','datos.db')
		path = config.xget(section,'path','C:\\Documents and Settings\\All Users\\Application Data\\Full Gauge\\Sitrad')
		if path not in ['.','']:
			dbfile = path.rstrip('/')+'/'+dbfile
		return sitrad.database(dbfile)
	raise 'No configuration for a "{}" database'.format(maker)

def grid(paper):
	from reportlab.lib.units import inch
	from reportlab.lib.colors import pink
	paper.setStrokeColor(pink)
	paper.grid([x*inch/2 for x in range(2,16)],[y*inch/2 for y in range(2,21)])
	
def figure(paper,name,data,lt,tp,rt,bt):
	wd = rt-lt
	ht = tp-bt
	from reportlab.lib.colors import black,white,blue
	paper.setStrokeColor(black)
	paper.setFillColor(white)
	paper.rect(lt,bt,wd,ht)
	paper.setStrokeColor(blue)
	paper.setFillColor(blue)
	paper.setFont('Helvetica-Bold',9)
	x,y = lt+wd/2,tp+3
	paper.drawCentredString(x,y,name)
	#paper.rect(x-10,y,20,20)
	kk = data.keys()
	x0,x1=[],[]
	y0,y1=[],[]
	k0 = []
	for k in kk:
		k1 = k[4:8]
		ds = [q[0] for q in data[k]]
		do = [q[1] for q in data[k]]
		x0.append(min(ds))
		x1.append(max(ds))
		y0.append(int(min(do)))
		y1.append(int(max(do)+1))
		if k1 in k0:
			ix = k0.index(k1)
			y0[-1] = min(y0[ix],y0[-1])
			y0[ix] = y0[-1]
			y1[-1] = max(y1[ix],y1[-1])
			y1[ix] = y1[-1]
		k0.append(k1)
	x0 = int(24*min(x0))/24.0
	x1 = int(24*max(x1)+1)/24.0
	dx = x1-x0
	fx = float(wd)/dx

	r = [i/8.0 for i in range(int(x0*8+1),int(x1*8+1))]
	ft = '%H:%M'
	if dx<1.5:
		pass
	elif dx<3:
		r = [i/4.0 for i in range(int(x0*4+1),int(x1*4+1))]
	elif dx<7:
		ft = '%D %p'
		r = [i/2.0 for i in range(int(x0*2+1),int(x1*2+1))]
	else:
		ft = '%D/%M'
		r = [float(i) for i in range(int(x0+1),int(x1+1))]
	paper.setFont('Helvetica',6)
	p = paper.beginPath()
	for t in r:
		x = lt+fx*(t-x0)
		paper.drawCentredString(x,bt-10,time.strftime(ft,time.localtime(sitrad.data2time(t))))
		p.moveTo(x,bt)
		p.lineTo(x,bt-5)
	paper.drawPath(p)
	i = 0
	colors = [(1,0,0),(0,.7,.7),(.4,.8,0),(.4,0,.8)]
	for k in kk:
		j = 0
		r,g,b = colors[i]
		rw,gw,bw = (1+r)/2,(1+g)/2,(1+b)/2
		dd = data[k]
		dy = y1[i]-y0[i]
		print dx,dy
		fy = float(ht)/dy
		p = paper.beginPath()
		p.moveTo(lt+(dd[0][0]-x0)*fx,bt+(dd[0][1]-y0[i])*fy)
		for q in dd[1:]:
			p.lineTo(lt+(q[0]-x0)*fx,bt+(q[1]-y0[i])*fy)
			j+= 1
		paper.setStrokeColorRGB(r,g,b)
		paper.drawPath(p)
		fac = 5
		if dy>60:
			fac = 10
		if dy>110:
			fac = 20
		s = [fac*h for h in range(int(y0[i]/fac+1),int(y1[i]/fac+1))]
		print s
		if k0[i][0]=='t':
			x2,x3=lt-5,lt
			paper.drawRightString(lt-5,bt+(s[-1]-y0[i])*fy,'{}'.format(s[-1]))
			paper.drawRightString(lt-5,bt+(s[0]-y0[i])*fy,'{}'.format(s[0]))
		else:
			x2,x3=rt,rt+5
			paper.drawString(rt+5,bt+(s[-1]-y0[i])*fy,'{}'.format(s[-1]))
			paper.drawString(rt+5,bt+(s[0]-y0[i])*fy,'{}'.format(s[0]))
		p = paper.beginPath()
		for y in s:
			p.moveTo(x2,bt+(y-y0[i])*fy)
			p.lineTo(x3,bt+(y-y0[i])*fy)
		paper.drawPath(p)
		i+=1

		
	#	paper.rect(lt+10*i,bt+10*i,wd-20*i,ht-20*i)
	#	paper.circle(lt+wd/2,bt+ht/2,20*i)
	#p.close()

figdist = {
	1: [( 0,0,17,9)],
	2: [( 0,0, 8,9),
	    ( 9,0,17,9)],
	3: [( 0,0, 8,4),
	    ( 9,0,17,4),
	    ( 4,5,13,9)],
	4: [( 0,0, 8,4),
	    ( 9,0,17,4),
	    ( 0,5, 8,9),
	    ( 9,5,17,9)],
	5: [( 0,0, 8,5),
	    ( 9,0,17,5),
	    ( 0,6, 5,9),
	    ( 6,6,11,9),
	    (12,6,17,9)],
	6: [( 0,0, 5,4),
	    ( 6,0,11,4),
	    (12,0,17,4),
	    ( 0,5, 5,9),
	    ( 6,5,11,9),
	    (12,5,17,9)],
}
def report(paper,config,data):
	global figdist;
	paper.setAuthor('Oruga Amarilla')
	title = config.xget('Report','title','Reporte')
	subtitle = "Reporte de {} generado el {}.".format(
		config.xget('Site','name'),
		time.strftime('%d de %B, %Y',time.localtime(data['time'])))
	paper.setTitle(title)
	paper.setSubject(title)
	grid(paper)
	paper.setFont('Helvetica-Bold',16)
	paper.drawCentredString(306,720,title)
	paper.setFont('Helvetica',11)
	paper.drawCentredString(306,702,subtitle)
	
	figs = config.xget('Report','figures').split(';\n')
	n = len(figs)
	dist = figdist[n]
	for i in range(n):
		name = config.xget(figs[i],'description')
		mets = config.xget(figs[i],'meters').split(';\n')
		d = {}
		for m in mets:
			ins,met = m.split('.')
			ins = int(ins)
			d[m] = data['data'][ins][met]
		print i,name
		figure(paper,name,d,68+dist[i][0]*28,660-dist[i][1]*28,68+dist[i][2]*28,660-dist[i][3]*28)
	
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
		d = {'time': ntime, 'data': {}, 'keys': {}}
		with getdb(config) as db:
			for table in db.tables():
				if table=='empresa':
					a,e = db.select(table)
					empresa = e[0][0]
					r = config.check('Site','name',empresa,True)
					r = config.check('Report','title',empresa)
					d[table] = empresa
				elif table in ['modulo_io_cfg']:
					a,e = db.select(table)
					d[table] = [dict(zip(a,q)) for q in e]
				elif table == 'instrumentos':
					a,e = db.select(table)
					dd = dict([[q[0],dict(sitrad.translate(zip(a[1:],q[1:])))] for q in e])
					d[table] = dd
					[config.check('Site','instrument-{}'.format(x),dd[x]['description'],True) for x in dd.keys()]
					[config.check('Figure {}'.format(x),'description',dd[x]['description']) for x in dd.keys()]
					for x in dd.keys():
						for k in dd[x].keys():
							if k in ['status','date','model','description']:
								config.check('Instrument {}'.format(x), k, dd[x][k])
					config.check('Report','figures',';\n'.join(['Figure {}'.format(x) for x in dd.keys()]))
				elif table=='rel_alarmes':
					a,e = db.select(table,where="dataInicio>{0} OR dataFim>{0}".format(stime))
					dd = [dict(zip(a,q)) for q in e]
					d[table] = dd
					larms = {}
					for l in e:
						if l[0] not in larms.keys():
							larms[l[0]] = set()
						larms[l[0]].add(l[1])
					z = [config.check('Instrument {}'.format(x), 'alarms', (';\n'.join(larms[x])).encode('utf8')) for x in larms.keys()]
					#print table,z
				else:
					u,v = db.query('SELECT id,COUNT(*) AS n FROM {} WHERE data>{} GROUP BY id;'.format(table,stime))
					if not len(v):
						continue
					for i,n in v:
						d['data'][i] = {}
						d['keys'][i] = []
						config.check('Instrument {}'.format(i), 'type', table)
						a,e = db.select(table,limit=n,where="data>{0} AND id={1}".format(stime,i),order='data')
						g = a.index('data')
						z = [config.check(table, sitrad.translate(x), False) for x in a]
						meters = set()
						for j in range(len(a)):
							if z[j] and z[j] != 'False':
								met = sitrad.translate(a[j])
								meters.add(met)
								d['data'][i][met] = [(q[g],sitrad.translatev(a[j],q[j])) for q in e]
								d['keys'][i].append(met)
						config.check('Instrument {}'.format(i), 'meters', ';\n'.join(meters),True)
						ii = ';\n{:03}.'.format(i)
						config.check('Figure {}'.format(i), 'meters', ii[2:]+ii.join(meters),True)

					#a,e = db.select(table,where="data>{0}".format(stime),order='data')
					#if len(e):
					#	#dd = [dict(zip(a,q)) for q in e]
					#	y = set([q[0] for q in e])
					#	z = [config.check(table,sitrad.translate(x),False) for x in a]
					#	for x in y:
					#		d['data'][x] = []
					#		d['keys'][x] = [a]
					#		config.check('Instrument {}'.format(x), 'type', table)
					#		for i in range(len(a)):
					#			if z[i] and z[i] != 'False':
					#				config.check('Instrument {}'.format(x), sitrad.translate(a[i]), z[i])
					#				config.check('Figure {}'.format(x), sitrad.translate(a[i]), z[i])
					#	for q in e:
					#		d['data'][q[0]].append(q[1:])
					#	config.xset(table,'instruments',','.join([str(x) for x in y]))
					#	#print table,y,z
			
		""" Form the document """
		docfn = "{}_{}.pdf".format(
			config.xget('Report','namebase','report'),
			time.strftime('%Y-%m-%d',time.localtime(ntime)))
		paper = canvas.Canvas(docfn,pagesize=letter)
		report(paper,config,d)
		paper.showPage()
		paper.save()
	
		""" Email the document """
		emailer.send(config,"""Este es un correo autom\u00e1matico generado
por el sistema de la Oruga Amarilla como reporte
de actividad.

Sitio: {}
Generado el {} a las {}
A partir del {} a las {}.
""".format(
			config.xget('Site','name'),
			time.strftime('%d de %B, %Y',time.localtime(ntime)),
			time.strftime('%H:%M:%S',time.localtime(ntime)),
			time.strftime('%d de %B, %Y',time.localtime(ttime)),
			time.strftime('%H:%M:%S',time.localtime(ttime))
			),
			[docfn])
	
		""" Saving configuration """
		config.xset('Run','time',time.ctime(ntime))


if __name__ == "__main__":
	main()
            

