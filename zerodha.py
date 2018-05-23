import os, sys, wget, csv, redis
from datetime import date, timedelta
from zipfile import ZipFile


url = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ'+(date.today()-timedelta(1)).strftime('%d%m%y')+'_CSV.ZIP'
try:
    wget.download(url, os.getcwd())
except:
    sys.exit()
file = 'EQ'+(date.today()-timedelta(1)).strftime('%d%m%y')
zip = ZipFile(file+'_CSV.ZIP').extractall()
file = open(file+'.csv')
file = csv.reader(file)

r = redis.Redis(host='localhost', port=6379, db=0, password=None)
r.set("total", 1)

for i in file:
    if file.line_num == 1:
        continue
    hash_key = "member:" + str(file.line_num - 1)
    r.hmset(hash_key, {"code": i[0],"name": i[1],"open": i[4],"high": i[5],"low": i[6],"close": i[7]})
    r.incr("total", 1)

r.client_kill(r.client_list()[0]['addr'])



