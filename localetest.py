from locale import setlocale,LC_TIME
from time import strftime,localtime,time

setlocale(LC_TIME,'es_CO.utf8')
n = time()
print [strftime('%A',localtime(n+t*86400)) for t in range(7)]
