#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify all pages are working correctly"""

import os
from pathlib import Path
import re

def check_file(filepath):
    """Check file for issues"""
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        dir_path = filepath.parent
        
        # Check images
        imgs = re.findall(r'<img[^>]+src="([^"]+)"', content)
        for img_src in imgs:
            if img_src.startswith('http'):
                continue
            if img_src.startswith('../'):
                img_path = dir_path.parent / img_src[3:]
            elif img_src.startswith('./'):
                img_path = dir_path / img_src[2:]
            else:
                img_path = dir_path / img_src
            
            if not img_path.exists():
                issues.append(f"Image missing: {img_src}")
        
        # Check links (skip external, anchors, mailto)
        hrefs = re.findall(r'<a[^>]+href="([^"]+)"', content)
        for href in hrefs:
            if href.startswith('#') or href.startswith('http') or href.startswith('mailto'):
                continue
            if href.startswith('../'):
                link_path = dir_path.parent / href[3:]
            elif href.startswith('./'):
                link_path = dir_path / href[2:]
            else:
                link_path = dir_path / href
            
            if '#' in str(link_path):
                link_path = Path(str(link_path).split('#')[0])
            
            if link_path and str(link_path) != '.' and not link_path.exists():
                issues.append(f"Link broken: {href}")
        
        return issues
    except Exception as e:
        return [f"Read error: {e}"]

def main():
    base_dir = Path(__file__).parent
    services_dir = base_dir / 'services'
    
    # Check all HTML files
    html_files = list(services_dir.glob('*.html'))
    html_files.extend([base_dir / f for f in ['index.html', 'case-report-implant-001.html']])
    
    total_issues = 0
    ok_count = 0
    
    for filepath in sorted(html_files):
        issues = check_file(filepath)
        if issues:
            print(f"\n[FILE] {filepath.name}")
            for issue in issues:
                print(f"  [ERROR] {issue}")
            total_issues += len(issues)
        else:
            ok_count += 1
    
    print(f"\n{'='*50}")
    print(f"OK files: {ok_count}")
    print(f"Files with issues: {total_issues}")
    
    return total_issues

if __name__ == '__main__':
    error_count = main()
    if error_count == 0:
        print("\n*** All pages verified successfully! ***")
    else:
        print(f"\n*** Found {error_count} issues to fix ***")
