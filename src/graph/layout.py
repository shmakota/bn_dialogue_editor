"""Node positioning algorithms"""

from typing import Dict, Tuple, List
import math


class LayoutManager:
    """Manages node layout algorithms"""
    
    @staticmethod
    def force_directed_layout(
        graph_manager, 
        width: int = 1000, 
        height: int = 800,
        iterations: int = 50
    ) -> None:
        """Apply force-directed layout algorithm"""
        if not graph_manager.dialogue_graph.topics:
            return
        
        # Initialize positions randomly if not set
        topic_ids = list(graph_manager.dialogue_graph.topics.keys())
        
        for i, topic_id in enumerate(topic_ids):
            if topic_id not in graph_manager.node_positions:
                # Place in a grid initially
                cols = math.ceil(math.sqrt(len(topic_ids)))
                row = i // cols
                col = i % cols
                x = 100 + col * 200
                y = 100 + row * 150
                graph_manager.set_node_position(topic_id, x, y)
        
        # Simple force-directed algorithm
        for _ in range(iterations):
            forces: Dict[str, Tuple[float, float]] = {}
            
            for topic_id in topic_ids:
                forces[topic_id] = (0.0, 0.0)
            
            # Repulsion forces between all nodes
            k = math.sqrt(width * height / len(topic_ids))
            
            for i, topic_id1 in enumerate(topic_ids):
                pos1 = graph_manager.get_node_position(topic_id1)
                if not pos1:
                    continue
                
                for topic_id2 in topic_ids[i+1:]:
                    pos2 = graph_manager.get_node_position(topic_id2)
                    if not pos2:
                        continue
                    
                    dx = pos1[0] - pos2[0]
                    dy = pos1[1] - pos2[1]
                    dist = math.sqrt(dx*dx + dy*dy) + 0.1
                    
                    force = k * k / dist
                    fx = force * dx / dist
                    fy = force * dy / dist
                    
                    forces[topic_id1] = (forces[topic_id1][0] + fx, forces[topic_id1][1] + fy)
                    forces[topic_id2] = (forces[topic_id2][0] - fx, forces[topic_id2][1] - fy)
            
            # Attraction forces for connected nodes
            for topic_id in topic_ids:
                connections = graph_manager.dialogue_graph.get_connections(topic_id)
                pos1 = graph_manager.get_node_position(topic_id)
                if not pos1:
                    continue
                
                for conn_id in connections:
                    if conn_id in graph_manager.dialogue_graph.topics:
                        pos2 = graph_manager.get_node_position(conn_id)
                        if pos2:
                            dx = pos2[0] - pos1[0]
                            dy = pos2[1] - pos1[1]
                            dist = math.sqrt(dx*dx + dy*dy) + 0.1
                            
                            force = dist * dist / k
                            fx = force * dx / dist
                            fy = force * dy / dist
                            
                            forces[topic_id] = (forces[topic_id][0] + fx * 0.5, forces[topic_id][1] + fy * 0.5)
            
            # Apply forces with damping
            damping = 0.1
            for topic_id in topic_ids:
                fx, fy = forces[topic_id]
                pos = graph_manager.get_node_position(topic_id)
                if pos:
                    new_x = max(50, min(width - 50, pos[0] + fx * damping))
                    new_y = max(50, min(height - 50, pos[1] + fy * damping))
                    graph_manager.set_node_position(topic_id, new_x, new_y)
    
    @staticmethod
    def grid_layout(graph_manager, width: int = 1000, height: int = 800) -> None:
        """Apply grid layout"""
        topic_ids = list(graph_manager.dialogue_graph.topics.keys())
        if not topic_ids:
            return
        
        cols = math.ceil(math.sqrt(len(topic_ids)))
        rows = math.ceil(len(topic_ids) / cols)
        
        cell_width = (width - 200) / max(1, cols)
        cell_height = (height - 200) / max(1, rows)
        
        for i, topic_id in enumerate(topic_ids):
            row = i // cols
            col = i % cols
            x = 100 + col * cell_width
            y = 100 + row * cell_height
            graph_manager.set_node_position(topic_id, x, y)
    
    @staticmethod
    def untangle_layout(
        graph_manager,
        width: int = 1000,
        height: int = 800,
        iterations: int = 200
    ) -> None:
        """Apply untangling layout algorithm - improves existing layout with more iterations and better forces"""
        if not graph_manager.dialogue_graph.topics:
            return
        
        topic_ids = list(graph_manager.dialogue_graph.topics.keys())
        
        # Ensure all nodes have positions
        for i, topic_id in enumerate(topic_ids):
            if topic_id not in graph_manager.node_positions:
                cols = math.ceil(math.sqrt(len(topic_ids)))
                row = i // cols
                col = i % cols
                x = 100 + col * 200
                y = 100 + row * 150
                graph_manager.set_node_position(topic_id, x, y)
        
        # Enhanced force-directed algorithm with better parameters
        for iteration in range(iterations):
            forces: Dict[str, Tuple[float, float]] = {}
            
            for topic_id in topic_ids:
                forces[topic_id] = (0.0, 0.0)
            
            # Calculate optimal distance (decreases over iterations for convergence)
            k = math.sqrt(width * height / len(topic_ids))
            # Cooling factor - start stronger, decrease over time
            cooling = 1.0 - (iteration / iterations) * 0.5
            
            # Repulsion forces between all nodes (stronger repulsion)
            for i, topic_id1 in enumerate(topic_ids):
                pos1 = graph_manager.get_node_position(topic_id1)
                if not pos1:
                    continue
                
                for topic_id2 in topic_ids[i+1:]:
                    pos2 = graph_manager.get_node_position(topic_id2)
                    if not pos2:
                        continue
                    
                    dx = pos1[0] - pos2[0]
                    dy = pos1[1] - pos2[1]
                    dist = math.sqrt(dx*dx + dy*dy) + 0.1
                    
                    # Stronger repulsion to prevent overlap
                    force = (k * k / dist) * cooling * 1.2
                    fx = force * dx / dist
                    fy = force * dy / dist
                    
                    forces[topic_id1] = (forces[topic_id1][0] + fx, forces[topic_id1][1] + fy)
                    forces[topic_id2] = (forces[topic_id2][0] - fx, forces[topic_id2][1] - fy)
            
            # Attraction forces for connected nodes (tighter connections)
            for topic_id in topic_ids:
                connections = graph_manager.dialogue_graph.get_connections(topic_id)
                pos1 = graph_manager.get_node_position(topic_id)
                if not pos1:
                    continue
                
                for conn_id in connections:
                    if conn_id in graph_manager.dialogue_graph.topics:
                        pos2 = graph_manager.get_node_position(conn_id)
                        if pos2:
                            dx = pos2[0] - pos1[0]
                            dy = pos2[1] - pos1[1]
                            dist = math.sqrt(dx*dx + dy*dy) + 0.1
                            
                            # Optimal edge length
                            ideal_length = k * 0.6  # Shorter edges for tighter layout
                            force = (dist - ideal_length) / k * cooling
                            fx = force * dx / dist
                            fy = force * dy / dist
                            
                            forces[topic_id] = (forces[topic_id][0] + fx * 0.8, forces[topic_id][1] + fy * 0.8)
            
            # Apply forces with adaptive damping (decreases over iterations)
            damping = 0.15 * cooling + 0.05
            for topic_id in topic_ids:
                fx, fy = forces[topic_id]
                pos = graph_manager.get_node_position(topic_id)
                if pos:
                    new_x = max(50, min(width - 50, pos[0] + fx * damping))
                    new_y = max(50, min(height - 50, pos[1] + fy * damping))
                    graph_manager.set_node_position(topic_id, new_x, new_y)




