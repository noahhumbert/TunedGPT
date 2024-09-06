# Formats text for easy readablity.
# Takes the raw text as an input.
# Returns the formatted text

# Imports
import re

def format_text(text):
    # Handle LaTeX math that already uses $$ or $ notation
    text = re.sub(r'\$\$\s*(.*?)\s*\$\$', r'$$\1$$', text)
    text = re.sub(r'\$\s*(.*?)\s*\$', r'$\1$', text)

    # Now we process LaTeX-like expressions without affecting those inside dollar signs
    # Ensure we're not wrapping already-wrapped expressions
    text = re.sub(r'(?<!\$)\\int(?!\$)', r'\\int', text)
    text = re.sub(r'(?<!\$)\\frac(?!\$)', r'\\frac', text)
    text = re.sub(r'(?<!\$)\\dx(?!\$)', r'\\dx', text)
    text = re.sub(r'(?<!\$)\\lim(?!\$)', r'\\lim', text)

    # Replace \[ and \] with $$
    text = re.sub(r'\\\[', r'$$', text)
    text = re.sub(r'\\\]', r'$$', text)

    # Replace newlines with <br> for HTML line breaks
    text = text.replace('\n', '<br>')

    # Replace **message** with <strong>message</strong>
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)

    return text

