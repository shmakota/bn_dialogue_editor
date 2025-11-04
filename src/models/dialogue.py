"""Dialogue data models"""

from typing import List, Dict, Optional, Any, Union
from dataclasses import dataclass, field


@dataclass
class DialogueTopic:
    """Represents a single talk_topic"""
    id: str
    type: str = "talk_topic"
    dynamic_line: Optional[Union[str, Dict[str, Any], List[Any]]] = None
    speaker_effect: Optional[Dict[str, Any]] = None
    responses: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_json(self) -> Dict[str, Any]:
        """Convert to JSON dictionary"""
        result = {
            "type": self.type,
            "id": self.id
        }
        
        if self.dynamic_line is not None:
            # Export as-is (string, dict, or list for random selection)
            result["dynamic_line"] = self.dynamic_line
        
        if self.speaker_effect:
            result["speaker_effect"] = self.speaker_effect
        
        if self.responses:
            result["responses"] = self.responses
        
        return result
    
    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'DialogueTopic':
        """Create from JSON dictionary"""
        # Handle dynamic_line - it can be a string, a dict (conditional), a list (random selection), or missing
        dynamic_line_raw = data.get("dynamic_line")
        
        if dynamic_line_raw is None:
            # Missing field - default to None
            dynamic_line = None
        elif isinstance(dynamic_line_raw, dict):
            # Conditional dynamic line (dict) - store as dict
            dynamic_line = dynamic_line_raw
        elif isinstance(dynamic_line_raw, str):
            # Single string
            dynamic_line = dynamic_line_raw.strip() if dynamic_line_raw.strip() else None
        elif isinstance(dynamic_line_raw, list):
            # List - can be array of strings (random selection) or complex structure
            # For now, keep as list for random selection
            dynamic_line = dynamic_line_raw
        else:
            # Other type - try to convert to string
            try:
                as_string = str(dynamic_line_raw).strip()
                dynamic_line = as_string if as_string else None
            except:
                dynamic_line = None
        
        return cls(
            id=data.get("id", ""),
            type=data.get("type", "talk_topic"),
            dynamic_line=dynamic_line,
            speaker_effect=data.get("speaker_effect"),
            responses=data.get("responses", [])
        )
    
    def validate(self) -> List[str]:
        """Validate topic and return list of errors"""
        errors = []
        
        if not self.id:
            errors.append("Topic ID is required")
        
        # dynamic_line is optional - can be None, string, dict, or list
        # No validation needed for presence
        
        return errors


class DialogueGraph:
    """Manages collection of topics and connections"""
    
    def __init__(self):
        self.topics: Dict[str, DialogueTopic] = {}
    
    def add_topic(self, topic: DialogueTopic) -> None:
        """Add a topic to the graph"""
        self.topics[topic.id] = topic
    
    def remove_topic(self, topic_id: str) -> bool:
        """Remove a topic from the graph"""
        if topic_id in self.topics:
            del self.topics[topic_id]
            # Remove references from other topics
            for topic in self.topics.values():
                topic.responses = [
                    resp for resp in topic.responses 
                    if resp.get("topic") != topic_id
                ]
            return True
        return False
    
    def get_topic(self, topic_id: str) -> Optional[DialogueTopic]:
        """Get a topic by ID"""
        return self.topics.get(topic_id)
    
    def get_connections(self, topic_id: str) -> List[str]:
        """Get all topic IDs that this topic connects to"""
        topic = self.get_topic(topic_id)
        if not topic:
            return []
        
        connections = []
        for response in topic.responses:
            # Check for direct topic
            target = response.get("topic")
            if target and target not in connections:
                connections.append(target)
            
            # Check for trial with success/failure
            if "trial" in response:
                success = response.get("success", {})
                failure = response.get("failure", {})
                
                success_topic = success.get("topic") if isinstance(success, dict) else None
                failure_topic = failure.get("topic") if isinstance(failure, dict) else None
                
                if success_topic and success_topic not in connections:
                    connections.append(success_topic)
                if failure_topic and failure_topic not in connections:
                    connections.append(failure_topic)
        
        return connections
    
    def get_incoming_connections(self, topic_id: str) -> List[str]:
        """Get all topic IDs that connect to this topic"""
        incoming = []
        for topic_id_other, topic in self.topics.items():
            for response in topic.responses:
                # Check direct topic
                if response.get("topic") == topic_id:
                    incoming.append(topic_id_other)
                    break
                
                # Check trial success/failure
                if "trial" in response:
                    success = response.get("success", {})
                    failure = response.get("failure", {})
                    
                    success_topic = success.get("topic") if isinstance(success, dict) else None
                    failure_topic = failure.get("topic") if isinstance(failure, dict) else None
                    
                    if success_topic == topic_id or failure_topic == topic_id:
                        incoming.append(topic_id_other)
                        break
        return incoming
    
    def to_json(self) -> List[Dict[str, Any]]:
        """Export to JSON array"""
        return [topic.to_json() for topic in self.topics.values()]
    
    def validate_references(self) -> List[str]:
        """Check that all topic references exist"""
        errors = []
        special_topics = {"TALK_NONE", "TALK_DONE", "TALK_TRAIN"}
        
        for topic in self.topics.values():
            for response in topic.responses:
                # Check direct topic reference
                target = response.get("topic")
                if target and target not in special_topics and target not in self.topics:
                    errors.append(
                        f"Topic {topic.id} references non-existent topic: {target}"
                    )
                
                # Check trial success/failure references
                if "trial" in response:
                    success = response.get("success", {})
                    failure = response.get("failure", {})
                    
                    success_topic = success.get("topic") if isinstance(success, dict) else None
                    failure_topic = failure.get("topic") if isinstance(failure, dict) else None
                    
                    if success_topic and success_topic not in special_topics and success_topic not in self.topics:
                        errors.append(
                            f"Topic {topic.id} trial success references non-existent topic: {success_topic}"
                        )
                    
                    if failure_topic and failure_topic not in special_topics and failure_topic not in self.topics:
                        errors.append(
                            f"Topic {topic.id} trial failure references non-existent topic: {failure_topic}"
                        )
        
        return errors
    
    def validate_ids(self) -> List[str]:
        """Check for duplicate IDs"""
        errors = []
        seen_ids = set()
        
        for topic in self.topics.values():
            if topic.id in seen_ids:
                errors.append(f"Duplicate topic ID: {topic.id}")
            seen_ids.add(topic.id)
        
        return errors

