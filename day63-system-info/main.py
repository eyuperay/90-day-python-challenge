#!/usr/bin/env python3
"""
Day 63 - System Information
Collects and displays system information
"""

import time
from system_info import SystemInfo


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def main():
    print("=" * 60)
    print("DAY 63 - SYSTEM INFORMATION")
    print("=" * 60 + "\n")
    
    info = SystemInfo()
    
    print_section("1. COLLECTING SYSTEM INFORMATION")
    
    print("Collecting system information...")
    data = info.get_all_info()
    print("[OK] System information collected successfully!")
    
    print_section("2. SYSTEM SUMMARY")
    info.print_summary()
    
    print_section("3. OPERATING SYSTEM DETAILS")
    
    os_info = info.get_os_info()
    for key, value in os_info.items():
        print(f"  {key}: {value}")
    
    print_section("4. HARDWARE DETAILS")
    
    hardware = info.get_hardware_info()
    for key, value in hardware.items():
        print(f"  {key}: {value}")
    
    print_section("5. NETWORK DETAILS")
    
    network = info.get_network_info()
    for key, value in network.items():
        if key == 'all_ips' and value:
            print(f"  {key}: {', '.join(value)}")
        else:
            print(f"  {key}: {value}")
    
    print_section("6. ENVIRONMENT DETAILS")
    
    env = info.get_environment_info()
    for key, value in env.items():
        print(f"  {key}: {value}")
    
    print_section("7. JSON OUTPUT")
    
    json_data = info.to_json()
    print(json_data)
    
    print_section("8. GENERATING REPORT")
    
    report = info.generate_report()
    print("[OK] Report generated successfully!")
    print("Report saved to: output/system_report.txt")
    
    print_section("9. SAVING JSON")
    
    with open("output/system_info.json", 'w', encoding='utf-8') as f:
        f.write(info.to_json())
    print("[OK] JSON saved to: output/system_info.json")
    
    print_section("SUMMARY")
    print("""
System Information - Key Concepts:

1. Information Types:
   - Operating System: platform, release, version
   - Hardware: CPU, memory, disk
   - Network: hostname, IP addresses
   - Environment: paths, user, computer name

2. Python Modules Used:
   - platform: OS and system information
   - os: Operating system interfaces
   - sys: System-specific parameters
   - socket: Network information
   - psutil: System utilization (optional)

3. Use Cases:
   - System monitoring
   - Asset inventory
   - Troubleshooting
   - Performance analysis
   - Configuration management

4. Report Formats:
   - Text report (human-readable)
   - JSON (machine-readable)
   - Summary (quick overview)
    """)
    
    print("="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("Check 'output' folder for reports")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
