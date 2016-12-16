"""Classes for interfaces and links that are IP-agnostic. This basically
enhance the Intf class from Mininet, and then define sane defaults for the link
classes and a new TCIntf base."""
from itertools import chain
from ipaddress import ip_interface, IPv4Interface, IPv6Interface

from . import OSPF_DEFAULT_AREA, MIN_IGP_METRIC
from .utils import otherIntf, is_container

# Apparently there is a circular import between mininet.link and mininet.node,
# break it by importing node first
# FIXME wait for upstream PR to be accepted ... then remove the first include
import mininet.node as _
import mininet.link as _m
from mininet.log import lg as log


class IPIntf(_m.Intf):
    """This class represents a node interface. It is IP-agnostic, as in
    its `addresses` attribute is a dictionnary keyed by IP version,
    containing the list of all addresses for a given version"""
    def __init__(self, *args, **kwargs):
        # Only one IP broadcast domain per interface, VLANs are supported
        # by aliasing interfaces.
        self.broadcast_domain = None
        self.addresses = {4: [], 6: []}
        super(IPIntf, self).__init__(*args, **kwargs)
        self.isUp(setUp=True)
        self._refresh_addresses()

    @property
    def igp_area(self):
        """Return the igp area associated to this interface"""
        return self.get('igp_area', OSPF_DEFAULT_AREA)

    @property
    def igp_metric(self):
        """Return the igp metric associated to this interface"""
        return self.get('igp_metric', MIN_IGP_METRIC)

    @property
    def describe(self):
        """Return a string describing the interface facing this one"""
        other = otherIntf(self)
        return '-> %s' % (other.name if other else 'n/a')

    def get(self, key, val):
        """Check for a given key in the interface parameters"""
        return self.params.get(key, val)

    def __default(self, version):
        """Return the default addresses for a given IP version
        :raise IndexError:"""
        return self.addresses[version][0]

    def _ip(self, version):
        """Return the main IP of the given version for this interface"""
        try:
            return str(self.__default(version).ip)
        except IndexError:
            return None

    def _prefixLen(self, version):
        """Return the prefixLen of the main IP for the given version"""
        try:
            return self.__default(version).network.prefixlen
        except IndexError:
            return None

    # We want to stay API-compatible with Intf, so we override ip/prefixLen
    @property
    def ip(self):
        return self._ip(4)

    def ips(self):
        """Return a generator over all IPv4 assigned to this interface"""
        for i in self.addresses[4]:
            yield i

    @ip.setter
    def ip(self, ip):
        self.setIP(ip, prefixLen=self.prefixLen)

    @property
    def prefixLen(self):
        return self._prefixLen(4)

    @prefixLen.setter
    def prefixLen(self, prefixLen):
        self.setIP(self.ip, prefixLen=prefixLen)

    @property
    def ip6(self):
        """Return the default IPv6 for this interface"""
        return self._ip(6)

    def ip6s(self, exclude_lls=False):
        """Return a generator over all IPv6 assigned to this interface

        :param exclude_lls: Whether Link-locals should be included or not"""
        for i in self.addresses[6]:
            if not exclude_lls or not i.is_link_local:
                yield i

    @ip6.setter
    def ip6(self, ip):
        self.setIP6(ip, prefixLen=self.prefixLen6)

    @property
    def prefixLen6(self):
        """Return the prefix length for the default IPv6 for this interface"""
        return self._prefixLen(6)

    @prefixLen6.setter
    def prefixLen6(self, prefixLen):
        self.setIP6(self.ip6, prefixLen=prefixLen)

    def _set_ip(self, ip, prefixLen=None):
        """Set one or more IP addresses, possibly from different families.
        This will remove previously set addresses of the affected families.

        :param ip: either an IP string (mininet-like behavior),
                    or an ip_interface like, or a sequence of both
        :param prefixLen: the prefix length to use for all cases where
                          the addresses is given as a string without a given
                          prefix."""
        if not ip:
            return
        setv4 = setv6 = False
        # Make sure we have an up-to-date view of our addresses
        self._refresh_addresses()
        rval = []
        # We want to iterate over the new ip sets
        if not is_container(ip):
            ip = (ip,)
        for addr in ip:
            # Make sure we have ip_interface-like objects
            if isinstance(addr, basestring):
                if '/' not in addr and prefixLen is not None:
                    # And use the default prefix if absent
                    addr = ip_interface('%s/%s' % (addr, prefixLen))
                else:
                    # no prefixLen defaults to full /128 or /32
                    addr = ip_interface(addr)

            # Assign IP
            rval.append(self.cmd('ip', 'address', 'add', 'dev',
                                 self.name, addr.with_prefixlen))
            # Record assignement family
            if addr.version == 4:
                setv4 = True
            elif addr.version == 6:
                setv6 = True
        # Clean-up old addresses
        cleanup = []
        if setv4:
            cleanup.append(self.ips())
        if setv6:
            cleanup.append(self.ip6s(exclude_lls=True))
        map(self._del_ip, chain.from_iterable(cleanup))
        self._refresh_addresses()
        return rval.pop() if rval and len(rval) == 1 else rval

    def _del_ip(self, ip):
        """Remove an assigned IP fom this interface.
        Does not update self.addresses!

        :param ip: ip_interface-like"""
        self.cmd('ip', 'address', 'del', 'dev', self.name, ip.with_prefixlen)

    setIP = setIP6 = _set_ip

    def _refresh_addresses(self):
        """Request and parse the addresses of this interface"""
        self.mac = None
        self.addresses = {4: [], 6: []}
        addrstr = self.cmd('ip', 'address', 'show', 'dev', self.name)
        if not addrstr:
            raise RuntimeError('Failed to run ip address!')
        self.mac, v4, v6 = _parse_addresses(addrstr)
        self.addresses[4] = sorted(v4, cmp=address_comparator, reverse=True)
        self.addresses[6] = sorted(v6, cmp=address_comparator, reverse=True)

    def updateIP(self):
        self._refresh_addresses()
        return self.ip

    def updateIP6(self):
        self._refresh_addresses()
        return self.ip6

    def updateMAC(self):
        self._refresh_addresses()
        return self.mac

    def updateAddr(self):
        self._refresh_addresses()
        return self.ip, self.mac


def _parse_addresses(out):
    """Parse the output of an ip address command
    :return: mac, [ipv4], [ipv6]"""
    # 1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state ...
    #    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    #    inet 127.0.0.1/8 scope host lo
    #    valid_lft forever preferred_lft forever
    #    inet6 ::1/128 scope host
    #    valid_lft forever preferred_lft forever
    mac = None
    v4 = []
    v6 = []
    for line in out.strip(' \n\t\r').split('\n'):
        parts = line.strip(' \n\t\r').split(' ')
        try:
            t = parts[0]
            if t == 'inet':
                v4.append(IPv4Interface(parts[1]))
            elif t == 'inet6':
                v6.append(IPv6Interface(parts[1]))
            elif 'link/' in t:
                mac = parts[1]
        except IndexError:
            log.error('Malformed ip-address line:', line)
    return mac, v4, v6


class IPLink(_m.Link):
    """A Link class that defaults to IPIntf"""
    def __init__(self, node1, node2, intf=IPIntf, *args, **kwargs):
        """We override Link intf default to use IPIntf"""
        super(IPLink, self).__init__(node1=node1, node2=node2,
                                     intf=intf, *args, **kwargs)


# Monkey patch mininit.link ...
TCIntf = _m.TCIntf
TCIntf.__bases__ = (IPIntf,)


def address_comparator(a, b):
    """Return -1, 0, 1 if a is less, equally, more visible than b.
    We define visibility according to IP version, address scope, address class,
    and address value"""
    # We prefer IPv6
    if a.version > b.version:
        return 1
    if a.version < b.version:
        return -1
    # LLs have low visibility
    if a.is_link_local and not b.is_link_local:
        return -1
    if b.is_link_local and not a.is_link_local:
        return 1
    # We prefer global addresses over private ones
    if a.network.is_global and not b.network.is_global:
        return 1
    if b.network.is_global and not a.network.is_global:
        return -1
    # Otherwise simply rank the IP values
    if a > b:
        return 1
    return -1 if b > a else 0