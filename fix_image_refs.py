#!/usr/bin/env python3
"""
Fix all HTML references to match actual filenames in the images directory.
"""
import os
import re
from pathlib import Path

def main():
    project_dir = '/Users/noman/Downloads/vertex'
    images_dir = os.path.join(project_dir, 'images')
    
    print("Fixing HTML Image References")
    print("=" * 80)
    
    # Get all actual image filenames
    actual_images = set()
    for filename in os.listdir(images_dir):
        if not filename.startswith('.'):
            actual_images.add(filename)
    
    print(f"Found {len(actual_images)} images in directory")
    
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"Found {len(html_files)} HTML files")
    print()
    
    # Process each HTML file
    total_fixes = 0
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixes_in_file = 0
        
        # Find all image references
        # Pattern: images/filename or ../images/filename
        pattern = r'((?:\.\./)?images/)([^"\'\s]+)'
        
        def replace_image(match):
            nonlocal fixes_in_file
            prefix = match.group(1)
            old_filename = match.group(2)
            
            # Skip if it's part of srcset (contains space or 'w')
            if ' ' in old_filename or old_filename.endswith('w'):
                return match.group(0)
            
            # Check if file exists
            if old_filename in actual_images:
                return match.group(0)  # Already correct
            
            # Try to find the actual filename
            # Convert old filename to what it should be
            old_lower = old_filename.lower()
            
            # Look for exact match (case-insensitive)
            for actual in actual_images:
                if actual.lower() == old_lower:
                    fixes_in_file += 1
                    return prefix + actual
            
            # Look for similar filenames (handle the duplicate pattern issue)
            # e.g., About-Us---Image-1_1About-Us---Image-1.avif -> about-us-image-1-1about-us-image-1.avif
            for actual in actual_images:
                # Remove extension for comparison
                old_name, old_ext = os.path.splitext(old_filename)
                actual_name, actual_ext = os.path.splitext(actual)
                
                # Check if extensions match
                if old_ext.lower() != actual_ext.lower():
                    continue
                
                # Check if the actual filename contains the old filename pattern
                old_clean = re.sub(r'[^a-z0-9]', '', old_name.lower())
                actual_clean = re.sub(r'[^a-z0-9]', '', actual_name.lower())
                
                if old_clean in actual_clean or actual_clean in old_clean:
                    # Additional check: they should be similar enough
                    if len(old_clean) > 5 and len(actual_clean) > 5:
                        similarity = len(set(old_clean) & set(actual_clean)) / max(len(set(old_clean)), len(set(actual_clean)))
                        if similarity > 0.7:
                            fixes_in_file += 1
                            return prefix + actual
            
            # If no match found, return original
            return match.group(0)
        
        content = re.sub(pattern, replace_image, content)
        
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed {fixes_in_file} references in: {os.path.basename(html_file)}")
            total_fixes += fixes_in_file
    
    print()
    print("=" * 80)
    print(f"Total fixes: {total_fixes}")
    print("Complete!")

if __name__ == '__main__':
    main()
