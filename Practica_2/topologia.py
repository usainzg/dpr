from mininet.topo import Topo
from mininet.node import OVSKernelSwitch
from mininet.node import Host
from mininet.util import irange

class DatacenterTopology(Topo):

    def build(self, fo=3):

        topSwitch = self.addSwitch('Ts', cls=OVSKernelSwitch, dpid='0000000100000099')
        for i in irange(1, fo):
            swAccess = self.buildSwitchToHosts(i, nHostsPerSwitch=fo)
            self.addLink(topSwitch, swAccess, port2=1)

    def buildSwitchToHosts(self, loc, nHostsPerSwitch):
        #dpid = ( loc * 16 ) + 1
        switch = self.addSwitch('s{}'.format(loc), cls=OVSKernelSwitch)
        
        for n in irange(1, nHostsPerSwitch):
            hostName = 'h_{}_{}'.format(loc, n)
            ipHost = '10.0.{}.{}/16'.format(loc, n)
            portHost = n+1
            host = self.addHost(hostName, cls=Host, ip=ipHost)
            self.addLink(switch, host, port1=portHost)
        
        return switch

topos = {
    'datacenter': DatacenterTopology
}