"""Validation logic for dialogue files"""

from typing import List
from ..models.dialogue import DialogueGraph


class Validator:
    """Validation logic for dialogue graphs"""
    
    @staticmethod
    def validate_graph(graph: DialogueGraph) -> List[str]:
        """Run all validation checks on graph"""
        errors = []
        
        # Validate IDs
        errors.extend(graph.validate_ids())
        
        # Validate references
        errors.extend(graph.validate_references())
        
        # Validate individual topics
        for topic in graph.topics.values():
            errors.extend(topic.validate())
        
        return errors
    
    @staticmethod
    def validate_references(graph: DialogueGraph) -> List[str]:
        """Check all topic references exist"""
        return graph.validate_references()
    
    @staticmethod
    def validate_ids(graph: DialogueGraph) -> List[str]:
        """Check for duplicate IDs"""
        return graph.validate_ids()




