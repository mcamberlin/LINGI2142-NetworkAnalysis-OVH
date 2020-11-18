#!/usr/bin/env python3
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP,OSPF, OSPF6, RouterConfig,AF_INET, AF_INET6, set_rr, ebgp_session, SHARE, CLIENT_PROVIDER, IPTables, IP6Tables, InputFilter, NOT, Deny, Allow
from ipmininet.examples.static_address_network import StaticAddressNet
from ipmininet.examples.iptables import IPTablesTopo
from ipmininet.router.config import IPTables, IP6Tables, Rule, RouterConfig

class OVHTopology(IPTopo):

    def build(self, *args, **kwargs):
        # --- Metrics ---
        small = 1
        medium = 3
        large = 8
        extra_large = 13

        # IPv4 range 198.27.92.0/24
        # IPv6 range 2604:2dc0::/32
        # lan USA : 2604:2dc0::/34
        # lan EU : 2604:2dc0:8000::/34
        # lan APAC : 2604:2dc0:4000::/34
            
        # --- Hosts ---

        family = AF_INET6();

        lan_h1 = '1.1.0.0/24'
        lan_h1_v6 = '2604:2dc0:2000::/36'

        lan_h2 = '1.2.5.0/24'
        lan_h2_v6 = '2604:2dc0:3000::/36'
        
        lan_ggl = '1.3.1.0/24'
        lan_ggl_v6 = 'cafe:babe:dead:beaf::/64'

        lan_cgt = '1.4.2.0/24'
        lan_cgt_v6 = 'c1a4:4ad:c0ff:ee::/64'

        lan_lvl3 = '1.5.3.0/24'
        lan_lvl3_v6 = 'cafe:d0d0:e5:dead::/64'

        lan_tel = '1.6.4.0/24'
        lan_tel_v6 = 'aaaa:aaaa:aaaa:aaaa::/64'
        
        # --- Routers ---
        #OVH = \32
        #OVH+continent = \34
        #OVH+continent+type = \36
        sin = self.addRouter("sin", config=RouterConfig,lo_addresses=["2604:2dc0:4000::0/36","198.27.92.0/24"] );
        syd = self.addRouter("syd", config=RouterConfig,lo_addresses=["2604:2dc0:4000::1/36","198.27.92.1/24"]);

        pao = self.addRouter("pao", config=RouterConfig,lo_addresses=["2604:2dc0::0/36","198.27.92.2/24"]);
        sjo = self.addRouter("sjo", config=RouterConfig,lo_addresses=["2604:2dc0::1/36","198.27.92.3/24"]);
        lax1 = self.addRouter("lax1", config=RouterConfig,lo_addresses=["2604:2dc0::2/36","198.27.92.4/24"]);

        chi1 = self.addRouter("chi1", config=RouterConfig,lo_addresses=["2604:2dc0::3/36","198.27.92.5/24"]);
        chi5 = self.addRouter("chi5", config=RouterConfig,lo_addresses=["2604:2dc0::4/36","198.27.92.6/24"]);

        bhs1 = self.addRouter("bhs1", config=RouterConfig,lo_addresses=["2604:2dc0::5/36","198.27.92.7/24"]);
        bhs2 = self.addRouter("bhs2", config=RouterConfig,lo_addresses=["2604:2dc0::6/36","198.27.92.8/24"]);

        ash1 = self.addRouter("ash1", config=RouterConfig,lo_addresses=["2604:2dc0::7/36","198.27.92.9/24"]);
        ash5 = self.addRouter("ash5", config=RouterConfig,lo_addresses=["2604:2dc0::8/36","198.27.92.10/24"]);

        nwk1 = self.addRouter("nwk1", config=RouterConfig,lo_addresses=["2604:2dc0::9/36","198.27.92.11/24"]);
        nwk5 = self.addRouter("nwk5", config=RouterConfig,lo_addresses=["2604:2dc0::a/36","198.27.92.12/24"]);
        nyc = self.addRouter("nyc", config=RouterConfig,lo_addresses=["2604:2dc0::b/36","198.27.92.13/24"]);

        lon_thw = self.addRouter("lon_thw", config=RouterConfig,lo_addresses=["2604:2dc0:8000::0/36","198.27.92.14/24"]);
        lon_drch = self.addRouter("lon_drch", config=RouterConfig,lo_addresses=["2604:2dc0:8000::1/36","198.27.92.15/24"]);

        # --- Physical links between routers ---
        self.addLink(sin, sjo,igp_metric=extra_large);
        self.addLink(syd,lax1,igp_metric=extra_large);

        self.addLink(syd,sin,igp_metric=large);
        self.addLink(syd,lon_thw,igp_metric=extra_large);
        self.addLink(syd,lon_drch,igp_metric=extra_large);
        self.addLink(sin,lon_thw,igp_metric=extra_large);
        self.addLink(sin,lon_drch,igp_metric=extra_large);
        self.addLink(lon_thw,lon_drch,igp_metric=small);

        self.addLink(pao,sjo,igp_metric=medium);
        self.addLink(sjo,lax1,igp_metric=medium);

        self.addLink(pao,chi1,igp_metric=medium);
        self.addLink(pao,chi5,igp_metric=medium);
        self.addLink(chi1,chi5,igp_metric=small);

        self.addLink(lax1,ash1,igp_metric=large);
        self.addLink(lax1,ash5,igp_metric=large);
        self.addLink(ash1,ash5,igp_metric=small);

        self.addLink(chi1,bhs1,igp_metric=medium);
        self.addLink(chi5,bhs2,igp_metric=medium);
        self.addLink(bhs1,bhs2,igp_metric=small);

        self.addLink(bhs1,nwk1,igp_metric=medium);
        self.addLink(bhs2,nwk5,igp_metric=medium);

        self.addLink(ash1,nwk1,igp_metric=large);
        self.addLink(ash5,nwk5,igp_metric=large);

        self.addLink(ash1,chi1,igp_metric=large);
        self.addLink(ash5,chi5,igp_metric=large);

        self.addLink(nwk1,nwk5,igp_metric=small);
        link_42 = self.addLink(nwk1,nyc,igp_metric=small);
        self.addLink(nwk5,nyc,igp_metric=small);

        self.addLink(nwk1,lon_thw,igp_metric=extra_large);
        self.addLink(nwk5,lon_drch,igp_metric=extra_large);


        # --- OSPF and OSPF6 configuration as IGP ---

        sin.addDaemon(OSPF, KEYID=1, KEY="OVHKEY");
        syd.addDaemon(OSPF, KEYID=1, KEY="OVHKEY");
        pao.addDaemon(OSPF, KEYID=1, KEY="OVHKEY");
        sjo.addDaemon(OSPF, KEYID=1, KEY="OVHKEY");
        lax1.addDaemon(OSPF, KEYID=1, KEY="OVHKEY");
        chi1.addDaemon(OSPF, KEYID=1, KEY="OVHKEY");
        chi5.addDaemon(OSPF, KEYID=1, KEY="OVHKEY");
        bhs1.addDaemon(OSPF, KEYID=1, KEY="OVHKEY");
        bhs2.addDaemon(OSPF, KEYID=1, KEY="OVHKEY");
        ash1.addDaemon(OSPF, KEYID=1, KEY="OVHKEY");
        ash5.addDaemon(OSPF, KEYID=1, KEY="OVHKEY");
        nwk1.addDaemon(OSPF, KEYID=1, KEY="OVHKEY");
        nwk5.addDaemon(OSPF, KEYID=1, KEY="OVHKEY");
        nyc.addDaemon(OSPF, KEYID=1, KEY="OVHKEY");
        lon_thw.addDaemon(OSPF, KEYID=1, KEY="OVHKEY");
        lon_drch.addDaemon(OSPF, KEYID=1, KEY="OVHKEY");

        sin.addDaemon(OSPF6);
        syd.addDaemon(OSPF6);
        pao.addDaemon(OSPF6);
        sjo.addDaemon(OSPF6);
        lax1.addDaemon(OSPF6);
        chi1.addDaemon(OSPF6);
        chi5.addDaemon(OSPF6);
        bhs1.addDaemon(OSPF6);
        bhs2.addDaemon(OSPF6);
        ash1.addDaemon(OSPF6);
        ash5.addDaemon(OSPF6);
        nwk1.addDaemon(OSPF6);
        nwk5.addDaemon(OSPF6);
        nyc.addDaemon(OSPF6);
        lon_thw.addDaemon(OSPF6);
        lon_drch.addDaemon(OSPF6);


        # --- Rules for inputTable --- 

        ip_rules = [Rule("-P INPUT ACCEPT"),
                    Rule("-A INPUT -s 198.27.92.0/2 -j ACCEPT")]

        #  Rule("-P INPUT ACCEPT")

        ip6_rules = [
                    Rule("-A INPUT -s 8604:2dc0::/1 -j ACCEPT"),
                    # permit traffic on the loopback device, permit already established connections, drop invalid packets
                    Rule("-A INPUT -i lo -j ACCEPT"),
                    Rule("-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT"),
                    Rule("-A INPUT -m conntrack --ctstate INVALID -j DROP"),
                    # Chain to prevent SSH brute-force attacks
                    # Rule("-N SSHBRUTE"),
                    # Rule("-A SSHBRUTE -m recent --name SSH --set"),
                    # Rule("-A SSHBRUTE -m recent --name SSH --update --seconds 300 --hitcount 10 -m limit --limit 1/second --limit-burst 100"),
                    # Rule("-A SSHBRUTE -m recent --name SSH --update --seconds 300 --hitcount 10 -j DROP"),
                    # Rule("-A SSHBRUTE -j ACCEPT"),
                    # Chain to prevent ping flooding
                    # Rule("-N ICMPFLOOD"),
                    # Rule("-A ICMPFLOOD -m recent --set --name ICMP --rsource"),
                    # Rule("-A ICMPFLOOD -m recent --update --seconds 1 --hitcount 6 --name ICMP --rsource --rttl -m limit --limit 1/sec --limit-burst 1"),
                    # Rule("-A ICMPFLOOD -m recent --update --seconds 1 --hitcount 6 --name ICMP --rsource --rttl -j DROP"),
                    # Rule("-A ICMPFLOOD -j ACCEPT"),
                    #Rule("-A INPUT -p icmpv6 -m icmpv6 --icmpv6-type neighbour-advertisement -j DROP"),
                    # Rule('-A INPUT -p icmpv6 -m icmpv6 --icmpv6-type neighbour-solicitation -j ACCEPT'),
                    # Rule('-A INPUT -p icmpv6 -m icmpv6 --icmpv6-type neighbour-advertisement -j ACCEPT'),
                    # Accept ssh access + use SSHBRUTE to prevent brute-force attacks
                    # Rule("-A INPUT -p tcp --dport 22 --syn -m conntrack --ctstate NEW -j SSHBRUTE"),
                    # Permit echo request (ping) + use ICMPFLOOD to prevent ping flooding
                    # Rule("-A INPUT -p ipv6-icmp --icmpv6-type 128 -j ICMPFLOOD"),
                    
                    # Rule("-A INPUT -p ipv6-icmp --icmpv6-type 1   -j ACCEPT"),
                    # Rule("-A INPUT -p ipv6-icmp --icmpv6-type 2   -j ACCEPT"),
                    # Rule("-A INPUT -p ipv6-icmp --icmpv6-type 3   -j ACCEPT"),
                    # Rule("-A INPUT -p ipv6-icmp --icmpv6-type 4   -j ACCEPT"),
                    # Rule("-A INPUT -p ipv6-icmp --icmpv6-type 129   -j ACCEPT"),
                    # Rule("-A INPUT -p ipv6-icmp --icmpv6-type 130   -j ACCEPT"),
                    # Rule("-A INPUT -p ipv6-icmp --icmpv6-type 131   -j ACCEPT"),
                    # Rule("-A INPUT -p ipv6-icmp --icmpv6-type 132   -j ACCEPT"),
                    # Rule("-A INPUT -p ipv6-icmp --icmpv6-type 133   -j ACCEPT"),
                    # Rule("-A INPUT -p ipv6-icmp --icmpv6-type 134   -j ACCEPT"),
                    # Rule("-A INPUT -p ipv6-icmp --icmpv6-type 135   -j ACCEPT"),
                    # Rule("-A INPUT -p ipv6-icmp --icmpv6-type 136   -j ACCEPT"),
                    # Rule("-A INPUT -p ipv6-icmp --icmpv6-type 137   -j ACCEPT"),

                    Rule("-P INPUT ACCEPT")]

        sin.addDaemon(IPTables, rules=ip_rules);
        sin.addDaemon(IP6Tables, rules=ip6_rules);
        syd.addDaemon(IPTables, rules=ip_rules);
        syd.addDaemon(IP6Tables, rules=ip6_rules);
        pao.addDaemon(IPTables, rules=ip_rules);
        pao.addDaemon(IP6Tables, rules=ip6_rules);
        sjo.addDaemon(IPTables, rules=ip_rules);
        sjo.addDaemon(IP6Tables, rules=ip6_rules);
        lax1.addDaemon(IPTables, rules=ip_rules);
        lax1.addDaemon(IP6Tables, rules=ip6_rules);
        chi1.addDaemon(IPTables, rules=ip_rules);
        chi1.addDaemon(IP6Tables, rules=ip6_rules);
        chi5.addDaemon(IPTables, rules=ip_rules);
        chi5.addDaemon(IP6Tables, rules=ip6_rules);
        bhs1.addDaemon(IPTables, rules=ip_rules);
        bhs1.addDaemon(IP6Tables, rules=ip6_rules);
        bhs2.addDaemon(IPTables, rules=ip_rules);
        bhs2.addDaemon(IP6Tables, rules=ip6_rules);
        ash1.addDaemon(IPTables, rules=ip_rules);
        ash1.addDaemon(IP6Tables, rules=ip6_rules);
        ash5.addDaemon(IPTables, rules=ip_rules);
        ash5.addDaemon(IP6Tables, rules=ip6_rules);
        nwk1.addDaemon(IPTables, rules=ip_rules);
        nwk1.addDaemon(IP6Tables, rules=ip6_rules);
        nwk5.addDaemon(IPTables, rules=ip_rules);
        nwk5.addDaemon(IP6Tables, rules=ip6_rules);
        nyc.addDaemon(IPTables, rules=ip_rules);
        nyc.addDaemon(IP6Tables, rules=ip6_rules);
        lon_thw.addDaemon(IPTables, rules=ip_rules);
        lon_thw.addDaemon(IP6Tables, rules=ip6_rules);
        lon_drch.addDaemon(IPTables, rules=ip_rules);
        lon_drch.addDaemon(IP6Tables, rules=ip6_rules);

        
        # --- Create Ases : AS=1 for OVH   ---
        self.addAS(1, (sin,syd,pao,sjo,lax1,chi1,chi5,bhs1,bhs2,ash1,ash5,nwk1,nwk5,nyc,lon_thw,lon_drch))

        # --- Stub provider : google (AS2)  ---
        ggl = self.addRouter("ggl", config=RouterConfig);
        
        self.addLink(ggl,ash1,igp_metric=1);
        self.addLink(ggl,ash5,igp_metric=1);
        
        ggl.addDaemon(OSPF);
        ggl.addDaemon(OSPF6);
        ggl.addDaemon(BGP, address_families=(AF_INET(networks=(lan_ggl,)),AF_INET6(networks=(lan_ggl_v6,))) , routerid="1.1.1.1", bgppassword="OVHpsswd");
        
        self.addAS(2,(ggl , ));
        
        ebgp_session(self, ggl, ash1, link_type=SHARE);
        ebgp_session(self, ggl, ash5, link_type=SHARE);

        # --- Transit providers: Cogent, Level3 and Telia ---
        
        # Cogent (AS=3) 
        cgt = self.addRouter("cgt", config=RouterConfig);
        
        self.addLink(cgt,nwk1,igp_metric=1);
        self.addLink(cgt,nwk5,igp_metric=1);
        self.addLink(cgt,ash1,igp_metric=1);
        self.addLink(cgt,ash5,igp_metric=1);
        self.addLink(cgt,chi1,igp_metric=1);
        self.addLink(cgt,sjo,igp_metric=1);
        
        cgt.addDaemon(OSPF);
        cgt.addDaemon(OSPF6);
        cgt.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_cgt_v6,)),AF_INET(networks=(lan_cgt,)),), routerid="1.1.1.2", bgppassword="OVHpsswd");
        
        self.addAS(3,(cgt , ));
        
        ebgp_session(self, cgt, nwk1, link_type=SHARE);
        ebgp_session(self, cgt, nwk5, link_type=SHARE);
        ebgp_session(self, cgt, ash1, link_type=SHARE);
        ebgp_session(self, cgt, ash5, link_type=SHARE);
        ebgp_session(self, cgt, chi1, link_type=SHARE);
        ebgp_session(self, cgt, sjo, link_type=SHARE);
        
        #Level 3 (AS=4) 
        lvl3 = self.addRouter("lvl3", config=RouterConfig);
        
        self.addLink(lvl3,nwk1,igp_metric=1);
        self.addLink(lvl3,nwk5,igp_metric=1);
        self.addLink(lvl3,chi1,igp_metric=1);
        self.addLink(lvl3,chi5,igp_metric=1);
        self.addLink(lvl3,sjo,igp_metric=1);
        
        lvl3.addDaemon(OSPF);
        lvl3.addDaemon(OSPF6);
        lvl3.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_lvl3_v6,)),AF_INET(networks=(lan_lvl3,)),), routerid="1.1.1.3", bgppassword="OVHpsswd");

        self.addAS(4,(lvl3, ));
        
        ebgp_session(self, lvl3, nwk1, link_type=SHARE);
        ebgp_session(self, lvl3, nwk5, link_type=SHARE);
        ebgp_session(self, lvl3, chi1, link_type=SHARE);
        ebgp_session(self, lvl3, chi5, link_type=SHARE);
        ebgp_session(self, lvl3, sjo, link_type=SHARE);
        
        # Telia (AS=5) 
        tel = self.addRouter("tel", config=RouterConfig);
        
        self.addLink(tel,nwk1,igp_metric=1);
        self.addLink(tel,nwk5,igp_metric=1);
        self.addLink(tel,ash5,igp_metric=1);
        self.addLink(tel,chi5,igp_metric=1);
        self.addLink(tel,pao,igp_metric=1);
        
        tel.addDaemon(OSPF);
        tel.addDaemon(OSPF6);
        tel.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_tel_v6,)),AF_INET(networks=(lan_tel,)),), routerid="1.1.1.4", bgppassword="OVHpsswd");
        
        self.addAS(5,(tel, ));
        
        ebgp_session(self, tel, nwk1, link_type=SHARE);
        ebgp_session(self, tel, nwk5, link_type=SHARE);
        ebgp_session(self, tel, ash5, link_type=SHARE);
        ebgp_session(self, tel, chi5, link_type=SHARE);
        ebgp_session(self, tel, pao, link_type=SHARE);
        

        # --- BGP configuration ---

        sin.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_h1_v6,lan_h2_v6)),AF_INET(networks=(lan_h1,lan_h2)),), routerid="1.1.1.5", bgppassword="OVHpsswd");
        syd.addDaemon(BGP, bgppassword="OVHpsswd");
        
        pao.addDaemon(BGP, bgppassword="OVHpsswd");
        sjo.addDaemon(BGP, bgppassword="OVHpsswd");
        
        lax1.addDaemon(BGP, bgppassword="OVHpsswd");
        
        chi1.addDaemon(BGP, bgppassword="OVHpsswd");
        chi5.addDaemon(BGP, bgppassword="OVHpsswd");
        
        bhs1.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_h1_v6,lan_h2_v6)),AF_INET(networks=(lan_h1,lan_h2)),), routerid="1.1.1.6", bgppassword="OVHpsswd");
        bhs2.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_h1_v6,lan_h2_v6)),AF_INET(networks=(lan_h1,lan_h2)),), routerid="1.1.1.7", bgppassword="OVHpsswd");
        
        ash1.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_h1_v6,lan_h2_v6)),AF_INET(networks=(lan_h1,lan_h2)),), routerid="1.1.1.8", bgppassword="OVHpsswd");
        ash5.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_h1_v6,lan_h2_v6)),AF_INET(networks=(lan_h1,lan_h2)),), routerid="1.1.1.9", bgppassword="OVHpsswd");
        
        nwk1.addDaemon(BGP, bgppassword="OVHpsswd");
        nwk5.addDaemon(BGP, bgppassword="OVHpsswd");
        
        nyc.addDaemon(BGP, bgppassword="OVHpsswd");
        
        lon_thw.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_h1_v6,lan_h2_v6)),AF_INET(networks=(lan_h1,lan_h2,)),), routerid="1.1.1.10", bgppassword="OVHpsswd");
        lon_drch.addDaemon(BGP, bgppassword="OVHpsswd")

        # --- Configure the router reflectors ---
        set_rr(self, rr= bhs1, peers=[chi1,pao,nwk1,nyc,bhs2,ash5]);       
        set_rr(self, rr= bhs2, peers=[nwk5,pao,sjo,chi5,bhs1,ash5]);
        set_rr(self, rr= ash5, peers=[nyc,nwk5,lax1,bhs1,bhs2,chi5]);

        set_rr(self, rr= ash1, peers=[nwk1,lax1,sjo,bhs1,bhs2,chi1,ash5,lon_thw,sin]);      # This one is a super RR
        set_rr(self, rr = lon_thw, peers=[lon_drch,sin,ash1]);                              # This one is a super RR
        set_rr(self, rr = sin, peers=[syd,ash1,lon_thw]);                                   # This one is a super RR

        # --- Hosts --- (one host for each provider considered)
        h1 = self.addHost("h1");
        self.addSubnet(nodes = [chi1, h1], subnets=(lan_h1,lan_h1_v6));
        self.addLink(h1,chi1,igp_metric=1);

        h2 = self.addHost("h2");
        self.addSubnet(nodes = [nyc, h2], subnets=(lan_h2,lan_h2_v6));
        self.addLink(h2,nyc,igp_metric=1);
            
        h_ggl = self.addHost("h_ggl");
        self.addSubnet(nodes = [ggl, h_ggl], subnets=(lan_ggl,lan_ggl_v6));
        self.addLink(h_ggl,ggl,igp_metric=1);

        
        h_cgt = self.addHost("h_cgt");
        self.addSubnet(nodes = [cgt, h_cgt], subnets=(lan_cgt,lan_cgt_v6));
        self.addLink(h_cgt,cgt,igp_metric=1);

        
        h_lvl3 = self.addHost("h_lvl3");
        self.addSubnet(nodes = [lvl3, h_lvl3], subnets=(lan_lvl3,lan_lvl3_v6));
        self.addLink(h_lvl3,lvl3,igp_metric=1);
        
        
        h_tel = self.addHost("h_tel");
        self.addSubnet(nodes = [tel, h_tel], subnets=(lan_tel,lan_tel_v6));
        self.addLink(h_tel,tel,igp_metric=1);

        super().build(*args, **kwargs)


# Press the green button to run the script.
if __name__ == '__main__':
    net = IPNet(topo=OVHTopology())
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()
