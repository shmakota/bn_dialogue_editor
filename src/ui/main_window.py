"""Main application window"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from ..models.dialogue import DialogueGraph, DialogueTopic
from ..graph.graph_manager import GraphManager
from ..graph.layout import LayoutManager
from ..parsers.json_parser import JSONParser
from ..parsers.validator import Validator
from .graph_canvas import GraphCanvas
from .property_editor import PropertyEditor
from .toolbar import Toolbar, create_menu_bar
from .help_dialog import HelpDialog


class MainWindow(tk.Tk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        self.title("Cataclysm Bright Nights - Dialogue Writer")
        self.geometry("1400x900")
        
        # Initialize data
        self.dialogue_graph = DialogueGraph()
        self.graph_manager = GraphManager(self.dialogue_graph)
        self.layout_manager = LayoutManager()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create UI widgets"""
        # Toolbar
        toolbar = Toolbar(
            self,
            on_import=self.show_import_dialog,
            on_export=self.show_export_dialog,
            on_new_topic=self.add_new_topic,
            on_validate=self.validate_dialogue,
            on_layout=self.apply_auto_layout,
            on_untangle=self.apply_untangle_layout,
            on_zoom_in=self.zoom_in,
            on_zoom_out=self.zoom_out,
            on_zoom_reset=self.zoom_reset,
            on_help=self.show_help
        )
        toolbar.pack(fill="x", padx=5, pady=5)
        
        # Main content area
        main_paned = ttk.PanedWindow(self, orient="horizontal")
        main_paned.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Graph canvas with scrollbars
        canvas_frame = ttk.Frame(main_paned)
        main_paned.add(canvas_frame, weight=3)
        
        # Use grid layout for canvas and scrollbars
        self.graph_canvas = GraphCanvas(
            canvas_frame,
            self.graph_manager,
            on_node_select=self.on_node_select
        )
        self.graph_canvas.grid(row=0, column=0, sticky="nsew")
        self.graph_canvas.focus_set()  # Allow canvas to receive focus for mouse wheel
        
        # Configure grid weights
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        
        # Scrollbars for canvas - use grid layout
        self.graph_canvas.v_scroll.grid(row=0, column=1, sticky="ns")
        self.graph_canvas.h_scroll.grid(row=1, column=0, sticky="ew")
        
        # Property editor
        editor_frame = ttk.Frame(main_paned)
        main_paned.add(editor_frame, weight=1)
        
        self.property_editor = PropertyEditor(
            editor_frame,
            self.graph_manager,
            on_change=self.on_graph_change
        )
        self.property_editor.pack(fill="both", expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self, textvariable=self.status_var, relief="sunken")
        status_bar.pack(side="bottom", fill="x")
    
    def on_node_select(self, topic_id):
        """Handle node selection"""
        self.property_editor.load_topic(topic_id)
        if topic_id:
            self.status_var.set(f"Selected: {topic_id}")
        else:
            self.status_var.set("Ready")
    
    def on_graph_change(self):
        """Handle graph changes"""
        self.graph_canvas.redraw()
        self.status_var.set("Graph updated")
    
    def show_import_dialog(self, filename=None):
        """Show import file dialog or use provided filename"""
        if filename:
            self.import_file(filename)
        else:
            from tkinter import filedialog
            filename = filedialog.askopenfilename(
                title="Import Dialogue File",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                self.import_file(filename)
    
    def show_export_dialog(self, filename=None):
        """Show export file dialog or use provided filename"""
        if filename:
            self.export_file(filename)
        else:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                title="Export Dialogue File",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                self.export_file(filename)
    
    def import_file(self, filename):
        """Import dialogue file"""
        try:
            self.dialogue_graph = JSONParser.parse_file(filename)
            self.graph_manager = GraphManager(self.dialogue_graph)
            self.graph_canvas.graph_manager = self.graph_manager
            self.property_editor.graph_manager = self.graph_manager
            
            # Apply initial layout
            self.apply_auto_layout()
            
            # Refresh canvas
            self.graph_canvas.redraw()
            
            self.status_var.set(f"Imported: {filename}")
            messagebox.showinfo("Success", f"Imported {len(self.dialogue_graph.topics)} topics")
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import file:\n{str(e)}")
            self.status_var.set("Import failed")
    
    def export_file(self, filename):
        """Export dialogue file"""
        try:
            # Validate before export
            errors = Validator.validate_graph(self.dialogue_graph)
            if errors:
                msg = "Validation errors found:\n\n" + "\n".join(errors[:10])
                if len(errors) > 10:
                    msg += f"\n... and {len(errors) - 10} more"
                response = messagebox.askyesno(
                    "Validation Errors",
                    msg + "\n\nDo you want to export anyway?"
                )
                if not response:
                    return
            
            JSONParser.export_file(self.dialogue_graph, filename)
            self.status_var.set(f"Exported: {filename}")
            messagebox.showinfo("Success", f"Exported {len(self.dialogue_graph.topics)} topics")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export file:\n{str(e)}")
            self.status_var.set("Export failed")
    
    def add_new_topic(self):
        """Add a new topic"""
        topic_id = simpledialog.askstring(
            "New Topic",
            "Enter topic ID:",
            initialvalue="TALK_NEW_TOPIC_1"
        )
        
        if topic_id:
            if topic_id in self.dialogue_graph.topics:
                messagebox.showerror("Error", f"Topic ID '{topic_id}' already exists")
                return
            
            new_topic = DialogueTopic(
                id=topic_id,
                dynamic_line=["New dialogue line"]
            )
            self.dialogue_graph.add_topic(new_topic)
            
            # Position new node
            self.layout_manager.grid_layout(self.graph_manager, 1000, 800)
            self.graph_canvas.redraw()
            
            # Select the new node
            self.graph_manager.select_node(topic_id)
            self.on_node_select(topic_id)
            
            self.status_var.set(f"Created new topic: {topic_id}")
    
    def validate_dialogue(self):
        """Validate dialogue"""
        errors = Validator.validate_graph(self.dialogue_graph)
        
        if not errors:
            messagebox.showinfo("Validation", "No errors found!")
            self.status_var.set("Validation passed")
        else:
            msg = f"Found {len(errors)} error(s):\n\n" + "\n".join(errors[:20])
            if len(errors) > 20:
                msg += f"\n... and {len(errors) - 20} more"
            messagebox.showerror("Validation Errors", msg)
            self.status_var.set(f"Validation failed: {len(errors)} errors")
    
    def apply_auto_layout(self):
        """Apply automatic layout"""
        if not self.dialogue_graph.topics:
            messagebox.showinfo("Info", "No topics to layout")
            return
        
        self.layout_manager.force_directed_layout(self.graph_manager)
        self.graph_canvas.redraw()
        self.status_var.set("Layout applied")
    
    def apply_untangle_layout(self):
        """Apply untangle layout to improve graph appearance"""
        if not self.dialogue_graph.topics:
            messagebox.showinfo("Info", "No topics to untangle")
            return
        
        # Get canvas dimensions for layout
        canvas_width = max(1000, self.graph_canvas.winfo_width())
        canvas_height = max(800, self.graph_canvas.winfo_height())
        
        self.layout_manager.untangle_layout(self.graph_manager, canvas_width, canvas_height)
        self.graph_canvas.redraw()
        self.status_var.set("Graph untangled")
    
    def zoom_in(self):
        """Zoom in"""
        self.graph_canvas.zoom_in()
        self.status_var.set(f"Zoom: {int(self.graph_canvas.scale * 100)}%")
    
    def zoom_out(self):
        """Zoom out"""
        self.graph_canvas.zoom_out()
        self.status_var.set(f"Zoom: {int(self.graph_canvas.scale * 100)}%")
    
    def zoom_reset(self):
        """Reset zoom"""
        self.graph_canvas.zoom_reset()
        self.status_var.set("Zoom: 100%")
    
    def show_help(self):
        """Show help dialog"""
        HelpDialog(self)

