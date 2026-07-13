#!/usr/bin/env python3
"""
Day 49 - Regex Log Analyzer
Analyze server logs using regular expressions
"""

import os
from log_analyzer import LogAnalyzer


def display_statistics(analyzer: LogAnalyzer):
    """Display log statistics"""
    stats = analyzer.get_statistics()
    
    print("\n" + "="*60)
    print("LOG STATISTICS")
    print("="*60)
    
    print(f"Total Entries: {stats.get('total_entries', 0)}")
    
    print("\nLog Level Distribution:")
    for level, count in sorted(stats.get('level_counts', {}).items()):
        percentage = (count / stats['total_entries']) * 100
        bar = "█" * int(percentage)
        print(f"  {level}: {count} ({percentage:.1f}%) {bar}")
    
    print("\nTop 5 Active Users:")
    for username, count in stats.get('top_usernames', {}).items():
        print(f"  {username}: {count} events")
    
    print("\nTop 5 IP Addresses:")
    for ip, count in stats.get('top_ips', {}).items():
        print(f"  {ip}: {count} events")
    
    if stats.get('avg_response_time'):
        print(f"\nAverage Response Time: {stats['avg_response_time']} seconds")
        print(f"Max Response Time: {stats['max_response_time']} seconds")
    
    if stats.get('avg_percentage'):
        print(f"\nAverage Memory Usage: {stats['avg_percentage']}%")
        print(f"Peak Memory Usage: {stats['max_percentage']}%")
    
    emails = analyzer.extract_emails()
    if emails:
        print(f"\nUnique Emails Found: {len(emails)}")
    
    errors = analyzer.get_errors()
    warnings = analyzer.get_warnings()
    print(f"\nTotal Errors: {len(errors)}")
    print(f"Total Warnings: {len(warnings)}")
    
    print("="*60 + "\n")


def search_logs(analyzer: LogAnalyzer):
    """Search logs for keyword"""
    print("\n" + "="*60)
    print("SEARCH LOGS")
    print("="*60)
    
    keyword = input("Enter keyword to search: ").strip()
    
    if not keyword:
        print("No keyword entered")
        return
    
    results = analyzer.search_logs(keyword)
    
    print(f"\nFound {len(results)} entries containing '{keyword}':")
    print("-"*60)
    
    for entry in results[:10]:
        print(f"{entry.get('timestamp', 'N/A')} [{entry.get('level', 'N/A')}] {entry.get('message', '')[:80]}")
    
    if len(results) > 10:
        print(f"\n... and {len(results) - 10} more results")
    
    print("="*60 + "\n")


def main():
    print("=" * 60)
    print("DAY 49 - REGEX LOG ANALYZER")
    print("=" * 60 + "\n")
    
    # Initialize analyzer
    analyzer = LogAnalyzer()
    
    # Analyze log file
    log_file = "data/server.log"
    
    if not os.path.exists(log_file):
        print(f"[ERROR] Log file not found: {log_file}")
        print("Creating sample log file...")
        
        # Create sample log file
        os.makedirs("data", exist_ok=True)
        sample_log = """2026-07-13 10:15:23 INFO User login successful: username=test@email.com, ip=192.168.1.100
2026-07-13 10:16:12 ERROR Database connection failed: Timeout after 30 seconds
2026-07-13 10:17:01 WARNING High memory usage detected: 85%
"""
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(sample_log)
        print(f"[OK] Created sample log file: {log_file}")
    
    entries = analyzer.analyze_log_file(log_file)
    
    if not entries:
        print("[ERROR] No entries found in log file")
        return
    
    # Menu
    while True:
        print("\n" + "="*60)
        print("LOG ANALYZER MENU")
        print("="*60)
        print("1. Show Statistics")
        print("2. Search Logs")
        print("3. Show All Errors")
        print("4. Show All Warnings")
        print("5. Generate Report")
        print("6. Export Report to File")
        print("7. Exit")
        print("="*60)
        
        choice = input("Enter choice (1-7): ").strip()
        
        if choice == "1":
            display_statistics(analyzer)
        
        elif choice == "2":
            search_logs(analyzer)
        
        elif choice == "3":
            errors = analyzer.get_errors()
            print(f"\nTotal Errors: {len(errors)}")
            print("-"*60)
            for error in errors[:10]:
                print(f"{error.get('timestamp', 'N/A')} - {error.get('message', 'N/A')}")
            if len(errors) > 10:
                print(f"... and {len(errors) - 10} more errors")
            print("="*60 + "\n")
        
        elif choice == "4":
            warnings = analyzer.get_warnings()
            print(f"\nTotal Warnings: {len(warnings)}")
            print("-"*60)
            for warning in warnings[:10]:
                print(f"{warning.get('timestamp', 'N/A')} - {warning.get('message', 'N/A')}")
            if len(warnings) > 10:
                print(f"... and {len(warnings) - 10} more warnings")
            print("="*60 + "\n")
        
        elif choice == "5":
            report = analyzer.generate_report()
            print("\n" + report)
        
        elif choice == "6":
            filename = input("Enter filename (default: log_report.txt): ").strip()
            if not filename:
                filename = "log_report.txt"
            analyzer.export_report(filename)
        
        elif choice == "7":
            print("\n[OK] Exiting Log Analyzer...")
            break
        
        else:
            print("[ERROR] Invalid choice. Please try again.")
    
    print("\n" + "="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()