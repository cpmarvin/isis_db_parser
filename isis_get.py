from jnpr import junos
from jnpr.junos.exception import ConnectAuthError, ConnectRefusedError, ConnectTimeoutError
from isis import isisTable
import pandas as pd

devices = {'juniper.lab': '192.168.1.6'}

for name in devices:

  print '---------------------------------------------------------------------------'
  print devices[name]
  print '---------------------------------------------------------------------------'

  try:
    dev = junos.Device(host=devices[name], user='lab', password='lab123', gather_facts=False)
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
  print isis_table
  for isis in isis_table:
       for entry in isis.levelTable:
        for entry1 in entry.remoteTable:
         for entry2 in entry1.reachability:
          a = (entry.lsp_id[:-6],entry2.remoteRTR[:-3],entry2.metric,entry2.local_ip,entry2.local_interface,entry2.remote_ip,entry2.remote_interface)
          isis_db.insert(i,(a))
print "-------"

#create panda dataframe
labels = ['source', 'target', 'metric', 'l_ip','l_int','r_ip','r_int']
df = pd.DataFrame.from_records(isis_db, columns=labels)


#create ip pair and sort
df.loc[:, 'l_ip_r_ip'] = pd.Series([tuple(sorted(each)) for each in list(zip(df.l_ip.values.tolist(), df.r_ip.values.tolist()))])


#remove duplicates based on ip pair
df1 = df.drop_duplicates(subset=['l_ip_r_ip'])


#remove l_ip_r_ip
df1.pop('l_ip_r_ip')

#convert to dict
final = df1.to_dict(orient='records')

#print 
print final
