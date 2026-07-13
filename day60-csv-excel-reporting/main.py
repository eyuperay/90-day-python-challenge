#!/usr/bin/env python3
"""
Day 60 - CSV/Excel Reporting
Demonstrates CSV and Excel report generation
"""

import os
from report_generator import ReportGenerator


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def demo_data_generation(generator: ReportGenerator):
    """Demonstrate data generation"""
    print_section("1. DATA GENERATION")
    
    # Generate sales data
    sales_data = generator.generate_sample_sales_data(100)
    print(f"  Generated {len(sales_data)} sales records")
    print(f"  Headers: {generator.headers}")
    
    # Show sample
    print("\n  Sample record:")
    for key, value in sales_data[0].items():
        print(f"    {key}: {value}")
    
    # Save to CSV
    generator.write_csv(sales_data, "data/sales_data.csv")
    
    # Generate employee data
    employee_data = generator.generate_sample_employee_data(50)
    print(f"\n  Generated {len(employee_data)} employee records")
    generator.write_csv(employee_data, "data/employee_data.csv")


def demo_read_csv(generator: ReportGenerator):
    """Demonstrate CSV reading"""
    print_section("2. READ CSV")
    
    data = generator.read_csv("data/sales_data.csv")
    
    if data:
        print(f"  Read {len(data)} records")
        print(f"  Headers: {generator.headers}")
        print(f"  First record: {data[0]}")


def demo_summary_report(generator: ReportGenerator):
    """Demonstrate summary report"""
    print_section("3. SUMMARY REPORT")
    
    data = generator.read_csv("data/sales_data.csv")
    
    if data:
        # Group by region
        summary = generator.create_summary_report(data, 'region', 'sum')
        
        print("\n  Sales by Region:")
        for record in summary:
            print(f"    {record['region']}: {record.get('total_total', 0):,.2f} TRY, {record['count']} orders")
        
        # Save summary
        generator.write_csv(summary, "output/sales_by_region.csv")
        
        # Group by category
        summary = generator.create_summary_report(data, 'category', 'sum')
        
        print("\n  Sales by Category:")
        for record in summary:
            print(f"    {record['category']}: {record.get('total_total', 0):,.2f} TRY, {record['count']} orders")
        
        generator.write_csv(summary, "output/sales_by_category.csv")


def demo_pivot_report(generator: ReportGenerator):
    """Demonstrate pivot report"""
    print_section("4. PIVOT REPORT")
    
    data = generator.read_csv("data/sales_data.csv")
    
    if data:
        # Pivot by region and category
        pivot = generator.create_pivot_report(
            data, 
            rows=['region'], 
            columns=['category'], 
            value='total'
        )
        
        print("\n  Pivot: Region x Category (Total Sales)")
        for record in pivot:
            print(f"    {record.get('region', '')}:")
            for key, value in record.items():
                if key != 'region':
                    print(f"      {key}: {value}")
        
        generator.write_csv(pivot, "output/pivot_region_category.csv")


def demo_summary_stats(generator: ReportGenerator):
    """Demonstrate summary statistics"""
    print_section("5. SUMMARY STATISTICS")
    
    data = generator.read_csv("data/sales_data.csv")
    
    if data:
        stats = generator.generate_summary_stats(data)
        
        print("\n  Summary Statistics:")
        for key, value in stats.items():
            print(f"    {key}: {value}")


def demo_filter_and_sort(generator: ReportGenerator):
    """Demonstrate filter and sort"""
    print_section("6. FILTER AND SORT")
    
    data = generator.read_csv("data/sales_data.csv")
    
    if data:
        # Filter by status
        filtered = generator.filter_report(data, {'status': 'Delivered'})
        print(f"\n  Delivered orders: {len(filtered)}")
        
        # Sort by total
        sorted_data = generator.sort_report(filtered, 'total', reverse=True)
        
        print("  Top 5 Delivered orders:")
        for i, record in enumerate(sorted_data[:5], 1):
            print(f"    {i}. {record['product']}: {record['total']:.2f} TRY")
        
        generator.write_csv(sorted_data[:10], "output/top_delivered_orders.csv")


def demo_multi_format_export(generator: ReportGenerator):
    """Demonstrate multi-format export"""
    print_section("7. MULTI-FORMAT EXPORT")
    
    data = generator.read_csv("data/sales_data.csv")
    
    if data:
        # Export to JSON
        generator.export_to_json(data[:20], "output/sales_sample.json")
        
        # Export to HTML
        generator.export_to_html(data[:20], "output/sales_report.html", "Sales Report")


def demo_employee_report(generator: ReportGenerator):
    """Demonstrate employee report"""
    print_section("8. EMPLOYEE REPORT")
    
    data = generator.read_csv("data/employee_data.csv")
    
    if data:
        # Group by department
        summary = generator.create_summary_report(data, 'department', 'sum')
        
        print("\n  Employees by Department:")
        for record in summary:
            print(f"    {record['department']}: {record['count']} employees")
        
        generator.write_csv(summary, "output/employees_by_department.csv")
        
        # Summary statistics
        stats = generator.generate_summary_stats(data)
        print(f"\n  Total Employees: {stats.get('record_count', 0)}")
        print(f"  Average Salary: {stats.get('salary_avg', 0):,.2f} TRY")
        print(f"  Min Salary: {stats.get('salary_min', 0):,.2f} TRY")
        print(f"  Max Salary: {stats.get('salary_max', 0):,.2f} TRY")


def print_summary():
    """Print summary"""
    print_section("SUMMARY")
    print("""
CSV/Excel Reporting - Key Concepts:

1. CSV Operations:
   - Read CSV files
   - Write CSV files
   - Filter and sort data
   - Group and aggregate

2. Report Types:
   - Summary reports (group by field)
   - Pivot reports (rows x columns)
   - Filtered reports
   - Statistics reports

3. Export Formats:
   - CSV (compatible with Excel)
   - JSON (API ready)
   - HTML (web viewable)

4. Data Analysis:
   - Group by categories
   - Calculate totals/averages
   - Find min/max values
   - Filter by conditions
   - Sort by fields

5. Use Cases:
   - Sales reports
   - Employee reports
   - Financial reports
   - Inventory reports
   - Performance reports

6. Best Practices:
   - Use headers
   - Handle missing data
   - Validate input
   - Add timestamps
   - Keep backup
    """)
    print("="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("[OK] Check 'data' and 'output' folders for results")
    print("="*60 + "\n")


def main():
    print("=" * 60)
    print("DAY 60 - CSV/EXCEL REPORTING")
    print("=" * 60 + "\n")
    
    generator = ReportGenerator()
    
    # Run all demos
    demo_data_generation(generator)
    demo_read_csv(generator)
    demo_summary_report(generator)
    demo_pivot_report(generator)
    demo_summary_stats(generator)
    demo_filter_and_sort(generator)
    demo_multi_format_export(generator)
    demo_employee_report(generator)
    
    # Print summary
    print_summary()


if __name__ == "__main__":
    main()
