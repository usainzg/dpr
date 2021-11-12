#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, failMode='standalone')
    r4 = net.addHost('r4', cls=Node, ip='0.0.0.0')
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')


    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.1.100/24', defaultRoute='via 10.0.1.1')
    h2 = net.addHost('h2', cls=Host, ip='10.0.1.101/24', defaultRoute='via 10.0.1.1')
    h3 = net.addHost('h3', cls=Host, ip='10.0.2.100/24', defaultRoute='via 10.0.2.1')
    h4 = net.addHost('h4', cls=Host, ip='10.0.2.101/24', defaultRoute='via 10.0.2.1')
    h5 = net.addHost('h5', cls=Host, ip='10.0.3.100/24', defaultRoute='via 10.0.3.1')
    h6 = net.addHost('h6', cls=Host, ip='10.0.3.101/24', defaultRoute='via 10.0.3.1')
    

    info( '*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s2)
    net.addLink(h4, s2)
    net.addLink(h5, s3)
    net.addLink(h6, s3)
    net.addLink(s1, r4)
    net.addLink(s2, r4)
    net.addLink(s3, r4)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s2').start([])
    net.get('s3').start([])
    net.get('s1').start([])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

