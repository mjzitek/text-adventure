"""
Text formatting utilities for the text adventure game.
Provides functions for styling terminal text with colors and formatting.
"""

# ANSI escape codes for text styling
RESET = "\033[0m"
BOLD = "\033[1m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
REVERSE = "\033[7m"

# Text colors
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# Background colors
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

def bold(text):
    """Format text as bold."""
    return f"{BOLD}{text}{RESET}"

def italic(text):
    """Format text as italic."""
    return f"{ITALIC}{text}{RESET}"

def underline(text):
    """Format text as underlined."""
    return f"{UNDERLINE}{text}{RESET}"

def colored(text, color):
    """Format text with specified color."""
    return f"{color}{text}{RESET}"

def bg_colored(text, bg_color):
    """Format text with specified background color."""
    return f"{bg_color}{text}{RESET}"

def styled(text, *styles):
    """Apply multiple styles to text."""
    styled_text = text
    for style in styles:
        styled_text = f"{style}{styled_text}"
    return f"{styled_text}{RESET}"

def format_markdown(text):
    """Format markdown text with appropriate terminal styling.
    
    Handles:
    - Headers (# Header)
    - Bold (**text**)
    - Italic (*text*)
    - Underline (_text_)
    - Bullet points (- item)
    - Numbered lists (1. item)
    - Blockquotes (> text)
    - Code blocks (```code```)
    - Horizontal rules (---, ___, ***)
    """
    import re
    
    # Process headers (# Header)
    for i in range(6, 0, -1):  # Process h6 to h1
        pattern = r'^' + r'#' * i + r'\s+(.+?)$'
        if i <= 2:  # h1 and h2 get special treatment
            color = CYAN if i == 1 else YELLOW
            text = re.sub(pattern, 
                         lambda m: f"\n{BOLD}{color}{m.group(1)}{RESET}\n", 
                         text, 
                         flags=re.MULTILINE)
        else:
            text = re.sub(pattern, 
                         lambda m: f"\n{BOLD}{m.group(1)}{RESET}", 
                         text, 
                         flags=re.MULTILINE)
    
    # Process bold (**text**)
    text = re.sub(r'\*\*(.*?)\*\*', lambda m: f"{BOLD}{m.group(1)}{RESET}", text)
    
    # Process italic (*text*)
    text = re.sub(r'(?<!\*)\*([^\*]+)\*(?!\*)', lambda m: f"{ITALIC}{m.group(1)}{RESET}", text)
    
    # Process underline (_text_)
    text = re.sub(r'(?<!_)_([^_]+)_(?!_)', lambda m: f"{UNDERLINE}{m.group(1)}{RESET}", text)
    
    # Process bullet points
    text = re.sub(r'^(\s*)-\s+(.+?)$',
                 lambda m: f"{m.group(1)}• {m.group(2)}",
                 text,
                 flags=re.MULTILINE)
    
    # Process numbered lists with color
    text = re.sub(r'^(\s*)(\d+)\.\s+(.+?)$',
                 lambda m: f"{m.group(1)}{YELLOW}{m.group(2)}.{RESET} {m.group(3)}",
                 text,
                 flags=re.MULTILINE)
    
    # Process blockquotes
    text = re.sub(r'^(\s*)>\s+(.+?)$',
                 lambda m: f"{m.group(1)}{CYAN}│ {m.group(2)}{RESET}",
                 text,
                 flags=re.MULTILINE)
    
    # Process horizontal rules
    text = re.sub(r'^(\s*)(---|\*\*\*|___)(\s*)$',
                 lambda m: f"\n{CYAN}{'─' * 80}{RESET}\n",
                 text,
                 flags=re.MULTILINE)
    
    return text

def format_choices(choices_text):
    """Format the choices section of the story output.
    
    Converts markdown-style formatting to terminal formatting.
    Example: "**Choices:**" becomes bold text.
    """
    lines = choices_text.split('\n')
    formatted_lines = []
    
    for line in lines:
        # Format "**Choices:**" or "Choices:" as bold
        if "**Choices:**" in line:
            line = line.replace("**Choices:**", f"{BOLD}Choices:{RESET}")
        elif "Choices:" in line:
            line = line.replace("Choices:", f"{BOLD}Choices:{RESET}")
        
        # Format numbered choices with color and handle potential bold formatting in choices
        # Check for various formats: "1.", "**1.**", etc.
        import re
        choice_pattern = re.compile(r'^(\s*)(\*\*)?(\d+)(\.\*\*|\.)(.*)$')
        match = choice_pattern.match(line)
        
        if match:
            spaces = match.group(1)
            number = match.group(3)
            rest = match.group(5)
            
            # Apply yellow color to the number
            line = f"{spaces}{YELLOW}{number}.{RESET}{rest}"
        
        formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)

def format_story_text(text):
    """Format the entire story text with appropriate styling.
    
    Handles various markdown-style formatting in the story text.
    """
    # First, apply general markdown formatting
    text = format_markdown(text)
    
    # Check for different ways the choices section might be formatted
    choices_patterns = ["Choices:", "CHOICES:", "**Choices:**", "**CHOICES:**"]
    
    for pattern in choices_patterns:
        if pattern in text:
            # Split the text to separate the story from choices
            parts = text.split(pattern, 1)
            
            if len(parts) > 1:
                story_text = parts[0]
                choices_text = "Choices:" + parts[1]  # Normalize to "Choices:"
                
                # Format the choices section
                formatted_choices = format_choices(choices_text)
                
                return story_text + formatted_choices
    
    # If we reach here, either there's no choices section or it's already been processed
    return text 