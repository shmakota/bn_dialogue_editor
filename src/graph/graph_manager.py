"""Graph state management"""

from typing import Dict, Tuple, Optional
from ..models.dialogue import DialogueGraph


class GraphManager:
    """Manages graph state including node positions"""
    
    def __init__(self, dialogue_graph: DialogueGraph):
        self.dialogue_graph = dialogue_graph
        self.node_positions: Dict[str, Tuple[float, float]] = {}
        self.selected_nodes: set = set()
    
    def set_node_position(self, topic_id: str, x: float, y: float) -> None:
        """Set position of a node"""
        self.node_positions[topic_id] = (x, y)
    
    def get_node_position(self, topic_id: str) -> Optional[Tuple[float, float]]:
        """Get position of a node"""
        return self.node_positions.get(topic_id)
    
    def select_node(self, topic_id: str) -> None:
        """Select a node"""
        self.selected_nodes.add(topic_id)
    
    def deselect_node(self, topic_id: str) -> None:
        """Deselect a node"""
        self.selected_nodes.discard(topic_id)
    
    def clear_selection(self) -> None:
        """Clear all selections"""
        self.selected_nodes.clear()
    
    def is_selected(self, topic_id: str) -> bool:
        """Check if node is selected"""
        return topic_id in self.selected_nodes




