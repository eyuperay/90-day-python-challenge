#!/usr/bin/env python3
"""
CLI Tool - Command Line Interface Tool
A versatile command-line tool with multiple subcommands
"""

import argparse
import os
import json
import sys
import random
import datetime
import textwrap
from typing import List, Dict, Any


class CLITool:
    """Main CLI tool class"""
    
    def __init__(self):
        self.parser = None
        self.subparsers = None
        self._setup_parser()
    
    def _setup_parser(self):
        """Setup argument parser"""
        self.parser = argparse.ArgumentParser(
            description="CLI Tool - A versatile command-line utility",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent("""
                Examples:
                  %(prog)s hello --name John
                  %(prog)s math add 5 3
                  %(prog)s file read data.txt
                  %(prog)s generate numbers --count 10
                  %(prog)s weather --city Istanbul
            """)
        )
        
        # Global options
        self.parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Enable verbose output'
        )
        
        self.parser.add_argument(
            '--version',
            action='version',
            version='CLI Tool v1.0.0'
        )
        
        # Subparsers
        self.subparsers = self.parser.add_subparsers(
            dest='command',
            title='Commands',
            description='Available commands',
            help='Command to execute'
        )
        
        # ==================== HELLO COMMAND ====================
        hello_parser = self.subparsers.add_parser(
            'hello',
            help='Say hello',
            description='Say hello to someone'
        )
        hello_parser.add_argument(
            '--name',
            type=str,
            default='World',
            help='Name to greet (default: World)'
        )
        hello_parser.add_argument(
            '-u', '--uppercase',
            action='store_true',
            help='Output in uppercase'
        )
        
        # ==================== MATH COMMAND ====================
        math_parser = self.subparsers.add_parser(
            'math',
            help='Mathematical operations',
            description='Perform mathematical operations'
        )
        math_subparsers = math_parser.add_subparsers(
            dest='operation',
            title='Math operations',
            description='Available math operations'
        )
        
        # Add
        add_parser = math_subparsers.add_parser('add', help='Add two numbers')
        add_parser.add_argument('a', type=float, help='First number')
        add_parser.add_argument('b', type=float, help='Second number')
        
        # Subtract
        sub_parser = math_subparsers.add_parser('sub', help='Subtract two numbers')
        sub_parser.add_argument('a', type=float, help='First number')
        sub_parser.add_argument('b', type=float, help='Second number')
        
        # Multiply
        mul_parser = math_subparsers.add_parser('mul', help='Multiply two numbers')
        mul_parser.add_argument('a', type=float, help='First number')
        mul_parser.add_argument('b', type=float, help='Second number')
        
        # Divide
        div_parser = math_subparsers.add_parser('div', help='Divide two numbers')
        div_parser.add_argument('a', type=float, help='Dividend')
        div_parser.add_argument('b', type=float, help='Divisor')
        
        # Power
        pow_parser = math_subparsers.add_parser('pow', help='Power of a number')
        pow_parser.add_argument('base', type=float, help='Base')
        pow_parser.add_argument('exponent', type=float, help='Exponent')
        
        # ==================== FILE COMMAND ====================
        file_parser = self.subparsers.add_parser(
            'file',
            help='File operations',
            description='Perform file operations'
        )
        file_subparsers = file_parser.add_subparsers(
            dest='operation',
            title='File operations',
            description='Available file operations'
        )
        
        # Read file
        read_parser = file_subparsers.add_parser('read', help='Read a file')
        read_parser.add_argument('filename', type=str, help='File to read')
        read_parser.add_argument(
            '-l', '--lines',
            type=int,
            help='Number of lines to display (default: all)'
        )
        
        # Write file
        write_parser = file_subparsers.add_parser('write', help='Write to a file')
        write_parser.add_argument('filename', type=str, help='File to write')
        write_parser.add_argument('content', type=str, help='Content to write')
        write_parser.add_argument(
            '-a', '--append',
            action='store_true',
            help='Append to file instead of overwriting'
        )
        
        # List files
        list_parser = file_subparsers.add_parser('list', help='List files')
        list_parser.add_argument(
            '-p', '--path',
            type=str,
            default='.',
            help='Directory path (default: current)'
        )
        list_parser.add_argument(
            '--json',
            action='store_true',
            help='Output in JSON format'
        )
        
        # ==================== GENERATE COMMAND ====================
        gen_parser = self.subparsers.add_parser(
            'generate',
            help='Generate data',
            description='Generate random data'
        )
        gen_subparsers = gen_parser.add_subparsers(
            dest='type',
            title='Data types',
            description='Types of data to generate'
        )
        
        # Generate numbers
        num_parser = gen_subparsers.add_parser('numbers', help='Generate random numbers')
        num_parser.add_argument(
            '-c', '--count',
            type=int,
            default=5,
            help='Number of random numbers (default: 5)'
        )
        num_parser.add_argument(
            '-m', '--min',
            type=int,
            default=1,
            help='Minimum value (default: 1)'
        )
        num_parser.add_argument(
            '-M', '--max',
            type=int,
            default=100,
            help='Maximum value (default: 100)'
        )
        
        # Generate password
        pwd_parser = gen_subparsers.add_parser('password', help='Generate random password')
        pwd_parser.add_argument(
            '-l', '--length',
            type=int,
            default=12,
            help='Password length (default: 12)'
        )
        pwd_parser.add_argument(
            '--no-special',
            action='store_true',
            help='Exclude special characters'
        )
        pwd_parser.add_argument(
            '--no-digits',
            action='store_true',
            help='Exclude digits'
        )
        
        # Generate UUID
        uuid_parser = gen_subparsers.add_parser('uuid', help='Generate UUID')
        uuid_parser.add_argument(
            '-c', '--count',
            type=int,
            default=1,
            help='Number of UUIDs to generate (default: 1)'
        )
        
        # ==================== WEATHER COMMAND ====================
        weather_parser = self.subparsers.add_parser(
            'weather',
            help='Weather information (demo)',
            description='Get weather information for a city'
        )
        weather_parser.add_argument(
            '--city',
            type=str,
            default='Istanbul',
            help='City name (default: Istanbul)'
        )
        weather_parser.add_argument(
            '--days',
            type=int,
            default=3,
            help='Number of days forecast (default: 3)'
        )
        
        # ==================== SYSTEM COMMAND ====================
        sys_parser = self.subparsers.add_parser(
            'system',
            help='System information',
            description='Get system information'
        )
        sys_subparsers = sys_parser.add_subparsers(
            dest='operation',
            title='System operations',
            description='Available system operations'
        )
        
        # Info
        info_parser = sys_subparsers.add_parser('info', help='Show system info')
        info_parser.add_argument(
            '--json',
            action='store_true',
            help='Output in JSON format'
        )
        
        # Time
        time_parser = sys_subparsers.add_parser('time', help='Show current time')
        time_parser.add_argument(
            '-f', '--format',
            type=str,
            default='%Y-%m-%d %H:%M:%S',
            help='Time format (default: %%Y-%%m-%%d %%H:%%M:%%S)'
        )
        
        # ==================== CONVERT COMMAND ====================
        convert_parser = self.subparsers.add_parser(
            'convert',
            help='Convert units',
            description='Convert between units'
        )
        convert_subparsers = convert_parser.add_subparsers(
            dest='type',
            title='Conversion types',
            description='Available conversions'
        )
        
        # Temperature
        temp_parser = convert_subparsers.add_parser('temp', help='Convert temperature')
        temp_parser.add_argument('value', type=float, help='Temperature value')
        temp_parser.add_argument(
            '-f', '--from',
            dest='from_unit',
            choices=['C', 'F', 'K'],
            default='C',
            help='Source unit (C, F, K) default: C'
        )
        temp_parser.add_argument(
            '-t', '--to',
            dest='to_unit',
            choices=['C', 'F', 'K'],
            default='F',
            help='Target unit (C, F, K) default: F'
        )
        
        # Length
        len_parser = convert_subparsers.add_parser('length', help='Convert length')
        len_parser.add_argument('value', type=float, help='Length value')
        len_parser.add_argument(
            '-f', '--from',
            dest='from_unit',
            choices=['m', 'km', 'cm', 'mm', 'ft', 'in', 'yd', 'mi'],
            default='m',
            help='Source unit (default: m)'
        )
        len_parser.add_argument(
            '-t', '--to',
            dest='to_unit',
            choices=['m', 'km', 'cm', 'mm', 'ft', 'in', 'yd', 'mi'],
            default='km',
            help='Target unit (default: km)'
        )
    
    def run(self, args: List[str] = None):
        """Run the CLI tool"""
        if args is None:
            args = sys.argv[1:]
        
        parsed_args = self.parser.parse_args(args)
        
        if not parsed_args.command:
            self.parser.print_help()
            return
        
        # Execute command
        command = parsed_args.command
        verbose = getattr(parsed_args, 'verbose', False)
        
        if verbose:
            print(f"[Verbose] Executing command: {command}")
        
        # Route to appropriate handler
        handlers = {
            'hello': self._handle_hello,
            'math': self._handle_math,
            'file': self._handle_file,
            'generate': self._handle_generate,
            'weather': self._handle_weather,
            'system': self._handle_system,
            'convert': self._handle_convert,
        }
        
        handler = handlers.get(command)
        if handler:
            handler(parsed_args, verbose)
        else:
            print(f"Unknown command: {command}")
    
    # ==================== HANDLERS ====================
    
    def _handle_hello(self, args, verbose):
        """Handle hello command"""
        message = f"Hello, {args.name}!"
        if args.uppercase:
            message = message.upper()
        print(message)
    
    def _handle_math(self, args, verbose):
        """Handle math command"""
        result = None
        op = args.operation
        
        if op == 'add':
            result = args.a + args.b
            expression = f"{args.a} + {args.b} = {result}"
        elif op == 'sub':
            result = args.a - args.b
            expression = f"{args.a} - {args.b} = {result}"
        elif op == 'mul':
            result = args.a * args.b
            expression = f"{args.a} * {args.b} = {result}"
        elif op == 'div':
            if args.b == 0:
                print("Error: Division by zero!")
                return
            result = args.a / args.b
            expression = f"{args.a} / {args.b} = {result}"
        elif op == 'pow':
            result = args.base ** args.exponent
            expression = f"{args.base} ^ {args.exponent} = {result}"
        else:
            print(f"Unknown math operation: {op}")
            return
        
        if verbose:
            print(f"[Verbose] Operation: {op}")
            print(f"[Verbose] Result: {result}")
        
        print(f"Result: {result}")
    
    def _handle_file(self, args, verbose):
        """Handle file command"""
        op = args.operation
        
        if op == 'read':
            try:
                with open(args.filename, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                if args.lines:
                    lines = lines[:args.lines]
                
                print(''.join(lines))
                
                if verbose:
                    print(f"[Verbose] Read {len(lines)} lines")
                    
            except FileNotFoundError:
                print(f"Error: File '{args.filename}' not found")
            except Exception as e:
                print(f"Error: {e}")
        
        elif op == 'write':
            try:
                mode = 'a' if args.append else 'w'
                os.makedirs(os.path.dirname(args.filename) or '.', exist_ok=True)
                
                with open(args.filename, mode, encoding='utf-8') as f:
                    f.write(args.content + '\n')
                
                action = "Appended to" if args.append else "Written to"
                print(f"{action}: {args.filename}")
                
                if verbose:
                    print(f"[Verbose] Content length: {len(args.content)}")
                    
            except Exception as e:
                print(f"Error: {e}")
        
        elif op == 'list':
            path = args.path
            try:
                items = os.listdir(path)
                files = []
                dirs = []
                
                for item in items:
                    full_path = os.path.join(path, item)
                    if os.path.isdir(full_path):
                        dirs.append(item)
                    else:
                        files.append(item)
                
                if args.json:
                    result = {
                        'path': path,
                        'directories': sorted(dirs),
                        'files': sorted(files),
                        'total': len(items)
                    }
                    print(json.dumps(result, indent=2))
                else:
                    print(f"Directory: {path}")
                    print(f"Total: {len(items)} items")
                    if dirs:
                        print(f"\nDirectories ({len(dirs)}):")
                        for d in sorted(dirs):
                            print(f"  [DIR] {d}")
                    if files:
                        print(f"\nFiles ({len(files)}):")
                        for f in sorted(files):
                            print(f"  [FILE] {f}")
                            
            except FileNotFoundError:
                print(f"Error: Directory '{path}' not found")
            except Exception as e:
                print(f"Error: {e}")
        
        else:
            print(f"Unknown file operation: {op}")
    
    def _handle_generate(self, args, verbose):
        """Handle generate command"""
        data_type = args.type
        
        if data_type == 'numbers':
            numbers = [random.randint(args.min, args.max) for _ in range(args.count)]
            print(f"Random numbers ({args.count}):")
            print(', '.join(str(n) for n in numbers))
            print(f"Min: {min(numbers)}, Max: {max(numbers)}, Avg: {sum(numbers)/len(numbers):.2f}")
        
        elif data_type == 'password':
            import string
            chars = string.ascii_letters
            
            if not args.no_digits:
                chars += string.digits
            if not args.no_special:
                chars += string.punctuation
            
            password = ''.join(random.choice(chars) for _ in range(args.length))
            print(f"Generated password ({args.length} chars):")
            print(password)
            
            if verbose:
                print(f"[Verbose] Character set size: {len(chars)}")
        
        elif data_type == 'uuid':
            import uuid
            for i in range(args.count):
                print(uuid.uuid4())
        
        else:
            print(f"Unknown generate type: {data_type}")
    
    def _handle_weather(self, args, verbose):
        """Handle weather command (demo)"""
        import textwrap
        conditions = ['Sunny', 'Partly Cloudy', 'Cloudy', 'Rainy', 'Stormy']
        temps = list(range(15, 35))
        
        print(f"Weather forecast for {args.city}:")
        print("-" * 40)
        
        for i in range(args.days):
            day = datetime.datetime.now() + datetime.timedelta(days=i)
            temp = random.choice(temps)
            condition = random.choice(conditions)
            humidity = random.randint(40, 90)
            wind = random.randint(5, 30)
            
            print(f"  Day {i+1} ({day.strftime('%Y-%m-%d')}):")
            print(f"    Condition: {condition}")
            print(f"    Temp: {temp}°C")
            print(f"    Humidity: {humidity}%")
            print(f"    Wind: {wind} km/h")
        
        if verbose:
            print(f"[Verbose] Forecast for {args.days} days")
    
    def _handle_system(self, args, verbose):
        """Handle system command"""
        import platform
        
        op = args.operation
        
        if op == 'info':
            info = {
                'system': platform.system(),
                'node': platform.node(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'python_version': sys.version,
                'python_implementation': platform.python_implementation()
            }
            
            if args.json:
                print(json.dumps(info, indent=2))
            else:
                print("System Information:")
                print("-" * 40)
                for key, value in info.items():
                    print(f"  {key}: {value}")
        
        elif op == 'time':
            now = datetime.datetime.now()
            print(now.strftime(args.format))
        
        else:
            print(f"Unknown system operation: {op}")
    
    def _handle_convert(self, args, verbose):
        """Handle convert command"""
        conv_type = args.type
        
        if conv_type == 'temp':
            value = args.value
            from_unit = args.from_unit
            to_unit = args.to_unit
            
            # Convert to Celsius first
            if from_unit == 'C':
                celsius = value
            elif from_unit == 'F':
                celsius = (value - 32) * 5/9
            elif from_unit == 'K':
                celsius = value - 273.15
            else:
                print(f"Unknown unit: {from_unit}")
                return
            
            # Convert from Celsius to target
            if to_unit == 'C':
                result = celsius
            elif to_unit == 'F':
                result = celsius * 9/5 + 32
            elif to_unit == 'K':
                result = celsius + 273.15
            else:
                print(f"Unknown unit: {to_unit}")
                return
            
            print(f"{value}°{from_unit} = {result:.2f}°{to_unit}")
        
        elif conv_type == 'length':
            value = args.value
            from_unit = args.from_unit
            to_unit = args.to_unit
            
            # Conversion factors to meters
            factors = {
                'm': 1,
                'km': 1000,
                'cm': 0.01,
                'mm': 0.001,
                'ft': 0.3048,
                'in': 0.0254,
                'yd': 0.9144,
                'mi': 1609.344
            }
            
            if from_unit not in factors or to_unit not in factors:
                print(f"Error: Invalid unit")
                return
            
            # Convert to meters then to target
            meters = value * factors[from_unit]
            result = meters / factors[to_unit]
            
            print(f"{value} {from_unit} = {result:.4f} {to_unit}")
        
        else:
            print(f"Unknown conversion type: {conv_type}")


def main():
    """Main entry point"""
    tool = CLITool()
    tool.run()


if __name__ == "__main__":
    main()
