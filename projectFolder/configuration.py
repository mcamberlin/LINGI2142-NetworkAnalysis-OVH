#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
Created on Wed Oct 14 14:34:13 2020
@authors: Merlin & Aurélien
"""
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, OSPF,OSPF6, RouterConfig, AF_INET6, set_rr, ebgp_session, SHARE

class OVHTopology(IPTopo):

    def build(self, *args, **kwargs):

        # --- Routers --- 
        """ 
        By default, OSPF and OSPF6 are launched on each router. This means that your network has basic routing working by default. 
        To change that, we have to modify the router configuration class.
        """ 
        
        sin = self.addRouter("sin", config= RouterConfig);
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
        
        # adding OSPF6 as IGP

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
        
        
        # --- Physical links between routers ---
        self.addLink(sin, sjo,igp_metric=1);
        self.addLink(syd,lax1,igp_metric=1);
        
        self.addLink(pao,sjo,igp_metric=1);
        self.addLink(sjo,lax1,igp_metric=1);
        
        self.addLink(pao,chi1,igp_metric=1);
        self.addLink(pao,chi5,igp_metric=1);
        self.addLink(chi1,chi5,igp_metric=1);
        
        self.addLink(lax1,ash1,igp_metric=1);
        self.addLink(lax1,ash5,igp_metric=1);
        self.addLink(ash1,ash5,igp_metric=1);
        
        self.addLink(chi1,bhs1,igp_metric=1);
        self.addLink(chi5,bhs2,igp_metric=1);
        self.addLink(bhs1,bhs2,igp_metric=1);
        
        self.addLink(bhs1,nwk1,igp_metric=1);
        self.addLink(bhs2,nwk5,igp_metric=1);
        
        self.addLink(ash1,nwk1,igp_metric=1);
        self.addLink(ash5,nwk5,igp_metric=1);
        
        self.addLink(nwk1,nwk5,igp_metric=1);
        self.addLink(nwk1,nyc,igp_metric=1);
        self.addLink(nwk5,nyc,igp_metric=1);
        
        self.addLink(nwk1,lon_thw,igp_metric=1);
        self.addLink(nwk5,lon_drch,igp_metric=1);
        
        # --- Hosts ---
        h1 = self.addHost("h1");
        h2 = self.addHost("h2");
        
        
        lan_h1 = '192.168.1.0/24'
        lan_h2 = '192.168.2.0/24'
        
        lan_h1_v6 = 'cafe:babe:dead:beaf::/64'
        lan_h2_v6 = 'c1a4:4ad:c0ff:ee::/64'
        
        self.addSubnet((lon_drch, h1), subnets=(lan_h1,))
        self.addSubnet((sin, h2), subnets=(lan_h2,))
        
        self.addSubnet((lon_drch, h1), subnets=(lan_h1_v6,))
        self.addSubnet((sin, h2), subnets=(lan_h2_v6,))
        
        
        self.addLink(h1,lon_drch,igp_metric=1);
        self.addLink(h2,sin,igp_metric=1);
        
        
        
        super().build(*args, **kwargs)
        
        
# Press the green button to run the script.
if __name__ == '__main__':
    net = IPNet(topo=OVHTopology())
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()
        