from mininet.topo import Topo
from mininet.node import OVSKernelSwitch
from mininet.node import Host
from mininet.util import irange

class DatacenterTopology(Topo):

    def build(self, fo=3):
        # Comprobamos si fo cumple los valores permitidos
        if fo < 1 or fo > 254:
            print("[ERROR] => Introduce un valor de fo valido!")
            return
        
        # Anadimos el switch cabecera con nombre y dpid adecuado
        topSwitch = self.addSwitch('Ts', cls=OVSKernelSwitch, dpid='0000000100000099')
        
        # Creamos fo switches de acceso con fo hosts conectados a ellos.
        # Conectamos los switches de acceso al switch cabecera.
        for i in irange(1, fo):
            swAccess = self.buildSwitchToHosts(i, nHostsPerSwitch=fo)
            self.addLink(topSwitch, swAccess, port2=1)

    # Funcion que crea el switch s{n} y sus fo hosts conectados a el.
    def buildSwitchToHosts(self, dpid, nHostsPerSwitch):
        switch = self.addSwitch('s{}'.format(dpid), cls=OVSKernelSwitch)
        
        for n in irange(1, nHostsPerSwitch):
            hostName = 'h_{}_{}'.format(dpid, n)
            ipHost = '10.0.{}.{}/16'.format(dpid, n)
            portHost = n+1
            host = self.addHost(hostName, cls=Host, ip=ipHost)
            self.addLink(switch, host, port1=portHost)
        
        return switch

topos = {
    'datacenter': DatacenterTopology
}