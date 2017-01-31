#!/usr/bin/python
#from clients import nova, glance, cinder
from cinderclient import client as cClient
from novaclient import client as nClient
cinder = cClient.Client('2', "admin" , "devstack" , "admin", "http://10.108.203.127:5000/v2.0")
nova = nClient.Client('2', "admin" , "devstack" , "admin", "http://10.108.203.127:5000/v2.0")
import time

image = nova.images.find(name='cirros-0.3.4-x86_64-uec')
flavor = nova.flavors.find(name='m1.tiny')
net = nova.networks.find(label='private')
instance = nova.servers.create(
    name="vm01", image=image, flavor=flavor)
volume = cinder.volumes.create(size=1, name='volume01')

while instance.status == 'BUILD':
    print "Waiting status to be active."
    time.sleep(10)
    instance = nova.servers.get(instance.id)

while volume.status == 'creating':
    time.sleep(1)
    volume = cinder.volumes.get(volume.id)

nova.volumes.create_server_volume(instance.id, volume.id, '/dev/vdb')

for floating_ip in nova.floating_ips.list():
    if floating_ip.instance_id == None:
        instance.add_floating_ip(floating_ip)
        print "Floating IP: %s" % floating_ip.ip
        break
