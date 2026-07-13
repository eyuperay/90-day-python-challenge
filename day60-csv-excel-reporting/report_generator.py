"""
Report Generator Module
Handles CSV and Excel report generation
"""

import csv
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional


class ReportGenerator:
    """Generate reports in CSV and Excel formats"""
    
    def __init__(self):
        self.data = []
        self.headers = []
    
    # ==================== DATA GENERATION ====================
    
    def generate_sample_sales_data(self, num_records: int = 100) -> List[Dict]:
        """
        Generate sample sales data
        
        Args:
            num_records: Number of records to generate
        
        Returns:
            List of sales records
        """
        import random
        
        products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Printer', 'Scanner', 'Tablet', 'Phone']
        regions = ['North', 'South', 'East', 'West', 'Central']
        categories = ['Electronics', 'Accessories', 'Computers', 'Office']
        statuses = ['Pending', 'Shipped', 'Delivered', 'Cancelled']
        
        data = []
        for i in range(num_records):
            product = random.choice(products)
            price = round(random.uniform(50, 2000), 2)
            quantity = random.randint(1, 20)
            
            record = {
                'id': i + 1,
                'product': product,
                'category': random.choice(categories),
                'region': random.choice(regions),
                'price': price,
                'quantity': quantity,
                'total': round(price * quantity, 2),
                'date': datetime.now().strftime('%Y-%m-%d'),
                'status': random.choice(statuses)
            }
            data.append(record)
        
        self.data = data
        self.headers = list(data[0].keys()) if data else []
        return data
    
    def generate_sample_employee_data(self, num_records: int = 50) -> List[Dict]:
        """
        Generate sample employee data
        
        Args:
            num_records: Number of records to generate
        
        Returns:
            List of employee records
        """
        import random
        
        departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance']
        positions = ['Manager', 'Senior', 'Junior', 'Intern', 'Lead']
        cities = ['Istanbul', 'Ankara', 'Izmir', 'Bursa', 'Antalya']
        statuses = ['Active', 'Inactive', 'On Leave']
        
        data = []
        for i in range(num_records):
            record = {
                'id': i + 1,
                'name': f"Employee_{i+1}",
                'department': random.choice(departments),
                'position': random.choice(positions),
                'salary': random.randint(30000, 150000),
                'hire_date': datetime.now().strftime('%Y-%m-%d'),
                'city': random.choice(cities),
                'status': random.choice(statuses)
            }
            data.append(record)
        
        self.data = data
        self.headers = list(data[0].keys()) if data else []
        return data
    
    # ==================== CSV OPERATIONS ====================
    
    def write_csv(self, data: List[Dict], filename: str, headers: List[str] = None) -> bool:
        """
        Write data to CSV file
        
        Args:
            data: List of dictionaries
            filename: Output filename
            headers: Column headers (optional)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
            
            if not data:
                print("[ERROR] No data to write")
                return False
            
            if headers is None:
                headers = list(data[0].keys())
            
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
            
            print(f"[OK] CSV saved to: {filename} ({len(data)} records)")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to write CSV: {e}")
            return False
    
    def read_csv(self, filename: str) -> List[Dict]:
        """
        Read CSV file and convert numeric strings to appropriate types
        
        Args:
            filename: CSV file path
        
        Returns:
            List of dictionaries with proper types
        """
        try:
            with open(filename, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                data = []
                
                for row in reader:
                    converted_row = {}
                    for key, value in row.items():
                        # Try to convert to int
                        try:
                            if '.' in value:
                                converted_row[key] = float(value)
                            else:
                                converted_row[key] = int(value)
                        except (ValueError, TypeError):
                            converted_row[key] = value
                    data.append(converted_row)
            
            self.data = data
            self.headers = reader.fieldnames or []
            print(f"[OK] Read CSV from: {filename} ({len(data)} records)")
            return data
            
        except FileNotFoundError:
            print(f"[ERROR] File not found: {filename}")
            return []
        except Exception as e:
            print(f"[ERROR] Failed to read CSV: {e}")
            return []
    
    # ==================== REPORT OPERATIONS ====================
    
    def create_summary_report(self, data: List[Dict], group_by: str, 
                               aggregate: str = 'sum') -> List[Dict]:
        """
        Create summary report by grouping data
        
        Args:
            data: List of dictionaries
            group_by: Field to group by
            aggregate: Aggregation method (sum, count, avg)
        
        Returns:
            Summary report as list of dictionaries
        """
        if not data:
            return []
        
        groups = {}
        numeric_fields = []
        
        # Find numeric fields
        for key, value in data[0].items():
            if isinstance(value, (int, float)):
                numeric_fields.append(key)
        
        # Group data
        for record in data:
            key = record.get(group_by, 'Unknown')
            if key not in groups:
                groups[key] = {'count': 0, 'values': {}}
                for field in numeric_fields:
                    groups[key]['values'][field] = 0
                groups[key]['records'] = []
            
            groups[key]['count'] += 1
            groups[key]['records'].append(record)
            
            for field in numeric_fields:
                groups[key]['values'][field] += record.get(field, 0)
        
        # Create summary
        summary = []
        for key, group in groups.items():
            record = {group_by: key, 'count': group['count']}
            
            for field, value in group['values'].items():
                if aggregate == 'avg':
                    record[f'avg_{field}'] = round(value / group['count'], 2) if group['count'] > 0 else 0
                else:
                    record[f'total_{field}'] = round(value, 2)
            
            summary.append(record)
        
        return summary
    
    def create_pivot_report(self, data: List[Dict], rows: List[str], 
                            columns: List[str], value: str) -> List[Dict]:
        """
        Create pivot-like report
        
        Args:
            data: List of dictionaries
            rows: Row fields
            columns: Column fields
            value: Value field to aggregate
        
        Returns:
            Pivot report as list of dictionaries
        """
        pivot = {}
        
        for record in data:
            row_key = tuple(str(record.get(field, '')) for field in rows)
            col_key = tuple(str(record.get(field, '')) for field in columns)
            
            if row_key not in pivot:
                pivot[row_key] = {}
            
            if col_key not in pivot[row_key]:
                pivot[row_key][col_key] = {'count': 0, 'total': 0}
            
            pivot[row_key][col_key]['count'] += 1
            pivot[row_key][col_key]['total'] += record.get(value, 0)
        
        # Convert to list
        result = []
        for row_key, cols in pivot.items():
            record = dict(zip(rows, row_key))
            for col_key, values in cols.items():
                col_name = '_'.join(col_key) if len(col_key) > 1 else col_key[0]
                record[f'{col_name}_count'] = values['count']
                record[f'{col_name}_total'] = round(values['total'], 2)
            result.append(record)
        
        return result
    
    def generate_summary_stats(self, data: List[Dict]) -> Dict:
        """
        Generate summary statistics for numeric fields
        
        Args:
            data: List of dictionaries
        
        Returns:
            Dictionary with summary statistics
        """
        if not data:
            return {}
        
        stats = {'record_count': len(data)}
        
        numeric_fields = []
        for key, value in data[0].items():
            if isinstance(value, (int, float)):
                numeric_fields.append(key)
        
        for field in numeric_fields:
            values = [record.get(field, 0) for record in data if isinstance(record.get(field), (int, float))]
            
            if values:
                stats[f'{field}_min'] = min(values)
                stats[f'{field}_max'] = max(values)
                stats[f'{field}_avg'] = round(sum(values) / len(values), 2)
                stats[f'{field}_sum'] = round(sum(values), 2)
                stats[f'{field}_count'] = len(values)
        
        return stats
    
    def filter_report(self, data: List[Dict], filters: Dict) -> List[Dict]:
        """
        Filter data based on conditions
        
        Args:
            data: List of dictionaries
            filters: Dictionary of field: value pairs
        
        Returns:
            Filtered data
        """
        result = data
        for field, value in filters.items():
            result = [r for r in result if r.get(field) == value]
        return result
    
    def sort_report(self, data: List[Dict], field: str, reverse: bool = False) -> List[Dict]:
        """
        Sort data by field
        
        Args:
            data: List of dictionaries
            field: Field to sort by
            reverse: Reverse order
        
        Returns:
            Sorted data
        """
        return sorted(data, key=lambda x: x.get(field, 0) if isinstance(x.get(field), (int, float)) else str(x.get(field, '')), reverse=reverse)
    
    # ==================== EXPORT OPERATIONS ====================
    
    def export_to_csv(self, data: List[Dict], filename: str, 
                     headers: List[str] = None) -> bool:
        """Export data to CSV"""
        return self.write_csv(data, filename, headers)
    
    def export_to_json(self, data: List[Dict], filename: str) -> bool:
        """
        Export data to JSON
        
        Args:
            data: List of dictionaries
            filename: Output filename
        
        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"[OK] JSON saved to: {filename} ({len(data)} records)")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to write JSON: {e}")
            return False
    
    def export_to_html(self, data: List[Dict], filename: str, title: str = "Report") -> bool:
        """
        Export data to HTML table
        
        Args:
            data: List of dictionaries
            filename: Output filename
            title: Report title
        
        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
            
            if not data:
                print("[ERROR] No data to export")
                return False
            
            headers = list(data[0].keys())
            
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        tr:hover {{ background-color: #ddd; }}
        .summary {{ background-color: #f9f9f9; padding: 10px; margin-bottom: 20px; border: 1px solid #ddd; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="summary">
        <strong>Total Records:</strong> {len(data)}
    </div>
    <table>
        <thead>
            <tr>
"""
            
            for header in headers:
                html += f"                <th>{header}</th>\n"
            
            html += """            </tr>
        </thead>
        <tbody>
"""
            
            for record in data[:100]:
                html += "            <tr>\n"
                for header in headers:
                    html += f"                <td>{record.get(header, '')}</td>\n"
                html += "            </tr>\n"
            
            if len(data) > 100:
                html += f'            <tr><td colspan="{len(headers)}" style="text-align: center;"><em>... and {len(data) - 100} more records</em></td></tr>\n'
            
            html += """        </tbody>
    </table>
</body>
</html>
"""
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
            
            print(f"[OK] HTML saved to: {filename}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to write HTML: {e}")
            return False
