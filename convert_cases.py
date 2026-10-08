#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert old Vocus case files to Tailwind CSS style
"""

import os
import re
import glob
from pathlib import Path

# Template for new case pages
CASE_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | 治療案例 | 科技渥爾牙醫診所</title>
  <meta name="description" content="{description}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>tailwind.config={{theme:{{extend:{{colors:{{primary:{{50:'#eff6ff',100:'#dbeafe',200:'#bfdbfe',600:'#1E3A8A',700:'#1e3a8a',800:'#1e40af'}},warm:{{50:'#faf7f2',100:'#f5f0e6'}},titanium:{{50:'#f8f9fa',100:'#e9ecef',200:'#dee2e6',300:'#ced4da',400:'#adb5bd',500:'#6c757d',600:'#495057',700:'#343a40',800:'#212529'}}}}}}}}</script>
  <style>html{{scroll-behavior:smooth}}.nav-link{{position:relative}}.nav-link::after{{content:'';position:absolute;bottom:-4px;left:0;width:0;height:2px;background:#1E3A8A;transition:width .3s}}.nav-link:hover::after{{width:100%}}</style>
</head>
<body class="font-sans text-titanium-700 antialiased bg-titanium-50">

<!-- Navigation -->
<nav class="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-md shadow-sm">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between items-center h-20">
      <a href="../index.html" class="flex items-center space-x-3">
        <div class="w-10 h-10 bg-primary-600 rounded-xl flex items-center justify-center text-white text-xl shadow-lg"><i class="fas fa-tooth"></i></div>
        <div><span class="text-xl font-bold text-primary-600">科技渥爾</span><span class="text-sm text-titanium-500 block -mt-1">牙醫診所</span></div>
      </a>
      <div class="hidden lg:flex items-center space-x-8">
        <a href="../index.html" class="nav-link text-titanium-700 hover:text-primary-600 font-medium">回首頁</a>
        <a href="cases.html" class="nav-link text-primary-600 font-medium">治療案例</a>
        <a href="https://line.me/R/ti/p/@599heehy" target="_blank" class="bg-green-500 hover:bg-green-600 text-white px-6 py-2.5 rounded-full font-medium text-sm inline-flex items-center space-x-2 transition-all hover:-translate-y-0.5"><i class="fab fa-line"></i><span>Line</span></a>
      </div>
      <button class="lg:hidden text-titanium-700 p-2" onclick="document.getElementById('mobile-menu').classList.toggle('hidden')"><i class="fas fa-bars text-2xl"></i></button>
    </div>
  </div>
  <div id="mobile-menu" class="lg:hidden hidden bg-white border-t border-titanium-100">
    <div class="px-4 py-4 space-y-3">
      <a href="../index.html" class="block py-2 text-titanium-700 font-medium">回首頁</a>
      <a href="cases.html" class="block py-2 text-primary-600 font-medium">治療案例</a>
      <a href="https://line.me/R/ti/p/@599heehy" target="_blank" class="block bg-green-500 text-white px-6 py-3 rounded-full font-medium text-center mt-4"><i class="fab fa-line mr-2"></i>Line</a>
    </div>
  </div>
</nav>

<!-- Hero Section -->
<section class="relative pt-32 pb-16 bg-gradient-to-br from-primary-600 to-primary-700">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="text-center">
      <div class="inline-flex items-center space-x-2 bg-white/20 backdrop-blur-sm rounded-full px-4 py-2 mb-6 text-sm font-medium text-white/90">
        <i class="fas fa-file-medical-alt"></i>
        <span>治療案例</span>
      </div>
      <h1 class="text-4xl lg:text-5xl font-bold text-white mb-4">{title}</h1>
      <div class="flex items-center justify-center space-x-4 text-white/80 text-sm">
        <span><i class="fas fa-calendar-alt mr-2"></i>{date}</span>
        <span>·</span>
        <span>{category}</span>
      </div>
    </div>
  </div>
</section>

<!-- Content -->
<section class="py-16 bg-white">
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
    {content}
  </div>
</section>

<!-- CTA -->
<section class="py-16 bg-gradient-to-br from-primary-600 to-primary-700">
  <div class="max-w-4xl mx-auto px-4 text-center">
    <h2 class="text-2xl lg:text-3xl font-bold text-white mb-4">想了解更多治療方案？</h2>
    <p class="text-white/80 mb-8">每個人的口腔狀況都不同，讓我們為您量身規劃最適合的治療方案。</p>
    <a href="https://line.me/R/ti/p/@599heehy" target="_blank" class="bg-white text-green-600 px-8 py-4 rounded-full font-bold text-lg inline-flex items-center space-x-3 shadow-2xl hover:-translate-y-1 transition-all">
      <i class="fab fa-line"></i><span>Line</span>
    </a>
  </div>
</section>

<!-- Footer -->
<footer class="bg-titanium-800 text-white py-12">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="grid md:grid-cols-3 gap-8">
      <div>
        <div class="flex items-center space-x-3 mb-4">
          <div class="w-10 h-10 bg-primary-600 rounded-xl flex items-center justify-center text-white text-xl"><i class="fas fa-tooth"></i></div>
          <div><span class="text-xl font-bold">科技渥爾</span><span class="text-sm text-titanium-400 block">牙醫診所</span></div>
        </div>
        <p class="text-titanium-400 text-sm">以專業與溫度，打造專屬於您的自信微笑。</p>
      </div>
      <div>
        <div class="font-bold mb-4">聯絡我們</div>
        <div class="space-y-2 text-titanium-400 text-sm">
          <div><i class="fas fa-map-marker-alt w-5"></i> 台北市大安區復興南路二段302號</div>
          <div><i class="fab fa-line w-5 text-green-400"></i> <a href="https://line.me/R/ti/p/@599heehy" target="_blank" class="hover:text-white">@599heehy</a></div>
        </div>
      </div>
      <div>
        <div class="font-bold mb-4">快速導覽</div>
        <div class="grid grid-cols-2 gap-2 text-sm">
          <a href="../index.html" class="text-titanium-400 hover:text-white">回診所首頁</a>
          <a href="cases.html" class="text-titanium-400 hover:text-white">治療案例</a>
        </div>
      </div>
    </div>
    <div class="border-t border-titanium-700 mt-8 pt-8 text-center text-titanium-500 text-sm">
      © 2024 科技渥爾牙醫診所. All rights reserved.
    </div>
  </div>
</footer>

</body>
</html>
'''

def extract_case_info(content):
    """Extract case information from old file"""
    # Try to extract title
    title_match = re.search(r'<title>([^<|]+)', content)
    title = title_match.group(1).strip() if title_match else "治療案例"
    # Clean up garbled characters
    title = title.replace('', '').replace('| 治療案例 | 科技渥爾牙醫診所', '').strip()
    if not title or title == '治':
        title = "治療案例"
    
    # Extract date from content
    date_match = re.search(r'(\d{4})/(\d{1,2})/(\d{1,2})', content)
    date = date_match.group(0) if date_match else "2025/01/01"
    
    # Extract main content - find text between body tags
    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
    if body_match:
        body_content = body_match.group(1)
        # Remove header, footer, nav
        body_content = re.sub(r'<header.*?</header>', '', body_content, flags=re.DOTALL)
        body_content = re.sub(r'<footer.*?</footer>', '', body_content, flags=re.DOTALL)
        body_content = re.sub(r'<nav.*?</nav>', '', body_content, flags=re.DOTALL)
        # Remove script tags
        body_content = re.sub(r'<script.*?</script>', '', body_content, flags=re.DOTALL)
        # Keep main content
        main_match = re.search(r'<main[^>]*>(.*?)</main>', body_content, re.DOTALL)
        if main_match:
            content_html = main_match.group(1)
        else:
            content_html = body_content
    else:
        content_html = "<p>案例內容整理中...</p>"
    
    # Clean up the content
    content_html = re.sub(r'class="[^"]*"', '', content_html)  # Remove old classes
    content_html = re.sub(r'style="[^"]*"', '', content_html)  # Remove inline styles
    
    # Wrap in Tailwind classes
    # Convert sections to Tailwind styled sections
    content_html = f'<div class="prose prose-lg max-w-none">{content_html}</div>'
    
    return {
        'title': title,
        'date': date,
        'category': '牙科治療',
        'description': f'{title} - 科技渥爾牙醫診所治療案例',
        'content': content_html
    }

def convert_case_file(filepath):
    """Convert a single case file"""
    try:
        # Read with different encodings
        content = None
        for encoding in ['utf-8', 'big5', 'gbk', 'latin-1']:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except:
                continue
        
        if not content:
            print(f"Failed to read {filepath}")
            return False
        
        info = extract_case_info(content)
        new_html = CASE_TEMPLATE.format(**info)
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print(f"Converted: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(f"Error converting {filepath}: {e}")
        return False

def main():
    services_dir = Path(__file__).parent / 'services'
    case_files = list(services_dir.glob('case-vocus-*.html'))
    
    print(f"Found {len(case_files)} case files to convert")
    
    success_count = 0
    for filepath in case_files:
        if convert_case_file(filepath):
            success_count += 1
    
    print(f"\nConverted {success_count}/{len(case_files)} files successfully")

if __name__ == '__main__':
    main()
