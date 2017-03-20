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
       print isis
       for entry in isis.levelTable:
	print " second print %s" %entry
        for entry1 in entry.remoteTable:
 	 print entry1
         for entry2 in entry1.reachability:
	  print "localRTR:%s , remoteRTR:%s , metric: %s , local_ip: %s , local_interface: %s ,remote_ip: %s ,remote_interface: %s" % (entry.lsp_id,entry2.remoteRTR,entry2.metric,entry2.local_ip,entry2.local_interface,entry2.remote_ip,entry2.remote_interface)
          a = (entry.lsp_id[:-6],entry2.remoteRTR[:-3],entry2.metric,entry2.local_ip,entry2.local_interface,entry2.remote_ip,entry2.remote_interface)
          isis_db.insert(i,(a))
print "-------"

#create panda dataframe
labels = ['source', 'target', 'metric', 'l_ip','l_int','r_ip','r_int']
df = pd.DataFrame.from_records(isis_db, columns=labels)
print "---before sort----"
print df

#create ip pair and sort
df.loc[:, 'l_ip_r_ip'] = pd.Series([tuple(sorted(each)) for each in list(zip(df.l_ip.values.tolist(), df.r_ip.values.tolist()))])
print df

#remove duplicates based on ip pair
df1 = df.drop_duplicates(subset=['l_ip_r_ip'])
print "---after remove duplicates---"
print df1

#remove l_ip_r_ip
df1.pop('l_ip_r_ip')
print "---remove l_ip_r_ip" 
print df1
#convert to dict
final = df1.to_dict(orient='records')

#print 
print final
