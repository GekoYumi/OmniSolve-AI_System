"""
Text parsing utilities with optimized regex patterns.
Handles extraction of JSON and code from LLM outputs.
"""
import json
import re
from typing import Optional, List
from ..logging import get_logger

logger = get_logger('parsers')

# Pre-compiled regex patterns for efficiency
CODE_BLOCK_PATTERN = re.compile(r"```(?:python)?\s*(.*?)```", re.DOTALL)
COMMENT_PATTERN = re.compile(r'^\s*#', re.MULTILINE)


def extract_json(text: str) -> Optional[List[dict]]:
    """
    Extract JSON list from text using bracket counting.
    Robust against chatty explanations after the JSON.
    
    Args:
        text: Text potentially containing JSON
        
    Returns:
        Parsed JSON list or None if not found
        
    Raises:
        ParsingError: If JSON is malformed
    """
    text = text.strip()
    start_index = text.find('[')
    
    if start_index == -1:
        logger.debug("No JSON list found in text")
        return None
    
    # Scan forward from the first '['
    bracket_count = 0
    for i, char in enumerate(text[start_index:], start_index):
        if char == '[':
            bracket_count += 1
        elif char == ']':
            bracket_count -= 1
        
        # If brackets are balanced (count is 0) and we found at least one pair
        if bracket_count == 0:
            json_candidate = text[start_index:i+1]
            try:
                parsed = json.loads(json_candidate)
                if isinstance(parsed, list):
                    logger.debug(f"Successfully extracted JSON list with {len(parsed)} items")
                    return parsed
                else:
                    logger.warning("Extracted JSON is not a list")
                    return None
            except json.JSONDecodeError as e:
                # Maybe we stopped too early (nested brackets?), continue searching
                logger.debug(f"JSON decode failed at position {i}: {e}")
                continue
    
    logger.warning("Could not find valid JSON list in text")
    return None


def extract_json_any(text: str) -> Optional[object]:
    """
    Extract the first JSON value (object or array) from text.
    Returns the parsed JSON (dict or list), or None if none found.
    """
    text = text.strip()
    # Look for either '{' or '['
    idx_obj = text.find('{') if '{' in text else -1
    idx_arr = text.find('[') if '[' in text else -1
    if idx_obj == -1 and idx_arr == -1:
        logger.debug("No JSON object or array found in text")
        return None

    start_index = min([i for i in (idx_obj, idx_arr) if i != -1])
    opening = text[start_index]
    if opening == '{':
        open_ch, close_ch = '{', '}'
    else:
        open_ch, close_ch = '[', ']'

    depth = 0
    for i, ch in enumerate(text[start_index:], start_index):
        if ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
        if depth == 0:
            candidate = text[start_index:i+1]
            try:
                parsed = json.loads(candidate)
                logger.debug("Successfully extracted JSON value")
                return parsed
            except json.JSONDecodeError as e:
                logger.debug(f"JSON decode failed at position {i}: {e}")
                continue

    logger.debug("Could not extract any JSON value")
    return None


def extract_code(text: str, validate_non_empty: bool = True) -> Optional[str]:
    """
    Extract Python code from markdown code blocks.
    Validates that code contains more than just comments.
    
    Args:
        text: Text potentially containing code blocks
        validate_non_empty: If True, reject code that's only comments
        
    Returns:
        Extracted code or None if not found/invalid
    """
    matches = CODE_BLOCK_PATTERN.findall(text)
    
    for block in matches:
        if not validate_non_empty:
            return block
        
        # Filter out comments and empty lines
        lines = block.split('\n')
        code_lines = [
            line for line in lines 
            if line.strip() and not line.strip().startswith('#')
        ]
        
        if len(code_lines) > 0:
            logger.debug(f"Extracted code block with {len(lines)} lines ({len(code_lines)} non-comment)")
            return block
        else:
            logger.warning("Code block contains only comments, skipping")
    
    logger.debug("No valid code blocks found in text")
    return None


def extract_code_blocks(text: str) -> List[str]:
    """
    Extract all code blocks from text.
    
    Args:
        text: Text containing code blocks
        
    Returns:
        List of all code blocks found
    """
    return CODE_BLOCK_PATTERN.findall(text)


def validate_python_syntax(code: str) -> tuple[bool, Optional[str]]:
    """
    Validate Python code syntax without executing it.
    
    Args:
        code: Python code to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        compile(code, '<string>', 'exec')
        return True, None
    except SyntaxError as e:
        error_msg = f"Syntax error at line {e.lineno}: {e.msg}"
        logger.warning(f"Code validation failed: {error_msg}")
        return False, error_msg
    except Exception as e:
        error_msg = f"Validation error: {str(e)}"
        logger.warning(error_msg)
        return False, error_msg


def clean_response(text: str, remove_system_prompts: bool = True) -> str:
    """
    Clean LLM response by removing common artifacts.
    
    Args:
        text: Raw LLM response
        remove_system_prompts: Whether to remove system prompt markers
        
    Returns:
        Cleaned text
    """
    text = text.strip()
    
    if remove_system_prompts:
        # Remove common system markers
        markers = [
            "SYSTEM ROLE:",
            "[CURRENT TASK]",
            "[END]",
            "RESPONSE:",
            "USER:",
            "ASSISTANT:"
        ]
        for marker in markers:
            if marker in text:
                text = text.split(marker)[0].strip()
    
    return text


def extract_file_paths(text: str) -> List[str]:
    """
    Extract file paths from text.
    
    Args:
        text: Text containing file paths
        
    Returns:
        List of extracted file paths
    """
    # Pattern to match common file path formats
    pattern = r'(?:^|\s)([a-zA-Z0-9_\-./\\]+\.[a-zA-Z0-9]+)(?:\s|$|,|;)'
    matches = re.findall(pattern, text, re.MULTILINE)
    return list(set(matches))  # Remove duplicates
