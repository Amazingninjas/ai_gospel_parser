
import sys
from bs4 import BeautifulSoup
import re

def strip_html_to_text(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Get all the text from the body
    if soup.body:
        text_content = soup.body.get_text()
    else:
        text_content = soup.get_text()

    # Clean up the text
    lines = text_content.split('\n')
    cleaned_lines = []
    for line in lines:
        # Remove leading/trailing whitespace
        line = line.strip()
        # Skip empty lines
        if not line:
            continue
        # Skip lines that are likely javascript or css
        if re.match(r'^\s*[\{\}\(\);,\[\]]', line):
            continue
        if 'function(' in line or 'var ' in line:
            continue
        
        cleaned_lines.append(line)

    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned_lines))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python strip_html.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    strip_html_to_text(input_file, output_file)
