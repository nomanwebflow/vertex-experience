#!/usr/bin/env python3
"""
Script to rename image files to URL-friendly names and update HTML references.
"""
import os
import re
import shutil
from pathlib import Path

def make_url_friendly(filename):
    """Convert filename to URL-friendly format."""
    # Split filename and extension
    name, ext = os.path.splitext(filename)
    
    # Remove duplicate naming patterns like "filename_1filename"
    # Pattern: word_1word or word_1Word
    name = re.sub(r'(.+?)_1\1', r'\1', name, flags=re.IGNORECASE)
    
    # Remove hash prefixes (e.g., "365cf3adf1b8ced6ecc57c70b839f820_")
    name = re.sub(r'^[a-f0-9]{32}_', '', name)
    
    # Replace multiple hyphens/underscores with single hyphen
    name = re.sub(r'[-_]+', '-', name)
    
    # Remove special characters, keep only alphanumeric, hyphens, and 'p' for responsive suffixes
    # Keep patterns like "-p-500", "-p-800", etc.
    name = re.sub(r'[^\w\-]', '-', name)
    
    # Replace multiple hyphens with single hyphen
    name = re.sub(r'-+', '-', name)
    
    # Convert to lowercase
    name = name.lower()
    
    # Remove leading/trailing hyphens
    name = name.strip('-')
    
    # Reconstruct filename
    return name + ext.lower()

def generate_mapping(images_dir):
    """Generate mapping of old to new filenames."""
    mapping = {}
    
    for filename in os.listdir(images_dir):
        if filename.startswith('.'):
            continue
            
        new_filename = make_url_friendly(filename)
        
        # Only add to mapping if filename changes
        if filename != new_filename:
            mapping[filename] = new_filename
    
    return mapping

def rename_files(images_dir, mapping, dry_run=False):
    """Rename files according to mapping."""
    renamed_count = 0
    
    for old_name, new_name in mapping.items():
        old_path = os.path.join(images_dir, old_name)
        new_path = os.path.join(images_dir, new_name)
        
        if not os.path.exists(old_path):
            print(f"Warning: {old_name} does not exist, skipping...")
            continue
        
        if os.path.exists(new_path) and old_path != new_path:
            print(f"Warning: {new_name} already exists, skipping {old_name}...")
            continue
        
        if dry_run:
            print(f"Would rename: {old_name} -> {new_name}")
        else:
            shutil.move(old_path, new_path)
            print(f"Renamed: {old_name} -> {new_name}")
        
        renamed_count += 1
    
    return renamed_count

def update_html_files(project_dir, mapping, dry_run=False):
    """Update HTML files with new image references."""
    html_files = []
    
    # Find all HTML files
    for root, dirs, files in os.walk(project_dir):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    updated_files = []
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace image references
        for old_name, new_name in mapping.items():
            # Escape special regex characters in filenames
            old_name_escaped = re.escape(old_name)
            
            # Replace in src and href attributes
            # Pattern: images/filename or ../images/filename
            content = re.sub(
                rf'((?:\.\./)?images/)({old_name_escaped})',
                rf'\1{new_name}',
                content
            )
        
        if content != original_content:
            if dry_run:
                print(f"Would update: {html_file}")
            else:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated: {html_file}")
            
            updated_files.append(html_file)
    
    return updated_files

def main():
    project_dir = '/Users/noman/Downloads/vertex'
    images_dir = os.path.join(project_dir, 'images')
    
    print("=" * 80)
    print("Image Renaming Script - URL-Friendly Names")
    print("=" * 80)
    print()
    
    # Generate mapping
    print("Generating filename mapping...")
    mapping = generate_mapping(images_dir)
    
    print(f"Found {len(mapping)} files to rename")
    print()
    
    # Save mapping to file for reference
    mapping_file = os.path.join(project_dir, 'image_rename_mapping.txt')
    with open(mapping_file, 'w', encoding='utf-8') as f:
        f.write("OLD_FILENAME -> NEW_FILENAME\n")
        f.write("=" * 80 + "\n")
        for old, new in sorted(mapping.items()):
            f.write(f"{old} -> {new}\n")
    
    print(f"Mapping saved to: {mapping_file}")
    print()
    
    # Rename files
    print("Renaming image files...")
    renamed_count = rename_files(images_dir, mapping, dry_run=False)
    print(f"Renamed {renamed_count} files")
    print()
    
    # Update HTML files
    print("Updating HTML files...")
    updated_files = update_html_files(project_dir, mapping, dry_run=False)
    print(f"Updated {len(updated_files)} HTML files")
    print()
    
    print("=" * 80)
    print("Complete!")
    print("=" * 80)

if __name__ == '__main__':
    main()
