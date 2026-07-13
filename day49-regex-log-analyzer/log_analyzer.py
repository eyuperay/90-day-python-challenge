"""
Log Analyzer with Regular Expressions
Extracts and analyzes log data using regex patterns
"""

import re
import os
from datetime import datetime
from collections import Counter
from typing import List, Dict, Any, Optional


class LogAnalyzer:
    """Log file analyzer using regular expressions"""
    
    def __init__(self):
        # Regex patterns
        self.patterns = {
            'timestamp': r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',
            'level': r'(INFO|WARNING|ERROR|DEBUG)',
            'message': r'(?:INFO|WARNING|ERROR|DEBUG)\s+(.*?)(?:\s+username=|\s+ip=|$)',
            'username': r'username=([a-zA-Z0-9@._-]+)',
            'ip_address': r'ip=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'file_path': r'/var/www/html/[^\s]+',
            'percentage': r'(\d+)%',
            'time_seconds': r'(\d+\.\d+)\s+seconds',
            'error_type': r'ERROR\s+(.*?):'
        }
        
        self.log_entries = []
        self.stats = {}
    
    def parse_log_line(self, line: str) -> Optional[Dict[str, Any]]:
        """
        Parse a single log line using regex patterns
        
        Args:
            line: Log line string
        
        Returns:
            Dictionary with parsed data or None
        """
        if not line.strip():
            return None
        
        entry = {'raw': line.strip()}
        
        # Extract timestamp
        timestamp_match = re.search(self.patterns['timestamp'], line)
        if timestamp_match:
            entry['timestamp'] = timestamp_match.group(1)
        
        # Extract log level
        level_match = re.search(self.patterns['level'], line)
        if level_match:
            entry['level'] = level_match.group(1)
        
        # Extract username
        username_match = re.search(self.patterns['username'], line)
        if username_match:
            entry['username'] = username_match.group(1)
        
        # Extract IP address
        ip_match = re.search(self.patterns['ip_address'], line)
        if ip_match:
            entry['ip'] = ip_match.group(1)
        
        # Extract email
        email_match = re.search(self.patterns['email'], line)
        if email_match:
            entry['email'] = email_match.group(0)
        
        # Extract file path
        file_match = re.search(self.patterns['file_path'], line)
        if file_match:
            entry['file_path'] = file_match.group(0)
        
        # Extract percentage
        percent_match = re.search(self.patterns['percentage'], line)
        if percent_match:
            entry['percentage'] = int(percent_match.group(1))
        
        # Extract time in seconds
        time_match = re.search(self.patterns['time_seconds'], line)
        if time_match:
            entry['response_time'] = float(time_match.group(1))
        
        # Extract error type
        error_match = re.search(self.patterns['error_type'], line)
        if error_match:
            entry['error_type'] = error_match.group(1)
        
        # Extract message
        message_match = re.search(self.patterns['message'], line)
        if message_match:
            entry['message'] = message_match.group(1).strip()
        
        return entry
    
    def analyze_log_file(self, filepath: str) -> List[Dict[str, Any]]:
        """
        Analyze entire log file
        
        Args:
            filepath: Path to log file
        
        Returns:
            List of parsed log entries
        """
        print(f"[INFO] Analyzing log file: {filepath}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            print(f"[OK] Read {len(lines)} lines from file")
            
            for line in lines:
                entry = self.parse_log_line(line)
                if entry:
                    self.log_entries.append(entry)
            
            print(f"[OK] Parsed {len(self.log_entries)} log entries")
            return self.log_entries
            
        except FileNotFoundError:
            print(f"[ERROR] File not found: {filepath}")
            return []
        except Exception as e:
            print(f"[ERROR] Failed to analyze file: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Calculate statistics from parsed log entries
        
        Returns:
            Dictionary with statistics
        """
        if not self.log_entries:
            return {"error": "No log entries to analyze"}
        
        # Count by level
        levels = [entry.get('level') for entry in self.log_entries if entry.get('level')]
        level_counts = Counter(levels)
        
        # Count by username
        usernames = [entry.get('username') for entry in self.log_entries if entry.get('username')]
        username_counts = Counter(usernames)
        
        # Count by IP
        ips = [entry.get('ip') for entry in self.log_entries if entry.get('ip')]
        ip_counts = Counter(ips)
        
        # Count by error type
        error_types = [entry.get('error_type') for entry in self.log_entries if entry.get('error_type')]
        error_counts = Counter(error_types)
        
        # File paths
        file_paths = [entry.get('file_path') for entry in self.log_entries if entry.get('file_path')]
        file_counts = Counter(file_paths)
        
        # Response times
        response_times = [entry.get('response_time') for entry in self.log_entries if entry.get('response_time')]
        
        # Percentage values
        percentages = [entry.get('percentage') for entry in self.log_entries if entry.get('percentage')]
        
        self.stats = {
            'total_entries': len(self.log_entries),
            'level_counts': dict(level_counts),
            'top_usernames': dict(username_counts.most_common(5)),
            'top_ips': dict(ip_counts.most_common(5)),
            'top_errors': dict(error_counts.most_common(5)),
            'top_files': dict(file_counts.most_common(5)),
            'avg_response_time': round(sum(response_times) / len(response_times), 2) if response_times else 0,
            'max_response_time': max(response_times) if response_times else 0,
            'min_response_time': min(response_times) if response_times else 0,
            'avg_percentage': round(sum(percentages) / len(percentages), 1) if percentages else 0,
            'max_percentage': max(percentages) if percentages else 0,
        }
        
        return self.stats
    
    def extract_emails(self) -> List[str]:
        """
        Extract all emails from log entries
        
        Returns:
            List of unique emails
        """
        emails = set()
        for entry in self.log_entries:
            if entry.get('email'):
                emails.add(entry['email'])
        return sorted(list(emails))
    
    def get_errors(self) -> List[Dict[str, Any]]:
        """
        Get all ERROR level entries
        
        Returns:
            List of error entries
        """
        return [entry for entry in self.log_entries if entry.get('level') == 'ERROR']
    
    def get_warnings(self) -> List[Dict[str, Any]]:
        """
        Get all WARNING level entries
        
        Returns:
            List of warning entries
        """
        return [entry for entry in self.log_entries if entry.get('level') == 'WARNING']
    
    def search_logs(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Search logs for keyword
        
        Args:
            keyword: Search term
        
        Returns:
            List of matching entries
        """
        keyword_lower = keyword.lower()
        results = []
        for entry in self.log_entries:
            if keyword_lower in entry.get('raw', '').lower():
                results.append(entry)
        return results
    
    def generate_report(self) -> str:
        """
        Generate a text report of log analysis
        
        Returns:
            Report as string
        """
        if not self.stats:
            self.get_statistics()
        
        lines = []
        lines.append("="*60)
        lines.append("LOG ANALYSIS REPORT")
        lines.append("="*60)
        lines.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("="*60)
        lines.append("")
        
        lines.append(f"Total Log Entries: {self.stats.get('total_entries', 0)}")
        lines.append("")
        
        # Level counts
        lines.append("-"*40)
        lines.append("LOG LEVEL DISTRIBUTION")
        lines.append("-"*40)
        for level, count in sorted(self.stats.get('level_counts', {}).items()):
            percentage = (count / self.stats['total_entries']) * 100
            lines.append(f"  {level}: {count} ({percentage:.1f}%)")
        lines.append("")
        
        # Top usernames
        lines.append("-"*40)
        lines.append("TOP 5 ACTIVE USERS")
        lines.append("-"*40)
        for username, count in self.stats.get('top_usernames', {}).items():
            lines.append(f"  {username}: {count} events")
        lines.append("")
        
        # Top IPs
        lines.append("-"*40)
        lines.append("TOP 5 IP ADDRESSES")
        lines.append("-"*40)
        for ip, count in self.stats.get('top_ips', {}).items():
            lines.append(f"  {ip}: {count} events")
        lines.append("")
        
        # Top errors
        if self.stats.get('top_errors'):
            lines.append("-"*40)
            lines.append("TOP 5 ERROR TYPES")
            lines.append("-"*40)
            for error, count in self.stats.get('top_errors', {}).items():
                lines.append(f"  {error}: {count} occurrences")
            lines.append("")
        
        # Response time stats
        if self.stats.get('avg_response_time'):
            lines.append("-"*40)
            lines.append("RESPONSE TIME STATISTICS")
            lines.append("-"*40)
            lines.append(f"  Average: {self.stats['avg_response_time']} seconds")
            lines.append(f"  Maximum: {self.stats['max_response_time']} seconds")
            lines.append(f"  Minimum: {self.stats['min_response_time']} seconds")
            lines.append("")
        
        # Memory usage
        if self.stats.get('avg_percentage'):
            lines.append("-"*40)
            lines.append("MEMORY/CPU USAGE")
            lines.append("-"*40)
            lines.append(f"  Average Usage: {self.stats['avg_percentage']}%")
            lines.append(f"  Peak Usage: {self.stats['max_percentage']}%")
            lines.append("")
        
        # Emails
        emails = self.extract_emails()
        if emails:
            lines.append("-"*40)
            lines.append("UNIQUE EMAILS IN LOGS")
            lines.append("-"*40)
            for email in emails[:10]:
                lines.append(f"  {email}")
            if len(emails) > 10:
                lines.append(f"  ... and {len(emails) - 10} more")
            lines.append("")
        
        # Error summary
        errors = self.get_errors()
        if errors:
            lines.append("-"*40)
            lines.append("ERROR SUMMARY")
            lines.append("-"*40)
            for error in errors[:5]:
                lines.append(f"  {error.get('timestamp', 'N/A')}: {error.get('message', 'N/A')[:60]}")
            if len(errors) > 5:
                lines.append(f"  ... and {len(errors) - 5} more errors")
        
        lines.append("")
        lines.append("="*60)
        
        return "\n".join(lines)
    
    def export_report(self, filename: str = "log_report.txt"):
        """
        Export report to file
        
        Args:
            filename: Output filename
        """
        os.makedirs("output", exist_ok=True)
        report = self.generate_report()
        filepath = f"output/{filename}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"[OK] Report saved to: {filepath}")
        return filepath
