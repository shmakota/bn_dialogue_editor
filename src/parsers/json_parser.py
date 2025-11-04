"""JSON import/export functionality"""

import json
from typing import List, Dict, Any
from pathlib import Path

from ..models.dialogue import DialogueGraph, DialogueTopic


class JSONParser:
    """Handles JSON import/export"""
    
    @staticmethod
    def parse_file(file_path: str) -> DialogueGraph:
        """Load JSON file into DialogueGraph"""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            raise ValueError("Dialogue file must be a JSON array")
        
        graph = DialogueGraph()
        
        for item in data:
            # Load talk_topic and other dialogue-related types (like TRIAL, etc.)
            item_type = item.get("type", "")
            # Accept talk_topic and any type that has an id and looks like a dialogue topic
            if item_type == "talk_topic" or (item_type and item.get("id") and "dynamic_line" in item):
                topic = DialogueTopic.from_json(item)
                # Preserve the original type even if it's not "talk_topic"
                if item_type != "talk_topic":
                    topic.type = item_type
                graph.add_topic(topic)
        
        return graph
    
    @staticmethod
    def export_file(graph: DialogueGraph, file_path: str) -> None:
        """Save DialogueGraph to JSON file"""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        json_data = graph.to_json()
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def validate_structure(data: Any) -> List[str]:
        """Check if JSON structure is valid"""
        errors = []
        
        if not isinstance(data, list):
            errors.append("Root must be a JSON array")
            return errors
        
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                errors.append(f"Item {i} is not an object")
                continue
            
            if "type" not in item:
                errors.append(f"Item {i} missing 'type' field")
            
            if item.get("type") == "talk_topic":
                if "id" not in item:
                    errors.append(f"Item {i} (talk_topic) missing 'id' field")
        
        return errors

