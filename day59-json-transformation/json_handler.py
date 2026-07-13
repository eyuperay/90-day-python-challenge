"""
JSON Handler Module
Handles JSON operations: read, write, transform, validate
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional


class JSONHandler:
    """Handler for JSON operations"""
    
    def __init__(self):
        self.data = None
        self.filename = None
    
    # ==================== READ OPERATIONS ====================
    
    def read_json(self, filename: str) -> Dict[str, Any]:
        """
        Read JSON from file
        
        Args:
            filename: Path to JSON file
        
        Returns:
            Dictionary with JSON data
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
                self.filename = filename
                print(f"[OK] Read JSON from: {filename}")
                return self.data
        except FileNotFoundError:
            print(f"[ERROR] File not found: {filename}")
            return {}
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON: {e}")
            return {}
    
    def read_json_string(self, json_string: str) -> Dict[str, Any]:
        """
        Read JSON from string
        
        Args:
            json_string: JSON string
        
        Returns:
            Dictionary with JSON data
        """
        try:
            self.data = json.loads(json_string)
            print("[OK] Read JSON from string")
            return self.data
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON string: {e}")
            return {}
    
    # ==================== WRITE OPERATIONS ====================
    
    def write_json(self, data: Dict[str, Any], filename: str, indent: int = 2) -> bool:
        """
        Write JSON to file
        
        Args:
            data: Data to write
            filename: Output filename
            indent: Indentation level
        
        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            print(f"[OK] Written JSON to: {filename}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to write JSON: {e}")
            return False
    
    def to_json_string(self, data: Dict[str, Any], indent: int = 2) -> str:
        """
        Convert data to JSON string
        
        Args:
            data: Data to convert
            indent: Indentation level
        
        Returns:
            JSON string
        """
        try:
            return json.dumps(data, indent=indent, ensure_ascii=False)
        except Exception as e:
            print(f"[ERROR] Failed to convert to JSON: {e}")
            return ""
    
    # ==================== TRANSFORM OPERATIONS ====================
    
    def flatten_json(self, data: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
        """
        Flatten nested JSON
        
        Args:
            data: Nested dictionary
            parent_key: Parent key for recursion
            sep: Separator for nested keys
        
        Returns:
            Flattened dictionary
        """
        items = []
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_json(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    def extract_fields(self, data: List[Dict], fields: List[str]) -> List[Dict]:
        """
        Extract specific fields from list of dictionaries
        
        Args:
            data: List of dictionaries
            fields: Fields to extract
        
        Returns:
            List of dictionaries with only specified fields
        """
        result = []
        for item in data:
            new_item = {field: item.get(field) for field in fields}
            result.append(new_item)
        return result
    
    def filter_data(self, data: List[Dict], key: str, value: Any) -> List[Dict]:
        """
        Filter data by key-value pair
        
        Args:
            data: List of dictionaries
            key: Key to filter by
            value: Value to match
        
        Returns:
            Filtered list
        """
        return [item for item in data if item.get(key) == value]
    
    def transform_keys(self, data: Dict, key_map: Dict[str, str]) -> Dict:
        """
        Transform dictionary keys
        
        Args:
            data: Original dictionary
            key_map: Mapping of old_key -> new_key
        
        Returns:
            Dictionary with transformed keys
        """
        result = {}
        for old_key, value in data.items():
            new_key = key_map.get(old_key, old_key)
            if isinstance(value, dict):
                result[new_key] = self.transform_keys(value, key_map)
            elif isinstance(value, list):
                result[new_key] = [
                    self.transform_keys(item, key_map) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                result[new_key] = value
        return result
    
    def add_timestamp(self, data: Dict) -> Dict:
        """
        Add timestamp to data
        
        Args:
            data: Original data
        
        Returns:
            Data with timestamp
        """
        result = data.copy()
        result['timestamp'] = datetime.now().isoformat()
        result['processed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return result
    
    def merge_json(self, data1: Dict, data2: Dict) -> Dict:
        """
        Merge two JSON objects
        
        Args:
            data1: First JSON object
            data2: Second JSON object
        
        Returns:
            Merged JSON object
        """
        result = data1.copy()
        for key, value in data2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self.merge_json(result[key], value)
            else:
                result[key] = value
        return result
    
    # ==================== VALIDATION OPERATIONS ====================
    
    def validate_schema(self, data: Dict, schema: Dict) -> List[str]:
        """
        Validate data against schema
        
        Args:
            data: Data to validate
            schema: Schema with required fields and types
        
        Returns:
            List of validation errors
        """
        errors = []
        
        for field, field_type in schema.items():
            if field not in data:
                errors.append(f"Missing required field: {field}")
            elif not isinstance(data[field], field_type):
                errors.append(f"Field '{field}' should be {field_type.__name__}, got {type(data[field]).__name__}")
        
        return errors
    
    def validate_required_fields(self, data: Dict, required_fields: List[str]) -> List[str]:
        """
        Validate required fields
        
        Args:
            data: Data to validate
            required_fields: List of required fields
        
        Returns:
            List of missing fields
        """
        return [field for field in required_fields if field not in data]
    
    # ==================== UTILITY OPERATIONS ====================
    
    def get_nested_value(self, data: Dict, path: str, default: Any = None) -> Any:
        """
        Get nested value using dot notation
        
        Args:
            data: Dictionary
            path: Dot-separated path (e.g., 'user.address.city')
            default: Default value if path not found
        
        Returns:
            Value at path or default
        """
        keys = path.split('.')
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        
        return current
    
    def set_nested_value(self, data: Dict, path: str, value: Any) -> Dict:
        """
        Set nested value using dot notation
        
        Args:
            data: Dictionary
            path: Dot-separated path
            value: Value to set
        
        Returns:
            Updated dictionary
        """
        keys = path.split('.')
        current = data
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
        return data
    
    def remove_empty_values(self, data: Dict) -> Dict:
        """
        Remove keys with None or empty values
        
        Args:
            data: Dictionary
        
        Returns:
            Dictionary with empty values removed
        """
        result = {}
        for key, value in data.items():
            if value is None or value == "" or value == [] or value == {}:
                continue
            if isinstance(value, dict):
                cleaned = self.remove_empty_values(value)
                if cleaned:
                    result[key] = cleaned
            else:
                result[key] = value
        return result
