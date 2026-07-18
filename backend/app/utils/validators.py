"""Input validation utilities."""

import re
from typing import Optional


def sanitize_input(text: str, max_length: int = 5000) -> str:
    """
    Sanitize user input by removing potentially harmful content.
    
    Args:
        text: Raw user input
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Trim whitespace
    text = text.strip()
    
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    return text


def validate_reflection_content(content: str) -> tuple[bool, Optional[str]]:
    """
    Validate reflection content.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not content or not content.strip():
        return False, "Reflection content cannot be empty"
    
    if len(content) > 5000:
        return False, "Reflection content must be less than 5000 characters"
    
    # Check for minimum meaningful content (at least 10 chars)
    if len(content.strip()) < 10:
        return False, "Reflection must be at least 10 characters long"
    
    return True, None


def validate_habit_id(habit_id: str) -> bool:
    """Validate habit ID format."""
    valid_habits = {
        'social_media',
        'screen_time', 
        'gaming',
        'procrastination',
        'junk_food',
        'other'
    }
    return habit_id in valid_habits


def escape_html(text: str) -> str:
    """Escape HTML special characters to prevent XSS."""
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }
    return "".join(html_escape_table.get(c, c) for c in text)
