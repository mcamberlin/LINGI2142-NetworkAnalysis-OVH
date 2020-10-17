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
        lan_h1 = '192.168.1.0/24'
        lan_h2 = '192.168.2.0/24'

        lan_h1_v6 = 'cafe:babe:dead:beaf::/64'
        lan_h2_v6 = 'c1a4:4ad:c0ff:ee::/64'
        lan_h3_v6 = 'cafe:d0d0:e5:dead::/64'

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

        lon_thw = self.addRouter("lon-thw", config=RouterConfig);
        lon_drch = self.addRouter("lon-drch", config=RouterConfig);

        # --- Physical links between routers ---

        """ TO DO: Adjust metric according to the distance between cables (short, middle, long) """
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

        # --- Add a google router ---
        ggl = self.addRouter("ggl", config=RouterConfig);
        ggl2 = self.addRouter("ggl2", config=RouterConfig);
        self.addLink(ggl,ash1,igp_metric=1);
        self.addLink(ggl,ggl2,igp_metric=1);
        ggl.addDaemon(OSPF);
        ggl.addDaemon(OSPF6);
        ggl2.addDaemon(OSPF);
        ggl2.addDaemon(OSPF6);
        ggl.addDaemon(BGP, address_families=(AF_INET6(redistribute=['connected']),));
        ggl2.addDaemon(BGP, address_families=(AF_INET6(redistribute=['connected']),));
        self.addAS(2,(ggl,ggl2));
        ebgp_session(self, ggl, ash1, link_type=SHARE);

        # --- BGP configuration ---
        family = AF_INET6();

        sin.addDaemon(BGP, address_families=(family,));
        syd.addDaemon(BGP, address_families=(family,));
        pao.addDaemon(BGP, address_families=(family,));
        sjo.addDaemon(BGP, address_families=(family,));
        lax1.addDaemon(BGP, address_families=(family,));
        chi1.addDaemon(BGP, address_families=(family,));
        chi5.addDaemon(BGP, address_families=(family,));
        bhs1.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_h1_v6,),),));
        bhs2.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_h1_v6,),),));
        ash1.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_h1_v6,),),));
        ash5.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_h1_v6,),),));
        nwk1.addDaemon(BGP, address_families=(family,));
        nwk5.addDaemon(BGP, address_families=(family,));
        nyc.addDaemon(BGP, address_families=(family,));
        lon_thw.addDaemon(BGP, address_families=(family,));
        lon_drch.addDaemon(BGP, address_families=(family,));

        # --- Configure the router reflectors ---
        set_rr(self, rr= bhs1, peers=[chi1,pao,nwk1,nyc,bhs2,ash1,ash5,lon_thw,sin]);
        set_rr(self, rr= bhs2, peers=[pao,chi5,sjo,nwk5,bhs1,ash1,ash5,lon_thw,sin]);
        set_rr(self, rr= ash1, peers=[chi1,sjo,lax1,nwk1,bhs1,bhs2,ash5,ggl,lon_thw,sin]);
        set_rr(self, rr= ash5, peers=[chi5,lax1,nwk5,nyc,bhs1,bhs2,ash1,lon_thw,sin]);
        set_rr(self, rr = lon_thw, peers=[lon_drch,bhs1,bhs2,ash1,ash5,sin,lon_thw,sin]);
        set_rr(self, rr = sin, peers=[syd,bhs1,bhs2,ash1,ash5,lon_thw]);

        # --- Create Ases
        self.addAS(1, (sin,syd,pao,sjo,lax1,chi1,chi5,bhs1,bhs2,ash1,ash5,nwk1,nwk5,nyc,lon_thw,lon_drch))

        # --- Configure



        # --- Hosts ---
        h1 = self.addHost("h1");
        h2 = self.addHost("h2");
        h3 = self.addHost("h3");

        self.addSubnet((nyc, h1), subnets=(lan_h1,));
        self.addSubnet((ggl, h2), subnets=(lan_h2,));

        self.addSubnet((nyc, h1), subnets=(lan_h1_v6,));
        self.addSubnet((ggl, h2), subnets=(lan_h2_v6,));
        self.addSubnet((lax1, h3), subnets=(lan_h3_v6,));


        self.addLink(h1,nyc,igp_metric=1);
        self.addLink(h2,ggl,igp_metric=1);
        self.addLink(h3,lax1,igp_metric=1);




        super().build(*args, **kwargs)


# Press the green button to run the script.
if __name__ == '__main__':
    net = IPNet(topo=OVHTopology())
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()
