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
        
        # Navigation history for back button
        self.navigation_history = []
        self.current_history_index = -1
        
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
            on_help=self.show_help,
            on_back=self.navigate_back
        )
        toolbar.pack(fill="x", padx=5, pady=5)
        
        # Main content area
        main_paned = ttk.PanedWindow(self, orient="horizontal")
        main_paned.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Graph canvas
        canvas_frame = ttk.Frame(main_paned)
        main_paned.add(canvas_frame, weight=3)
        
        # Use grid layout for canvas and scrollbars
        self.graph_canvas = GraphCanvas(
            canvas_frame,
            self.graph_manager,
            on_node_select=self.on_node_select,
            on_mouse_move=self.on_canvas_mouse_move
        )
        self.graph_canvas.grid(row=0, column=0, sticky="nsew")
        self.graph_canvas.focus_set()  # Allow canvas to receive focus for mouse wheel
        
        # Bind mouse back button (Button-8) for navigation - try multiple button numbers
        # Button-8/9 are typically browser back/forward buttons, but support varies
        for button_num in [8, 9]:
            try:
                self.graph_canvas.bind(f"<Button-{button_num}>", lambda e: self.navigate_back())
                self.bind_all(f"<Button-{button_num}>", lambda e: self.navigate_back())
                break  # Successfully bound, no need to try others
            except tk.TclError:
                continue  # This button number not supported, try next
        
        # Configure grid weights
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        
        # Hide scrollbars: do not grid them
        
        # Property editor
        editor_frame = ttk.Frame(main_paned)
        main_paned.add(editor_frame, weight=1)
        
        self.property_editor = PropertyEditor(
            editor_frame,
            self.graph_manager,
            on_change=self.on_graph_change,
            on_node_select=self.on_node_select
        )
        self.property_editor.pack(fill="both", expand=True)
        
        # Bottom status area with coordinates (left) and status (right)
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(side="bottom", fill="x")
        
        self.coords_var = tk.StringVar(value="x: -, y: -")
        coords_label = ttk.Label(bottom_frame, textvariable=self.coords_var, relief="sunken")
        coords_label.pack(side="left", padx=(0, 4))
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(bottom_frame, textvariable=self.status_var, relief="sunken")
        status_label.pack(side="right", fill="x", expand=True)

    def on_canvas_mouse_move(self, x: float, y: float):
        """Update coordinates label from canvas mouse movement"""
        try:
            self.coords_var.set(f"x: {int(x)}  y: {int(y)}")
        except Exception:
            pass
    
    def on_node_select(self, topic_id, add_to_history=True):
        """Handle node selection"""
        # Add to history if not navigating back
        if add_to_history and topic_id:
            # If we're not at the end of history, truncate forward history
            if self.current_history_index < len(self.navigation_history) - 1:
                self.navigation_history = self.navigation_history[:self.current_history_index + 1]
            # Add new node to history
            self.navigation_history.append(topic_id)
            self.current_history_index = len(self.navigation_history) - 1
        
        # Update graph manager selection
        self.graph_manager.clear_selection()
        if topic_id:
            self.graph_manager.select_node(topic_id)
        
        # Update property editor
        self.property_editor.load_topic(topic_id)
        
        # Redraw canvas to show selection
        self.graph_canvas.redraw()
        
        if topic_id:
            self.status_var.set(f"Selected: {topic_id}")
        else:
            self.status_var.set("Ready")
    
    def navigate_back(self):
        """Navigate back to previous node in history"""
        if self.current_history_index > 0:
            self.current_history_index -= 1
            previous_topic_id = self.navigation_history[self.current_history_index]
            self.on_node_select(previous_topic_id, add_to_history=False)
    
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

