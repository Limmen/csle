# Networks

Scripts used to create virtual subnetworks of Docker containers  

## Useful commands

```bash
python create_networks.py -n 40 # Creates 40 subnetworks
python create_networks.py -d -n 40 # Deletes 40 subnetworks

sudo route add -net 172.18.8.0 netmask 255.255.255.0 gw 172.18.8.1 # If you have trouble with network connectivity
sudo route del -net 172.18.12.0 gw 172.18.12.1 netmask 255.255.255.0 # To delete created route      
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](../../LICENSE.md)

Creative Commons

(C) 2020, Kim Hammar