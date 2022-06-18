
# OVS

## Useful commands
```bash
/usr/share/openvswitch/scripts/ovs-ctl start  # starts the virtual switch and its daemons 
ovs-vsctl add-br br0 # add bridge
ifconfig br0 up # after creating a bridge you can turn up its interface
ovs-vsctl add-port br0 eth0 # add eth0 as a trunk port, this means all traffic for eth0 goes through that bridge
ifconfig eth0 0 # reset any ip configuration for eth0 interface
dhclient br0 # give br0 an IP via dhcp
# you can also give IP manually:
ip addr flush dev eth0
ip addr add 192.168.128.5/24 dev br0
ip link set br0 up
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
# NOTE that the /24 is crucial, otherwise the container cannot communicate
sudo ovs-docker set-vlan br0 eth0 csle-host_vlan_1_1-001 1 # set VLAN on the container

# Example setup that works for communication between host and 2 containers through OVS:
sudo ovs-vsctl add-br ovs-br1
sudo ifconfig ovs-br1 173.16.1.1 netmask 255.255.255.0 up
sudo ovs-docker add-port ovs-br1 eth0 csle-test2-001 --ipaddress=173.16.1.2/24 --gateway=173.16.1.1
sudo ovs-docker add-port ovs-br1 eth0 csle-test1-001 --ipaddress=173.16.1.3/24 --gateway=173.16.1.1

sudo ovs-ofctl add-flow ovs-br2 ip,nw_dst=8.8.8.8,action=output:prov-to-int
# Note that you can add several IPs to an OVS switch by creating multiple ports and assigning IPs to them.

# To reach Internet from container: 
# 1. Make sure the switch the container is attached to has an IP on the same subnet as the host
# 2. Setup a default gateway in the container to be the same as the router that the host talks to


# You can use multiple IP addresses on an inteface using standard Linux IP aliasing:

ifconfig br0 192.168.128.5
ifconfig br0:1 192.168.128.6
ifconfig br0:2 192.168.128.9

# Connect two bridges:

# Create two devices using veth type:
sudo ip link add dev "int-to-prov" type veth peer name "prov-to-int"

# Add the int-to-prov veth port to the first bridge, set the type to be patch and peer altogether:
sudo ovs-vsctl add-port br0 int-to-prov
sudo ovs-vsctl set interface int-to-prov type=patch
sudo ovs-vsctl set interface int-to-prov options:peer=prov-to-int

# Add the other port to the second bridge, the -- allows to pass two commands at the same time
sudo ovs-vsctl add-port br1 prov-to-int -- set interface prov-to-int type=patch options:peer=int-to-prov

# Now bring both ports up:
ip link set dev prov-to-int up
ip link set dev int-to-prov up


# Delete bridge
ovs-vsctl del-br br0

# Delete veth pair
ip link delete int-to-prov
```