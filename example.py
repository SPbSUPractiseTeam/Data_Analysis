from Analisys import Analisys as an
from preprocessing import logParser as pp
import os.path

dbname = pp.openLogs('example_logs')

an.SetData(dbname)

res1 = an.UseModule(0)

res2 = an.UseModule(1)

if res1 == None or res2  == None:
    print('Failed')
else:
    print('Result file names - ' + res1 + ', ' + res2)
