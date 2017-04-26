# Little script to directly connect with a ethernet cable to the
# RaspberryPi.
# The RaspberryPi is set in static ip with address 192.168.200.100.

# You should probably desactive your wifi or others connections before
# running the script.

# This script has only be tested on Linux (ArchLinux more precisely).

# interface is your internet computer interface (likely eth0 on Linux).
interface="enp0s20u2"
sudo ip addr add 192.168.200.101/24 broadcast 192.168.200.255 dev $interface
# Set the default gateway.
sudo ip route add default via 192.168.200.1 dev $interface

# To restore the connection: just execute this line:
# > sudo ip addr flush dev "your_interface"
# This will remove any assigned IP to the given interface.

# If you want more information, go checkout:
# https://wiki.archlinux.org/index.php/Network_configuration#Manual_assignement
