# Network Packet Analyzer & DDoS Log Generator

This project provides two core tools:

1. **Packet Analyzer**: A log parser that reads packet logs, extracts network traffic data, and detects DDoS attack patterns using heuristics.
2. **Log Generator**: A synthetic network traffic simulator that creates DDoS and legitimate traffic logs for testing and analysis.

---

## Features

### Packet Analyzer

* Parses classic `tcpdump`-style logs (text format)
* Detects DDoS threats based on traffic volume
* Supports TCP and UDP protocols
* Shows protocol usage and top source IPs
* Designed with object-oriented programming (OOP)

### DDoS Log Generator

* Generates:

  * SYN Flood
  * UDP Flood
  * Volumetric attacks
  * Coordinated (multi-source) DDoS attacks
  * Background legitimate traffic
* Produces both `.csv` and `.txt` logs
* Supports mixed or attack-specific datasets

---

## Class Structure

### Packet Analyzer (in `Mini.py`)

#### 1. `Packet` (Base Class)

* **Attributes**: `src_ip`, `src_port`, `dst_ip`, `dst_port`, `protocol`
* **Methods**:

  * `summary()`: Returns formatted string for the packet

#### 2. `TCPPacket` (Derived from `Packet`)

* Inherits all attributes/methods from `Packet`
* Automatically sets protocol to `"TCP"`

#### 3. `UDPPacket` (Derived from `Packet`)

* Inherits all attributes/methods from `Packet`
* Automatically sets protocol to `"UDP"`

#### 4. `PacketAnalyzer`

* Maintains:

  * List of parsed packets
  * Count of packets per source IP
  * Count of packets by protocol
* **Methods**:

  * `parse_log_line(line)`
  * `load_log_file(filepath)`
  * `show_summary()`
  * `detect_ddos(threshold=5)`

---

## File Structure

```
project/
├── packet_analyzer.py         # OOP-based packet log parser
├── log_generator.py           # DDoS traffic simulator
```

---

## Getting Started

### Requirements

* Python 3.6+
* No third-party libraries required

---

## 1. Generate DDoS Logs

Run this command to simulate logs:

```bash
python log_generator.py
```

It will generate:

* Mixed and specific attack datasets in `.csv`
* Classic `tcpdump`-like text logs in `.txt`

### Output Examples

* `DDoS_log.txt`: For the analyzer
* `DDoS_dataset.csv`: All attack types + background traffic
* `syn_flood_dataset.csv`, `udp_flood_dataset.csv`, etc.: Isolated attack types

---

## 2. Analyze the Logs

Run the packet analyzer script:

```bash
python Mini.py
```

Ensure `DDoS_log.txt` exists in the same directory. You’ll see:

* Each packet’s summary (protocol, src > dst)
* Protocol distribution
* Top 5 talkers (source IPs)
* DDoS alerts for high-volume IPs

---

## Sample Output

```
Packet Summary:
TCP Packet: 192.168.1.10:43215 > 10.0.0.2:80

Protocol Summary:
TCP: 520 packets
UDP: 480 packets

Top Active Source IPs:
192.168.1.5: 103 packets
...

DDoS Detection (Heuristic):
[ALERT] Possible DDoS source: 192.168.1.5 (103 packets)
```
