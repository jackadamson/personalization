#!/usr/bin/python
from __future__ import print_function
import socket
import array
import struct
import fcntl

__all__ = ["get_active_device_info", "is_64"]

# from header /usr/include/bits/ioctls.h
SIOCGIFCONF = 0x8912
SIOCGIFFLAGS = 0x8913
SIOCGIFNETMASK = 0x891b
SIOCGIFBRDADDR = 0x8919
SIOCGIFADDR = 0x8915
SIOCGIFHWADDR = 0x8927

SIOCETHTOOL = 0x8946  # As defined in include/uapi/linux/sockios.h
ETHTOOL_GSET = 0x00000001  # Get status command.

# struct definition from header /usr/include/net/if.h
# the struct size varies according to the platform arch size
# a minimal c program was used to determine the size of the
# struct, standard headers removed for brevity.
"""
#include <linux/if.h>
int main() {
  printf("Size of struct %lu\n", sizeof(struct ifreq));
}
"""

IF_STRUCT_SIZE_32 = 32
IF_STRUCT_SIZE_64 = 40


def is_64():
    """Returns C{True} if the platform is 64-bit, otherwise C{False}."""
    return struct.calcsize("l") == 8


# initialize the struct size as per the machine's architecture
IF_STRUCT_SIZE = is_64() and IF_STRUCT_SIZE_64 or IF_STRUCT_SIZE_32


def get_active_device_info(skipped_interfaces=("lo",),
                           skip_vlan=True, skip_alias=True):
    """
    Returns a dictionary containing information on each active network
    interface present on a machine.
    """
    results = []
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                             socket.IPPROTO_IP)
        for interface in get_active_interfaces(sock):
            interface_string = interface.decode("ascii")
            if interface_string in skipped_interfaces:
                continue
            if skip_vlan and b"." in interface:
                continue
            if skip_alias and b":" in interface:
                continue
            # We keep values as byte strings for use in struct.pack() in
            # different getter methods, and only use the decoded value of the
            # interface name here.
            interface_info = {"interface": interface_string, "ip_address": get_ip_address(sock, interface)}
            results.append(interface_info)
    finally:
        del sock

    return results


def get_active_interfaces(sock):
    """Generator yields active network interface names.

    @param sock: a socket instance.
    """
    max_interfaces = 128

    # Setup an array to hold our response, and initialized to null strings.
    interfaces = array.array("B", b"\0" * max_interfaces * IF_STRUCT_SIZE)
    buffer_size = interfaces.buffer_info()[0]
    packed_bytes = struct.pack(
        "iL", max_interfaces * IF_STRUCT_SIZE, buffer_size)

    byte_length = struct.unpack(
        "iL", fcntl.ioctl(sock.fileno(), SIOCGIFCONF, packed_bytes))[0]
    try:
        result = interfaces.tobytes()
    except AttributeError:
        result = interfaces.tostring()
    # Generator over the interface names
    already_found = set()
    for index in range(0, byte_length, IF_STRUCT_SIZE):
        ifreq_struct = result[index:index + IF_STRUCT_SIZE]
        interface_name = ifreq_struct[:ifreq_struct.index(b"\0")]
        if interface_name not in already_found:
            already_found.add(interface_name)
            yield interface_name


def get_ip_address(sock, interface):
    """Return the IP address associated to the interface.

    @param sock: a socket instance.
    @param interface: The name of the interface.
    """
    return socket.inet_ntoa(fcntl.ioctl(
        sock.fileno(),
        SIOCGIFADDR,
        struct.pack("256s", interface[:15]))[20:24])


if __name__ == "__main__":
    for i in get_active_device_info():
        print("{}: {}".format(i['interface'], i['ip_address']))
