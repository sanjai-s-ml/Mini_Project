import re
from collections import defaultdict

# Base class
class Packet:
    def __init__(self, src_ip, src_port, dst_ip, dst_port, protocol):
        self.src_ip = src_ip
        self.src_port = src_port
        self.dst_ip = dst_ip
        self.dst_port = dst_port
        self.protocol = protocol

    def summary(self):
        return f"{self.protocol} Packet: {self.src_ip}:{self.src_port} > {self.dst_ip}:{self.dst_port}"

# TCP subclass
class TCPPacket(Packet):
    def __init__(self, src_ip, src_port, dst_ip, dst_port):
        super().__init__(src_ip, src_port, dst_ip, dst_port, "TCP")

# UDP subclass
class UDPPacket(Packet):
    def __init__(self, src_ip, src_port, dst_ip, dst_port):
        super().__init__(src_ip, src_port, dst_ip, dst_port, "UDP")

# Utility class (for calculating packets and ips)
class PacketAnalyzer:
    def __init__(self):
        self.packet_list = []
        self.ip_count = defaultdict(int)
        self.protocol_count = defaultdict(int)
    
    def parse_log_line(self, line): # regex to extract ips and ports
        try:
            
            match = re.search(r'IP (\d+\.\d+\.\d+\.\d+)\.(\d+) > (\d+\.\d+\.\d+\.\d+)\.(\d+): (.+)', line)
            if not match:
                return None

            src_ip, src_port, dst_ip, dst_port, proto_info = match.groups()
            proto_info = proto_info.upper()

            if "UDP" in proto_info:
                pkt = UDPPacket(src_ip, src_port, dst_ip, dst_port)
            else:
                pkt = TCPPacket(src_ip, src_port, dst_ip, dst_port)

            self.packet_list.append(pkt)
            self.ip_count[src_ip] += 1 
            self.protocol_count[pkt.protocol] += 1
            return pkt

        except Exception as e:
            print(f"[ERROR] Failed to parse line: {line.strip()} - {e}")
            return None
    
    # Read logs from log file
    def load_log_file(self, filepath):
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    self.parse_log_line(line)
        except FileNotFoundError:
            print("[ERROR] File not found.")

    def show_summary(self):
        print("\nProtocol Summary:")
        for proto in self.protocol_count:
            print(f"{proto}: {self.protocol_count[proto]} packets")

        print("\nTop Active Source IPs:")
        ip_list = list(self.ip_count.items())

        # sort the list based on maximum number of packets tranfered
        for i in range(len(ip_list)):
            for j in range(i + 1, len(ip_list)):
                if ip_list[j][1] > ip_list[i][1]:
                    temp = ip_list[i]
                    ip_list[i] = ip_list[j]
                    ip_list[j] = temp
        
        for ind, ip_data in enumerate(ip_list): # just printing top 5 ips which has maximum packets tansfered
            if ind == 5:
                break
            print(f"{ip_data[0]}: {ip_data[1]} packets")


    def detect_ddos(self, threshold=5):
        print("\nDDoS Detection (Heuristic):")
        flagged = False
        for ip in self.ip_count:
            if self.ip_count[ip] >= threshold:
                print(f"[ALERT] Possible DDoS source: {ip} ({self.ip_count[ip]} packets)")
                flagged = True
        if not flagged:
            print("No suspicious activity detected.")

# Main
if __name__ == "__main__":
    analyzer = PacketAnalyzer()
    analyzer.load_log_file("DDoS_log.txt")

    print("\nPacket Summary:")
    for pkt in analyzer.packet_list:
        print(pkt.summary())

    analyzer.show_summary()
    analyzer.detect_ddos(threshold=5)