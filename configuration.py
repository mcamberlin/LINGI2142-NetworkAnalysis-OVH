#!/usr/bin/env python3
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP,OSPF, OSPF6, RouterConfig, AF_INET6, set_rr, ebgp_session, SHARE, CLIENT_PROVIDER

class OVHTopology(IPTopo):

    def build(self, *args, **kwargs):
        # --- Metrics ---
        small = 1
        medium = 3
        large = 8
        extra_large = 13

        # --- Hosts ---

        family = AF_INET6();

        lan_h1 = '192.168.0.0/24'
        lan_h1_v6 = 'aaaa:aaaa:0000:0000::/64'

        lan_h2 = '192.168.5.0/24'
        lan_h2_v6 = 'aaaa:aaaa:aaaa:0000::/64'
        
        lan_ggl = '192.168.1.0/24'
        lan_ggl_v6 = 'cafe:babe:dead:beaf::/64'

        lan_cgt = '192.168.2.0/24'
        lan_cgt_v6 = 'c1a4:4ad:c0ff:ee::/64'

        lan_lvl = '192.168.3.0/24'
        lan_lvl_v6 = 'cafe:d0d0:e5:dead::/64'

        lan_tel = '192.168.4.0/24'
        lan_tel_v6 = 'aaaa:aaaa:aaaa:aaaa::/64'
        
        # --- Routers ---
        sin = self.addRouter("sin", config=RouterConfig);
        syd = self.addRouter("syd", config=RouterConfig);

        pao = self.addRouter("pao", config=RouterConfig);
        sjo = self.addRouter("sjo", config=RouterConfig);
        lax1 = self.addRouter("lax1", config=RouterConfig);

        chi1 = self.addRouter("chi1", config=RouterConfig);
        chi5 = self.addRouter("chi5", config=RouterConfig);

        bhs1 = self.addRouter("bhs1", config=RouterConfig);
        bhs2 = self.addRouter("bhs2", config=RouterConfig);

        ash1 = self.addRouter("ash1", config=RouterConfig);
        ash5 = self.addRouter("ash5", config=RouterConfig);

        nwk1 = self.addRouter("nwk1", config=RouterConfig);
        nwk5 = self.addRouter("nwk5", config=RouterConfig);
        nyc = self.addRouter("nyc", config=RouterConfig);

        lon_thw = self.addRouter("lon_thw", config=RouterConfig);
        lon_drch = self.addRouter("lon_drch", config=RouterConfig);

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

        # --- Stub provider : google (AS2)  ---
        ggl = self.addRouter("ggl", config=RouterConfig);
        
        self.addLink(ggl,ash1,igp_metric=1);
        
        ggl.addDaemon(OSPF);
        ggl.addDaemon(OSPF6);
        
        
        ggl.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_ggl_v6,),),));
        
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
        
        cgt.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_cgt_v6,),),));
        
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
        
        lvl3.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_lvl_v6,),),));

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
        
        tel.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_tel_v6,),),));
        
        self.addAS(5,(tel, ));
        
        ebgp_session(self, tel, nwk1, link_type=SHARE);
        ebgp_session(self, tel, nwk5, link_type=SHARE);
        ebgp_session(self, tel, ash5, link_type=SHARE);
        ebgp_session(self, tel, chi5, link_type=SHARE);
        ebgp_session(self, tel, pao, link_type=SHARE);
        

        # --- BGP configuration ---

        sin.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_h1_v6,lan_h2_v6),),));
        syd.addDaemon(BGP);
        
        pao.addDaemon(BGP);
        sjo.addDaemon(BGP);
        
        lax1.addDaemon(BGP);
        
        chi1.addDaemon(BGP);
        chi5.addDaemon(BGP);
        
        bhs1.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_h1_v6,lan_h2_v6),),))
        bhs2.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_h1_v6,lan_h2_v6),),))
        
        ash1.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_h1_v6,lan_h2_v6),),));
        ash5.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_h1_v6,lan_h2_v6),),));
        
        nwk1.addDaemon(BGP);
        nwk5.addDaemon(BGP);
        
        nyc.addDaemon(BGP);
        
        lon_thw.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_h1_v6,lan_h2_v6),),))
        lon_drch.addDaemon(BGP)

        # --- Configure the router reflectors ---
        set_rr(self, rr= bhs1, peers=[chi1,pao,nwk1,nyc,bhs2,ash5]);       
        set_rr(self, rr= bhs2, peers=[nwk5,pao,sjo,chi5,bhs1,ash5]);
        set_rr(self, rr= ash1, peers=[nwk1,lax1,sjo,bhs1,bhs2,chi1,ash5,lon_thw,sin]);      # This one is a super RR
        set_rr(self, rr= ash5, peers=[nyc,nwk5,lax1,bhs1,bhs2,chi5]);

        set_rr(self, rr = lon_thw, peers=[lon_drch,sin,ash1]);                              # This one is a super RR
        set_rr(self, rr = sin, peers=[syd,ash1,lon_thw]);                                   # This one is a super RR

        # --- Create Ases : AS=1 for OVH
        #self.addAS(1, (nyc,sjo,pao,lax1,chi1,chi5,bhs1,bhs2,ash1,ash5,nwk1,nwk5)) 
        self.addAS(1, (sin,syd,pao,sjo,lax1,chi1,chi5,bhs1,bhs2,ash1,ash5,nwk1,nwk5,nyc,lon_thw,lon_drch))



        # --- Hosts --- (one host for each provider considered)
        h1 = self.addHost("h1");
        self.addSubnet((chi1, h1), subnets=(lan_h1,));
        self.addSubnet((chi1, h1), subnets=(lan_h1_v6,));
        self.addLink(h1,chi1,igp_metric=1);

        h2 = self.addHost("h2");
        self.addSubnet((nyc, h2), subnets=(lan_h2,));
        self.addSubnet((nyc, h2), subnets=(lan_h2_v6,));
        self.addLink(h2,nyc,igp_metric=1);
            
        h_ggl = self.addHost("h_ggl");
        self.addSubnet((ggl, h_ggl), subnets=(lan_ggl,));
        self.addSubnet((ggl, h_ggl), subnets=(lan_ggl_v6,));
        self.addLink(h_ggl,ggl,igp_metric=1);

        
        h_cgt = self.addHost("h_cgt");
        self.addSubnet((cgt, h_cgt), subnets=(lan_cgt,));
        self.addSubnet((cgt, h_cgt), subnets=(lan_cgt_v6,));
        self.addLink(h_cgt,cgt,igp_metric=1);

        
        h_lvl = self.addHost("h_lvl");
        self.addSubnet((lvl, h_lvl), subnets=(lan_lvl,));
        self.addSubnet((lvl, h_lvl), subnets=(lan_lvl_v6,));
        self.addLink(h_lvl,lvl,igp_metric=1);
        
        
        h_tel = self.addHost("h_tel");
        self.addSubnet((tel, h_tel), subnets=(lan_tel,));
        self.addSubnet((tel, h_tel), subnets=(lan_tel_v6,));
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
