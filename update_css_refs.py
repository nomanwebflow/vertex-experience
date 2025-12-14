#!/usr/bin/env python3
"""
Update all HTML files to use combined.css instead of three separate CSS files.
"""
import os
import re

def main():
    project_dir = '/Users/noman/Downloads/vertex'
    
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"Updating {len(html_files)} HTML files...")
    print()
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern to match the three CSS link tags
        # They appear in this order: normalize.css, webflow.css, vertexexperience-staging...css
        pattern = r'(\s*<link href="(?:\.\./)?css/normalize\.css" rel="stylesheet" type="text/css">\s*\n\s*<link href="(?:\.\./)?css/webflow\.css" rel="stylesheet" type="text/css">\s*\n\s*<link href="(?:\.\./)?css/vertexexperience-staging-864a5215a71ee9\.webflow\.css" rel="stylesheet" type="text/css">)'
        
        # Determine the correct path prefix (../ for case-studies subdirectory)
        is_subdirectory = '/case-studies/' in html_file
        css_path = '../css/combined.css' if is_subdirectory else 'css/combined.css'
        
        # Replace with single combined.css link
        replacement = f'  <link href="{css_path}" rel="stylesheet" type="text/css">'
        
        content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated: {os.path.basename(html_file)}")
        else:
            print(f"✗ No changes: {os.path.basename(html_file)}")
    
    print()
    print("Complete!")

if __name__ == '__main__':
    main()
