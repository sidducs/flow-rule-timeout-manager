# 22.Flow Rule Timeout Manager

## Problem Statement

This project implements timeout-based flow rule management using Software Defined Networking (SDN). The goal is to dynamically install and remove flow rules based on network activity.

---

## Objective

* Configure idle and hard timeouts
* Remove expired flow rules
* Demonstrate flow rule lifecycle
* Analyze network behavior

---

## Tools Used

* Mininet (Network Emulator)
* POX Controller (SDN Controller)
* Open vSwitch (OVS)
* OpenFlow Protocol

---

## Network Topology

* Single switch (s1)
* Two hosts (h1, h2)

---

## Setup and Execution

### Step 1: Run Controller

```
cd ~/pox
python3 pox.py openflow.of_01 forwarding.timeout_manager
```

### Step 2: Run Mininet

```
sudo mn --topo single,2 --controller=remote,ip=127.0.0.1,port=6633 --switch ovsk,protocols=OpenFlow10
```

---

## Functional Demonstration

### Test 1: Connectivity

pingall
<img width="535" height="178" alt="image" src="https://github.com/user-attachments/assets/2c04757a-4e03-4a8c-9a62-1d35f61bbca4" />



Result: 0% packet loss

---

### Test 2: Flow Table Observation


sh ovs-ofctl dump-flows s1
<img width="900" height="696" alt="image" src="https://github.com/user-attachments/assets/d2218594-d34a-4373-8de6-776fbfeec0ff" />



* Flow entries are created after traffic
* Each flow has:

  * idle_timeout = 10
  * hard_timeout = 30

---

### Test 3: Timeout Behavior

* Stop traffic
* Wait 10 seconds
* Check flow table again

  <img width="500" height="76" alt="image" src="https://github.com/user-attachments/assets/10a57974-570b-4bab-b173-b2da658f78a5" />

Result:

* Flow entries are removed automatically

---
### Controller Logs
<img width="892" height="782" alt="image" src="https://github.com/user-attachments/assets/b1070020-63ce-4818-82d3-16e7832d98b8" />

The controller handles PacketIn events and installs flow rules with timeout.


## Performance Analysis

### Latency

* First packet: higher delay (controller involved)
* Later packets: lower delay (flow rule exists)

### Throughput

```
h1 iperf -s &
h2 iperf -c h1
```

---

## Flow Rule Lifecycle

1. Packet arrives → PacketIn event
2. Controller installs flow rule
3. Traffic flows through switch
4. No traffic → idle timeout triggers
5. Flow rule removed

---

## Proof of Execution

### Screenshots Included:

* Ping results (0% loss)
* Flow table before timeout
* Flow table after timeout
* Controller logs showing flow installation

---

## Conclusion

Flow rules are dynamically managed using timeouts, improving network efficiency by removing inactive entries.

---

## References

* Mininet Documentation: https://mininet.org/
* POX Controller GitHub: https://github.com/noxrepo/pox
* OpenFlow Specification: https://opennetworking.org/
