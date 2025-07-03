import random
import csv
from datetime import datetime, timedelta

# Network configuration for DDoS simulation
target_servers = ["192.168.1.100", "10.0.0.50", "172.16.1.10"]
legitimate_ips = [f"192.168.1.{i}" for i in range(1, 50)]
botnet_ips = [f"{a}.{b}.{c}.{d}" for a in range(10, 200, 20) for b in range(1, 10) for c in range(0, 5) for d in range(1, 255, 10)]

# Attack patterns
tcp_flags = ['S', 'P.', 'F.', '.', 'S.', 'FA', 'R.', 'SF']
common_ports = [80, 443, 22, 21, 25, 53, 3389, 8080]
attack_ports = [80, 443, 22]  # Most targeted ports
udp_lengths = [32, 64, 128, 256, 512, 1024, 1500]  # Various packet sizes

def random_ip():
    return random.choice(legitimate_ips + botnet_ips)

def random_botnet_ip():
    return random.choice(botnet_ips)

def random_legitimate_ip():
    return random.choice(legitimate_ips)

def random_target():
    return random.choice(target_servers)

def random_port():
    return random.randint(1024, 65535)

def random_attack_port():
    return random.choice(attack_ports)

# DDoS Attack Pattern Generators
def generate_syn_flood_entry():
    """Generate SYN flood attack entry"""
    src_ip = random_target()
    dst_ip = random_botnet_ip()
    src_port = random_port()
    dst_port = random_attack_port()
    seq = random.randint(0, 4294967295)
    win = random.choice([1024, 2048, 4096, 8192])
    
    return {
        'highest_layer': 'TCP',
        'transport_layer': 'TCP', 
        'source_ip': src_ip,
        'dest_ip': dst_ip,
        'source_port': src_port,
        'dest_port': dst_port,
        'packet_length': random.choice([40, 44, 48]),  # Small SYN packets
        'packets_time': round(random.uniform(500, 2000), 1),
        'target': 1  # Attack traffic
    }

def generate_udp_flood_entry():
    """Generate UDP flood attack entry"""
    src_ip = random_botnet_ip()
    dst_ip = random_target()
    src_port = random_port()
    dst_port = random.choice([53, 123, 1900])  # DNS, NTP, SSDP amplification
    packet_size = random.choice([512, 1024, 1500])  # Large UDP packets
    
    return {
        'highest_layer': 'UDP',
        'transport_layer': 'UDP',
        'source_ip': src_ip,
        'dest_ip': dst_ip,
        'source_port': src_port,
        'dest_port': dst_port,
        'packet_length': packet_size,
        'packets_time': round(random.uniform(800, 3000), 1),
        'target': 1  # Attack traffic
    }

def generate_volumetric_attack_entry():
    """Generate high-volume attack entry"""
    src_ip = random_botnet_ip()
    dst_ip = random_target()
    src_port = random_port()
    dst_port = random_attack_port()
    protocol = random.choice(['TCP', 'UDP'])
    
    return {
        'highest_layer': protocol,
        'transport_layer': protocol,
        'source_ip': src_ip,
        'dest_ip': dst_ip,
        'source_port': src_port,
        'dest_port': dst_port,
        'packet_length': random.choice([1400, 1500, 1518]),  # Large packets
        'packets_time': round(random.uniform(1000, 5000), 1),
        'target': 1  # Attack traffic
    }

def generate_legitimate_entry():
    """Generate legitimate traffic entry"""
    src_ip = random_legitimate_ip()
    dst_ip = random.choice(target_servers + legitimate_ips)
    src_port = random_port()
    dst_port = random.choice(common_ports)
    protocol = random.choice(['TCP', 'UDP'])
    
    return {
        'highest_layer': protocol,
        'transport_layer': protocol,
        'source_ip': src_ip,
        'dest_ip': dst_ip,
        'source_port': src_port,
        'dest_port': dst_port,
        'packet_length': random.choice([64, 128, 256, 512]),
        'packets_time': round(random.uniform(50, 200), 1),
        'target': 0  # Legitimate traffic
    }

def generate_ddos_attack_pattern():
    """Generate a DDoS attack pattern entry based on attack type"""
    attack_type = random.choices(
        ['syn_flood', 'udp_flood', 'volumetric', 'legitimate'],
        weights=[0.4, 0.3, 0.2, 0.1],  # 90% attack, 10% legitimate
        k=1
    )[0]
    
    if attack_type == 'syn_flood':
        return generate_syn_flood_entry()
    elif attack_type == 'udp_flood':
        return generate_udp_flood_entry()
    elif attack_type == 'volumetric':
        return generate_volumetric_attack_entry()
    else:
        return generate_legitimate_entry()

def generate_coordinated_attack(target_ip, attack_duration_seconds=300):
    """Generate a coordinated DDoS attack from multiple sources"""
    attack_entries = []
    attacker_count = random.randint(50, 200)  # Number of attacking IPs
    
    for _ in range(attack_duration_seconds):
        # Multiple packets per second during attack
        packets_per_second = random.randint(10, 50)
        
        for _ in range(packets_per_second):
            src_ip = random_botnet_ip()
            attack_type = random.choice(['syn_flood', 'udp_flood', 'volumetric'])
            
            if attack_type == 'syn_flood':
                entry = generate_syn_flood_entry()
            elif attack_type == 'udp_flood':
                entry = generate_udp_flood_entry()
            else:
                entry = generate_volumetric_attack_entry()
            
            entry['dest_ip'] = target_ip  # Focus attack on specific target
            attack_entries.append(entry)
    
    return attack_entries

def generate_ddos_csv_file(filename='ddos_dataset.csv', entry_count=10000, include_coordinated_attack=True):
    """Generate a CSV file with DDoS attack patterns and save as TXT as well"""
    entries = []
    
    print(f"[+] Generating {entry_count} DDoS log entries...")
    
    # Generate mixed traffic (attacks + legitimate)
    for i in range(entry_count):
        if i % 1000 == 0:
            print(f"    Generated {i}/{entry_count} entries...")
        
        entry = generate_ddos_attack_pattern()
        entries.append(entry)
    
    # Add coordinated attack if requested
    if include_coordinated_attack:
        print("[+] Adding coordinated DDoS attack pattern...")
        target = random.choice(target_servers)
        coordinated_entries = generate_coordinated_attack(target, 120)  # 2-minute attack
        entries.extend(coordinated_entries)
    
    # Shuffle entries to make it more realistic
    random.shuffle(entries)
    
    # Write to CSV file
    fieldnames = ['highest_layer', 'transport_layer', 'source_ip', 'dest_ip', 
                  'source_port', 'dest_port', 'packet_length', 'packets_time', 'target']
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(entries)
    
    # Write to TXT file (tab-separated)
    txt_filename = filename.rsplit('.', 1)[0] + '.txt'
    with open(txt_filename, 'w', encoding='utf-8') as txtfile:
        txtfile.write('\t'.join(fieldnames) + '\n')
        for entry in entries:
            row = [str(entry[field]) for field in fieldnames]
            txtfile.write('\t'.join(row) + '\n')
    
    attack_count = sum(1 for entry in entries if entry['target'] == 1)
    legitimate_count = len(entries) - attack_count
    
    print(f"[+] DDoS dataset '{filename}' generated successfully!")
    print(f"    Total entries: {len(entries)}")
    print(f"    Attack entries: {attack_count} ({attack_count/len(entries)*100:.1f}%)")
    print(f"    Legitimate entries: {legitimate_count} ({legitimate_count/len(entries)*100:.1f}%)")
    print(f"    Target servers: {', '.join(target_servers)}")
    print(f"    Botnet size: {len(botnet_ips)} IPs")

def generate_specific_attack_type(attack_type, filename=None, entry_count=1000):
    """Generate a specific type of DDoS attack and save as TXT as well"""
    if filename is None:
        filename = f"{attack_type}_attack.csv"
    
    entries = []
    
    print(f"[+] Generating {entry_count} {attack_type} attack entries...")
    
    for i in range(entry_count):
        if attack_type == 'syn_flood':
            entry = generate_syn_flood_entry()
        elif attack_type == 'udp_flood':
            entry = generate_udp_flood_entry()
        elif attack_type == 'volumetric':
            entry = generate_volumetric_attack_entry()
        else:
            print(f"[-] Unknown attack type: {attack_type}")
            return
        
        entries.append(entry)
    
    # Write to CSV
    fieldnames = ['highest_layer', 'transport_layer', 'source_ip', 'dest_ip', 
                  'source_port', 'dest_port', 'packet_length', 'packets_time', 'target']
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(entries)
    
    # Write to TXT file (tab-separated)
    txt_filename = filename.rsplit('.', 1)[0] + '.txt'
    with open(txt_filename, 'w', encoding='utf-8') as txtfile:
        txtfile.write('\t'.join(fieldnames) + '\n')
        for entry in entries:
            row = [str(entry[field]) for field in fieldnames]
            txtfile.write('\t'.join(row) + '\n')
    
    print(f"[+] {attack_type.title()} attack dataset '{filename}' generated successfully!")
    print(f"    Total entries: {len(entries)}")

def generate_ddos_text_log(filename='DDoS_log.txt', line_count=1000, start_time="12:00:00"):
    """Generate a DDoS log file in classic text format with timestamps and packet details, matching the requested format."""
    current_time = datetime.strptime(start_time, "%H:%M:%S")
    with open(filename, 'w', encoding='utf-8') as f:
        for _ in range(line_count):
            timestamp = current_time.strftime("%H:%M:%S")
            attack_type = random.choices(
                ['syn_flood', 'udp_flood', 'legitimate'],
                weights=[0.5, 0.4, 0.1],
                k=1
            )[0]
            if attack_type == 'udp_flood':
                src_ip = random_botnet_ip()
                dst_ip = random_target()
                src_port = random_port()
                dst_port = random.choice([53, 123, 1900])
                length = random.choice([32, 64, 128, 256, 512, 1024, 1500])
                log = f"IP {src_ip}.{src_port} > {dst_ip}.{dst_port}: UDP, length {length}"
            else:  # TCP (SYN flood or legitimate)
                src_ip = random_botnet_ip() if attack_type == 'syn_flood' else random_legitimate_ip()
                dst_ip = random_target() if attack_type == 'syn_flood' else random.choice(target_servers + legitimate_ips)
                src_port = random_port()
                dst_port = random_attack_port() if attack_type == 'syn_flood' else random.choice(common_ports)
                flag = random.choice(['S', 'P.', 'F.', '.', 'FA']) if attack_type == 'syn_flood' else random.choice(['.', 'P.', 'F.', 'S.', 'FA'])
                seq = random.randint(0, 100000)
                win = random.choice([8192, 65535])
                length = random.choice([0, 32, 64])
                if flag == 'S':
                    log = f"IP {src_ip}.{src_port} > {dst_ip}.{dst_port}: Flags [{flag}], seq {seq}, win {win}, length {length}"
                elif flag == '.':
                    ack = random.randint(1, 100000)
                    log = f"IP {src_ip}.{src_port} > {dst_ip}.{dst_port}: Flags [{flag}], ack {ack}, length {length}"
                elif flag in ['P.', 'F.', 'FA']:
                    log = f"IP {src_ip}.{src_port} > {dst_ip}.{dst_port}: Flags [{flag}], length {length}"
                else:
                    log = f"IP {src_ip}.{src_port} > {dst_ip}.{dst_port}: Flags [{flag}], length {length}"
            f.write(f"{timestamp} {log}\n")
            current_time += timedelta(seconds=1)
    print(f"[+] DDoS text log '{filename}' generated with {line_count} entries.")

def print_attack_statistics():
    """Print statistics about the simulated network"""
    print("\n" + "="*60)
    print("DDoS SIMULATION ENVIRONMENT")
    print("="*60)
    print(f"Target Servers: {len(target_servers)}")
    for i, server in enumerate(target_servers, 1):
        print(f"  {i}. {server}")
    print(f"\nLegitimate Network: {len(legitimate_ips)} IPs")
    print(f"  Range: {legitimate_ips[0]} - {legitimate_ips[-1]}")
    print(f"\nBotnet Size: {len(botnet_ips)} IPs")
    print(f"  Distributed across multiple subnets")
    print(f"\nAttack Types Simulated:")
    print(f"  • SYN Flood - TCP connection exhaustion")
    print(f"  • UDP Flood - High-volume UDP traffic") 
    print(f"  • Volumetric - Bandwidth exhaustion")
    print(f"  • Coordinated - Multi-source attacks")
    print("="*60)

if __name__ == "__main__":
    print_attack_statistics()
    
    # Generate main DDoS dataset
    generate_ddos_csv_file('DDoS_dataset.csv', entry_count=15000, include_coordinated_attack=True)
    
    # Generate specific attack type datasets for testing
    print("\n[+] Generating specific attack type datasets...")
    generate_specific_attack_type('syn_flood', 'syn_flood_dataset.csv', 2000)
    generate_specific_attack_type('udp_flood', 'udp_flood_dataset.csv', 2000)
    generate_specific_attack_type('volumetric', 'volumetric_dataset.csv', 2000)
    
    # Generate classic text log for DDoS
    print("\n[+] Generating classic DDoS text log format...")
    generate_ddos_text_log('DDoS_log.txt', line_count=1000, start_time="12:00:01")
    
    print("\n" + "="*60)
    print("DDoS DATASET GENERATION COMPLETE!")
    print("="*60)
    print("Files generated:")
    print("  • DDoS_dataset.csv - Mixed traffic with attacks")
    print("  • syn_flood_dataset.csv - SYN flood attacks only")
    print("  • udp_flood_dataset.csv - UDP flood attacks only") 
    print("  • volumetric_dataset.csv - Volumetric attacks only")
    print("  • DDoS_log.txt - Classic text log format")
    print("\nUse these files with the Flask web application for analysis!")
    print("="*60)
