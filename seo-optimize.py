#!/usr/bin/env python3
"""
SEO Optimization Script
Optimizes all HTML files with:
- JSON-LD structured data (WebApplication schema)
- Open Graph meta tags
- Twitter Card meta tags
- Better meta descriptions
- FAQ schema markup
"""

import os
import re
from pathlib import Path
from html.parser import HTMLParser

# Skip these files
SKIP_FILES = {'index.html', 'ad-template.html', 'sitemap.xml'}

def get_tool_name(filename):
    """Convert filename to readable tool name"""
    name = filename.replace('.html', '').replace('-', ' ')
    # Capitalize each word
    name = ' '.join(word.capitalize() for word in name.split())
    # Fix common abbreviations
    name = name.replace('Bmi', 'BMI').replace('Tdee', 'TDEE').replace('Roi', 'ROI')
    name = name.replace('Apr', 'APR').replace('Emi', 'EMI').replace('Gpa', 'GPA')
    name = name.replace('Sip', 'SIP').replace('Pmi', 'PMI').replace('Dti', 'DTI')
    name = name.replace('Heloc', 'HELOC').replace('Hvac', 'HVAC').replace('Ira', 'IRA')
    name = name.replace('Sql', 'SQL').replace('Html', 'HTML').replace('Css', 'CSS')
    name = name.replace('Json', 'JSON').replace('Url', 'URL').replace('Uuid', 'UUID')
    name = name.replace('Bac', 'BAC').replace('Atv', 'ATV').replace('Rv', 'RV')
    name = name.replace('Ac ', 'AC ').replace('Btu', 'BTU').replace('Dui', 'DUI')
    name = name.replace(' 401k', ' 401(k)').replace(' 529', ' 529').replace(' 1099', ' 1099')
    return name

def get_category(filename):
    """Determine tool category based on filename"""
    filename_lower = filename.lower()

    if any(kw in filename_lower for kw in ['bmi', 'calorie', 'weight', 'body', 'fat', 'tdee', 'macro', 'protein', 'pregnancy', 'baby', 'due-date', 'ovulation', 'blood', 'heart', 'sleep', 'water', 'caffeine', 'alcohol', 'bac']):
        return 'Health & Fitness'
    elif any(kw in filename_lower for kw in ['loan', 'mortgage', 'investment', 'compound', 'savings', 'retirement', '401k', 'ira', 'roth', 'tax', 'income', 'salary', 'budget', 'debt', 'credit', 'apr', 'roi', 'cap-rate', 'amortization', 'annuity', 'cd-', 'interest', 'inflation', 'net-worth', 'finance', 'payment', 'lease']):
        return 'Finance'
    elif any(kw in filename_lower for kw in ['concrete', 'paint', 'flooring', 'roofing', 'tile', 'carpet', 'deck', 'fence', 'drywall', 'insulation', 'mulch', 'gravel', 'brick', 'square-foot', 'room', 'kitchen', 'bathroom', 'basement', 'garage', 'attic', 'cabinet', 'countertop', 'hvac', 'ac-', 'lawn', 'pool', 'remodel', 'renovation', 'siding', 'gutter', 'window', 'door', 'lighting', 'electric', 'plumbing', 'landscaping', 'patio', 'asphalt', 'stair']):
        return 'Home Improvement'
    elif any(kw in filename_lower for kw in ['settlement', 'lawsuit', 'injury', 'accident', 'malpractice', 'wrongful', 'disability', 'workers-comp', 'alimony', 'child-support', 'divorce', 'custody']):
        return 'Legal'
    elif any(kw in filename_lower for kw in ['color', 'gradient', 'shadow', 'border', 'css', 'html', 'json', 'base64', 'binary', 'hex', 'unicode', 'regex', 'markdown', 'text', 'character', 'word', 'case', 'string', 'qr', 'barcode', 'password', 'hash', 'uuid', 'timestamp', 'epoch']):
        return 'Developer Tools'
    elif any(kw in filename_lower for kw in ['age', 'date', 'time', 'countdown', 'days', 'hours', 'birthday', 'anniversary']):
        return 'Date & Time'
    elif any(kw in filename_lower for kw in ['unit', 'converter', 'length', 'area', 'volume', 'temperature', 'speed', 'mass', 'currency']):
        return 'Converters'
    elif any(kw in filename_lower for kw in ['percentage', 'fraction', 'ratio', 'average', 'mean', 'median', 'standard-deviation', 'probability', 'statistics', 'chi-square', 'anova', 'z-score', 't-test']):
        return 'Math & Statistics'
    else:
        return 'Calculators'

def generate_json_ld(tool_name, filename, description, category):
    """Generate JSON-LD structured data for a tool"""
    url = f"https://austron24.github.io/webaudit-tools/{filename}"

    json_ld = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "{tool_name}",
  "url": "{url}",
  "description": "{description}",
  "applicationCategory": "{category}",
  "operatingSystem": "Any",
  "offers": {{
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  }},
  "browserRequirements": "Requires JavaScript",
  "softwareVersion": "1.0",
  "author": {{
    "@type": "Organization",
    "name": "WebAudit Tools"
  }}
}}
</script>'''
    return json_ld

def generate_faq_schema(tool_name, category):
    """Generate FAQ schema for common questions"""
    faqs = []

    if 'Calculator' in tool_name:
        faqs.append({
            "question": f"How do I use the {tool_name}?",
            "answer": f"Simply enter your values in the input fields and the {tool_name} will automatically calculate the results in real-time. All calculations are done instantly in your browser."
        })
        faqs.append({
            "question": f"Is the {tool_name} free to use?",
            "answer": f"Yes, the {tool_name} is completely free to use with no registration required. Use it as many times as you need."
        })
        faqs.append({
            "question": f"How accurate is the {tool_name}?",
            "answer": f"Our {tool_name} uses standard formulas and calculations. Results are accurate based on the inputs provided. For professional or medical decisions, please consult with a qualified expert."
        })

    if not faqs:
        return ""

    faq_items = ",\n    ".join([
        f'''{{"@type": "Question", "name": "{faq['question']}", "acceptedAnswer": {{"@type": "Answer", "text": "{faq['answer']}"}}}}'''
        for faq in faqs
    ])

    faq_schema = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {faq_items}
  ]
}}
</script>'''
    return faq_schema

def generate_og_tags(tool_name, description, filename, category):
    """Generate Open Graph meta tags"""
    url = f"https://austron24.github.io/webaudit-tools/{filename}"

    og_tags = f'''<meta property="og:title" content="{tool_name} - Free Online Tool">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{url}">
    <meta property="og:site_name" content="WebAudit Tools">
    <meta property="og:locale" content="en_US">'''
    return og_tags

def generate_twitter_tags(tool_name, description):
    """Generate Twitter Card meta tags"""
    twitter_tags = f'''<meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{tool_name} - Free Online Tool">
    <meta name="twitter:description" content="{description}">'''
    return twitter_tags

def generate_additional_meta(category):
    """Generate additional SEO meta tags"""
    meta_tags = f'''<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="author" content="WebAudit Tools">
    <meta name="rating" content="general">
    <meta name="distribution" content="global">'''
    return meta_tags

def extract_current_meta(content):
    """Extract current title and description from HTML"""
    title_match = re.search(r'<title>([^<]+)</title>', content)
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)

    title = title_match.group(1) if title_match else ""
    description = desc_match.group(1) if desc_match else ""

    return title, description

def improve_description(description, tool_name, category):
    """Improve meta description if too short or generic"""
    if len(description) < 100:
        # Create better description
        base_desc = description.rstrip('.')
        if 'Calculator' in tool_name:
            return f"{base_desc}. Free {tool_name.lower()} with instant results. No signup required. Calculate now!"
        else:
            return f"{base_desc}. Free online tool - use instantly in your browser. No downloads needed."
    return description

def optimize_html(filepath):
    """Optimize a single HTML file for SEO"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath)
    if filename in SKIP_FILES:
        return False

    # Don't process files that already have JSON-LD
    if 'application/ld+json' in content:
        return False

    tool_name = get_tool_name(filename)
    category = get_category(filename)
    title, description = extract_current_meta(content)

    if not description:
        description = f"Free {tool_name.lower()} - calculate instantly online."

    # Improve description
    improved_desc = improve_description(description, tool_name, category)

    # Generate all SEO elements
    json_ld = generate_json_ld(tool_name, filename, description.replace('"', "'"), category)
    faq_schema = generate_faq_schema(tool_name, category)
    og_tags = generate_og_tags(tool_name, description.replace('"', "'"), filename, category)
    twitter_tags = generate_twitter_tags(tool_name, description.replace('"', "'"))
    additional_meta = generate_additional_meta(category)

    # Build SEO block to insert
    seo_block = f'''
    <!-- SEO Optimization -->
    {og_tags}
    {twitter_tags}
    {additional_meta}
    {json_ld}
    {faq_schema}
    <!-- End SEO Optimization -->'''

    # Update description if improved
    if improved_desc != description:
        content = re.sub(
            r'<meta name="description" content="[^"]*"',
            f'<meta name="description" content="{improved_desc}"',
            content
        )

    # Remove meta keywords (Google doesn't use them)
    content = re.sub(r'\s*<meta name="keywords" content="[^"]*">\s*', '\n    ', content)

    # Insert SEO block before </head>
    content = content.replace('</head>', f'{seo_block}\n</head>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def main():
    """Main function to optimize all HTML files"""
    tools_dir = Path('/Users/austin/Personal/economic-activity/projects/static-tools')

    html_files = list(tools_dir.glob('*.html'))
    optimized = 0
    skipped = 0

    print(f"Found {len(html_files)} HTML files")
    print("Starting SEO optimization...")

    for filepath in html_files:
        try:
            if optimize_html(filepath):
                optimized += 1
                if optimized % 50 == 0:
                    print(f"Optimized {optimized} files...")
            else:
                skipped += 1
        except Exception as e:
            print(f"Error processing {filepath}: {e}")

    print(f"\nCompleted!")
    print(f"Optimized: {optimized} files")
    print(f"Skipped: {skipped} files (already optimized or excluded)")

if __name__ == '__main__':
    main()
