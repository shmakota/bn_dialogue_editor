"""Helper utility functions"""

from typing import Tuple


def calculate_node_size(text_lines: list, min_width: int = 150, min_height: int = 60) -> Tuple[int, int]:
    """Calculate node size based on content"""
    if not text_lines:
        return (min_width, min_height)
    
    # Estimate width based on longest line
    max_line_length = max(len(line) for line in text_lines if line)
    width = max(min_width, min(300, max_line_length * 7 + 40))
    
    # Estimate height based on number of lines
    height = max(min_height, len(text_lines) * 20 + 60)
    
    return (width, height)


def truncate_text(text: str, max_length: int = 40) -> str:
    """Truncate text with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def format_topic_id(topic_id: str, max_length: int = 30) -> str:
    """Format topic ID for display"""
    return truncate_text(topic_id, max_length)




