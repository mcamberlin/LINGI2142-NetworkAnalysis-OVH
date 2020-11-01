#!/usr/bin/env python3
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP,OSPF, OSPF6, RouterConfig,AF_INET, AF_INET6, set_rr, ebgp_session, SHARE, CLIENT_PROVIDER, bgp_peering
from ipmininet.router.config.zebra import DENY, PERMIT, CommunityList, AccessList

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

        lan_OVH = '2604:2dc0::/32'

        lan_h1 = '1.1.0.0/24'
        lan_h1_v6 = '2604:2dc0::/48'
        #"2604:2dc0::3/34
        #"2604:2dc0::b/34"

        lan_h2 = '1.2.5.0/24'
        lan_h2_v6 = '2604:2dc0:0001::/48'

        lan_hEU = '1.1.6.0/24'
        lan_hEU_v6 = '2604:2dc0:8000::/48'

        lan_hAPAC = '1.1.7.0/24'
        lan_hAPAC_v6 = '2604:2dc0:4000::/48'
        
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
        #OVH routers = \48
        #r1 = self.addRouter('r1', lo_addresses=["2604:2dc0::1/64", "10.1.1.1/24"])
        sin = self.addRouter("sin", config=RouterConfig,lo_addresses=["2604:2dc0:4fff::0/48","198.27.92.0/24"] );
        syd = self.addRouter("syd", config=RouterConfig,lo_addresses=["2604:2dc0:4fff::1/48","198.27.92.1/24"]);

        pao = self.addRouter("pao", config=RouterConfig,lo_addresses=["2604:2dc0:0fff::0/48","198.27.92.2/24"]);
        sjo = self.addRouter("sjo", config=RouterConfig,lo_addresses=["2604:2dc0:0fff::1/48","198.27.92.3/24"]);
        lax1 = self.addRouter("lax1", config=RouterConfig,lo_addresses=["2604:2dc0:0fff::2/48","198.27.92.4/24"]);

        chi1 = self.addRouter("chi1", config=RouterConfig,lo_addresses=["2604:2dc0:0fff::3/48","198.27.92.5/24"]);
        chi5 = self.addRouter("chi5", config=RouterConfig,lo_addresses=["2604:2dc0:0fff::4/48","198.27.92.6/24"]);

        bhs1 = self.addRouter("bhs1", config=RouterConfig,lo_addresses=["2604:2dc0:0fff::5/48","198.27.92.7/24"]);
        bhs2 = self.addRouter("bhs2", config=RouterConfig,lo_addresses=["2604:2dc0:0fff::6/48","198.27.92.8/24"]);

        ash1 = self.addRouter("ash1", config=RouterConfig,lo_addresses=["2604:2dc0:0fff::7/48","198.27.92.9/24"]);
        ash5 = self.addRouter("ash5", config=RouterConfig,lo_addresses=["2604:2dc0:0fff::8/48","198.27.92.10/24"]);

        nwk1 = self.addRouter("nwk1", config=RouterConfig,lo_addresses=["2604:2dc0:0fff::9/48","198.27.92.11/24"]);
        nwk5 = self.addRouter("nwk5", config=RouterConfig,lo_addresses=["2604:2dc0:0fff::a/48","198.27.92.12/24"]);
        nyc = self.addRouter("nyc", config=RouterConfig,lo_addresses=["2604:2dc0:0fff::b/48","198.27.92.13/24"]);

        lon_thw = self.addRouter("lon_thw", config=RouterConfig,lo_addresses=["2604:2dc0:8fff::0/48","198.27.92.14/24"]);
        lon_drch = self.addRouter("lon_drch", config=RouterConfig,lo_addresses=["2604:2dc0:8fff::1/48","198.27.92.15/24"]);

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
        self.addLink(nwk1,nyc,igp_metric=small);
        self.addLink(nwk5,nyc,igp_metric=small);

        self.addLink(nwk1,lon_thw,igp_metric=extra_large);
        self.addLink(nwk5,lon_drch,igp_metric=extra_large);


        # --- OSPF and OSPF6 configuration as IGP ---

        sin.addDaemon(OSPF);
        syd.addDaemon(OSPF);
        pao.addDaemon(OSPF);
        sjo.addDaemon(OSPF);
        lax1.addDaemon(OSPF);
        chi1.addDaemon(OSPF);
        chi5.addDaemon(OSPF);
        bhs1.addDaemon(OSPF);
        bhs2.addDaemon(OSPF);
        ash1.addDaemon(OSPF);
        ash5.addDaemon(OSPF);
        nwk1.addDaemon(OSPF);
        nwk5.addDaemon(OSPF);
        nyc.addDaemon(OSPF);
        lon_thw.addDaemon(OSPF);
        lon_drch.addDaemon(OSPF);

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

        # --- Create Ases : AS=1 for OVH
        self.addAS(1, (sin,syd,pao,sjo,lax1,chi1,chi5,bhs1,bhs2,ash1,ash5,nwk1,nwk5,nyc,lon_thw,lon_drch))

        # --- Stub provider : google (AS2)  ---
        ggl = self.addRouter("ggl", config=RouterConfig);
        
        self.addLink(ggl,ash1,igp_metric=1);
        self.addLink(ggl,ash5,igp_metric=1);
        
        ggl.addDaemon(OSPF);
        ggl.addDaemon(OSPF6);
        ggl.addDaemon(BGP, address_families=(AF_INET(networks=(lan_ggl,)),AF_INET6(networks=(lan_ggl_v6,))) , routerid="1.1.1.1");
        
        self.addAS(2,(ggl , ));
        
        ebgp_session(self, ggl, ash1, link_type=SHARE,region=162761000);
        ebgp_session(self, ggl, ash5, link_type=SHARE,region=162761000);

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
        cgt.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_cgt_v6,)),AF_INET(networks=(lan_cgt,)),), routerid="1.1.1.2");
        
        self.addAS(3,(cgt , ));
        
        ebgp_session(self, cgt, nwk1, link_type=SHARE,region=162761000);
        ebgp_session(self, cgt, nwk5, link_type=SHARE,region=162761000);
        ebgp_session(self, cgt, ash1, link_type=SHARE,region=162761000);
        ebgp_session(self, cgt, ash5, link_type=SHARE,region=162761000);
        ebgp_session(self, cgt, chi1, link_type=SHARE,region=162761000);
        ebgp_session(self, cgt, sjo, link_type=SHARE,region=162761000);
        
        #Level 3 (AS=4) 
        lvl3 = self.addRouter("lvl3", config=RouterConfig);
        
        self.addLink(lvl3,nwk1,igp_metric=1);
        self.addLink(lvl3,nwk5,igp_metric=1);
        self.addLink(lvl3,chi1,igp_metric=1);
        self.addLink(lvl3,chi5,igp_metric=1);
        self.addLink(lvl3,sjo,igp_metric=1);
        
        lvl3.addDaemon(OSPF);
        lvl3.addDaemon(OSPF6);
        lvl3.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_lvl3_v6,)),AF_INET(networks=(lan_lvl3,)),), routerid="1.1.1.3");

        self.addAS(4,(lvl3, ));
        
        ebgp_session(self, lvl3, nwk1, link_type=SHARE,region=162761000);
        ebgp_session(self, lvl3, nwk5, link_type=SHARE,region=162761000);
        ebgp_session(self, lvl3, chi1, link_type=SHARE,region=162761000);
        ebgp_session(self, lvl3, chi5, link_type=SHARE,region=162761000);
        ebgp_session(self, lvl3, sjo, link_type=SHARE,region=162761000);
        
        # Telia (AS=5) 
        tel = self.addRouter("tel", config=RouterConfig);
        
        self.addLink(tel,nwk1,igp_metric=1);
        self.addLink(tel,nwk5,igp_metric=1);
        self.addLink(tel,ash5,igp_metric=1);
        self.addLink(tel,chi5,igp_metric=1);
        self.addLink(tel,pao,igp_metric=1);
        
        tel.addDaemon(OSPF);
        tel.addDaemon(OSPF6);
        tel.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_tel_v6,)),AF_INET(networks=(lan_tel,)),), routerid="1.1.1.4");
        
        # --- test filter for telnet --- 
        all_al = AccessList('All', ('any',))
        tel_EU = self.addRouter("telEU",config=RouterConfig);

        self.addLink(tel_EU,lon_thw,igp_metric=1);
        tel_EU.addDaemon(OSPF);
        tel_EU.addDaemon(OSPF6);
        tel_EU.addDaemon(BGP, address_families=(AF_INET6(networks=("eeee:eeee::/48",)),))
        #tel_EU.get_config(BGP).set_community(162763100,to_peer=lon_drch,matching=(all_al,));
        self.addAS(5,(tel,tel_EU ));
        
        ebgp_session(self, tel_EU,lon_thw,link_type=SHARE,region=162763000);

        ebgp_session(self, tel, nwk1, link_type=SHARE,region=162761000);
        ebgp_session(self, tel, nwk5, link_type=SHARE,region=162761000);
        ebgp_session(self, tel, ash5, link_type=SHARE,region=162761000);
        ebgp_session(self, tel, chi5, link_type=SHARE,region=162761000);
        ebgp_session(self, tel, pao, link_type=SHARE,region=162761000);
        

        # --- BGP configuration ---

        sin.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_hAPAC_v6,)),AF_INET(networks=(lan_hAPAC,))), routerid="1.1.1.5");
        syd.addDaemon(BGP);
        
        pao.addDaemon(BGP);
        sjo.addDaemon(BGP);
        
        lax1.addDaemon(BGP);
        
        chi1.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_h1_v6,)),AF_INET(networks=(lan_h1,))));
        chi5.addDaemon(BGP);
        
        bhs1.addDaemon(BGP, routerid="1.1.1.6")
        bhs2.addDaemon(BGP, routerid="1.1.1.7")
        
        ash1.addDaemon(BGP,routerid="1.1.1.8");
        ash5.addDaemon(BGP,routerid="1.1.1.9");
        
        nwk1.addDaemon(BGP);
        nwk5.addDaemon(BGP);
        
        nyc.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_h2_v6,)),AF_INET(networks=(lan_h2,))));
        
        lon_thw.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_hEU_v6,)),AF_INET(networks=(lan_hEU,))), routerid="1.1.1.10");
        lon_drch.addDaemon(BGP)

        # --- Configure the router reflectors ---
        set_rr(self, rr= bhs1, peers=[chi1,pao,nwk1,nyc]);
        set_rr(self, rr= bhs2, peers=[nwk5,pao,sjo,chi5,bhs1,ash1,ash5]);
        set_rr(self, rr= ash5, peers=[nyc,nwk5,lax1,bhs1,bhs2,ash1,chi5]);

        bgp_peering(self, bhs1, bhs2);
        bgp_peering(self, bhs1, ash5);
        bgp_peering(self, bhs2, ash5);


        set_rr(self, rr= ash1, peers=[nwk1,lax1,sjo,bhs1,bhs2,chi1,ash5]);      # This one is a super RR
        set_rr(self, rr = lon_thw, peers=[lon_drch]);                              # This one is a super RR
        set_rr(self, rr = sin, peers=[syd]);                                   # This one is a super RR

        bgp_peering(self, ash1, lon_thw)
        bgp_peering(self, ash1, sin)
        bgp_peering(self, sin, lon_thw)


        # --- Configure the BGP communities --- 
        NAonly = CommunityList(name='NAonly',community=162761100,action=PERMIT)
        EUonly = CommunityList(name='EUonly',community=162763100,action=PERMIT)
        APAConly = CommunityList(name='APAConly',community=162765100,action=PERMIT)

        sin.get_config(BGP).deny(from_peer = "sjo",matching = (EUonly,NAonly))
        sin.get_config(BGP).deny(from_peer = "lon_thw",matching = (EUonly,NAonly))
        sin.get_config(BGP).deny(from_peer = "lon_drch",matching = (EUonly,NAonly))

        syd.get_config(BGP).deny(from_peer = "lax1",matching = (EUonly,NAonly))
        syd.get_config(BGP).deny(from_peer = "lon_thw",matching = (EUonly,NAonly))
        syd.get_config(BGP).deny(from_peer = "lon_drch",matching = (EUonly,NAonly))

        sjo.get_config(BGP).deny(from_peer = "sin",matching = (EUonly,APAConly))
        lax1.get_config(BGP).deny(from_peer = "syd",matching = (EUonly,APAConly))

        lon_drch.get_config(BGP).deny(from_peer = "nwk1",matching = (APAConly,NAonly))
        lon_drch.get_config(BGP).deny(from_peer = "syd",matching = (APAConly,NAonly))
        lon_drch.get_config(BGP).deny(from_peer = "sin",matching = (APAConly,NAonly))

        lon_thw.get_config(BGP).deny(from_peer = "nwk5",matching = (APAConly,NAonly))
        lon_thw.get_config(BGP).deny(from_peer = "syd",matching = (APAConly,NAonly))
        lon_thw.get_config(BGP).deny(from_peer = "sin",matching = (APAConly,NAonly))

        nwk1.get_config(BGP).deny(from_peer = "lon_drch",matching = (EUonly,APAConly))
        nwk5.get_config(BGP).deny(from_peer = "lon_thw",matching = (EUonly,APAConly))

    
        # --- Hosts --- (one host for each provider considered)
        h1 = self.addHost("h1");
        self.addSubnet((chi1, h1), subnets=(lan_h1,));
        self.addSubnet((chi1, h1), subnets=(lan_h1_v6,));
        self.addLink(h1,chi1,igp_metric=1);

        h2 = self.addHost("h2");
        self.addSubnet((nyc, h2), subnets=(lan_h2,));
        self.addSubnet((nyc, h2), subnets=(lan_h2_v6,));
        self.addLink(h2,nyc,igp_metric=1);

        hEU = self.addHost("hEU");
        self.addSubnet((lon_thw, hEU), subnets=(lan_hEU,));
        self.addSubnet((lon_thw, hEU), subnets=(lan_hEU_v6,));
        self.addLink(hEU,lon_thw,igp_metric=1);

        hAPAC = self.addHost("hAPAC");
        self.addSubnet((sin, hAPAC), subnets=(lan_hAPAC,));
        self.addSubnet((sin, hAPAC), subnets=(lan_hAPAC_v6,));
        self.addLink(hAPAC,sin,igp_metric=1);
            
        h_ggl = self.addHost("h_ggl");
        self.addSubnet((ggl, h_ggl), subnets=(lan_ggl,));
        self.addSubnet((ggl, h_ggl), subnets=(lan_ggl_v6,));
        self.addLink(h_ggl,ggl,igp_metric=1);

        
        h_cgt = self.addHost("h_cgt");
        self.addSubnet((cgt, h_cgt), subnets=(lan_cgt,));
        self.addSubnet((cgt, h_cgt), subnets=(lan_cgt_v6,));
        self.addLink(h_cgt,cgt,igp_metric=1);

        
        h_lvl3 = self.addHost("h_lvl3");
        self.addSubnet((lvl3, h_lvl3), subnets=(lan_lvl3,));
        self.addSubnet((lvl3, h_lvl3), subnets=(lan_lvl3_v6,));
        self.addLink(h_lvl3,lvl3,igp_metric=1);
        
        
        h_tel = self.addHost("h_tel");
        self.addSubnet((tel, h_tel), subnets=(lan_tel,));
        self.addSubnet((tel, h_tel), subnets=(lan_tel_v6,));
        self.addLink(h_tel,tel,igp_metric=1);

        h_telEU = self.addHost("h_telEU");
        self.addSubnet((tel_EU,h_telEU), subnets=("eeee:eeee::/48",));
        self.addLink(h_telEU,tel_EU,igp_metric=1);

        super().build(*args, **kwargs)


# Press the green button to run the script.
if __name__ == '__main__':
    net = IPNet(topo=OVHTopology())
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()
