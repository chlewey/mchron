# -*- coding: UTF-8 -*-

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from mytime import *
import sitrad

__totalpages = 1
__currentpage = 1

def grid(paper):
	from reportlab.lib.units import inch
	from reportlab.lib.colors import pink
	paper.setStrokeColor(pink)
	paper.grid([x*inch/2 for x in range(2,16)],[y*inch/2 for y in range(2,21)])

def resettime(c):
	c.remove_option('Run','from')
	c.remove_option('Run','to')

def setfromtime(c,n):
	ta = c.xget('Run','from')
	tf = ta and asc2data(ta)
	if type(n) == list:
		m = min(n)
		if tf:
			m = min(m,tf)
	elif tf:
		m = min(n,tf)
	else:
		m = n
	c.set('Run','from',data2asc(m))
	return m

def settotime(c,n):
	ta = c.xget('Run','to')
	tt = ta and asc2data(ta)
	if type(n) == list:
		M = max(n)
		if tt:
			M = max(M,tt)
	elif tt:
		M = max(n,tt)
	else:
		M = n
	c.set('Run','to',data2asc(M))
	return M

figurecolors = [
	(0.0,0.7,0.7),
	(1.0,0.0,0.0),
	(0.4,0.8,0.0),
	(0.4,0.0,0.8)]
	
def figure(paper,name,c,data,coords):
	global figurecolors
	lt,tp,rt,bt = coords
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
	#kk = [k[0] for k in data]
	x0,x1=[],[]
	y0,y1=[],[]
	k0 = []
	for l in data:
#		print type(l),type(l[0])
		k1 = l[0][4:8]
		ds = [q[0] for q in l[1]]
		do = [q[1] for q in l[1]]
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
	x0 = setfromtime(c,x0)
	x1 = settotime(c,x1)
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
		paper.drawCentredString(x,bt-10,data2fmt(ft,t))
		p.moveTo(x,bt)
		p.lineTo(x,bt-5)
	paper.drawPath(p)

	i = 0
	for l in data:
		j = 0
		r,g,b = figurecolors[i]
		rw,gw,bw = (1+r)/2,(1+g)/2,(1+b)/2
		dd = l[1]
		dy = y1[i]-y0[i]
#		print dx,dy
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
#		print s
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
def dist2paper(co,left=68,upper=660,scale=28):
	return (
		left + co[0]*scale,
		upper- co[1]*scale,
		left + co[2]*scale,
		upper- co[3]*scale)

__translations = {
	'VoltR': 'actividad',
	'humidity': 'humedad',
	'temp_dry': 'temperatura seca',
	'temp_wet': 'temperatura húmeda',
	'temperature': 'temperatura',
}
def translate(met):
	global __translations
	return met in __translations.keys() and __translations[met] or met

__units = {
	'humidity': '%',
	'temp_dry': '°C',
	'temp_wet': '°C',
	'temperature': '°C',
}
def unit(met):
	global __units
	return met in __units.keys() and __units[met] or ''

def analize(c,name,met,data):
	line = ''
	dt = [q[0] for q in data]
	dv = [q[1] for q in data]
	line+= '{} de {}: '.format(translate(met).capitalize(),name)
	m = min(dv)
	i = dv.index(m)
	t = dt[i]
	line+= ' Mínimo {}{} el {} a las {}.'.format(m,unit(met),data2fmt('%A %d',t),data2fmt('%H:%M',t))
	M = max(dv)
	i = dv.index(M)
	t = dt[i]
	line+= ' Máximo {}{} el {} a las {}.'.format(M,unit(met),data2fmt('%A %d',t),data2fmt('%H:%M',t))

#	print line
	return line

def drawline(paper,line,offset=0,top=720,left=72):
	from reportlab.lib.colors import black
	paper.setFillColor(black)
	paper.setFont('Helvetica',10)
	while len(line)>100:
		n = line[:100].rfind(' ')
		if n>66:
			paper.drawString(left,top-offset,line[:n])
			line = line[n:]
			offset+= 13
		else:
			break
	paper.drawString(left,top-offset,line)

	return offset+16

def drawsimpleline(paper,begin,end,color=(0,0,0)):
	r,g,b = color
	p = paper.beginPath()
	p.moveTo(begin[0],begin[1])
	p.lineTo(end[0],end[1])
	paper.setStrokeColorRGB(r,g,b)
	paper.drawPath(p)
	
def frontpage(paper,config,data):
	global figdist,__totalpages;
	#grid(paper)

	figs = config.xget('Report','figures').split(';\n')
	n = len(figs)
	dist = figdist[n]
	d = [[] for i in range(n)]
	for i in range(n):
		name = config.xget(figs[i],'description')
		mets = config.xget(figs[i],'meters').split(';\n')
		for m in mets:
			ins,met = m.split('.')
			ins = int(ins)
			dl = data['data'][ins][met]
			d[i].append((m,dl))
		figure(paper,name,config,d[i],dist2paper(dist[i]))
	frontpagetitle(paper,config,data)

	offset = 360
	for i in range(n):
		name = config.xget(figs[i],'description')
		mets = config.xget(figs[i],'meters').split(';\n')
		j = 0
		for m in mets:
			ins,met = m.split('.')
			ins = int(ins)
			dl = data['data'][ins][met]
			line = analize(config,name,met,dl)
			drawsimpleline(paper,(72,724-offset),(76,720-offset),figurecolors[j])
			drawsimpleline(paper,(76,720-offset),(81,728-offset),figurecolors[j])
			offset = drawline(paper,line,offset,left=84)
			if offset >= 640:
				offset = 13
				__totalpages += 1
				paginate(paper)
				brand(paper,config)
			j += 1
			

def frontpagetitle(paper,config,data):
	from reportlab.lib.colors import black
	title = config.xget('Report','title','Reporte')
	subtitle1 = "Reporte de {} generado el {}.".format(
		config.xget('Site','name'),
		time2esk(data['time'][0]))
	subtitle2 = "Período del {} al {}.".format(
		time2esh(conf2time(config,'Run','From',data['time'][1])),
		time2esh(conf2time(config,'Run','To',data['time'][0])))
	paper.setFillColor(black)
	paper.setTitle(title)
	paper.setSubject('{}\n{}'.format(subtitle1,subtitle2))
	paper.setFont('Helvetica-Bold',16)
	paper.drawCentredString(306,720,title)
	paper.setFont('Helvetica',11)
	paper.drawCentredString(306,702,subtitle1)
	paper.drawCentredString(306,686,subtitle2)

def otherpagetitle(paper,title,subtitle=None):
	from reportlab.lib.colors import black
	paper.setFillColor(black)
	paper.setFont('Helvetica-Bold',13)
	paper.drawCentredString(306,705,title)
	if subtitle:
		paper.setFont('Helvetica',12)
		paper.drawCentredString(306,690,subtitle)

def paginate(paper):
	global __totalpages,__currentpage
	from reportlab.lib.colors import black
	paper.setFillColor(black)
	paper.setFont('Helvetica',10)
	paper.drawCentredString(306,48,'– pág. {0:d} de {1:d} –'.format(__currentpage,__totalpages))
	paper.showPage()
	__currentpage += 1
	
def brand(paper,config):
	from reportlab.lib.colors import black,blue

	paper.setFillColor(black)
	paper.setFont('Helvetica-Bold',9)
	paper.drawString(72,63,config.xget('Brand 1','name'))
	paper.setFont('Helvetica',8)
	paper.drawString(72,54,config.xget('Brand 1','address'))
	paper.drawString(72,45,config.xget('Brand 1','phone'))
	paper.setFillColor(blue)
	paper.drawString(72,36,config.xget('Brand 1','url'))

	paper.setFillColor(black)
	paper.setFont('Helvetica-Bold',9)
	paper.drawRightString(540,62,config.xget('Brand 2','name'))
	paper.setFont('Helvetica',8)
	paper.drawRightString(540,54,config.xget('Brand 2','address'))
	paper.drawRightString(540,45,config.xget('Brand 2','phone'))
	paper.setFillColor(blue)
	paper.drawRightString(540,36,config.xget('Brand 2','url'))
	
def report(docfn,config,data):
	global __totalpages
	paper = canvas.Canvas(docfn,pagesize=letter)
	paper.setAuthor('Oruga Amarilla')

	figs = config.xget('Report','figures').split(';\n')
	__totalpages += len(figs)

	brand(paper,config)
	frontpage(paper,config,data)
	
	site = config.xget('Site','name')
	for fig in figs:
		paginate(paper)
		brand(paper,config)
		name = config.xget(fig,'description')
		mets = config.xget(fig,'meters').split(';\n')
		d = []
		offset,j = 400,0
		for m in mets:
			ins,met = m.split('.')
			ins = int(ins)
			dl = data['data'][ins][met]
			d.append((m,dl))

			line = analize(config,name,met,dl)
			drawsimpleline(paper,(72,724-offset),(76,720-offset),figurecolors[j])
			drawsimpleline(paper,(76,720-offset),(81,728-offset),figurecolors[j])
			offset = drawline(paper,line,offset,left=84)
			j+= 1

		otherpagetitle(paper,name,site)
		figure(paper,name,config,d,(72,660,540,360))

	paginate(paper)
	paper.save()
