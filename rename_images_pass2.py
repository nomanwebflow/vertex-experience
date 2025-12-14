#!/usr/bin/env python3
"""
Second pass: Fix remaining uppercase and special character filenames.
"""
import os
import re
import shutil

def make_url_friendly_v2(filename):
    """Convert filename to URL-friendly format - improved version."""
    # Split filename and extension
    name, ext = os.path.splitext(filename)
    
    # Remove duplicate naming patterns more aggressively
    # Pattern 1: word_1word or word_1Word or Word_1Word
    while True:
        new_name = re.sub(r'(.+?)_1\1', r'\1', name, flags=re.IGNORECASE)
        if new_name == name:
            break
        name = new_name
    
    # Remove hash prefixes
    name = re.sub(r'^[a-f0-9]{32}_', '', name)
    
    # Replace underscores with hyphens
    name = name.replace('_', '-')
    
    # Remove special characters, keep only alphanumeric and hyphens
    name = re.sub(r'[^\w\-]', '-', name)
    
    # Replace multiple hyphens with single hyphen
    name = re.sub(r'-+', '-', name)
    
    # Convert to lowercase
    name = name.lower()
    
    # Remove leading/trailing hyphens
    name = name.strip('-')
    
    return name + ext.lower()

def main():
    project_dir = '/Users/noman/Downloads/vertex'
    images_dir = os.path.join(project_dir, 'images')
    
    print("Second Pass - Fixing Remaining Files")
    print("=" * 80)
    
    # Generate new mapping
    mapping = {}
    for filename in os.listdir(images_dir):
        if filename.startswith('.'):
            continue
        
        new_filename = make_url_friendly_v2(filename)
        
        if filename != new_filename:
            # Check if target already exists
            old_path = os.path.join(images_dir, filename)
            new_path = os.path.join(images_dir, new_filename)
            
            if os.path.exists(new_path) and old_path.lower() != new_path.lower():
                # File exists and it's not just a case change
                # Delete the old file since the new one already exists
                print(f"Deleting duplicate: {filename} (keeping {new_filename})")
                os.remove(old_path)
            else:
                mapping[filename] = new_filename
    
    print(f"\nFound {len(mapping)} files to rename")
    
    # Rename files
    for old_name, new_name in mapping.items():
        old_path = os.path.join(images_dir, old_name)
        new_path = os.path.join(images_dir, new_name)
        
        if not os.path.exists(old_path):
            continue
        
        # Use a temporary name for case-only changes on case-insensitive filesystems
        if old_name.lower() == new_name.lower():
            temp_path = old_path + '.tmp'
            shutil.move(old_path, temp_path)
            shutil.move(temp_path, new_path)
            print(f"Renamed (case): {old_name} -> {new_name}")
        else:
            shutil.move(old_path, new_path)
            print(f"Renamed: {old_name} -> {new_name}")
    
    # Update HTML files
    print("\nUpdating HTML files...")
    html_files = []
    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace all image references
        for old_name, new_name in mapping.items():
            old_name_escaped = re.escape(old_name)
            content = re.sub(
                rf'((?:\.\./)?images/)({old_name_escaped})',
                rf'\1{new_name}',
                content
            )
        
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {html_file}")
    
    print("\n" + "=" * 80)
    print("Complete!")

if __name__ == '__main__':
    main()
