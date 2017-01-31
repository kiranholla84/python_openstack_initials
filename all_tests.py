import pprint
import time
pp = pprint.PrettyPrinter(indent=4)

from cinderclient import client as Cclient
from novaclient import client as nClient

cinder = Cclient.Client('2', "admin" , "devstack" , "admin", "http://10.108.203.127:5000/v2.0")
nova = nClient.Client('2', "admin" , "devstack" , "admin", "http://10.108.203.127:5000/v2.0")

print "===============CREATE, UPDATE, DELETE VOLUMES======================"
print "Create empty volumes (sample-1, sample-2)."
volume01 = cinder.volumes.create(size=1, name='sample-1',
                                 description='test volume No.1')
volume02 = cinder.volumes.create(size=1, name='sample-2')

while (volume01.status != 'available'):
    print "Wait sample-1 to be available."
    time.sleep(10)
    volume01 = cinder.volumes.get(volume01.id)

while (volume02.status != 'available'):
    print "Wait sample-2 to be available."
    time.sleep(10)
    volume02 = cinder.volumes.get(volume02.id)

print "Update an attribute."
volume02.update(description='test volume No.2')

print "List all volumes"
for volume in cinder.volumes.list():
   print "----"
   print "Attributes of %s" % volume.name
   pp.pprint(volume._info)
print ""

print "Delete a volume through an volume object."
volume01.delete()
print "Delete a image through the volume manager."
cinder.volumes.delete(volume02)

while (volume01):
    try:
        cinder.volumes.get(volume01.id)
        print "Wait sample-1 to be deleted."
        time.sleep(10)
    except:
        volume01=None

while (volume02):
    try:
        cinder.volumes.get(volume02.id)
        print "Wait sample-2 to be deleted."
        time.sleep(10)
    except:
        volume02=None

print "List all volumes, again"
for volume in cinder.volumes.list():
   print "----"
   print "Attributes of %s" % volume.name
   pp.pprint(volume._info)

print "===============CREATE, UPDATE, DELETE VOLUME SNAPSHOTS======================"
print "Create a sample volume (sample-1)."
volume01 = cinder.volumes.create(size=1, name='sample-1',
                                 description='test volume No.1')

while (volume01.status != 'available'):
    print "Wait the sample volume to be available."
    time.sleep(10)
    volume01 = cinder.volumes.get(volume01.id)

print "Create snapshot from the sample."
snapshot01 = cinder.volume_snapshots.create(volume01.id,
                                     name='snaphsot_sample-1')

while (snapshot01.status != 'available'):
    print "Wait the snapshot to be available."
    time.sleep(10)
    snapshot01 = cinder.volume_snapshots.get(snapshot01.id)

print "Update an attribute of the snapshot through a snapshot object."
snapshot01.update(description='test snapshot No.1')

print "List all snapshots"
for snapshot in cinder.volume_snapshots.list():
   print "----"
   print "Attributes of snapshot %s" % snapshot.name
   pp.pprint(snapshot._info)
   base_volume = cinder.volumes.get(snapshot.volume_id)
   print "Attributes of base volume %s" % base_volume.name
   pp.pprint(base_volume._info)
print ""

print "Update an attribute of the snapshot through the manager."
cinder.volume_snapshots.update(snapshot01, name='to_be_deleted')
print "Find a snapshot with name='to_be_deleted'"
for snapshot in cinder.volume_snapshots.findall(name='to_be_deleted'):
    print "Delete the snapshot and its base volume."
    base_volume = cinder.volumes.get(snapshot.volume_id)
    snapshot.delete()
    while (snapshot):
        try:
            cinder.volume_snapshots.get(snapshot.id)
            print "Wait the snapshot to be deleted."
            time.sleep(10)
        except:
            snapshot=None
    base_volume.delete()

print "===============ATTACH VOLUME TO INSTANCE======================"
image = nova.images.find(name='cirros-0.3.4-x86_64-uec')
flavor = nova.flavors.find(name='m1.tiny')
net = nova.networks.find(label='private')
print "Creating a server"
instance = nova.servers.create(
    name="vm01", image=image, flavor=flavor)
print "Creating a cinder volume"
volume = cinder.volumes.create(size=1, name='volume01')

while instance.status == 'BUILD':
    print "Waiting status of the server to be active."
    time.sleep(10)
    instance = nova.servers.get(instance.id)

while volume.status == 'creating':
    time.sleep(10)
    volume = cinder.volumes.get(volume.id)

nova.volumes.create_server_volume(instance.id, volume.id, '/dev/vdb')

for floating_ip in nova.floating_ips.list():
    if floating_ip.instance_id == None:
        instance.add_floating_ip(floating_ip)
        print "Floating IP: %s" % floating_ip.ip
        break


