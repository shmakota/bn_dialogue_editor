"""Node graph canvas for displaying and interacting with dialogue nodes"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable, Tuple
import math

from ..models.dialogue import DialogueGraph
from ..graph.graph_manager import GraphManager
from ..utils.helpers import calculate_node_size, truncate_text


class GraphCanvas(tk.Canvas):
    """Canvas for displaying node graph"""
    
    NODE_WIDTH = 200
    NODE_HEIGHT = 80
    NODE_PADDING = 10
    GRID_SIZE = 20  # Grid spacing in pixels
    
    def __init__(self, parent, graph_manager: GraphManager, on_node_select: Optional[Callable] = None):
        super().__init__(parent, bg='#f5f5f5', highlightthickness=0)
        self.graph_manager = graph_manager
        self.on_node_select = on_node_select
        
        # Canvas state
        self.scale = 1.0
        self.pan_start_x = 0
        self.pan_start_y = 0
        self.is_panning = False
        self.is_dragging = False
        self.drag_node_id = None
        self.show_grid = True
        self.snap_to_grid = True
        
        # Bind events
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Button-3>", self.on_right_click)
        # Mouse wheel (Windows/Mac)
        self.bind("<MouseWheel>", self.on_zoom)
        # Mouse wheel (Linux)
        self.bind("<Button-4>", self.on_zoom)
        self.bind("<Button-5>", self.on_zoom)
        self.bind("<Button-2>", self.on_pan_start)
        self.bind("<B2-Motion>", self.on_pan)
        self.bind("<ButtonRelease-2>", self.on_pan_end)
        # Arrow key panning
        self.bind("<Left>", self.on_arrow_key)
        self.bind("<Right>", self.on_arrow_key)
        self.bind("<Up>", self.on_arrow_key)
        self.bind("<Down>", self.on_arrow_key)
        self.bind("<KeyPress-Left>", self.on_arrow_key)
        self.bind("<KeyPress-Right>", self.on_arrow_key)
        self.bind("<KeyPress-Up>", self.on_arrow_key)
        self.bind("<KeyPress-Down>", self.on_arrow_key)
        # Redraw on window resize (but only for this widget)
        self.bind("<Configure>", self._on_configure)
        
        # Allow canvas to receive focus for keyboard events
        self.focus_set()
        
        # Scrollbars - need to be created but packed by parent
        # Scroll commands should NOT trigger redraws - they just update scrollbar position
        # Redraws should only happen when content changes, not when scrolling
        def h_scroll_command(*args):
            # Just update the scrollbar - don't redraw
            self.h_scroll.set(*args)
        
        def v_scroll_command(*args):
            # Just update the scrollbar - don't redraw
            self.v_scroll.set(*args)
        
        self.h_scroll = ttk.Scrollbar(parent, orient="horizontal", command=self.xview)
        self.v_scroll = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.configure(xscrollcommand=h_scroll_command, yscrollcommand=v_scroll_command)
        
        # Set initial scroll region
        self.configure(scrollregion=(0, 0, 2000, 2000))
    
    def _on_configure(self, event):
        """Handle window resize"""
        if event.widget == self:
            self.after_idle(self.redraw)
    
    def snap_to_grid_coordinate(self, coord: float) -> float:
        """Snap a coordinate to the nearest grid point"""
        if not self.snap_to_grid:
            return coord
        return round(coord / self.GRID_SIZE) * self.GRID_SIZE
    
    
    def on_click(self, event):
        """Handle mouse click"""
        # Ensure canvas has focus for keyboard events (arrow keys)
        self.focus_set()
        
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        
        # Check if clicking on a node
        node_id = self.get_node_at(x, y)
        if node_id:
            self.is_dragging = True
            self.drag_node_id = node_id
            self.graph_manager.clear_selection()
            self.graph_manager.select_node(node_id)
            if self.on_node_select:
                self.on_node_select(node_id)
            self.redraw()
        else:
            self.graph_manager.clear_selection()
            if self.on_node_select:
                self.on_node_select(None)
            self.redraw()
    
    def on_drag(self, event):
        """Handle mouse drag"""
        if self.is_dragging and self.drag_node_id:
            x = self.canvasx(event.x)
            y = self.canvasy(event.y)
            # Convert canvas coordinates to world coordinates
            world_x = x / self.scale
            world_y = y / self.scale
            # Snap to grid (grid size doesn't change, only visual scale)
            world_x = self.snap_to_grid_coordinate(world_x)
            world_y = self.snap_to_grid_coordinate(world_y)
            self.graph_manager.set_node_position(self.drag_node_id, world_x, world_y)
            self.redraw()
        elif self.is_panning:
            dx = event.x - self.pan_start_x
            dy = event.y - self.pan_start_y
            self.scan_dragto(event.x, event.y, gain=1)
            self.pan_start_x = event.x
            self.pan_start_y = event.y
    
    def on_release(self, event):
        """Handle mouse release"""
        self.is_dragging = False
        self.drag_node_id = None
    
    def on_right_click(self, event):
        """Handle right click (context menu)"""
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        # Could add context menu here
        pass
    
    def zoom_in(self, factor=1.1):
        """Zoom in"""
        self.scale *= factor
        self.scale = min(3.0, self.scale)
        self.redraw()
    
    def zoom_out(self, factor=1.1):
        """Zoom out"""
        self.scale /= factor
        self.scale = max(0.25, self.scale)
        self.redraw()
    
    def zoom_reset(self):
        """Reset zoom to 1.0"""
        self.scale = 1.0
        self.redraw()
    
    def on_zoom(self, event):
        """Handle mouse wheel zoom"""
        # Get mouse position for zoom-to-point
        mouse_x = event.x
        mouse_y = event.y
        
        # Convert to canvas coordinates
        canvas_x = self.canvasx(mouse_x)
        canvas_y = self.canvasy(mouse_y)
        
        # Handle different platforms
        zoom_in = False
        if hasattr(event, 'delta'):
            # Windows/Mac - delta sign can vary by system
            # On Windows: positive delta = scroll up (zoom in)
            # On Mac with natural scrolling: positive delta = scroll down (zoom out)  
            # On some Linux systems with MouseWheel: delta sign may be inverted
            # If both directions zoom the same way, we need to invert
            if event.delta < 0:  # Inverted: negative = scroll up (zoom in)
                zoom_in = True
            elif event.delta > 0:  # Inverted: positive = scroll down (zoom out)
                zoom_in = False
            else:
                return  # No movement
        elif event.num == 4:
            # Linux scroll up (Button-4) - zoom in
            zoom_in = True
        elif event.num == 5:
            # Linux scroll down (Button-5) - zoom out
            zoom_in = False
        else:
            return  # Unknown event
        
        old_scale = self.scale
        if zoom_in:
            self.scale *= 1.1
            self.scale = min(3.0, self.scale)
        else:
            self.scale /= 1.1
            self.scale = max(0.25, self.scale)
        
        # Zoom to point (keep mouse position fixed)
        if old_scale != self.scale:
            self.scale_to_point(canvas_x, canvas_y, mouse_x, mouse_y)
            self.redraw()
    
    def scale_to_point(self, canvas_x, canvas_y, screen_x, screen_y):
        """Scale around a specific point to keep it under the cursor"""
        # After zoom, the same screen position should point to the same canvas position
        # Calculate how much the canvas moved due to scaling
        # This is a simplified version - full implementation would require more complex math
        pass  # For now, just let it zoom from center
    
    def on_pan_start(self, event):
        """Start panning"""
        self.is_panning = True
        self.pan_start_x = event.x
        self.pan_start_y = event.y
    
    def on_pan(self, event):
        """Handle panning"""
        if self.is_panning:
            self.scan_dragto(event.x, event.y, gain=1)
            self.pan_start_x = event.x
            self.pan_start_y = event.y
    
    def on_pan_end(self, event):
        """End panning"""
        self.is_panning = False
    
    def on_arrow_key(self, event):
        """Handle arrow key panning"""
        pan_distance = 20  # Pixels to pan per keypress
        
        # Use scan_dragto for panning, then redraw to update grid
        if event.keysym == "Left":
            self.scan_mark(0, 0)
            self.scan_dragto(pan_distance, 0, gain=1)
        elif event.keysym == "Right":
            self.scan_mark(0, 0)
            self.scan_dragto(-pan_distance, 0, gain=1)
        elif event.keysym == "Up":
            self.scan_mark(0, 0)
            self.scan_dragto(0, pan_distance, gain=1)
        elif event.keysym == "Down":
            self.scan_mark(0, 0)
            self.scan_dragto(0, -pan_distance, gain=1)
        
        # Redraw to update grid position with new view
        self.redraw()
    
    def get_node_at(self, x: float, y: float) -> Optional[str]:
        """Get node ID at given coordinates"""
        # Convert canvas coordinates to world coordinates (inverse of zoom)
        world_x = x / self.scale
        world_y = y / self.scale
        
        for topic_id, pos in self.graph_manager.node_positions.items():
            node_x, node_y = pos
            # Check if click is within node bounds (in world coordinates)
            if abs(world_x - node_x) < self.NODE_WIDTH / 2 and abs(world_y - node_y) < self.NODE_HEIGHT / 2:
                return topic_id
        return None
    
    def draw_node(self, topic_id: str, x: float, y: float):
        """Draw a single node"""
        topic = self.graph_manager.dialogue_graph.get_topic(topic_id)
        if not topic:
            return
        
        is_selected = self.graph_manager.is_selected(topic_id)
        
        # Node colors
        if is_selected:
            fill_color = '#4A90E2'
            outline_color = '#2E5C8A'
        else:
            fill_color = '#E8E8E8'
            outline_color = '#888888'
        
        # Scale positions with zoom (zooming in makes things appear closer)
        scaled_x = x * self.scale
        scaled_y = y * self.scale
        
        # Draw node rectangle (scale size with zoom)
        width = self.NODE_WIDTH * self.scale
        height = self.NODE_HEIGHT * self.scale
        
        x1 = scaled_x - width / 2
        y1 = scaled_y - height / 2
        x2 = scaled_x + width / 2
        y2 = scaled_y + height / 2
        
        self.create_rectangle(
            x1, y1, x2, y2,
            fill=fill_color,
            outline=outline_color,
            width=2 if is_selected else 1,
            tags=(topic_id, "node")
        )
        
        # Draw topic ID (scale font with zoom)
        font_size = max(7, int(9 * self.scale))
        display_id = truncate_text(topic.id, 25)
        self.create_text(
            scaled_x, scaled_y - 20 * self.scale,
            text=display_id,
            font=("Arial", font_size, "bold"),
            fill="#333333",
            tags=(topic_id, "node_text")
        )
        
        # Draw preview of first dynamic line
        if topic.dynamic_line is not None:
            # Get preview text from dynamic_line
            if isinstance(topic.dynamic_line, str):
                first_line = topic.dynamic_line
            elif isinstance(topic.dynamic_line, dict):
                # Conditional - show yes branch if available
                first_line = topic.dynamic_line.get("yes", "") if "yes" in topic.dynamic_line else str(topic.dynamic_line)
            elif isinstance(topic.dynamic_line, list):
                # Array for random selection - get first item
                first_line = str(topic.dynamic_line[0]) if len(topic.dynamic_line) > 0 else ""
            else:
                first_line = str(topic.dynamic_line)
            
            if first_line:
                preview = truncate_text(first_line, 30)
                preview_font_size = max(6, int(8 * self.scale))
                self.create_text(
                    scaled_x, scaled_y + 5 * self.scale,
                    text=preview,
                    font=("Arial", preview_font_size),
                    fill="#666666",
                    tags=(topic_id, "node_text")
                )
        
        # Draw response count
        if topic.responses:
            count_font_size = max(6, int(8 * self.scale))
            self.create_text(
                scaled_x + width / 2 - 10 * self.scale, scaled_y - height / 2 + 10 * self.scale,
                text=f"{len(topic.responses)}",
                font=("Arial", count_font_size),
                fill="#888888",
                tags=(topic_id, "node_text")
            )
    
    def draw_connection(self, from_id: str, to_id: str):
        """Draw connection between nodes"""
        pos1 = self.graph_manager.get_node_position(from_id)
        pos2 = self.graph_manager.get_node_position(to_id)
        
        if not pos1 or not pos2:
            return
        
        x1, y1 = pos1
        x2, y2 = pos2
        
        # Scale positions with zoom
        scaled_x1 = x1 * self.scale
        scaled_y1 = y1 * self.scale
        scaled_x2 = x2 * self.scale
        scaled_y2 = y2 * self.scale
        
        # Calculate connection points (edges of nodes)
        dx = scaled_x2 - scaled_x1
        dy = scaled_y2 - scaled_y1
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist < 1:
            return
        
        # Start point on edge of source node (scale with zoom)
        sx = scaled_x1 + (dx / dist) * (self.NODE_WIDTH * self.scale / 2)
        sy = scaled_y1 + (dy / dist) * (self.NODE_HEIGHT * self.scale / 2)
        
        # End point on edge of target node (scale with zoom)
        ex = scaled_x2 - (dx / dist) * (self.NODE_WIDTH * self.scale / 2)
        ey = scaled_y2 - (dy / dist) * (self.NODE_HEIGHT * self.scale / 2)
        
        self.create_line(
            sx, sy, ex, ey,
            fill="#333333",
            width=max(2, int(2 * self.scale)),
            arrow=tk.LAST,
            arrowshape=(8, 10, 3),
            tags="connection"
        )
    
    def draw_grid(self):
        """Draw grid lines on the canvas"""
        if not self.show_grid:
            return
        
        try:
            # Get visible canvas area (not window coordinates)
            width = self.winfo_width()
            height = self.winfo_height()
            
            # Check for valid dimensions
            if width <= 0 or height <= 0:
                return
            
            # Get visible canvas area in canvas coordinates (accounts for scrolling)
            canvas_x1 = self.canvasx(0)
            canvas_y1 = self.canvasy(0)
            canvas_x2 = self.canvasx(width)
            canvas_y2 = self.canvasy(height)
            
            # Validate coordinates
            if not all(isinstance(v, (int, float)) and not (math.isnan(v) or math.isinf(v)) 
                      for v in [canvas_x1, canvas_y1, canvas_x2, canvas_y2]):
                return
            
            # Grid size in canvas coordinates (scales with zoom)
            # Base grid size in world coordinates, then scale to canvas
            effective_grid_size = self.GRID_SIZE * self.scale
            effective_grid_size = max(10, min(50, effective_grid_size))
            
            # Work in canvas coordinates directly (which already account for scrolling)
            min_x = min(canvas_x1, canvas_x2)
            min_y = min(canvas_y1, canvas_y2)
            max_x = max(canvas_x1, canvas_x2)
            max_y = max(canvas_y1, canvas_y2)
            
            # Expand visible area by one grid size for smoother scrolling
            min_x -= effective_grid_size
            min_y -= effective_grid_size
            max_x += effective_grid_size
            max_y += effective_grid_size
            
            # Limit grid drawing to reasonable bounds to prevent excessive lines
            grid_width = abs(max_x - min_x)
            grid_height = abs(max_y - min_y)
            if grid_width > 5000 or grid_height > 5000:
                # Skip grid drawing if area is too large (performance)
                return
            
            # Also limit based on number of grid lines that would be drawn
            estimated_vertical_lines = grid_width / effective_grid_size if effective_grid_size > 0 else 0
            estimated_horizontal_lines = grid_height / effective_grid_size if effective_grid_size > 0 else 0
            if estimated_vertical_lines > 150 or estimated_horizontal_lines > 150:
                return
            
            # Snap grid start to grid boundaries (in canvas coordinates)
            grid_start_x = (int(min_x) // int(effective_grid_size)) * int(effective_grid_size)
            grid_start_y = (int(min_y) // int(effective_grid_size)) * int(effective_grid_size)
            
            # Limit number of lines to prevent performance issues
            max_lines = 200
            
            # Draw vertical grid lines (in canvas coordinates)
            x = grid_start_x
            line_count = 0
            while x <= max_x and line_count < max_lines:
                self.create_line(
                    int(x), int(min_y), int(x), int(max_y),
                    fill='#d0d0d0',
                    width=max(1, int(self.scale)),
                    tags="grid"
                )
                x += effective_grid_size
                line_count += 1
            
            # Draw horizontal grid lines (in canvas coordinates)
            y = grid_start_y
            line_count = 0
            while y <= max_y and line_count < max_lines:
                self.create_line(
                    int(min_x), int(y), int(max_x), int(y),
                    fill='#d0d0d0',
                    width=max(1, int(self.scale)),
                    tags="grid"
                )
                y += effective_grid_size
                line_count += 1
            
            # Draw major grid lines every 5 grid units
            major_grid = effective_grid_size * 5
            major_start_x = (int(min_x) // int(major_grid)) * int(major_grid)
            major_start_y = (int(min_y) // int(major_grid)) * int(major_grid)
            
            x = major_start_x
            line_count = 0
            while x <= max_x and line_count < max_lines // 5:
                self.create_line(
                    int(x), int(min_y), int(x), int(max_y),
                    fill='#b0b0b0',
                    width=max(1, int(self.scale)),
                    tags="grid_major"
                )
                x += major_grid
                line_count += 1
            
            y = major_start_y
            line_count = 0
            while y <= max_y and line_count < max_lines // 5:
                self.create_line(
                    int(min_x), int(y), int(max_x), int(y),
                    fill='#b0b0b0',
                    width=max(1, int(self.scale)),
                    tags="grid_major"
                )
                y += major_grid
                line_count += 1
        except Exception as e:
            # Silently fail if grid drawing has issues (don't break the app)
            pass
    
    def redraw(self):
        """Redraw the entire canvas"""
        # Use delete("all") - it's actually quite fast for Tkinter
        self.delete("all")
        
        # Draw grid first (background) - skip if canvas is too small
        try:
            width = self.winfo_width()
            height = self.winfo_height()
            if width > 1 and height > 1:
                self.draw_grid()
        except:
            pass
        
        # Draw connections (behind nodes)
        for topic_id in self.graph_manager.dialogue_graph.topics.keys():
            connections = self.graph_manager.dialogue_graph.get_connections(topic_id)
            for conn_id in connections:
                if conn_id in self.graph_manager.dialogue_graph.topics:
                    self.draw_connection(topic_id, conn_id)
        
        # Draw nodes (on top) - positions are in world coordinates
        for topic_id, pos in self.graph_manager.node_positions.items():
            self.draw_node(topic_id, pos[0], pos[1])
        
        # Update scroll region based on content
        # Note: We update the scrollregion, but the scroll commands (h_scroll_command/v_scroll_command)
        # no longer trigger redraws, so this won't cause feedback loops
        try:
            bbox = self.bbox("all")
            if bbox:
                # Add padding for scrolling
                padding = 100
                min_x, min_y, max_x, max_y = bbox
                self.configure(scrollregion=(
                    min_x - padding, min_y - padding,
                    max_x + padding, max_y + padding
                ))
            else:
                # Default scroll region
                self.configure(scrollregion=(0, 0, 2000, 2000))
        except Exception:
            # If scrollregion update fails, just continue - don't break the app
            pass

