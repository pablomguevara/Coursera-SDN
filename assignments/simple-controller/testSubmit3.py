#!/usr/bin/python
'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment 2

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta, Muhammad Shahbaz
'''

from mininet.net import Mininet
from mininet.node import Controller
from mininet.topo import SingleSwitchTopo
from mininet.log import setLogLevel
from mininet.cli import CLI
import os

class POXBridge( Controller ):         
  "Custom Controller class to invoke POX"
                                   
  def start( self ):
    "Start POX learning switch"
    self.pox = '%s/pox/pox.py' % os.environ[ 'HOME' ]
    self.cmd( self.pox, 'forwarding.l2_learning misc.firewall &' )

  def stop( self ):
    "Stop POX"
    self.cmd( 'kill %' + self.pox )                      

outputString = ''

print "a. Firing up Mininet"

net = Mininet( topo=SingleSwitchTopo( 8 ), controller=POXBridge, autoSetMacs=True )

net.start()

h3 = net.get('h3')
h4 = net.get('h4')
h6 = net.get('h6')

print "b. Starting Test"

# Start pings
print "Ping from H3 to H6, should DROP"
outputString += h3.cmd('ping', '-c3', h6.IP())
print "Ping from H4 to H6, should FORWARD"
outputString += h4.cmd('ping', '-c3', h6.IP())

print outputString

print "Go to CLI for other checks"
CLI(net)

print "c. Stopping Mininet"
net.stop()


exit (0)
