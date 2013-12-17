
import sqlite3,debug,json

latest = 25568.0
instrumentos = {}
empresa = ''

def time2data(time):
    return (time+57600)/86400 + 25568

def data2time(data):
    return (data-25568)*86400-57600

class sitradDB:
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

    def query(self,table,limit=100,where=None,order=None,desc=False):
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
        k,r = self.query('sqlite_master',where="type='table'")
        return [i[1] for i in r]

    def getall(self):
        global latest
        ll = latest
        d = {}
        for table in self.tables():
            if table=='empresa':
                a,e = self.query(table)
                d[table] = e[0][0]
            elif table=='modulo_io_cfg':
                a,e = self.query(table)
                d[table] = [dict(zip(a,q)) for q in e]
            elif table=='instrumentos':
                a,e = self.query(table)
                d[table] = dict([[q[0],translate(zip(a[1:],q[1:]))] for q in e])
            elif table=='rel_alarmes':
                a,e = self.query(table,where="dataInicio>{0} OR dataFim>{0}".format(ll))
                d[table] = [translate(zip(a,q)) for q in e]
                if not len(e): continue
                i = a.index('dataFim')
                m = max([q[i] for q in e])
                debug.out2('max alarmes',m)
                if latest<m: latest = m
            else:
                a,e = self.query(table,100,"data>{0}".format(ll),"data",True)
                d[table+'*'] = a
                d[table] = [translate(zip(a,q)) for q in e]
                if not len(e): continue
                i = a.index('data')
                m = max([q[i] for q in e])
                if latest<m: latest = m
        #debug.out("Latest: {} {}".format(latest,data2time(latest)))
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
    return v/10

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
    'datacad':('time_cad',data2time),
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
    }
def translate(x):
    global translations,latest
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

