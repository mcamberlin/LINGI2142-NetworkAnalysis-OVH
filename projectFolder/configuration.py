#!/usr/bin/env python3
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, OSPF6, RouterConfig, AF_INET6, set_rr, ebgp_session, SHARE, CLIENT_PROVIDER

class OVHTopology(IPTopo):

    def build(self, *args, **kwargs):

        # --- Routers ---
        """
        By default, OSPF and OSPF6 are launched on each router. This means that your network has basic routing working by default.
        To change that, we have to modify the router configuration class.
        """

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

        # adding OSPF6 as IGP

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


        # h1 = self.addHost("h1")
        # h2 = self.addHost("h2")

        super().build(*args, **kwargs)


# Press the green button to run the script.
if __name__ == '__main__':
    net = IPNet(topo=OVHTopology())
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()
