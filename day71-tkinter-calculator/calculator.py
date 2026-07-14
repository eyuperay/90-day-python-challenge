#!/usr/bin/env python3
"""
Day 71 - Tkinter Calculator
Simple calculator with GUI using tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math


class Calculator:
    """Calculator GUI application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#2c3e50')
        
        # Variables
        self.current = ""
        self.expression = ""
        self.result = ""
        self.memory = 0
        self.new_calculation = True
        
        # Create UI
        self.create_widgets()
        
        # Keyboard bindings
        self.bind_keys()
    
    def create_widgets(self):
        """Create all widgets"""
        # Display frame
        display_frame = tk.Frame(self.root, bg='#34495e', height=120)
        display_frame.pack(fill=tk.X, padx=10, pady=10)
        display_frame.pack_propagate(False)
        
        # Expression display
        self.expression_var = tk.StringVar()
        self.expression_var.set("")
        self.expression_label = tk.Label(
            display_frame,
            textvariable=self.expression_var,
            font=('Arial', 14),
            bg='#34495e',
            fg='#95a5a6',
            anchor='e',
            height=1
        )
        self.expression_label.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        # Result display
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        self.result_label = tk.Label(
            display_frame,
            textvariable=self.result_var,
            font=('Arial', 32, 'bold'),
            bg='#34495e',
            fg='#ecf0f1',
            anchor='e',
            height=1
        )
        self.result_label.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg='#2c3e50')
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Button layout
        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '−'],
            ['1', '2', '3', '+'],
            ['0', '.', '=', '⌫']
        ]
        
        # Button colors
        colors = {
            'number': '#3498db',
            'operator': '#e67e22',
            'function': '#95a5a6',
            'equals': '#2ecc71'
        }
        
        # Create buttons
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                if text == '0':
                    # Zero button spans 2 columns
                    btn = tk.Button(
                        buttons_frame,
                        text=text,
                        font=('Arial', 20, 'bold'),
                        bg=colors['number'],
                        fg='white',
                        relief=tk.FLAT,
                        command=lambda t=text: self.on_button_click(t)
                    )
                    btn.grid(row=i+1, column=j, columnspan=2, sticky='nsew', padx=2, pady=2)
                else:
                    if text in ['C', '±', '%', '⌫']:
                        color = colors['function']
                    elif text in ['÷', '×', '−', '+', '=']:
                        color = colors['operator'] if text != '=' else colors['equals']
                    else:
                        color = colors['number']
                    
                    btn = tk.Button(
                        buttons_frame,
                        text=text,
                        font=('Arial', 20, 'bold'),
                        bg=color,
                        fg='white',
                        relief=tk.FLAT,
                        command=lambda t=text: self.on_button_click(t)
                    )
                    
                    # Adjust grid for zero button
                    if text == '0':
                        btn.grid(row=i+1, column=j, columnspan=2, sticky='nsew', padx=2, pady=2)
                    else:
                        btn.grid(row=i+1, column=j, sticky='nsew', padx=2, pady=2)
        
        # Configure grid weights
        for i in range(6):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.grid_columnconfigure(j, weight=1)
    
    def bind_keys(self):
        """Bind keyboard keys"""
        self.root.bind('<Key>', self.on_key_press)
        self.root.bind('<Return>', lambda e: self.on_button_click('='))
        self.root.bind('<BackSpace>', lambda e: self.on_button_click('⌫'))
        self.root.bind('<Escape>', lambda e: self.on_button_click('C'))
    
    def on_key_press(self, event):
        """Handle keyboard input"""
        key = event.char
        if key in '0123456789':
            self.on_button_click(key)
        elif key in '+-*/':
            if key == '*':
                self.on_button_click('×')
            elif key == '/':
                self.on_button_click('÷')
            else:
                self.on_button_click(key)
        elif key == '.':
            self.on_button_click('.')
        elif key == '=':
            self.on_button_click('=')
        elif key == '\x08':  # Backspace
            self.on_button_click('⌫')
    
    def on_button_click(self, value):
        """Handle button clicks"""
        if value == 'C':
            self.clear()
        elif value == '⌫':
            self.backspace()
        elif value == '=':
            self.calculate()
        elif value in ['+', '−', '×', '÷']:
            self.add_operator(value)
        elif value == '±':
            self.toggle_sign()
        elif value == '%':
            self.percentage()
        elif value == '.':
            self.add_decimal()
        else:  # Numbers
            self.add_number(value)
    
    def clear(self):
        """Clear all"""
        self.current = ""
        self.expression = ""
        self.result = ""
        self.new_calculation = True
        self.update_display()
    
    def backspace(self):
        """Remove last character"""
        if self.new_calculation:
            self.clear()
        else:
            self.current = self.current[:-1]
            self.update_display()
    
    def add_number(self, value):
        """Add number to current"""
        if self.new_calculation:
            self.current = ""
            self.expression = ""
            self.new_calculation = False
        
        # Limit to 15 characters
        if len(self.current) >= 15:
            return
        
        # Prevent multiple leading zeros
        if self.current == "0" and value != ".":
            self.current = value
        else:
            self.current += value
        
        self.update_display()
    
    def add_decimal(self):
        """Add decimal point"""
        if self.new_calculation:
            self.current = "0."
            self.expression = ""
            self.new_calculation = False
            self.update_display()
            return
        
        if "." not in self.current:
            self.current += "."
            self.update_display()
    
    def add_operator(self, operator):
        """Add operator"""
        if self.current == "" and not self.expression:
            return
        
        if self.expression and self.current:
            self.calculate()
        
        if self.result:
            self.current = self.result
            self.result = ""
        
        self.expression = self.current + " " + operator + " "
        self.current = ""
        self.new_calculation = False
        self.update_display()
    
    def toggle_sign(self):
        """Toggle positive/negative"""
        if self.current == "":
            return
        
        if self.current.startswith("-"):
            self.current = self.current[1:]
        else:
            self.current = "-" + self.current
        
        self.update_display()
    
    def percentage(self):
        """Calculate percentage"""
        if self.current == "":
            return
        
        try:
            num = float(self.current)
            self.current = str(num / 100)
            self.update_display()
        except ValueError:
            pass
    
    def calculate(self):
        """Calculate the result"""
        if self.current == "" and not self.expression:
            return
        
        if self.expression == "" and self.current:
            self.result = self.current
            self.current = ""
            self.update_display()
            return
        
        if not self.expression:
            return
        
        try:
            # Build expression
            expr = self.expression + self.current
            
            # Replace symbols
            expr = expr.replace('×', '*')
            expr = expr.replace('÷', '/')
            expr = expr.replace('−', '-')
            
            # Calculate
            result = eval(expr)
            
            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            
            self.result = str(result)
            self.expression = self.expression + self.current + " ="
            self.current = str(result)
            self.new_calculation = True
            self.update_display()
            
        except ZeroDivisionError:
            messagebox.showerror("Error", "Cannot divide by zero!")
            self.clear()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid expression: {e}")
            self.clear()
    
    def update_display(self):
        """Update display labels"""
        # Update expression
        if self.expression:
            self.expression_var.set(self.expression)
        else:
            self.expression_var.set("")
        
        # Update result
        if self.current:
            display_text = self.current
            # Format large numbers
            try:
                num = float(display_text)
                if num.is_integer():
                    display_text = str(int(num))
                else:
                    # Limit decimal places
                    display_text = f"{num:.10g}"
            except:
                pass
            self.result_var.set(display_text)
        else:
            self.result_var.set("0")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
