import pprint
pp = pprint.PrettyPrinter(indent=4)
from cinderclient import client
cinder = client.Client('1', "admin" , "devstack" , "admin", "http://10.108.203.127:5000/v2.0")

for volume in cinder.volumes.list():
   print "----"
   print "Attributes of %s" % volume.display_name
   pp.pprint(volume._info)
print ""
