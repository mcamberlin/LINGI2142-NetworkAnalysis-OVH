#!/usr/bin/env python3
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import RouterConfig,AF_INET, AF_INET6 #for router configuration
from ipmininet.router.config import OSPF, OSPF6 # for OSPF configuration
from ipmininet.router.config import BGP, bgp_fullmesh, set_rr, ebgp_session, SHARE, CLIENT_PROVIDER, bgp_peering # for BGP configuration
from ipmininet.router.config.bgp import rm_setup, ebgp_Client, ebgp_Peer, ibgp_Inter_Region # for BGP communities 
from ipmininet.router.config import IPTables, IP6Tables, Rule # for firewalls
from ipmininet.router.config.bgp import bgp_anycast # for anycast configuration
from ipmininet.router.config import STATIC, StaticRoute # for anycast
from ipmininet.router.config import IPTables, IP6Tables, Rule, InputFilter, OutputFilter, TransitFilter, NOT, Deny, Allow # for firewalls

class OVHTopology(IPTopo):

    def build(self, *args, **kwargs):
        # --- Metrics ---
        small = 1
        medium = 3
        large = 8
        extra_large = 13

        # IPv4 range 198.27.92.0/24
        # IPv6 range 2604:2dc0::/32
        # lan USA : 2604:2dc0:0000::/34
        # OTHER : 2604:2dc0:2000::/34
        # lan APAC : 2604:2dc0:4000::/34
        # lan EU : 2604:2dc0:8000::/34
            
        #OVH = \32
        #OVH+continent = \34
        #OVH+continent+type = \36

        # ===================== OVH Router configurations ==================
        # 16 routers identified by a single IPv4, IPv6 address
        # ==================================================================        
        # --- Routers configuration ---
        sin = self.addRouter("sin", config=RouterConfig,lo_addresses=["2604:2dc0:4000::0/36","198.27.92.0/24"])
        syd = self.addRouter("syd", config=RouterConfig,lo_addresses=["2604:2dc0:4000::1/36","198.27.92.1/24"])

        pao = self.addRouter("pao", config=RouterConfig,lo_addresses=["2604:2dc0::0/36","198.27.92.2/24"])
        sjo = self.addRouter("sjo", config=RouterConfig,lo_addresses=["2604:2dc0::1/36","198.27.92.3/24"])
        lax1 = self.addRouter("lax1", config=RouterConfig,lo_addresses=["2604:2dc0::2/36","198.27.92.4/24"])

        chi1 = self.addRouter("chi1", config=RouterConfig,lo_addresses=["2604:2dc0::3/36","198.27.92.5/24"])
        chi5 = self.addRouter("chi5", config=RouterConfig,lo_addresses=["2604:2dc0::4/36","198.27.92.6/24"])

        bhs1 = self.addRouter("bhs1", config=RouterConfig,lo_addresses=["2604:2dc0::5/36","198.27.92.7/24"])
        bhs2 = self.addRouter("bhs2", config=RouterConfig,lo_addresses=["2604:2dc0::6/36","198.27.92.8/24"])

        ash1 = self.addRouter("ash1", config=RouterConfig,lo_addresses=["2604:2dc0::7/36","198.27.92.9/24"])
        ash5 = self.addRouter("ash5", config=RouterConfig,lo_addresses=["2604:2dc0::8/36","198.27.92.10/24"])

        nwk1 = self.addRouter("nwk1", config=RouterConfig,lo_addresses=["2604:2dc0::9/36","198.27.92.11/24"])
        nwk5 = self.addRouter("nwk5", config=RouterConfig,lo_addresses=["2604:2dc0::a/36","198.27.92.12/24"])
        nyc = self.addRouter("nyc", config=RouterConfig,lo_addresses=["2604:2dc0::b/36","198.27.92.13/24"])

        lon_thw = self.addRouter("lon_thw", config=RouterConfig,lo_addresses=["2604:2dc0:8000::0/36","198.27.92.14/24"])
        lon_drch = self.addRouter("lon_drch", config=RouterConfig,lo_addresses=["2604:2dc0:8000::1/36","198.27.92.15/24"])
        
        anycast1 = self.addRouter("anycast1",config = RouterConfig, lo_addresses = ["2604:2dc1::0/128","192.27.92.255/32",] )   
        anycast2 = self.addRouter("anycast2",config = RouterConfig, lo_addresses = ["2604:2dc1::0/128","192.27.92.255/32",] )   
        anycast3 = self.addRouter("anycast3",config = RouterConfig, lo_addresses = ["2604:2dc1::0/128","192.27.92.255/32",] ) 
        anycastServers = [anycast1,anycast2,anycast3]

        OVHRouters = [sin, syd, pao, sjo, lax1, chi1, chi5, bhs1, bhs2, ash1, ash5, nwk1, nwk5, nyc, lon_thw, lon_drch,anycast1,anycast2,anycast3]
        NARouters = [pao,sjo,lax1,chi1,chi5,bhs1,bhs2,ash1,ash5,nwk1,nwk5,nyc]
        APACRouters = [sin,syd]
        EURouters = [lon_thw,lon_drch]
        self.addAS(16276, OVHRouters)
        
        
        # --- Subnets of each router ---
        #       IPv6
        subnetSin6 = "2604:2dc0:4800::0/40"
        subnetSyd6 = "2604:2dc0:4900::0/40"
        
        subnetPao6 = "2604:2dc0:0800::0/40"
        subnetSjo6 = "2604:2dc0:0900::0/40"
        subnetLax16 = "2604:2dc0:0a00::0/40"
        
        subnetChi16 = "2604:2dc0:0b00::0/40"
        subnetChi56 = "2604:2dc0:0c00::0/40"

        subnetBhs16 = "2604:2dc0:0d00::0/40"
        subnetBhs26 = "2604:2dc0:0e00::0/40"
        
        subnetAsh16 = "2604:2dc0:0f00::0/40"
        subnetAsh56 = "2604:2dc0:1000::0/40"
        
        subnetNwk16 = "2604:2dc0:1100::0/40"
        subnetNwk56 = "2604:2dc0:1200::0/40"
        subnetNyc6 = "2604:2dc0:1300::0/40"
        
        subnetLon_thw6 = "2604:2dc0:8800::0/40"
        subnetLon_drch6 = "2604:2dc0:8900::0/40"
        
        #       IPv4
        subnetSin = "198.27.92.16/28"
        subnetSyd = "198.27.92.32/28"
        
        subnetPao = "198.27.92.48/28"
        subnetSjo = "198.27.92.64/28"
        subnetLax1 = "198.27.92.80/28"
    
        subnetChi1 = "198.27.92.96/28"
        subnetChi5 = "198.27.92.112/28"
        
        subnetBhs1 = "198.27.92.128/28"
        subnetBhs2 = "198.27.92.144/28"
        
        subnetAsh1 = "198.27.92.160/28"
        subnetAsh5 = "198.27.92.176/28"
        
        subnetNwk1 = "198.27.92.192/28"
        subnetNwk5 = "198.27.92.208/28"
        subnetNyc = "198.27.92.224/28"
        
        subnetLon_thw = "198.27.92.240/29"
        subnetLon_drch = "198.27.92.248/29"

        OVHSubsnets4 = [subnetSin, subnetSyd,subnetPao,subnetSjo,subnetLax1,subnetChi1,subnetChi5,subnetBhs1,subnetBhs2,subnetAsh1,subnetAsh5,subnetNwk1,subnetNwk5,subnetNyc,subnetLon_thw,subnetLon_drch]
        OVHSubsnets6 = [subnetSin6, subnetSyd6,subnetPao6,subnetSjo6,subnetLax16,subnetChi16,subnetChi56,subnetBhs16,subnetBhs26,subnetAsh16,subnetAsh56,subnetNwk16,subnetNwk56,subnetNyc6,subnetLon_thw6,subnetLon_drch6]

        # ====== Host configuration ========================================
        #  
        # ==================================================================
        hpao = self.addHost("hpao")
        self.addLink(hpao,pao)

        hsjo = self.addHost("hsjo")
        self.addLink(hsjo,sjo)  

        hlax1 = self.addHost("hlax1")
        self.addLink(hlax1,lax1)

        hchi1 = self.addHost("hchi1")
        self.addLink(hchi1,chi1)

        hchi5 = self.addHost("hchi5")
        self.addLink(hchi5,chi5)

        hbhs1 = self.addHost("hbhs1")
        self.addLink(hbhs1,bhs1)  

        hbhs2 = self.addHost("hbhs2")
        self.addLink(hbhs2,bhs2)  

        hash1 = self.addHost("hash1")
        self.addLink(hash1,ash1)

        hash5 = self.addHost("hash5")
        self.addLink(hash5,ash5)  

        hnwk1 = self.addHost("hnwk1")
        self.addLink(hnwk1,nwk1)

        hnwk5 = self.addHost("hnwk5")
        self.addLink(hnwk5,nwk5)  

        hnyc = self.addHost("hnyc")
        self.addLink(hnyc,nyc)
      

        hEU = self.addHost("hEU")
        self.addLink(hEU,lon_thw,igp_metric=1)

        hAPAC = self.addHost("hAPAC")
        self.addLink(hAPAC,sin,igp_metric=1)
        
        self.addSubnet(nodes = [sin,hAPAC], subnets = [subnetSin6, subnetSin])
        self.addSubnet(nodes = [syd], subnets = [subnetSyd6,subnetSyd])
    
        self.addSubnet(nodes = [pao,hpao], subnets = [subnetPao6,subnetPao])
        self.addSubnet(nodes = [sjo,hsjo], subnets = [subnetSjo6,subnetSjo])
        self.addSubnet(nodes = [lax1,hlax1], subnets = [subnetLax16,subnetLax1])
        
        self.addSubnet(nodes = [chi1,hchi1], subnets = [subnetChi16,subnetChi1])
        self.addSubnet(nodes = [chi5,hchi5], subnets = [subnetChi56,subnetChi5])
        
        self.addSubnet(nodes = [bhs1,hbhs1], subnets = [subnetBhs16,subnetBhs1])
        self.addSubnet(nodes = [bhs2,hbhs2], subnets = [subnetBhs26,subnetBhs2])
        
        self.addSubnet(nodes = [ash1,hash1], subnets = [subnetAsh16,subnetAsh1])
        self.addSubnet(nodes = [ash5,hash5], subnets = [subnetAsh56,subnetAsh5])

        self.addSubnet(nodes = [nwk1,hnwk1], subnets = [subnetNwk16,subnetNwk1])
        self.addSubnet(nodes = [nwk5,hnwk5], subnets = [subnetNwk56,subnetNwk5])
        self.addSubnet(nodes = [nyc,hnyc], subnets = [subnetNyc6,subnetNyc])
        
        self.addSubnet(nodes = [lon_thw,hEU], subnets = [subnetLon_thw6,subnetLon_thw])
        self.addSubnet(nodes = [lon_drch], subnets = [subnetLon_drch6,subnetLon_drch])
        
        
        # --- Physical links between routers ---
        self.addLink(sin, sjo,igp_metric=extra_large)
        self.addLink(syd,lax1,igp_metric=extra_large)

        self.addLink(syd,sin,igp_metric=large)
        self.addLink(syd,lon_thw,igp_metric=extra_large)
        self.addLink(syd,lon_drch,igp_metric=extra_large)
        self.addLink(sin,lon_thw,igp_metric=extra_large)
        self.addLink(sin,lon_drch,igp_metric=extra_large)
        self.addLink(lon_thw,lon_drch,igp_metric=small)

        self.addLink(pao,sjo,igp_metric=medium)
        self.addLink(sjo,lax1,igp_metric=medium)

        self.addLink(pao,chi1,igp_metric=medium)
        self.addLink(pao,chi5,igp_metric=medium)
        self.addLink(chi1,chi5,igp_metric=small)

        self.addLink(lax1,ash1,igp_metric=large)
        self.addLink(lax1,ash5,igp_metric=large)
        self.addLink(ash1,ash5,igp_metric=small)

        self.addLink(chi1,bhs1,igp_metric=medium)
        self.addLink(chi5,bhs2,igp_metric=medium)
        self.addLink(bhs1,bhs2,igp_metric=small)

        self.addLink(bhs1,nwk1,igp_metric=medium)
        self.addLink(bhs2,nwk5,igp_metric=medium)

        self.addLink(ash1,nwk1,igp_metric=large)
        self.addLink(ash5,nwk5,igp_metric=large)

        self.addLink(ash1,chi1,igp_metric=large)
        self.addLink(ash5,chi5,igp_metric=large)

        self.addLink(nwk1,nwk5,igp_metric=small)
        self.addLink(nwk1,nyc,igp_metric=small)
        self.addLink(nwk5,nyc,igp_metric=small)

        self.addLink(nwk1,lon_thw,igp_metric=extra_large)
        self.addLink(nwk5,lon_drch,igp_metric=extra_large)
        
        """
        self.addLink(anycast1,sin)
        self.addLink(anycast2,ash1);     
        self.addLink(anycast3,lon_thw)   

        """ 

        anycast1_link = self.addLink(anycast1,  sin)
        anycast1_link[anycast1].addParams(ip = ("fc00:0:27::2/48","192.168.39.2/24"))
        anycast1_link[sin].addParams(ip = ("fc00:0:27::1/48","192.168.39.1/24"))


        anycast2_link = self.addLink(anycast2,  ash1)
        anycast2_link[anycast2].addParams(ip = ("fc00:0:28::1/48","192.168.40.1/24"))
        anycast2_link[ash1].addParams(ip = ("fc00:0:28::2/48","192.168.40.2/24"))


        anycast3_link = self.addLink(anycast3,  lon_thw)
        anycast3_link[anycast3].addParams(ip = ("fc00:0:29::1/48","192.168.41.1/24"))
        anycast3_link[lon_thw].addParams(ip = ("fc00:0:29::2/48","192.168.41.2/24"))




        # --- Rules for inputTable --- 

        ip_rules = [InputFilter(default="DROP", rules=[
            Allow(iif='lo'),
            Allow(m='conntrack --ctstate RELATED,ESTABLISHED'),
            Deny(m='conntrack --ctstate INVALID'),
            Allow(p='icmp --icmp-type 0', m='conntrack --ctstate NEW'),
            Allow(p='icmp --icmp-type 3', m='conntrack --ctstate NEW'),
            Allow(p='icmp --icmp-type 8', m='conntrack --ctstate NEW'),
            Allow(p='icmp --icmp-type 9', m='conntrack --ctstate NEW'),
            Allow(p='icmp --icmp-type 10', m='conntrack --ctstate NEW'),
            Allow(p='icmp --icmp-type 11', m='conntrack --ctstate NEW'),
            Allow(src='1.3.1.0/24'),
            Allow(src='1.4.2.0/24'),
            Allow(src='1.5.3.0/24'),
            Allow(src='1.6.4.0/24'),
            Allow(src='198.27.92.0/24'),            
            ]),
            OutputFilter(default="ACCEPT", rules=[
            Deny(m='state --state INVALID'),
            ]),
            TransitFilter(default="ACCEPT", rules=[
            Deny(m='state --state INVALID'),
            ])]

        ip6_rules = [
            Rule('-A INPUT -i lo -j ACCEPT'),
            Rule('-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT'),
            Rule('-A INPUT -m conntrack --ctstate INVALID -j DROP'),
            Rule('-A INPUT -p icmpv6 --icmpv6-type 0 -m conntrack --ctstate NEW -j ACCEPT'),
            Rule('-A INPUT -p icmpv6 --icmpv6-type 3 -m conntrack --ctstate NEW -j ACCEPT'),
            Rule('-A INPUT -p icmpv6 --icmpv6-type 8 -m conntrack --ctstate NEW -j ACCEPT'),
            Rule('-A INPUT -p icmpv6 --icmpv6-type 9 -m conntrack --ctstate NEW -j ACCEPT'),
            Rule('-A INPUT -p icmpv6 --icmpv6-type 10 -m conntrack --ctstate NEW -j ACCEPT'),
            Rule('-A INPUT -p icmpv6 --icmpv6-type 11 -m conntrack --ctstate NEW -j ACCEPT'),
            Rule('-A INPUT -s c1a4:4ad:c0ff:ee::/64 -j ACCEPT'),
            Rule('-A INPUT -s c1a4:4ad:c0ff:ee::/64 -j ACCEPT'),
            Rule('-A INPUT -s cafe:d0d0:e5:dead::/64 -j ACCEPT'),
            Rule('-A INPUT -s aaaa:aaaa:aaaa:aaaa::/64 -j ACCEPT'),
            Rule('-A INPUT -s 2604:2dc0::/32 -j ACCEPT'),
            Rule('-P INPUT ACCEPT')]

        for r in OVHRouters: 
            r.addDaemon(IPTables, rules=ip_rules)
            r.addDaemon(IP6Tables, rules=ip6_rules) 

        # ========================= OSPF configuration ==================
        #
        # ===============================================================
        # --- Add a OSPF daemon on each router of OVH
        for r in OVHRouters: 
            if(r not in anycastServers):
                r.addDaemon(OSPF, KEYID=1, KEY="OVHKEY")
                r.addDaemon(OSPF6)      
        
        # ========================= BGP configuration ==================
        #   - 3 route reflectors at level 1 (highest in hierarchy)
        #   - 3 route reflectors at level 0 
        # ==============================================================
        # --- Add a BGP daemon on each router ---
        for i in range(len(OVHRouters)-len(anycastServers)):
            OVHRouters[i].addDaemon(BGP,debug = ("neighbor",),address_families=(AF_INET(networks=(OVHSubsnets4[i],)),AF_INET6(networks=(OVHSubsnets6[i],))), bgppassword="OVHpsswd")
        
        anycast1.addDaemon(BGP,RouterConfig,address_families = ( AF_INET6( networks=("2604:2dc0::0/128",) ), AF_INET( networks=("192.27.92.255/32",))));  
        anycast2.addDaemon(BGP,RouterConfig,address_families = ( AF_INET6( networks=("2604:2dc0::0/128",) ), AF_INET( networks=("192.27.92.255/32",))));  
        anycast3.addDaemon(BGP,RouterConfig,address_families = ( AF_INET6( networks=("2604:2dc0::0/128",) ), AF_INET( networks=("192.27.92.255/32",))));  

        bgp_anycast(self,sin,anycast1)
        bgp_anycast(self,ash1,anycast2)
        bgp_anycast(self,lon_thw,anycast3)


        # add bgp communities setup
        for r in NARouters:
            rm_setup(self,r,'NA')
        for r in EURouters:
            rm_setup(self,r,'EU')
        for r in APACRouters:
            rm_setup(self,r,'APAC')
                

        # --- Configure the router reflectors ---
        #       Lower hierarchy route reflectors
        
        # --- Configure the router reflectors ---
        set_rr(self, rr= bhs1, peers=[chi1,pao,nwk1,nyc])
        set_rr(self, rr= bhs2, peers=[nwk5,pao,sjo,chi1,chi5,lax1])
        set_rr(self, rr= ash5, peers=[nyc,chi5,nwk5,lax1,sjo,nwk1])

        bgp_peering(self, bhs1, bhs2)
        bgp_peering(self, bhs1, ash5)
        bgp_peering(self, bhs2, ash5)

        #       higher hierarchy route reflectors 
        set_rr(self, rr= ash1, peers=[bhs1,bhs2,ash5,anycast1])      # This one is a super RR
        set_rr(self, rr = lon_thw, peers=[lon_drch,anycast2])                           # This one is a super RR
        set_rr(self, rr = sin, peers=[syd,anycast3])                                    # This one is a super RR

        ibgp_Inter_Region(self, ash1, lon_thw)
        ibgp_Inter_Region(self, ash1, sin)
        ibgp_Inter_Region(self, sin, lon_thw)

        
        # ====== Router configurations of transit/stub providers ===========
        # - 1 stub provider : Google (ggl)
        # - 3 transit providers : 
        #       - Cogent (cgt)
        #       - Level3 (lvl3) 
        #       - Telia (tel) 
        # ==================================================================
        
        # --- Google (AS=2)  
        ggl = self.addRouter("ggl", config=RouterConfig)
        self.addLinks( (ggl,ash1), (ggl,ash5) )
        self.addAS(2,(ggl , ))
        
        lan_ggl = '1.3.1.0/24'
        lan_ggl_v6 = 'cafe:babe:dead:beaf::/64'            
        ggl.addDaemon(BGP, address_families=(AF_INET(networks=(lan_ggl,)),AF_INET6(networks=(lan_ggl_v6,))), bgppassword="OVHpsswd")
        
        h_ggl = self.addHost("h_ggl")
        self.addSubnet(nodes = [ggl, h_ggl], subnets=(lan_ggl,lan_ggl_v6))
        self.addLink(h_ggl,ggl,igp_metric=1)

        ebgp_Client(self,ash5,ggl,'NA')
        ebgp_Client(self,ash1,ggl,'NA')

        # --- Cogent (AS=3) 
        cgt = self.addRouter("cgt", config=RouterConfig) 
        self.addLinks( (cgt,nwk1), (cgt,nwk5), (cgt,ash1), (cgt,ash5), (cgt,chi1), (cgt,sjo) )
        self.addAS(3,(cgt , ))
        
        lan_cgt = '1.4.2.0/24'
        lan_cgt_v6 = 'c1a4:4ad:c0ff:ee::/64'
        cgt.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_cgt_v6,)),AF_INET(networks=(lan_cgt,)),), bgppassword="OVHpsswd")
        
        h_cgt = self.addHost("h_cgt")
        self.addSubnet(nodes = [cgt, h_cgt], subnets=(lan_cgt,lan_cgt_v6))
        self.addLink(h_cgt,cgt,igp_metric=1)

        ebgp_Peer(self,nwk1, cgt,'NA')
        ebgp_Peer(self,nwk5, cgt,'NA')
        ebgp_Peer(self,ash1, cgt,'NA')
        ebgp_Peer(self,ash5, cgt,'NA')
        ebgp_Peer(self,chi1, cgt,'NA')
        ebgp_Peer(self,sjo, cgt,'NA')

        # --- Level 3 (AS=4) 
        lvl3 = self.addRouter("lvl3", config=RouterConfig)
        self.addLinks( (lvl3,nwk1), (lvl3,nwk5), (lvl3,chi1), (lvl3,chi5), (lvl3,sjo) )
        self.addAS(4,(lvl3, ))
        
        lan_lvl3 = '1.5.3.0/24'
        lan_lvl3_v6 = 'cafe:d0d0:e5:dead::/64'
        lvl3.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_lvl3_v6,)),AF_INET(networks=(lan_lvl3,)),), bgppassword="OVHpsswd")

        h_lvl3 = self.addHost("h_lvl3")
        self.addSubnet(nodes = [lvl3, h_lvl3], subnets=(lan_lvl3,lan_lvl3_v6))
        self.addLink(h_lvl3,lvl3,igp_metric=1)

        ebgp_Peer(self,nwk1, lvl3,'NA')
        ebgp_Peer(self,nwk5, lvl3,'NA')
        ebgp_Peer(self,chi1, lvl3,'NA')
        ebgp_Peer(self,chi5, lvl3,'NA')
        ebgp_Peer(self,sjo, lvl3,'NA')
        
        # --- Telia (AS=5) 
        tel = self.addRouter("tel", config=RouterConfig)
        
        self.addLinks( (tel,nwk1), (tel,nwk5), (tel,ash5), (tel,chi5), (tel,pao) )
        self.addAS(5,(tel, ))
        
        lan_tel = '1.6.4.0/24'
        lan_tel_v6 = 'aaaa:aaaa:aaaa:aaaa::/64'        
        tel.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_tel_v6,)),AF_INET(networks=(lan_tel,)),), bgppassword="OVHpsswd")
        
        h_tel = self.addHost("h_tel")
        self.addSubnet(nodes = [tel, h_tel], subnets=(lan_tel,lan_tel_v6))
        self.addLink(h_tel,tel,igp_metric=1)

        ebgp_Peer(self,nwk1, tel,'NA')
        ebgp_Peer(self,nwk5, tel,'NA')
        ebgp_Peer(self,ash5, tel,'NA')
        ebgp_Peer(self,chi5, tel,'NA')
        ebgp_Peer(self,pao, tel,'NA')

        
        # ebgp_session(self, tel, nwk1, link_type=SHARE)
        # ebgp_session(self, tel, nwk5, link_type=SHARE)
        # ebgp_session(self, tel, ash5, link_type=SHARE)
        # ebgp_session(self, tel, chi5, link_type=SHARE)
        # ebgp_session(self, tel, pao, link_type=SHARE)
        
        
        externalRouters = [ggl, cgt, lvl3, tel]
        
        for eR in externalRouters:  
            eR.addDaemon(OSPF6)
            eR.addDaemon(OSPF)
        

        # --- Test for BGP communities ---
        
        # tel shouldn't be reached by hosts outside NA
        tel.get_config(BGP).set_community(community = '16276:31',to_peer= nwk1)
        tel.get_config(BGP).set_community(community = '16276:31',to_peer= nwk5)
        tel.get_config(BGP).set_community(community = '16276:31',to_peer= ash5)
        tel.get_config(BGP).set_community(community = '16276:31',to_peer= chi5)
        tel.get_config(BGP).set_community(community = '16276:31',to_peer= pao)

        # routes from ggl should be sent to other clients/peers with prepending
        ggl.get_config(BGP).set_community(community = '16276:9',to_peer= ash1)
        ggl.get_config(BGP).set_community(community = '16276:9',to_peer= ash5)

        # routes from cgt sent to other clients/peers should have the no-export community
        cgt.get_config(BGP).set_community(community= '16276:95',to_peer= nwk1)
        cgt.get_config(BGP).set_community(community= '16276:95',to_peer= nwk5)
        cgt.get_config(BGP).set_community(community= '16276:95',to_peer= ash1)
        cgt.get_config(BGP).set_community(community= '16276:95',to_peer= ash5)
        cgt.get_config(BGP).set_community(community= '16276:95',to_peer= chi1)
        cgt.get_config(BGP).set_community(community= '16276:95',to_peer= sjo)    

        # routes from lvl3 should be blackholed
        lvl3.get_config(BGP).set_community(community='blackhole',to_peer=nwk1)
        lvl3.get_config(BGP).set_community(community='blackhole',to_peer=nwk5)
        lvl3.get_config(BGP).set_community(community='blackhole',to_peer=chi1)
        lvl3.get_config(BGP).set_community(community='blackhole',to_peer=chi5)
        lvl3.get_config(BGP).set_community(community='blackhole',to_peer=sjo)
            


        super().build(*args, **kwargs)


def setFRRoutingCommands(net) :
    # Setup default route on anycast servers 

    net['anycast1'].cmd('route add -A inet6 default gw fc00:0:27::1')
    net['anycast1'].cmd('route add default gw 192.168.39.1')    

    net['anycast2'].cmd('route add -A inet6 default gw fc00:0:28::2')
    net['anycast2'].cmd('route add default gw 192.168.40.2')    
    
    net['anycast3'].cmd('route add -A inet6 default gw fc00:0:29::2')
    net['anycast3'].cmd('route add default gw 192.168.41.2')

        
# Press the green button to run the script.
if __name__ == '__main__':
    net = IPNet(topo=OVHTopology())
    try:
        net.start()
        setFRRoutingCommands(net)
        IPCLI(net)
    finally:
        net.stop()




