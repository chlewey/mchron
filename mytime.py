
import locale,time,config
__lstack = []
__mylocale = False
__locencod = None
__sit_dshift = 25569
__secday = 24*3600

def __localein(l=__mylocale):
	global __lstack,__mylocale,__locencod
	if not __mylocale:
		__mylocale = config.get('Database','locale','es_CO.utf8')
		__locencod = config.get('Database','locale encoding')
	if not l:
		l = __mylocale
	__lstack.append(locale.getlocale())
	locale.setlocale(locale.LC_TIME,l)
	return __locencod

def __localeout():
	global __lstack
	locale.setlocale(locale.LC_TIME,__lstack[-1])
	__lstack = __lstack[:-1]
	return len(__lstack) and __lstack[:-1] or None

def now():
	return time.time()
	
def asc2time(at):
	__localein('C')
	t = time.mktime(time.strptime(at))
	__localeout()
	return t
	
def asc2data(at):
	return time2data(asc2time(at))

def time2asc(t):
	return time.ctime(t)

def time2ymd(t):
	return time.strftime('%Y-%m-%d',time.localtime(t))

def time2hms(t):
	return time.strftime('%H:%M:%S',time.localtime(t))

def time2esk(t):
	__localein()
	e = time.strftime('%d de %B, %Y',time.localtime(t))
	__localeout()
	return e

def time2esd(t):
	__localein()
	e = time.strftime('%d de %B de %Y',time.localtime(t))
	__localeout()
	return e

def time2esh(t):
	__localein()
	e = time.strftime('%d de %B a las %H:%M',time.localtime(t))
	__localeout()
	return e

def time2fmt(ft,t):
	le = __localein()
	try:
        	s = time.strftime(ft,time.localtime(t))
        except:
                print ft
                exit()
	if le:
                s = s.decode(le)
	__localeout()
	return s

def data2fmt(ft,st):
	return time2fmt(ft,data2time(st))

def time2data(t):
	tshift = int(config.get('Database','time shift'))
	return float(t+tshift)/__secday + __sit_dshift

def data2time(st):
	tshift = int(config.get('Database','time shift'))
	return (st-__sit_dshift)*__secday-tshift
	
def data2asc(st):
	return time.ctime(data2time(st))

def conf2time(sec,op,dt=False):
	df = dt and time2asc(dt) or None
	return asc2time(config.get(sec,op,df))

locale.getlocale()
