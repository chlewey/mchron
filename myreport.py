# -*- coding: UTF-8 -*-

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from mytime import *
import sitrad,config

__totalpages = 1
__currentpage = 1

def grid(paper):
	from reportlab.lib.units import inch
	from reportlab.lib.colors import pink
	paper.setStrokeColor(pink)
	paper.grid([x*inch/2 for x in range(2,16)],[y*inch/2 for y in range(2,21)])

def resettime():
	config.remove('Run','from')
	config.remove('Run','to')

def setfromtime(n):
	ta = config.get('Run','from')
	tf = ta and asc2data(ta)
	if type(n) == list:
		if not n:
			m = tf or time2data(now())-1
		else:
			m = min(n)
			if tf:
				m = min(m,tf)
	elif tf:
		m = min(n,tf)
	else:
		m = n
	config.set('Run','from',data2asc(m))
	return m

def settotime(n):
	ta = config.get('Run','to')
	tt = ta and asc2data(ta)
	if type(n) == list:
		if not n:
			M = tt or time2data(now())
		else:
			M = max(n)
			if tt:
				M = max(M,tt)
	elif tt:
		M = max(n,tt)
	else:
		M = n
	config.set('Run','to',data2asc(M))
	return M

figurecolors = [
	(0.0,0.7,0.7),
	(1.0,0.0,0.0),
	(0.4,0.8,0.0),
	(0.4,0.0,0.8)]
	
def figure(paper,name,data,coords):
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
	x0 = setfromtime(x0)
	x1 = settotime(x1)
	dx = x1-x0
	fx = float(wd)/dx

	r = [i/8.0 for i in range(int(x0*8+1),int(x1*8+1))]
	ft = '%H:%M'
	if dx<1.5:
		pass
	elif dx<3:
		r = [i/4.0 for i in range(int(x0*4+1),int(x1*4+1))]
	elif dx<7:
		ft = '%a %p'
		r = [i/2.0 for i in range(int(x0*2+1),int(x1*2+1))]
	else:
		ft = '%d/%m'
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
		if not s:
			pass
		elif k0[i][0]=='t':
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

def analize(name,met,data):
	line = u''
	dt = [q[0] for q in data]
	dv = [q[1] for q in data]
	line+= u'{} de {}: '.format(translate(met).decode('utf-8').capitalize(),name)
	m = min(dv)
	i = dv.index(m)
	t = dt[i]
	s = data2fmt('%A %d',t)
	l = u' Mínimo {}{} el {} a las {}.'
	#print [line,s,l,m,met,unit(met)]
	l = l.format(m,unit(met).decode('utf-8'),s,data2fmt('%H:%M',t))
	line+= l
	M = max(dv)
	i = dv.index(M)
	t = dt[i]
	s = data2fmt('%A %d',t)
	l = u' Máximo {}{} el {} a las {}.'
	#print [s,l,M,met,unit(met)]
	l = l.format(M,unit(met).decode('utf-8'),s,data2fmt('%H:%M',t))
        line+= l

	#print line
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
	
def frontpage(paper,data):
	global figdist,__totalpages;
	#grid(paper)

	resettime()
	figs = config.getlist('Report','figures')
	n = len(figs)
	dist = figdist[n]
	d = [[] for i in range(n)]
	for i in range(n):
		name = config.get(figs[i],'description')
		mets = config.getlist(figs[i],'meters')
		for m in mets:
			ins,met = m.split('.')
			ins = int(ins)
			try:
        			dl = data['data'][ins][met]
        			d[i].append((m,dl))
        		except:
                                print ins,met
		figure(paper,name,d[i],dist2paper(dist[i]))
	frontpagetitle(paper,data)

	offset = 360
	for i in range(n):
		name = config.get(figs[i],'description')
		mets = config.getlist(figs[i],'meters')
		j = 0
		for m in mets:
			if offset >= 640:
				offset = 13
				__totalpages += 1
				paginate(paper)
				brand(paper)
			ins,met = m.split('.')
			ins = int(ins)
			inn = config.get('Instrument {}'.format(ins),'description',name)
			try:
        			dl = data['data'][ins][met]
        		except:
                                continue
			line = analize(inn,met,dl)
			drawsimpleline(paper,(72,724-offset),(76,720-offset),figurecolors[j])
			drawsimpleline(paper,(76,720-offset),(81,728-offset),figurecolors[j])
			offset = drawline(paper,line,offset,left=84)
			j += 1
			

def frontpagetitle(paper,data):
	from reportlab.lib.colors import black
	title = config.get('Report','title','Reporte')
	print title
	subtitle1 = "Reporte de {} generado el {}.".format(
		config.get('Site','name'),
		time2esk(data['time'][0]))
	subtitle2 = "Período del {} al {}.".format(
		time2esh(conf2time('Run','From',data['time'][1])),
		time2esh(conf2time('Run','To',data['time'][0])))
	paper.setFillColor(black)
	paper.setTitle(title)
	paper.setSubject('{}\n{}'.format(subtitle1,subtitle2))
	paper.setFont('Helvetica-Bold',16)
	#try:
	paper.drawCentredString(306,720,title or 'Titulo')
	#except:
	#	print ('ERROR:', title)
	#	config.save()
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
	
def brand(paper):
	from reportlab.platypus.flowables import Image
	from reportlab.lib.colors import black,blue

	paper.setFillColor(black)
	paper.setFont('Helvetica-Bold',9)
	paper.drawString(72,63,config.get('Brand 1','name'))
	paper.setFont('Helvetica',8)
	paper.drawString(72,54,config.get('Brand 1','address'))
	paper.drawString(72,45,config.get('Brand 1','phone'))
	paper.setFillColor(blue)
	paper.drawString(72,36,config.get('Brand 1','url'))
	logo = config.get('Brand 1','logo')
	if logo:
		offset = config.get('Brand 1','logo offset')
		if offset:
			osxy = offset.split(',')
			x,y = int(osxy[0]),int(osxy[1])
		else:
			x,y = 0,0
		size = config.get('Brand 1','logo size')
		if size:
			size = size.split(',')
			w,h = int(size[0]),int(size[1])
			paper.drawImage(logo,72+x,720+y,w,h)
		else:
			paper.drawImage(logo,72+x,720+y)

	paper.setFillColor(black)
	paper.setFont('Helvetica-Bold',9)
	paper.drawRightString(540,62,config.get('Brand 2','name'))
	paper.setFont('Helvetica',8)
	paper.drawRightString(540,54,config.get('Brand 2','address'))
	paper.drawRightString(540,45,config.get('Brand 2','phone'))
	paper.setFillColor(blue)
	paper.drawRightString(540,36,config.get('Brand 2','url'))
	logo = config.get('Brand 2','logo')
	if logo:
		offset = config.get('Brand 2','logo offset')
		if offset:
			osxy = offset.split(',')
			x,y = int(osxy[0]),int(osxy[1])
		else:
			x,y = 0,0
		size = config.get('Brand 2','logo size')
		if size:
			size = size.split(',')
			w,h = int(size[0]),int(size[1])
			paper.drawImage(logo,540+x-w,720+y,w,h)
		else:
			paper.drawImage(logo,540+x,720+y)
	
def report(docfn,data):
	global __totalpages
	paper = canvas.Canvas(docfn,pagesize=letter)
	paper.setAuthor('Oruga Amarilla')
        print 1
	figs = config.getlist('Report','figures')
	__totalpages += len(figs)
        print 2
	brand(paper)
	print 3
	frontpage(paper,data)
	print 3,figs
	site = config.get('Site','name')
	for fig in figs:
		paginate(paper)
		brand(paper)
		name = config.get(fig,'description')
		mets = config.getlist(fig,'meters')
		d = []
		offset,j = 400,0
		for m in mets:
			ins,met = m.split('.')
			ins = int(ins)
			inn = config.get('Instrument {}'.format(ins),'description',name)
			try:
        			dl = data['data'][ins][met]
        		except:
                                continue
			d.append((m,dl))

			line = analize(inn,met,dl)
			drawsimpleline(paper,(72,724-offset),(76,720-offset),figurecolors[j])
			drawsimpleline(paper,(76,720-offset),(81,728-offset),figurecolors[j])
			offset = drawline(paper,line,offset,left=84)
			j+= 1

		otherpagetitle(paper,name,site)
		figure(paper,name,d,(72,660,540,360))

	paginate(paper)
	paper.save()
