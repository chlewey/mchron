from locale import setlocale,LC_TIME
from time import strftime,localtime,time

setlocale(LC_TIME,'esp')
n = time()
print [strftime('%A',localtime(n+t*86400)).decode('latin-1').encode('utf8') for t in range(7)]
