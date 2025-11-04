"""Toolbar and menu bar"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class Toolbar(ttk.Frame):
    """Toolbar with common actions"""
    
    def __init__(self, parent, on_import=None, on_export=None, on_new_topic=None, on_validate=None, on_layout=None, on_untangle=None, on_zoom_in=None, on_zoom_out=None, on_zoom_reset=None, on_help=None):
        super().__init__(parent)
        self.on_import = on_import
        self.on_export = on_export
        self.on_new_topic = on_new_topic
        self.on_validate = on_validate
        self.on_layout = on_layout
        self.on_untangle = on_untangle
        self.on_zoom_in = on_zoom_in
        self.on_zoom_out = on_zoom_out
        self.on_zoom_reset = on_zoom_reset
        self.on_help = on_help
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create toolbar widgets"""
        ttk.Button(self, text="Import", command=self.import_file).pack(side="left", padx=2)
        ttk.Button(self, text="Export", command=self.export_file).pack(side="left", padx=2)
        ttk.Separator(self, orient="vertical").pack(side="left", fill="y", padx=5)
        ttk.Button(self, text="New Topic", command=self.new_topic).pack(side="left", padx=2)
        ttk.Separator(self, orient="vertical").pack(side="left", fill="y", padx=5)
        ttk.Button(self, text="Validate", command=self.validate).pack(side="left", padx=2)
        ttk.Button(self, text="Auto Layout", command=self.auto_layout).pack(side="left", padx=2)
        ttk.Button(self, text="Untangle", command=self.untangle).pack(side="left", padx=2)
        ttk.Separator(self, orient="vertical").pack(side="left", fill="y", padx=5)
        ttk.Button(self, text="Zoom In", command=self.zoom_in).pack(side="left", padx=2)
        ttk.Button(self, text="Zoom Out", command=self.zoom_out).pack(side="left", padx=2)
        ttk.Button(self, text="Reset Zoom", command=self.zoom_reset).pack(side="left", padx=2)
        ttk.Separator(self, orient="vertical").pack(side="left", fill="y", padx=5)
        ttk.Button(self, text="ℹ Information Atlas", command=self.show_help).pack(side="left", padx=2)
    
    def show_help(self):
        """Handle help action"""
        if self.on_help:
            self.on_help()
    
    def zoom_in(self):
        """Handle zoom in action"""
        if self.on_zoom_in:
            self.on_zoom_in()
    
    def zoom_out(self):
        """Handle zoom out action"""
        if self.on_zoom_out:
            self.on_zoom_out()
    
    def zoom_reset(self):
        """Handle zoom reset action"""
        if self.on_zoom_reset:
            self.on_zoom_reset()
    
    def import_file(self):
        """Handle import action"""
        if self.on_import:
            filename = filedialog.askopenfilename(
                title="Import Dialogue File",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                self.on_import(filename)
    
    def export_file(self):
        """Handle export action"""
        if self.on_export:
            filename = filedialog.asksaveasfilename(
                title="Export Dialogue File",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                self.on_export(filename)
    
    def new_topic(self):
        """Handle new topic action"""
        if self.on_new_topic:
            self.on_new_topic()
    
    def validate(self):
        """Handle validate action"""
        if self.on_validate:
            self.on_validate()
    
    def auto_layout(self):
        """Handle auto layout action"""
        if self.on_layout:
            self.on_layout()
    
    def untangle(self):
        """Handle untangle action"""
        if self.on_untangle:
            self.on_untangle()


def create_menu_bar(parent, on_import=None, on_export=None, on_exit=None):
    """Create menu bar"""
    menubar = tk.Menu(parent)
    parent.config(menu=menubar)
    
    # File menu
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    
    if on_import:
        file_menu.add_command(label="Import...", command=on_import)
    
    if on_export:
        file_menu.add_command(label="Export...", command=on_export)
    
    file_menu.add_separator()
    
    if on_exit:
        file_menu.add_command(label="Exit", command=on_exit)
    
    # Edit menu
    edit_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Edit", menu=edit_menu)
    # Can add more edit commands here
    
    # View menu
    view_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="View", menu=view_menu)
    # Can add view options here
    
    # Help menu
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=lambda: messagebox.showinfo(
        "About",
        "Cataclysm: Bright Nights Dialogue Editor\nVersion 0.1.0"
    ))
    
    return menubar

