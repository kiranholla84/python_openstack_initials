#!/usr/bin/python
#from clients import nova, glance, cinder
from cinderclient import client
cinder = client.Client('1', "admin" , "devstack" , "admin", "http://10.108.203.127:5000/v2.0")
import time
import pprint
pp = pprint.PrettyPrinter(indent=4)


print "Create a sample volume (sample-1)."
volume01 = cinder.volumes.create(size=1, display_name='sample-1',
                                 display_description='test volume No.1')

while (volume01.status != 'available'):
    print "Wait the sample volume to be available."
    time.sleep(1)
    volume01 = cinder.volumes.get(volume01.id)

print "Create snapshot from the sample."
snapshot01 = cinder.volume_snapshots.create(volume01.id,
                                     display_name='snaphsot_sample-1')

while (snapshot01.status != 'available'):
    print "Wait the snapshot to be available."
    time.sleep(1)
    snapshot01 = cinder.volume_snapshots.get(snapshot01.id)

print "Update an attribute of the snapshot through a snapshot object."
snapshot01.update(display_description='test snapshot No.1')

print "List all snapshots"
for snapshot in cinder.volume_snapshots.list():
   print "----"
   print "Attributes of snapshot %s" % snapshot.display_name
   pp.pprint(snapshot._info)
   base_volume = cinder.volumes.get(snapshot.volume_id)
   print "Attributes of base volume %s" % base_volume.display_name
   pp.pprint(base_volume._info)
print ""

print "Update an attribute of the snapshot through the manager."
cinder.volume_snapshots.update(snapshot01, display_name='to_be_deleted')
print "Find a snapshot with display_name='to_be_deleted'"
for snapshot in cinder.volume_snapshots.findall(display_name='to_be_deleted'):
    print "Delete the snapshot and its base volume."
    base_volume = cinder.volumes.get(snapshot.volume_id)
    snapshot.delete()
    while (snapshot):
        try:
            cinder.volume_snapshots.get(snapshot.id)
            print "Wait the snapshot to be deleted."
            time.sleep(1)
        except:
            snapshot=None
    base_volume.delete()
