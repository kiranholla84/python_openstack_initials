from cinderclient import client
cinder = client.Client('1', "admin" , "devstack" , "admin", "http://10.108.203.127:5000/v2.0")
cinder_vol_list =  cinder.volumes.list()
myvol = cinder.volumes.create(display_name="test-vol2", size=2)
vol_id = myvol.id
print "vol id is %r" % vol_id
cinder.volumes.list()

