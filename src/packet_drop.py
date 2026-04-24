# Import required Ryu modules
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3


# Main SDN application class
class PacketDrop(app_manager.RyuApp):
    
    # Specify OpenFlow version (1.3)
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    # Constructor
    def __init__(self, *args, **kwargs):
        super(PacketDrop, self).__init__(*args, **kwargs)

    # This function runs when switch connects to controller
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        
        # Get switch (datapath) object
        datapath = ev.msg.datapath
        
        # OpenFlow protocol reference
        ofproto = datapath.ofproto
        
        # Parser to create match/actions
        parser = datapath.ofproto_parser

        # Match all packets (no specific condition)
        match = parser.OFPMatch()
        
        # No actions → means DROP packets
        actions = []

        # Apply instructions (drop in this case)
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]

        # Create flow rule with lowest priority
        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=0,
            match=match,
            instructions=inst
        )

        # Send rule to switch
        datapath.send_msg(mod)
