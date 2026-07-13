"""
System Information Module
Collects system information using various Python modules
"""

import os
import sys
import platform
import socket
import datetime
import json
from typing import Dict, Any, List


class SystemInfo:
    """Collects and provides system information"""
    
    def __init__(self):
        self.info = {}
    
    def get_os_info(self) -> Dict[str, str]:
        """Get operating system information"""
        return {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'platform': platform.platform(),
            'python_version': sys.version,
            'python_implementation': platform.python_implementation()
        }
    
    def get_hardware_info(self) -> Dict[str, Any]:
        """Get hardware information"""
        try:
            import psutil
            cpu_count = psutil.cpu_count()
            cpu_count_logical = psutil.cpu_count(logical=True)
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu_physical_cores': cpu_count,
                'cpu_logical_cores': cpu_count_logical,
                'cpu_usage_percent': cpu_percent,
                'total_memory_gb': round(memory.total / (1024**3), 2),
                'available_memory_gb': round(memory.available / (1024**3), 2),
                'memory_usage_percent': memory.percent,
                'total_disk_gb': round(disk.total / (1024**3), 2),
                'used_disk_gb': round(disk.used / (1024**3), 2),
                'free_disk_gb': round(disk.free / (1024**3), 2),
                'disk_usage_percent': disk.percent
            }
        except ImportError:
            return {
                'cpu_physical_cores': os.cpu_count(),
                'cpu_logical_cores': os.cpu_count(),
                'cpu_usage_percent': 'N/A (psutil not installed)',
                'total_memory_gb': 'N/A (psutil not installed)',
                'available_memory_gb': 'N/A (psutil not installed)',
                'memory_usage_percent': 'N/A (psutil not installed)',
                'total_disk_gb': 'N/A (psutil not installed)',
                'used_disk_gb': 'N/A (psutil not installed)',
                'free_disk_gb': 'N/A (psutil not installed)',
                'disk_usage_percent': 'N/A (psutil not installed)'
            }
    
    def get_network_info(self) -> Dict[str, Any]:
        """Get network information"""
        info = {}
        
        info['hostname'] = socket.gethostname()
        try:
            info['ip_address'] = socket.gethostbyname(socket.gethostname())
        except:
            info['ip_address'] = 'N/A'
        
        try:
            info['all_ips'] = []
            hostname = socket.gethostname()
            ip_list = socket.gethostbyname_ex(hostname)
            info['all_ips'] = ip_list[2] if ip_list else []
        except:
            info['all_ips'] = []
        
        return info
    
    def get_environment_info(self) -> Dict[str, str]:
        """Get environment information"""
        return {
            'current_directory': os.getcwd(),
            'home_directory': os.path.expanduser('~'),
            'user': os.getenv('USERNAME') or os.getenv('USER') or 'N/A',
            'computer_name': os.getenv('COMPUTERNAME') or platform.node() or 'N/A'
        }
    
    def get_all_info(self) -> Dict[str, Any]:
        """Get all system information"""
        self.info = {
            'timestamp': datetime.datetime.now().isoformat(),
            'os': self.get_os_info(),
            'hardware': self.get_hardware_info(),
            'network': self.get_network_info(),
            'environment': self.get_environment_info()
        }
        return self.info
    
    def to_json(self, indent: int = 2) -> str:
        """Convert system info to JSON"""
        if not self.info:
            self.get_all_info()
        return json.dumps(self.info, indent=indent, ensure_ascii=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Get system info as dictionary"""
        if not self.info:
            self.get_all_info()
        return self.info
    
    def generate_report(self, filename: str = "system_report.txt") -> str:
        """Generate a formatted text report"""
        if not self.info:
            self.get_all_info()
        
        lines = []
        lines.append("="*60)
        lines.append("SYSTEM INFORMATION REPORT")
        lines.append("="*60)
        lines.append(f"Report Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("="*60)
        lines.append("")
        
        lines.append("OPERATING SYSTEM")
        lines.append("-"*40)
        for key, value in self.info['os'].items():
            lines.append(f"  {key}: {value}")
        lines.append("")
        
        lines.append("HARDWARE INFORMATION")
        lines.append("-"*40)
        for key, value in self.info['hardware'].items():
            lines.append(f"  {key}: {value}")
        lines.append("")
        
        lines.append("NETWORK INFORMATION")
        lines.append("-"*40)
        lines.append(f"  hostname: {self.info['network'].get('hostname', 'N/A')}")
        lines.append(f"  ip_address: {self.info['network'].get('ip_address', 'N/A')}")
        if self.info['network'].get('all_ips'):
            lines.append(f"  all_ips: {', '.join(self.info['network']['all_ips'])}")
        lines.append("")
        
        lines.append("ENVIRONMENT")
        lines.append("-"*40)
        for key, value in self.info['environment'].items():
            lines.append(f"  {key}: {value}")
        lines.append("")
        
        lines.append("="*60)
        lines.append("END OF REPORT")
        lines.append("="*60)
        
        report = "\n".join(lines)
        
        with open(f"output/{filename}", 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report
    
    def print_summary(self):
        """Print a summary of system information"""
        if not self.info:
            self.get_all_info()
        
        print("\n" + "="*50)
        print("SYSTEM SUMMARY")
        print("="*50)
        print(f"System: {self.info['os'].get('system', 'N/A')}")
        print(f"Release: {self.info['os'].get('release', 'N/A')}")
        print(f"Processor: {self.info['os'].get('processor', 'N/A')}")
        print(f"CPU Cores: {self.info['hardware'].get('cpu_physical_cores', 'N/A')}")
        print(f"Memory: {self.info['hardware'].get('total_memory_gb', 'N/A')} GB")
        print(f"Disk: {self.info['hardware'].get('total_disk_gb', 'N/A')} GB")
        print(f"Hostname: {self.info['network'].get('hostname', 'N/A')}")
        print(f"IP Address: {self.info['network'].get('ip_address', 'N/A')}")
        print(f"Python: {self.info['os'].get('python_version', 'N/A')[:50]}...")
        print("="*50)
