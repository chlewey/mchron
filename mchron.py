
import sqlite3

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

dfile = 'sanpedro/datos.db'
with SitradDB(dfile) as db:
	print db.check()
