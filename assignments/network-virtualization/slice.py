'''
Coursera:
- Software Defined Networking (SDN) course
-- Network Virtualization

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
from collections import defaultdict

import pox.openflow.libopenflow_01 as of
import pox.openflow.discovery
import pox.openflow.spanning_tree

from pox.lib.revent import *
from pox.lib.util import dpid_to_str
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
from collections import namedtuple
import os

log = core.getLogger()


class VideoSlice (EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        core.openflow_discovery.addListeners(self)

        # Adjacency map.  [sw1][sw2] -> port from sw1 to sw2
        self.adjacency = defaultdict(lambda:defaultdict(lambda:None))

        self.portmap = { 
                        ('00-00-00-00-00-01', EthAddr('00:00:00:00:00:01'),
                         EthAddr('00:00:00:00:00:03'), 80): '00-00-00-00-00-03',
                        ('00-00-00-00-00-01', EthAddr('00:00:00:00:00:01'),
                         EthAddr('00:00:00:00:00:04'), 80): '00-00-00-00-00-03',
                        ('00-00-00-00-00-01', EthAddr('00:00:00:00:00:02'),
                         EthAddr('00:00:00:00:00:03'), 80): '00-00-00-00-00-03',
                        ('00-00-00-00-00-01', EthAddr('00:00:00:00:00:02'),
                         EthAddr('00:00:00:00:00:04'), 80): '00-00-00-00-00-03',
                        ('00-00-00-00-00-04', EthAddr('00:00:00:00:00:03'),
                         EthAddr('00:00:00:00:00:01'), 80): '00-00-00-00-00-03',
                        ('00-00-00-00-00-04', EthAddr('00:00:00:00:00:03'),
                         EthAddr('00:00:00:00:00:02'), 80): '00-00-00-00-00-03',
                        ('00-00-00-00-00-04', EthAddr('00:00:00:00:00:04'),
                         EthAddr('00:00:00:00:00:01'), 80): '00-00-00-00-00-03',
                        ('00-00-00-00-00-04', EthAddr('00:00:00:00:00:04'),
                         EthAddr('00:00:00:00:00:02'), 80): '00-00-00-00-00-03',
                        
                        ('00-00-00-00-00-01', EthAddr('00:00:00:00:00:01'),
                         EthAddr('00:00:00:00:00:03'), '*'): '00-00-00-00-00-02',
                        ('00-00-00-00-00-01', EthAddr('00:00:00:00:00:01'),
                         EthAddr('00:00:00:00:00:04'), '*'): '00-00-00-00-00-02',
                        ('00-00-00-00-00-01', EthAddr('00:00:00:00:00:02'),
                         EthAddr('00:00:00:00:00:03'), '*'): '00-00-00-00-00-02',
                        ('00-00-00-00-00-01', EthAddr('00:00:00:00:00:02'),
                         EthAddr('00:00:00:00:00:04'), '*'): '00-00-00-00-00-02',
                        ('00-00-00-00-00-04', EthAddr('00:00:00:00:00:03'),
                         EthAddr('00:00:00:00:00:01'), '*'): '00-00-00-00-00-02',
                        ('00-00-00-00-00-04', EthAddr('00:00:00:00:00:03'),
                         EthAddr('00:00:00:00:00:02'), '*'): '00-00-00-00-00-02',
                        ('00-00-00-00-00-04', EthAddr('00:00:00:00:00:04'),
                         EthAddr('00:00:00:00:00:01'), '*'): '00-00-00-00-00-02',
                        ('00-00-00-00-00-04', EthAddr('00:00:00:00:00:04'),
                         EthAddr('00:00:00:00:00:02'), '*'): '00-00-00-00-00-02',

                        ('00-00-00-00-00-02', EthAddr('00:00:00:00:00:01'),
                         EthAddr('00:00:00:00:00:03'), '*'): '00-00-00-00-00-04',
                        ('00-00-00-00-00-02', EthAddr('00:00:00:00:00:01'),
                         EthAddr('00:00:00:00:00:04'), '*'): '00-00-00-00-00-04',
                        ('00-00-00-00-00-02', EthAddr('00:00:00:00:00:02'),
                         EthAddr('00:00:00:00:00:03'), '*'): '00-00-00-00-00-04',
                        ('00-00-00-00-00-02', EthAddr('00:00:00:00:00:02'),
                         EthAddr('00:00:00:00:00:04'), '*'): '00-00-00-00-00-04',
                        ('00-00-00-00-00-02', EthAddr('00:00:00:00:00:03'),
                         EthAddr('00:00:00:00:00:01'), '*'): '00-00-00-00-00-01',
                        ('00-00-00-00-00-02', EthAddr('00:00:00:00:00:03'),
                         EthAddr('00:00:00:00:00:02'), '*'): '00-00-00-00-00-01',
                        ('00-00-00-00-00-02', EthAddr('00:00:00:00:00:04'),
                         EthAddr('00:00:00:00:00:01'), '*'): '00-00-00-00-00-01',
                        ('00-00-00-00-00-02', EthAddr('00:00:00:00:00:04'),
                         EthAddr('00:00:00:00:00:02'), '*'): '00-00-00-00-00-01',

                        ('00-00-00-00-00-03', EthAddr('00:00:00:00:00:01'),
                         EthAddr('00:00:00:00:00:03'), '*'): '00-00-00-00-00-04',
                        ('00-00-00-00-00-03', EthAddr('00:00:00:00:00:01'),
                         EthAddr('00:00:00:00:00:04'), '*'): '00-00-00-00-00-04',
                        ('00-00-00-00-00-03', EthAddr('00:00:00:00:00:02'),
                         EthAddr('00:00:00:00:00:03'), '*'): '00-00-00-00-00-04',
                        ('00-00-00-00-00-03', EthAddr('00:00:00:00:00:02'),
                         EthAddr('00:00:00:00:00:04'), '*'): '00-00-00-00-00-04',
                        ('00-00-00-00-00-03', EthAddr('00:00:00:00:00:03'),
                         EthAddr('00:00:00:00:00:01'), '*'): '00-00-00-00-00-01',
                        ('00-00-00-00-00-03', EthAddr('00:00:00:00:00:03'),
                         EthAddr('00:00:00:00:00:02'), '*'): '00-00-00-00-00-01',
                        ('00-00-00-00-00-03', EthAddr('00:00:00:00:00:04'),
                         EthAddr('00:00:00:00:00:01'), '*'): '00-00-00-00-00-01',
                        ('00-00-00-00-00-03', EthAddr('00:00:00:00:00:04'),
                         EthAddr('00:00:00:00:00:02'), '*'): '00-00-00-00-00-01'

                        }

    def _handle_LinkEvent (self, event):
        l = event.link
        sw1 = dpid_to_str(l.dpid1)
        sw2 = dpid_to_str(l.dpid2)

        log.debug ("link %s[%d] <-> %s[%d]",
                   sw1, l.port1,
                   sw2, l.port2)

        self.adjacency[sw1][sw2] = l.port1
        self.adjacency[sw2][sw1] = l.port2


    def _handle_PacketIn (self, event):
        """
        Handle packet in messages from the switch to implement above algorithm.
        """
        packet = event.parsed
        tcpp = event.parsed.find('tcp')

        def install_fwdrule(event,packet,outport):
            msg = of.ofp_flow_mod()
            msg.idle_timeout = 10
            msg.hard_timeout = 30
            msg.match = of.ofp_match.from_packet(packet, event.port)
            msg.actions.append(of.ofp_action_output(port = outport))
            msg.data = event.ofp
            msg.in_port = event.port
            event.connection.send(msg)

        def forward (message = None):
            this_dpid = dpid_to_str(event.dpid)

            if packet.dst.is_multicast:
                flood()
                return
            else:
                log.debug("Got unicast packet for %s at %s (input port %d):",
                          packet.dst, dpid_to_str(event.dpid), event.port)

                try:
                    outport = 0

                    ports = [tcpp.dstport,tcpp.srcport,'*']
                    for port in ports:
                        if (this_dpid, packet.src,
                            packet.dst, port) in self.portmap.keys():
                            next_dpid = self.portmap[(this_dpid,
                                                      packet.src,
                                                      packet.dst,
                                                      port)]
                            outport = self.adjacency[this_dpid][next_dpid]
                            break

                    if outport > 0:
                        log.debug("output port is: %d", outport)
                        install_fwdrule(event,packet,outport)
                    else:
                        log.debug("unknown output port for (%s:%d -> %s:%d) at %s, flooding",
                                  packet.src, tcpp.srcport,
                                  packet.dst, tcpp.dstport, this_dpid)
                        # flood and install the flow table entry for the flood
                        install_fwdrule(event,packet,of.OFPP_FLOOD)

                except AttributeError:
                    log.debug("packet type has no transport ports, flooding")

                    # flood and install the flow table entry for the flood
                    install_fwdrule(event,packet,of.OFPP_FLOOD)

        # flood, but don't install the rule
        def flood (message = None):
            """ Floods the packet """
            msg = of.ofp_packet_out()
            msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
            msg.data = event.ofp
            msg.in_port = event.port
            event.connection.send(msg)

        forward()


    def _handle_ConnectionUp(self, event):
        dpid = dpidToStr(event.dpid)
        log.debug("Switch %s has come up.", dpid)



class TopologySlice (EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Slicing Module")
        # Mapping between dstmac addresses and inport for drop rules.
        self.portmap = { 
                        '00-00-00-00-00-01':[(EthAddr('00:00:00:00:00:01'),
                                              EthAddr('00:00:00:00:00:02')),
                                             (EthAddr('00:00:00:00:00:01'),
                                              EthAddr('00:00:00:00:00:04')),
                                             (EthAddr('00:00:00:00:00:02'),
                                              EthAddr('00:00:00:00:00:03'))],
                        '00-00-00-00-00-04':[(EthAddr('00:00:00:00:00:03'),
                                              EthAddr('00:00:00:00:00:04')),
                                             (EthAddr('00:00:00:00:00:03'),
                                              EthAddr('00:00:00:00:00:02')),
                                             (EthAddr('00:00:00:00:00:04'),
                                              EthAddr('00:00:00:00:00:01'))]
                        
                        }
    """This event will be raised each time a switch will connect to the controller"""
    def _handle_ConnectionUp(self, event):
        
        # Use dpid to differentiate between switches (datapath-id)
        # Each switch has its own flow table. As we'll see in this 
        # example we need to write different rules in different tables.
        dpid = dpidToStr(event.dpid)
        log.debug("Switch %s has come up.", dpid)
        
        if dpid in self.portmap:
            # Writing drop rules at edge switches itself should suffice.
            # It's always better to keep the complexity at edge of the network. (recall NVP)
            log.debug("Writing drop rules for switch %s.", dpid)
            for (srcmac, dstmac) in self.portmap[dpid]:
                msg = of.ofp_flow_mod()
                msg.priority = 200
                # We need to drop packets coming from <inport> and destined for <dstmac>
                msg.match.dl_src = srcmac
                msg.match.dl_dst = dstmac
                event.connection.send(msg)
                # No forwarding action implies drop action
                
        # Write flood rules for rest of the traffic
        log.debug("Writing flood rules for %s.", dpid)
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
        event.connection.send(msg)

        log.debug("Slicing rules installed on %s", dpid)
        

def launch():
    # Run spanning tree so that we can deal with topologies with loops
    pox.openflow.discovery.launch()
    pox.openflow.spanning_tree.launch()

    '''
    Starting the Overlay module
    '''
    core.registerNew(TopologySlice)
    #core.registerNew(VideoSlice)
