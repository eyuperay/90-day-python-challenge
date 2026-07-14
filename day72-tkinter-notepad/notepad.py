#!/usr/bin/env python3
"""
Day 72 - Tkinter Notepad
Simple text editor with GUI using tkinter
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
from datetime import datetime


class Notepad:
    """Notepad application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Notepad")
        self.root.geometry("800x600")
        self.root.minsize(400, 300)
        
        # Variables
        self.current_file = None
        self.modified = False
        
        # Set icon (optional)
        try:
            self.root.iconbitmap(default='notepad.ico')
        except:
            pass
        
        # Create UI
        self.create_menu()
        self.create_toolbar()
        self.create_text_area()
        self.create_status_bar()
        
        # Bind events
        self.bind_events()
        
        # New file
        self.new_file()
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Print", command=self.print_file, accelerator="Ctrl+P")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app, accelerator="Ctrl+Q")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        edit_menu.add_command(label="Delete", command=self.delete_selected, accelerator="Del")
        edit_menu.add_separator()
        edit_menu.add_command(label="Find", command=self.find_text, accelerator="Ctrl+F")
        edit_menu.add_command(label="Replace", command=self.replace_text, accelerator="Ctrl+H")
        edit_menu.add_separator()
        edit_menu.add_command(label="Clear All", command=self.clear_all)
        
        # Format menu
        format_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Format", menu=format_menu)
        format_menu.add_command(label="Word Wrap", command=self.toggle_word_wrap)
        format_menu.add_command(label="Font Size", command=self.change_font_size)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toolbar", command=self.toggle_toolbar)
        view_menu.add_command(label="Status Bar", command=self.toggle_status_bar)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Shortcuts", command=self.show_shortcuts)
    
    def create_toolbar(self):
        """Create toolbar"""
        self.toolbar = tk.Frame(self.root, bg='#f0f0f0', relief=tk.RAISED, bd=1)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Toolbar buttons
        buttons = [
            ('📄 New', self.new_file),
            ('📂 Open', self.open_file),
            ('💾 Save', self.save_file),
            ('🖨 Print', self.print_file),
            ('✂ Cut', self.cut),
            ('📋 Copy', self.copy),
            ('📥 Paste', self.paste)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                self.toolbar,
                text=text,
                command=command,
                bg='#f0f0f0',
                relief=tk.FLAT,
                padx=10,
                pady=5,
                font=('Arial', 9)
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Separator
        separator = tk.Frame(self.toolbar, bg='#cccccc', width=1, height=30)
        separator.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Undo/Redo
        btn_undo = tk.Button(
            self.toolbar,
            text='↩ Undo',
            command=self.undo,
            bg='#f0f0f0',
            relief=tk.FLAT,
            padx=10,
            pady=5,
            font=('Arial', 9)
        )
        btn_undo.pack(side=tk.LEFT, padx=2, pady=2)
        
        btn_redo = tk.Button(
            self.toolbar,
            text='↪ Redo',
            command=self.redo,
            bg='#f0f0f0',
            relief=tk.FLAT,
            padx=10,
            pady=5,
            font=('Arial', 9)
        )
        btn_redo.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Search
        separator2 = tk.Frame(self.toolbar, bg='#cccccc', width=1, height=30)
        separator2.pack(side=tk.LEFT, padx=5, pady=2)
        
        btn_find = tk.Button(
            self.toolbar,
            text='🔍 Find',
            command=self.find_text,
            bg='#f0f0f0',
            relief=tk.FLAT,
            padx=10,
            pady=5,
            font=('Arial', 9)
        )
        btn_find.pack(side=tk.LEFT, padx=2, pady=2)
    
    def create_text_area(self):
        """Create text area"""
        self.text_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            font=('Consolas', 12),
            undo=True,
            autoseparators=True,
            maxundo=100
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = tk.Frame(self.root, bg='#f0f0f0', relief=tk.SUNKEN, bd=1)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Left status
        self.status_left = tk.Label(
            self.status_bar,
            text="Ready",
            bg='#f0f0f0',
            anchor=tk.W,
            padx=5
        )
        self.status_left.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Right status
        self.status_right = tk.Label(
            self.status_bar,
            text="Ln: 1, Col: 1",
            bg='#f0f0f0',
            anchor=tk.E,
            padx=5
        )
        self.status_right.pack(side=tk.RIGHT)
        
        # Word wrap status
        self.status_wrap = tk.Label(
            self.status_bar,
            text="Wrap: ON",
            bg='#f0f0f0',
            anchor=tk.E,
            padx=5
        )
        self.status_wrap.pack(side=tk.RIGHT)
    
    def bind_events(self):
        """Bind keyboard events"""
        self.text_area.bind('<KeyRelease>', self.on_text_change)
        self.text_area.bind('<Control-s>', lambda e: self.save_file())
        self.text_area.bind('<Control-S>', lambda e: self.save_as_file())
        self.text_area.bind('<Control-o>', lambda e: self.open_file())
        self.text_area.bind('<Control-O>', lambda e: self.open_file())
        self.text_area.bind('<Control-n>', lambda e: self.new_file())
        self.text_area.bind('<Control-N>', lambda e: self.new_file())
        self.text_area.bind('<Control-q>', lambda e: self.exit_app())
        self.text_area.bind('<Control-Q>', lambda e: self.exit_app())
        self.text_area.bind('<Control-p>', lambda e: self.print_file())
        self.text_area.bind('<Control-P>', lambda e: self.print_file())
        self.text_area.bind('<Control-z>', lambda e: self.undo())
        self.text_area.bind('<Control-Z>', lambda e: self.undo())
        self.text_area.bind('<Control-y>', lambda e: self.redo())
        self.text_area.bind('<Control-Y>', lambda e: self.redo())
        self.text_area.bind('<Control-f>', lambda e: self.find_text())
        self.text_area.bind('<Control-F>', lambda e: self.find_text())
        self.text_area.bind('<Control-h>', lambda e: self.replace_text())
        self.text_area.bind('<Control-H>', lambda e: self.replace_text())
        
        # Update cursor position on click/release
        self.text_area.bind('<Button-1>', self.update_cursor_position)
        self.text_area.bind('<KeyRelease>', self.update_cursor_position)
    
    def update_cursor_position(self, event=None):
        """Update cursor position in status bar"""
        try:
            index = self.text_area.index(tk.INSERT)
            line, col = index.split('.')
            self.status_right.config(text=f"Ln: {line}, Col: {int(col)+1}")
        except:
            pass
    
    def on_text_change(self, event=None):
        """Handle text changes"""
        if not self.modified:
            self.modified = True
            self.update_title()
            self.status_left.config(text="Modified")
    
    def update_title(self):
        """Update window title"""
        title = "Notepad"
        if self.current_file:
            filename = os.path.basename(self.current_file)
            title = f"{filename} - Notepad"
        if self.modified:
            title = f"* {title}"
        self.root.title(title)
    
    # ==================== FILE OPERATIONS ====================
    
    def new_file(self):
        """Create a new file"""
        if self.modified and not self.confirm_save():
            return
        
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.modified = False
        self.update_title()
        self.status_left.config(text="New file created")
    
    def open_file(self):
        """Open a file"""
        if self.modified and not self.confirm_save():
            return
        
        file_path = filedialog.askopenfilename(
            title="Open File",
            filetypes=[
                ("Text Files", "*.txt"),
                ("Python Files", "*.py"),
                ("HTML Files", "*.html *.htm"),
                ("Markdown Files", "*.md"),
                ("All Files", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, content)
            self.current_file = file_path
            self.modified = False
            self.update_title()
            self.status_left.config(text=f"Opened: {os.path.basename(file_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file:\n{e}")
    
    def save_file(self):
        """Save the file"""
        if self.current_file:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.modified = False
                self.update_title()
                self.status_left.config(text=f"Saved: {os.path.basename(self.current_file)}")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")
                return False
        else:
            return self.save_as_file()
    
    def save_as_file(self):
        """Save as a new file"""
        file_path = filedialog.asksaveasfilename(
            title="Save As",
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("Python Files", "*.py"),
                ("HTML Files", "*.html"),
                ("Markdown Files", "*.md"),
                ("All Files", "*.*")
            ]
        )
        
        if not file_path:
            return False
        
        self.current_file = file_path
        return self.save_file()
    
    def print_file(self):
        """Print the file"""
        try:
            import subprocess
            import tempfile
            
            # Save temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(self.text_area.get(1.0, tk.END))
                temp_file = f.name
            
            # Open with default application
            subprocess.run(['notepad', '/p', temp_file], shell=True)
            
            self.status_left.config(text="Printing...")
            
        except Exception as e:
            messagebox.showinfo("Print", "Print functionality:\nSave file and print manually.")
    
    # ==================== EDIT OPERATIONS ====================
    
    def undo(self):
        """Undo"""
        try:
            self.text_area.edit_undo()
            self.status_left.config(text="Undo")
        except:
            pass
    
    def redo(self):
        """Redo"""
        try:
            self.text_area.edit_redo()
            self.status_left.config(text="Redo")
        except:
            pass
    
    def cut(self):
        """Cut selected text"""
        self.text_area.event_generate("<<Cut>>")
        self.status_left.config(text="Cut")
    
    def copy(self):
        """Copy selected text"""
        self.text_area.event_generate("<<Copy>>")
        self.status_left.config(text="Copied")
    
    def paste(self):
        """Paste text"""
        self.text_area.event_generate("<<Paste>>")
        self.status_left.config(text="Pasted")
    
    def select_all(self):
        """Select all text"""
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)
        self.status_left.config(text="All selected")
    
    def delete_selected(self):
        """Delete selected text"""
        self.text_area.event_generate("<<Clear>>")
        self.status_left.config(text="Deleted")
    
    def clear_all(self):
        """Clear all text"""
        if messagebox.askyesno("Clear All", "Are you sure you want to clear all text?"):
            self.text_area.delete(1.0, tk.END)
            self.status_left.config(text="Cleared all")
    
    def find_text(self):
        """Find text dialog"""
        find_window = tk.Toplevel(self.root)
        find_window.title("Find")
        find_window.geometry("400x150")
        find_window.resizable(False, False)
        find_window.transient(self.root)
        find_window.grab_set()
        
        tk.Label(find_window, text="Find:").pack(pady=5)
        find_entry = tk.Entry(find_window, width=40)
        find_entry.pack(pady=5)
        find_entry.focus()
        
        def find():
            text = find_entry.get()
            if not text:
                return
            
            # Remove previous tags
            self.text_area.tag_remove('found', '1.0', tk.END)
            
            # Find and highlight
            start = '1.0'
            count = 0
            while True:
                start = self.text_area.search(text, start, stopindex=tk.END)
                if not start:
                    break
                end = f"{start}+{len(text)}c"
                self.text_area.tag_add('found', start, end)
                self.text_area.tag_config('found', background='yellow')
                start = end
                count += 1
            
            if count == 0:
                messagebox.showinfo("Find", f"'{text}' not found")
            else:
                self.status_left.config(text=f"Found {count} matches")
        
        def close():
            self.text_area.tag_remove('found', '1.0', tk.END)
            find_window.destroy()
        
        tk.Button(find_window, text="Find", command=find, width=15).pack(pady=5)
        tk.Button(find_window, text="Close", command=close, width=15).pack()
        
        find_window.bind('<Return>', lambda e: find())
        find_window.bind('<Escape>', lambda e: close())
    
    def replace_text(self):
        """Replace text dialog"""
        replace_window = tk.Toplevel(self.root)
        replace_window.title("Replace")
        replace_window.geometry("400x250")
        replace_window.resizable(False, False)
        replace_window.transient(self.root)
        replace_window.grab_set()
        
        tk.Label(replace_window, text="Find:").pack(pady=2)
        find_entry = tk.Entry(replace_window, width=40)
        find_entry.pack(pady=5)
        
        tk.Label(replace_window, text="Replace with:").pack(pady=2)
        replace_entry = tk.Entry(replace_window, width=40)
        replace_entry.pack(pady=5)
        
        def replace_all():
            find_text = find_entry.get()
            replace_text = replace_entry.get()
            
            if not find_text:
                return
            
            content = self.text_area.get(1.0, tk.END)
            count = content.count(find_text)
            
            if count == 0:
                messagebox.showinfo("Replace", f"'{find_text}' not found")
                return
            
            new_content = content.replace(find_text, replace_text)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, new_content)
            self.modified = True
            self.update_title()
            self.status_left.config(text=f"Replaced {count} occurrences")
            messagebox.showinfo("Replace", f"Replaced {count} occurrences")
        
        def close():
            replace_window.destroy()
        
        btn_frame = tk.Frame(replace_window)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Replace All", command=replace_all, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Close", command=close, width=15).pack(side=tk.LEFT, padx=5)
        
        replace_window.bind('<Return>', lambda e: replace_all())
        replace_window.bind('<Escape>', lambda e: close())
    
    # ==================== FORMAT OPERATIONS ====================
    
    def toggle_word_wrap(self):
        """Toggle word wrap"""
        current_wrap = self.text_area.cget('wrap')
        if current_wrap == 'WORD':
            self.text_area.config(wrap='NONE')
            self.status_wrap.config(text="Wrap: OFF")
        else:
            self.text_area.config(wrap='WORD')
            self.status_wrap.config(text="Wrap: ON")
    
    def toggle_toolbar(self):
        """Toggle toolbar visibility"""
        if self.toolbar.winfo_ismapped():
            self.toolbar.pack_forget()
        else:
            self.toolbar.pack(side=tk.TOP, fill=tk.X)
    
    def toggle_status_bar(self):
        """Toggle status bar visibility"""
        if self.status_bar.winfo_ismapped():
            self.status_bar.pack_forget()
        else:
            self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def change_font_size(self):
        """Change font size"""
        size_window = tk.Toplevel(self.root)
        size_window.title("Font Size")
        size_window.geometry("300x150")
        size_window.resizable(False, False)
        size_window.transient(self.root)
        size_window.grab_set()
        
        tk.Label(size_window, text="Font Size (points):").pack(pady=10)
        
        current_size = 12
        font = self.text_area.cget('font')
        if font and isinstance(font, tuple) and len(font) > 1:
            try:
                current_size = int(font[1])
            except:
                pass
        
        size_var = tk.IntVar(value=current_size)
        size_spin = tk.Spinbox(
            size_window,
            from_=8,
            to=72,
            textvariable=size_var,
            width=10
        )
        size_spin.pack(pady=10)
        
        def apply_font():
            size = size_var.get()
            font = ('Consolas', size)
            self.text_area.config(font=font)
            size_window.destroy()
        
        tk.Button(size_window, text="Apply", command=apply_font, width=15).pack(pady=10)
    
    # ==================== HELP OPERATIONS ====================
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About Notepad",
            "Notepad\n\n"
            "Version: 1.0\n"
            "Created with Python Tkinter\n\n"
            "A simple text editor with basic features."
        )
    
    def show_shortcuts(self):
        """Show shortcuts dialog"""
        shortcuts = """
        Keyboard Shortcuts:
        
        File:
        Ctrl+N  - New File
        Ctrl+O  - Open File
        Ctrl+S  - Save File
        Ctrl+Shift+S - Save As
        Ctrl+P  - Print
        Ctrl+Q  - Exit
        
        Edit:
        Ctrl+Z  - Undo
        Ctrl+Y  - Redo
        Ctrl+X  - Cut
        Ctrl+C  - Copy
        Ctrl+V  - Paste
        Ctrl+A  - Select All
        Ctrl+F  - Find
        Ctrl+H  - Replace
        
        Other:
        Delete  - Delete Selected
        Esc     - Close Dialog
        """
        
        messagebox.showinfo("Keyboard Shortcuts", shortcuts)
    
    # ==================== UTILITY OPERATIONS ====================
    
    def confirm_save(self):
        """Confirm save before closing"""
        response = messagebox.askyesnocancel(
            "Notepad",
            "Do you want to save changes?",
            icon=messagebox.WARNING,
            default=messagebox.YES
        )
        
        if response is None:  # Cancel
            return False
        elif response:  # Yes
            return self.save_file()
        else:  # No
            return True
    
    def exit_app(self):
        """Exit application"""
        if self.modified and not self.confirm_save():
            return
        
        self.root.quit()
        self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = Notepad(root)
    root.mainloop()


if __name__ == "__main__":
    main()
