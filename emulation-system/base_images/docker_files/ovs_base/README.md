
# OVS

## Useful commands
```bash
/usr/share/openvswitch/scripts/ovs-ctl start  # starts the virtual switch and its daemons 
ovs-vsctl add-br br0 # add bridge
ovs-vsctl add-port br0 eth0 # add eth0 as a trunk port
ovs-vsctl add-port br0 eth1 tag=2 # add eth1 as a tap port
ovs-vsctl add-port br0 eth2 tag=3 # add eth2 as a tap port 
ovs-vsctl list-br # list bridges
ovs-vsctl show # show switch config
ovs-vsctl add-br br0 # show MAC address table
ovs-vsctl --help # get list of possible commands

ip addr flush dev eth0 # Flush interface
ip addr add 192.168.128.5/24 dev br0 # move IP to an OVS internal device br0
ip link # check link status

sudo ovs-docker add-port br0 eth0 csle-host_vlan_1_1-001 --ipaddress="55.41.78.5/24" # add container csle-host_vlan_1_1-001 to OVS and eth0
sudo ovs-docker set-vlan br0 eth0 csle-host_vlan_1_1-001 1 # set VLAN on the container

# Connect two bridges:

# Create two devices using veth type:
ip link add dev "int-to-prov" type veth peer name "prov-to-int"

# Add the int-to-prov veth port to the first bridge, set the type to be patch and peer altogether:
ovs-vsctl add-port br0 int-to-prov
ovs-vsctl set interface int-to-prov type=patch
ovs-vsctl set interface int-to-prov options:peer=prov-to-int

# Add the other port to the second bridge:
ovs-vsctl add-port br1 prov-to-int -- set interface prov-to-int type=patch options:peer=int-to-prov

# Now bring both ports up:
ip link set dev prov-to-int up
ip link set dev int-to-prov up


# Delete bridge
ovs-vsctl del-br br0

# Delete veth pair
ip link delete int-to-prov
```