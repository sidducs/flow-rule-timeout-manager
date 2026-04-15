from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class TimeoutManager(object):
    def __init__(self, connection):
        self.connection = connection
        self.mac_to_port = {}

        connection.addListeners(self)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        in_port = event.port

        if not packet.parsed:
            return

        src = packet.src
        dst = packet.dst

        log.info(f"Packet: {src} -> {dst} (port {in_port})")

        # Learn MAC address
        self.mac_to_port[src] = in_port

        # Decide output port
        if dst in self.mac_to_port:
            out_port = self.mac_to_port[dst]
        else:
            out_port = of.OFPP_FLOOD

        # 🔥 Install flow rule
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet, in_port)

        msg.actions.append(of.ofp_action_output(port=out_port))

        # 🔥 TIMEOUT LOGIC (MAIN PROJECT)
        msg.idle_timeout = 10   # remove if no traffic for 10 sec
        msg.hard_timeout = 30   # remove after 30 sec

        self.connection.send(msg)

        # 🔥 Send current packet
        out = of.ofp_packet_out()
        out.data = event.ofp
        out.actions.append(of.ofp_action_output(port=out_port))
        self.connection.send(out)

        log.info("Flow installed with timeout")


def launch():
    def start_switch(event):
        log.info("Switch connected")
        TimeoutManager(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)
