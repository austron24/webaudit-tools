#!/usr/bin/env python3
"""
SEO Optimizer - Enhances all HTML pages based on Google's SEO Starter Guide
Adds: BreadcrumbList schema, visible FAQ sections, How-to content, better heading structure
"""

import os
import re
import json
from pathlib import Path

# Tool categories for breadcrumbs
CATEGORIES = {
    'finance': ['mortgage', 'loan', 'investment', 'savings', 'interest', 'amortization', 'apr', 'credit', 'debt', 'budget', 'retirement', 'roth', 'ira', '401k', 'tax', 'income', 'net-worth', 'compound', 'dividend', 'inflation', 'car-payment', 'boat-loan', 'business-loan', 'sba', 'land-loan', 'jumbo', 'renovation-loan', 'earnest', 'closing-cost', 'house-afford', 'rent-', 'lease', 'payoff', 'extra-payment', 'refinance', 'va-loan', 'fha', 'heloc', 'equity', 'pmi', 'dti', 'emergency-fund', 'runway', 'break-even', 'markup', 'margin', 'roi', 'cagr', 'fire', 'coast-fire', 'barista-fire', 'leanfire'],
    'health': ['bmi', 'calorie', 'macro', 'protein', 'tdee', 'bmr', 'body-fat', 'ideal-weight', 'water-intake', 'sleep', 'heart-rate', 'blood-pressure', 'pregnancy', 'due-date', 'ovulation', 'conception', 'baby', 'child', 'growth', 'fasting', 'intermittent', 'keto', 'carb', 'weight-loss', 'weight-gain', 'workout', 'running', 'pace', 'vo2', 'one-rep', 'dog-weight', 'pet-age', 'dog-food', 'cat-food'],
    'home': ['concrete', 'mulch', 'gravel', 'soil', 'sod', 'lawn', 'fence', 'deck', 'patio', 'roof', 'siding', 'paint', 'flooring', 'tile', 'carpet', 'drywall', 'insulation', 'window', 'door', 'cabinet', 'countertop', 'bathroom', 'kitchen', 'hvac', 'solar', 'electricity', 'gas', 'water-bill', 'pool', 'landscap', 'tree', 'stump', 'gutter', 'chimney', 'asphalt', 'lumber', 'stair', 'wallpaper', 'brick', 'retaining', 'pergola', 'gazebo', 'shed', 'garage', 'basement', 'attic', 'shower', 'bathtub', 'toilet', 'sink', 'faucet', 'appliance', 'moving', 'cleaning', 'maid', 'pressure-wash', 'home-', 'house-', 'property', 'land-clear', 'demolition', 'excavat'],
    'legal': ['personal-injury', 'accident', 'settlement', 'lawsuit', 'divorce', 'child-support', 'alimony', 'custody', 'wrongful-death', 'medical-malpractice', 'workers-comp', 'disability', 'slip-and-fall', 'dog-bite', 'car-accident', 'truck-accident', 'motorcycle-accident', 'birth-injury', 'nursing-home', 'asbestos', 'mesothelioma', 'product-liability', 'premises-liability', 'defamation', 'discrimination', 'harassment', 'wage', 'overtime', 'unemployment', 'severance', 'non-compete', 'contract-breach'],
    'math': ['percentage', 'fraction', 'decimal', 'ratio', 'proportion', 'average', 'mean', 'median', 'standard-deviation', 'variance', 'z-score', 'probability', 'statistics', 'algebra', 'geometry', 'trigonometry', 'calculus', 'matrix', 'vector', 'logarithm', 'exponent', 'factorial', 'permutation', 'combination', 'prime', 'gcd', 'lcm', 'quadratic', 'scientific', 'binary', 'hex', 'octal'],
    'conversion': ['unit', 'length', 'weight', 'volume', 'temperature', 'area', 'speed', 'time', 'currency', 'cooking', 'metric', 'imperial', 'celsius', 'fahrenheit', 'miles', 'kilometer', 'pound', 'kilogram', 'gallon', 'liter', 'feet', 'meter', 'inch', 'centimeter', 'ounce', 'gram', 'acre', 'hectare', 'square-foot', 'square-meter'],
    'date-time': ['date', 'time', 'age', 'birthday', 'countdown', 'days-between', 'weeks-between', 'months-between', 'years-between', 'workdays', 'business-days', 'timezone', 'epoch', 'unix-timestamp', 'julian', 'leap-year', 'quarter', 'fiscal', 'paycheck', 'schedule'],
    'tools': ['qr', 'barcode', 'password', 'hash', 'encode', 'decode', 'encrypt', 'json', 'xml', 'csv', 'markdown', 'html', 'css', 'color', 'rgb', 'hex-color', 'hsl', 'gradient', 'lorem', 'uuid', 'random', 'case-convert', 'word-count', 'character-count', 'text', 'string', 'regex', 'diff', 'compare', 'merge', 'split', 'join', 'sort', 'dedupe', 'format', 'minify', 'beautify', 'compress', 'image', 'resize', 'crop', 'rotate', 'flip', 'filter']
}

def get_category(filename):
    """Determine category based on filename"""
    fname = filename.lower()
    for cat, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in fname:
                return cat
    return 'tools'

def get_category_name(cat):
    """Human-readable category name"""
    names = {
        'finance': 'Finance Calculators',
        'health': 'Health Calculators',
        'home': 'Home & DIY Calculators',
        'legal': 'Legal Calculators',
        'math': 'Math Calculators',
        'conversion': 'Unit Converters',
        'date-time': 'Date & Time Tools',
        'tools': 'Online Tools'
    }
    return names.get(cat, 'Online Tools')

def extract_tool_name(html):
    """Extract tool name from title or h1"""
    title_match = re.search(r'<title>([^<]+)</title>', html)
    if title_match:
        title = title_match.group(1)
        # Remove site name suffix
        title = re.sub(r'\s*[-|]\s*(WebAudit Tools|Free Online Tool|Calculator).*$', '', title, flags=re.IGNORECASE)
        return title.strip()
    return "Calculator"

def extract_description(html):
    """Extract meta description"""
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', html)
    if desc_match:
        return desc_match.group(1)
    return ""

def generate_faq_content(tool_name, category):
    """Generate visible FAQ content for SEO"""
    cat_name = get_category_name(category)

    faqs = [
        {
            "q": f"How do I use the {tool_name}?",
            "a": f"Enter your values in the input fields above and results will calculate automatically. Our {tool_name} provides instant, accurate results without requiring any signup or payment."
        },
        {
            "q": f"Is this {tool_name} accurate?",
            "a": f"Yes, our {tool_name} uses industry-standard formulas and is regularly tested for accuracy. For important decisions involving finances, health, or legal matters, we recommend consulting with a qualified professional."
        },
        {
            "q": f"Is the {tool_name} free to use?",
            "a": f"Absolutely! This {tool_name} is 100% free with no hidden costs, no registration required, and no limits on usage. Use it as many times as you need."
        },
        {
            "q": f"Can I use this on my phone?",
            "a": f"Yes, our {tool_name} is fully mobile-responsive and works perfectly on smartphones, tablets, and desktop computers. No app download required."
        },
        {
            "q": f"How are the results calculated?",
            "a": f"Our {tool_name} uses proven mathematical formulas and algorithms. All calculations happen instantly in your browser for privacy and speed."
        }
    ]
    return faqs

def generate_breadcrumb_schema(tool_name, category, filename):
    """Generate BreadcrumbList structured data"""
    cat_name = get_category_name(category)

    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": "https://austron24.github.io/webaudit-tools/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": cat_name,
                "item": f"https://austron24.github.io/webaudit-tools/#{category}"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": tool_name,
                "item": f"https://austron24.github.io/webaudit-tools/{filename}"
            }
        ]
    }
    return json.dumps(breadcrumb, indent=2)

def generate_howto_schema(tool_name, category):
    """Generate HowTo structured data"""
    howto = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": f"How to Use the {tool_name}",
        "description": f"Step-by-step guide to using our free online {tool_name}",
        "step": [
            {
                "@type": "HowToStep",
                "position": 1,
                "name": "Enter Your Values",
                "text": "Fill in the input fields with your specific numbers or values."
            },
            {
                "@type": "HowToStep",
                "position": 2,
                "name": "View Results",
                "text": "Results calculate automatically as you type - no submit button needed."
            },
            {
                "@type": "HowToStep",
                "position": 3,
                "name": "Adjust as Needed",
                "text": "Modify any input to instantly see how changes affect your results."
            }
        ],
        "totalTime": "PT1M"
    }
    return json.dumps(howto, indent=2)

def generate_visible_faq_html(faqs):
    """Generate visible FAQ section HTML"""
    html = '''
            <div class="card faq-section">
                <h2>❓ Frequently Asked Questions</h2>
                <div class="faq-list">
'''
    for faq in faqs:
        html += f'''                    <details class="faq-item">
                        <summary class="faq-question">{faq['q']}</summary>
                        <p class="faq-answer">{faq['a']}</p>
                    </details>
'''
    html += '''                </div>
            </div>
'''
    return html

def generate_faq_styles():
    """Generate CSS for FAQ section"""
    return '''
        .faq-section { margin-top: 20px; }
        .faq-list { display: flex; flex-direction: column; gap: 10px; }
        .faq-item { background: var(--bg-input); border-radius: 10px; overflow: hidden; }
        .faq-question { padding: 15px 20px; cursor: pointer; font-weight: 600; color: var(--text-primary); list-style: none; display: flex; justify-content: space-between; align-items: center; }
        .faq-question::-webkit-details-marker { display: none; }
        .faq-question::after { content: '+'; font-size: 1.5rem; color: var(--primary); transition: transform 0.3s; }
        details[open] .faq-question::after { content: '−'; }
        .faq-answer { padding: 0 20px 15px; color: var(--text-secondary); line-height: 1.7; }
        details[open] { background: var(--bg-input); border-left: 3px solid var(--primary); }
'''

def add_visible_breadcrumb_html(tool_name, category, filename):
    """Generate visible breadcrumb navigation"""
    cat_name = get_category_name(category)
    return f'''    <nav class="breadcrumb" aria-label="Breadcrumb">
        <ol itemscope itemtype="https://schema.org/BreadcrumbList">
            <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
                <a itemprop="item" href="index.html"><span itemprop="name">Home</span></a>
                <meta itemprop="position" content="1" />
            </li>
            <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
                <a itemprop="item" href="{category}-calculators.html"><span itemprop="name">{cat_name}</span></a>
                <meta itemprop="position" content="2" />
            </li>
            <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
                <span itemprop="name">{tool_name}</span>
                <meta itemprop="position" content="3" />
            </li>
        </ol>
    </nav>
'''

def generate_breadcrumb_styles():
    """CSS for visible breadcrumbs"""
    return '''
        .breadcrumb { padding: 15px 20px; background: var(--bg-card); margin-bottom: 0; }
        .breadcrumb ol { list-style: none; display: flex; flex-wrap: wrap; gap: 8px; max-width: 1200px; margin: 0 auto; padding: 0; }
        .breadcrumb li { display: flex; align-items: center; font-size: 14px; color: var(--text-secondary); }
        .breadcrumb li:not(:last-child)::after { content: '›'; margin-left: 8px; color: var(--text-secondary); }
        .breadcrumb a { color: var(--primary); text-decoration: none; }
        .breadcrumb a:hover { text-decoration: underline; }
        .breadcrumb li:last-child { color: var(--text-primary); }
'''

def optimize_page(filepath):
    """Optimize a single HTML page for SEO"""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    filename = os.path.basename(filepath)

    # Skip non-tool pages
    skip_files = ['index.html', 'compare.html', 'ad-template.html', 'health-calculators.html',
                  'finance-calculators.html', 'home-calculators.html', 'legal-calculators.html',
                  'seo-optimizer.py', 'upgrade-tools.py']
    if filename in skip_files:
        return False

    # Check if already optimized
    if 'faq-section' in html and 'BreadcrumbList' in html:
        print(f"  Skipping {filename} - already optimized")
        return False

    tool_name = extract_tool_name(html)
    category = get_category(filename)

    print(f"  Optimizing: {filename} ({tool_name}) - Category: {category}")

    # Generate new content
    faqs = generate_faq_content(tool_name, category)
    breadcrumb_schema = generate_breadcrumb_schema(tool_name, category, filename)
    howto_schema = generate_howto_schema(tool_name, category)
    faq_html = generate_visible_faq_html(faqs)
    breadcrumb_html = add_visible_breadcrumb_html(tool_name, category, filename)

    # Add breadcrumb and HowTo schema after existing schema
    if '<!-- End SEO Optimization -->' in html:
        schema_insert = f'''<script type="application/ld+json">
{breadcrumb_schema}
</script>
    <script type="application/ld+json">
{howto_schema}
</script>
    <!-- End SEO Optimization -->'''
        html = html.replace('<!-- End SEO Optimization -->', schema_insert)

    # Add CSS for FAQ and breadcrumbs
    faq_css = generate_faq_styles()
    breadcrumb_css = generate_breadcrumb_styles()

    # Insert CSS before </style>
    if '</style>' in html and 'faq-section' not in html:
        html = html.replace('</style>', f'{faq_css}{breadcrumb_css}</style>')

    # Add visible breadcrumb after <body> tag
    if '<body>' in html and 'breadcrumb' not in html:
        html = html.replace('<body>', f'<body>\n{breadcrumb_html}')

    # Add FAQ section before Related Tools or before closing content-area
    if 'faq-section' not in html:
        # Try to insert before Related Tools section
        if '<div class="card">\n                <h2>🔗 Related Tools</h2>' in html:
            html = html.replace('<div class="card">\n                <h2>🔗 Related Tools</h2>',
                              f'{faq_html}\n            <div class="card">\n                <h2>🔗 Related Tools</h2>')
        elif '🔗 Related Tools' in html:
            # Alternative format
            related_match = re.search(r'(<div class="card">\s*<h2>🔗 Related Tools</h2>)', html)
            if related_match:
                html = html.replace(related_match.group(1), f'{faq_html}\n            {related_match.group(1)}')

    # Write optimized file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    return True

def main():
    """Optimize all HTML pages"""
    tools_dir = Path('/Users/austin/Personal/economic-activity/projects/static-tools')

    html_files = list(tools_dir.glob('*.html'))
    print(f"Found {len(html_files)} HTML files")

    optimized = 0
    for filepath in html_files:
        try:
            if optimize_page(filepath):
                optimized += 1
        except Exception as e:
            print(f"  Error processing {filepath.name}: {e}")

    print(f"\nOptimized {optimized} pages for SEO")

if __name__ == '__main__':
    main()
