from jnpr import junos
from jnpr.junos.exception import ConnectAuthError, ConnectRefusedError, ConnectTimeoutError
from isis import isisTable
import pandas as pd

devices = {'juniper.lab': '192.168.0.6'}

for name in devices:

  print '---------------------------------------------------------------------------'
  print devices[name]
  print '---------------------------------------------------------------------------'

  try:
    dev = junos.Device(host=devices[name], user='changeme', password='changeme', gather_facts=False)
    dev.open()
    isis_table = isisTable(dev).get()
    dev.close()
  except ConnectAuthError:
    print 'ConnectAuthError'
    continue
  except ConnectRefusedError:
    print 'ConnectRefusedError'
    continue
  except ConnectTimeoutError:
    print 'ConnectTimeoutError'
    continue
  isis_db =[]
  i = 0
  for isis in isis_table:
       for localRTR in isis.entry:
	for remoteRTR in localRTR.remoteTable:
#	  print "{"
#	  print "'source':'{:10}','target':'{:10}','metric':'{:3}'".format(localRTR.lsp_id,remoteRTR.remoteRTR,remoteRTR.metric)
#	  print "},"
	  a = (localRTR.lsp_id[:-6],remoteRTR.remoteRTR[:-3],remoteRTR.metric)
	  isis_db.insert(i,(a))
print "-------"


#create panda dataframe
labels = ['source', 'target', 'metric']
df = pd.DataFrame.from_records(isis_db, columns=labels)

#sort by source and target
df[['source','target']] = df[['source','target']].apply(sorted,axis=1)

#remove duplicates
df1 = df.drop_duplicates(subset=['source','target'])

#convert to dict
final = df1.to_dict(orient='records')

#print 
print final
