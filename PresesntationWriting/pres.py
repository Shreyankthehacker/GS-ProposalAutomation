#!/usr/bin/env python3
"""
Enhanced Presentation Generator with Custom Colors and Design Elements
"""

import re
import os
from typing import Dict, List, Optional, Tuple

class PresentationConfig:
    """Configuration class for presentation styling"""
    
    def __init__(self, colors: List[str] = None):
        # Use provided colors or defaults
        if colors and len(colors) >= 4:
            self.primary_color = colors[0]
            self.secondary_color = colors[1] 
            self.accent_color = colors[2]
            self.success_color = colors[3]
            self.warning_color = colors[4] if len(colors) > 4 else colors[2]
        else:
            # Default colors
            self.primary_color = "#3498db"
            self.secondary_color = "#2c3e50"
            self.accent_color = "#e74c3c"
            self.success_color = "#27ae60"
            self.warning_color = "#f39c12"
            
        self.background_color = "#f8f9fa"
        self.text_color = "#333"
        self.light_text_color = "#666"
        
        # Typography
        self.font_family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
        self.title_font_size = "2.5em"
        self.section_title_font_size = "1.6em"
        self.content_font_size = "1.1em"
        
        # Layout
        self.container_width = "1200px"
        self.section_padding = "30px"
        self.border_radius = "8px"
        self.box_shadow = "0 4px 20px rgba(0,0,0,0.1)"
        
        # Page settings for PDF
        self.page_margin = "20mm"
        self.page_size = "A4"
    
    def get_css(self, logo_url: str) -> str:
        """Generate CSS with current configuration"""
        return f"""
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        @page {{
            size: {self.page_size};
            margin: {self.page_margin};
            @top-left {{
                content: "";
                background: url('{logo_url}') no-repeat;
                background-size: contain;
                width: 120px;
                height: 60px;
                margin: 10px;
            }}
            @bottom-center {{
                content: "";
                height: 30px;
                background: linear-gradient(135deg, {self.primary_color} 0%, {self.secondary_color} 30%, {self.accent_color} 60%, {self.success_color} 100%);
                width: 100%;
                border-radius: 15px 15px 0 0;
            }}
        }}

        body {{
            font-family: {self.font_family};
            line-height: 1.6;
            color: {self.text_color};
            background: {self.background_color};
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
            position: relative;
            min-height: 100vh;
        }}

        .page-logo {{
            position: fixed;
            top: 20px;
            left: 20px;
            width: 120px;
            height: 60px;
            background: url('{logo_url}') no-repeat center;
            background-size: contain;
            z-index: 1000;
        }}

        .page-footer-design {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 30px;
            background: linear-gradient(135deg, {self.primary_color} 0%, {self.secondary_color} 30%, {self.accent_color} 60%, {self.success_color} 100%);
            border-radius: 15px 15px 0 0;
            z-index: 999;
        }}

        .presentation-container {{
            max-width: {self.container_width};
            margin: 0 auto;
            padding: 100px 20px 50px 20px;
            background: white;
            box-shadow: {self.box_shadow};
            min-height: calc(100vh - 130px);
            position: relative;
        }}

        .header {{
            display: flex;
            align-items: center;
            margin-bottom: 50px;
            padding-bottom: 25px;
            border-bottom: 3px solid {self.primary_color};
            page-break-after: avoid;
        }}

        .logo {{
            width: 150px;
            height: 75px;
            background: url('{logo_url}') no-repeat center;
            background-size: contain;
            margin-right: 30px;
            flex-shrink: 0;
        }}

        .main-title {{
            font-size: {self.title_font_size};
            font-weight: 700;
            color: {self.primary_color};
            margin: 0;
            line-height: 1.2;
        }}

        .section {{
            margin-bottom: 25px;
            padding: {self.section_padding};
            border-left: 5px solid {self.primary_color};
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 0 {self.border_radius} {self.border_radius} 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            page-break-inside: auto;
            break-inside: auto;
            orphans: 2;
            widows: 2;
        }}

        .section-title {{
            font-size: {self.section_title_font_size};
            font-weight: 700;
            color: {self.secondary_color};
            margin-bottom: 20px;
            text-align: left;
            border-bottom: 2px solid {self.primary_color};
            padding-bottom: 10px;
            page-break-after: avoid;
        }}

        .section-content {{
            font-size: {self.content_font_size};
            font-weight: 400;
            line-height: 1.8;
            color: {self.text_color};
            orphans: 2;
            widows: 2;
        }}

        .section-content p {{
            margin-bottom: 12px;
        }}

        .section-content ul, .section-content ol {{
            margin-left: 25px;
            margin-top: 12px;
            margin-bottom: 12px;
        }}

        .section-content li {{
            margin-bottom: 8px;
            font-weight: 400;
        }}

        .phase-section {{
            background: white;
            border: 2px solid {self.primary_color};
            border-radius: {self.border_radius};
            padding: 25px;
            margin: 15px 0;
            page-break-inside: auto;
            break-inside: auto;
            orphans: 2;
            widows: 2;
        }}

        .phase-title {{
            font-size: 1.3em;
            font-weight: 700;
            color: {self.accent_color};
            margin-bottom: 15px;
            page-break-after: avoid;
        }}

        .phase-content {{
            font-weight: 400;
            line-height: 1.7;
        }}

        .timeline-item {{
            background: white;
            border-left: 4px solid {self.success_color};
            margin: 12px 0;
            padding: 20px 25px;
            border-radius: 0 {self.border_radius} {self.border_radius} 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            page-break-inside: auto;
            break-inside: auto;
            orphans: 2;
            widows: 2;
        }}

        .timeline-week {{
            font-weight: 700;
            color: {self.success_color};
            font-size: 1.2em;
        }}

        .pricing-highlight {{
            background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
            border: 3px solid {self.success_color};
            border-radius: {self.border_radius};
            padding: 30px;
            margin: 20px 0;
            text-align: center;
            page-break-inside: auto;
            break-inside: auto;
            orphans: 2;
            widows: 2;
        }}

        .price-amount {{
            font-size: 2.2em;
            font-weight: 700;
            color: {self.success_color};
            margin-bottom: 15px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .cta-section {{
            background: linear-gradient(135deg, {self.primary_color} 0%, {self.secondary_color} 100%);
            color: white;
            border-radius: {self.border_radius};
            padding: 40px;
            text-align: center;
            margin-top: 30px;
            page-break-inside: auto;
            break-inside: auto;
            orphans: 2;
            widows: 2;
        }}

        .cta-title {{
            font-size: 1.8em;
            font-weight: 700;
            color: white;
            margin-bottom: 20px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}

        .cta-content {{
            font-size: 1.2em;
            font-weight: 400;
            line-height: 1.6;
            color: white;
        }}

        .company-info {{
            background: linear-gradient(135deg, {self.secondary_color} 0%, {self.accent_color} 100%);
            color: white;
            border-radius: {self.border_radius};
            padding: 35px;
            margin: 25px 0;
            page-break-inside: auto;
            break-inside: auto;
            orphans: 2;
            widows: 2;
        }}

        .company-title {{
            font-size: 1.5em;
            font-weight: 700;
            margin-bottom: 15px;
            color: white;
        }}

        .company-content {{
            font-weight: 400;
            font-size: 1.1em;
            line-height: 1.7;
            color: white;
        }}

        .highlight-box {{
            background: linear-gradient(135deg, rgba({self._hex_to_rgb(self.warning_color)}, 0.1) 0%, rgba({self._hex_to_rgb(self.primary_color)}, 0.1) 100%);
            border: 2px solid {self.warning_color};
            border-radius: {self.border_radius};
            padding: 25px;
            margin: 15px 0;
            page-break-inside: auto;
            break-inside: auto;
            orphans: 2;
            widows: 2;
        }}

        .highlight-box .highlight-title {{
            font-weight: 700;
            color: {self.warning_color};
            margin-bottom: 10px;
        }}

        /* Enhanced print styles */
        @media print {{
            body {{
                background: white !important;
                font-size: 12pt;
            }}
            
            .page-logo,
            .page-footer-design {{
                display: none !important;
            }}
            
            .presentation-container {{
                box-shadow: none !important;
                margin: 0 !important;
                padding: 20px !important;
                max-width: none !important;
            }}
            
            .section,
            .company-info,
            .pricing-highlight,
            .highlight-box,
            .timeline-item,
            .phase-section,
            .cta-section {{
                page-break-inside: auto !important;
                break-inside: auto !important;
                box-shadow: none !important;
                orphans: 2 !important;
                widows: 2 !important;
            }}
            
            .header {{
                page-break-after: avoid !important;
            }}
            
            .section-title,
            .company-title,
            .cta-title,
            .phase-title {{
                page-break-after: avoid !important;
            }}
        }}

        /* Responsive design */
        @media (max-width: 768px) {{
            .presentation-container {{
                padding: 15px;
            }}
            
            .page-logo {{
                width: 90px;
                height: 45px;
            }}
            
            .header {{
                flex-direction: column;
                text-align: center;
            }}
            
            .logo {{
                margin-right: 0;
                margin-bottom: 20px;
            }}
            
            .main-title {{
                font-size: 2em;
            }}
            
            .section {{
                padding: 20px;
            }}
            
            .section-title {{
                font-size: 1.4em;
            }}
        }}
        """
    
    def _hex_to_rgb(self, hex_color: str) -> str:
        """Convert hex color to RGB values for CSS rgba"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        try:
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            return f"{rgb[0]}, {rgb[1]}, {rgb[2]}"
        except:
            return "0, 0, 0"

def generate_presentation(
    filename: str,
    logo_url: str,
    colors: List[str],
    output_format: str = "html"
) -> Optional[str]:
    """
    Generate HTML/PDF presentation from text file with custom colors
    
    Args:
        filename (str): Path to the input text file
        logo_url (str): URL for the logo image
        colors (List[str]): List of hex color values
        output_format (str): Output format - 'html', 'pdf', or 'both'
    
    Returns:
        str: Path to the generated file(s) or None if error
    """
    
    # Initialize configuration with custom colors
    config = PresentationConfig(colors)
    
    def parse_txt_file(file_path: str) -> List[Dict[str, str]]:
        """Parse the text file and extract title-text pairs"""
        sections = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error reading file: {e}")
        
        # Split content by title-text pattern
        pattern = r'Title:\s*(.+?)\nText:\s*(.+?)(?=\nTitle:|\Z)'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for title, text in matches:
            sections.append({
                'title': title.strip(),
                'content': text.strip()
            })
        
        if not sections:
            raise ValueError("No valid title-text pairs found in the file. Format should be:\nTitle: Your Title\nText: Your content")
        
        return sections
    
    def process_content(content: str) -> str:
        """Process content to handle special formatting"""
        # Convert **text** to HTML bold
        content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
        
        # Convert *text* to HTML italic
        content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
        
        # Handle bullet points (lines starting with *)
        lines = content.split('\n')
        processed_lines = []
        in_list = False
        
        for line in lines:
            line = line.strip()
            if line.startswith('• ') or line.startswith('* '):
                if not in_list:
                    processed_lines.append('<ul>')
                    in_list = True
                bullet_text = line[2:].strip()
                processed_lines.append(f'<li>{bullet_text}</li>')
            else:
                if in_list:
                    processed_lines.append('</ul>')
                    in_list = False
                if line:
                    processed_lines.append(f'<p>{line}</p>')
        
        if in_list:
            processed_lines.append('</ul>')
        
        # Join lines
        result = '\n'.join(processed_lines)
        
        # Handle phase sections (content with Phase X pattern)
        phase_pattern = r'(\*\*Phase \d+:.*?\*\*.*?)(?=\*\*Phase \d+:|\Z)'
        phases = re.findall(phase_pattern, result, re.DOTALL)
        
        if phases:
            phase_html = ""
            for phase in phases:
                phase_lines = phase.strip().split('\n')
                phase_title = phase_lines[0].replace('**', '').strip()
                phase_content = '\n'.join(phase_lines[1:]).strip()
                
                phase_html += f'''
                <div class="phase-section">
                    <div class="phase-title">{phase_title}</div>
                    <div class="phase-content">{process_content(phase_content)}</div>
                </div>
                '''
            return phase_html
        
        return result
    
    def categorize_sections(sections: List[Dict[str, str]]) -> Dict[str, List]:
        """Categorize sections for better presentation layout"""
        categorized = {
            'title': None,
            'main': [],
            'phases': [],
            'company': [],
            'cta': []
        }
        
        for section in sections:
            title_lower = section['title'].lower()
            
            # Check if this is the main title section - skip it for display
            if title_lower in ['title', 'main title', 'presentation title', 'title of the sales proposal']:
                categorized['title'] = section
            # Company information sections
            elif any(keyword in title_lower for keyword in ['who we are', 'what we do', 'team', 'expertise', 'about us', 'company']):
                categorized['company'].append(section)
            # Call to action sections
            elif any(keyword in title_lower for keyword in ['conclusion', 'call to action', 'contact', 'next steps']):
                categorized['cta'].append(section)
            # Phase/project breakdown sections
            elif any(keyword in title_lower for keyword in ['scope', 'project breakdown', 'timeline', 'milestone', 'phases']):
                categorized['phases'].append(section)
            # Main content sections
            else:
                categorized['main'].append(section)
        
        return categorized
    
    def generate_html(sections: List[Dict[str, str]]) -> str:
        """Generate the complete HTML presentation"""
        categorized = categorize_sections(sections)
        
        # Determine main title
        if categorized['title']:
            main_title = categorized['title']['content']
        elif sections:
            main_title = sections[0]['content']
        else:
            main_title = "Business Presentation"
        
        # Generate CSS
        css = config.get_css(logo_url)
        
        html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{main_title}</title>
    <style>{css}</style>
</head>
<body>
    <div class="page-logo"></div>
    <div class="page-footer-design"></div>
    
    <div class="presentation-container">
        <div class="header">
            <div class="logo"></div>
            <h1 class="main-title">{main_title}</h1>
        </div>
'''
        
        # Add main sections (skip title section)
        for section in categorized['main']:
            if section == categorized['title']:
                continue
                
            processed_content = process_content(section['content'])
            
            # Special handling for pricing sections
            if 'pricing' in section['title'].lower() or '$' in section['content']:
                price_match = re.search(r'\$[\d,]+', section['content'])
                if price_match:
                    price = price_match.group()
                    content_without_price = section['content'].replace(price, '').strip()
                    processed_content = f'''
                    <div class="pricing-highlight">
                        <div class="price-amount">{price}</div>
                        <div>{process_content(content_without_price)}</div>
                    </div>
                    '''
            
            html_template += f'''
        <div class="section">
            <h2 class="section-title">{section['title']}</h2>
            <div class="section-content">
                {processed_content}
            </div>
        </div>
'''
        
        # Add phase sections
        for section in categorized['phases']:
            processed_content = process_content(section['content'])
            html_template += f'''
        <div class="section">
            <h2 class="section-title">{section['title']}</h2>
            <div class="section-content">
                {processed_content}
            </div>
        </div>
'''
        
        # Add company sections
        for section in categorized['company']:
            processed_content = process_content(section['content'])
            html_template += f'''
        <div class="company-info">
            <div class="company-title">{section['title']}</div>
            <div class="company-content">
                {processed_content}
            </div>
        </div>
'''
        
        # Add CTA sections
        for section in categorized['cta']:
            processed_content = process_content(section['content'])
            html_template += f'''
        <div class="cta-section">
            <div class="cta-title">{section['title']}</div>
            <div class="cta-content">
                {processed_content}
            </div>
        </div>
'''
        
        html_template += '''
    </div>
</body>
</html>'''
        
        return html_template
    
    def generate_pdf_from_html(html_content: str, output_path: str) -> bool:
        """Generate PDF from HTML using WeasyPrint"""
        try:
            import weasyprint
            html_doc = weasyprint.HTML(string=html_content)
            html_doc.write_pdf(output_path)
            return True
        except ImportError:
            try:
                from playwright.sync_api import sync_playwright
                with sync_playwright() as p:
                    browser = p.chromium.launch()
                    page = browser.new_page()
                    page.set_content(html_content)
                    page.wait_for_load_state('networkidle')
                    page.pdf(
                        path=output_path,
                        format='A4',
                        margin={'top': '20mm', 'bottom': '20mm', 'left': '20mm', 'right': '20mm'},
                        print_background=True,
                        prefer_css_page_size=True
                    )
                    browser.close()
                return True
            except ImportError:
                print("❌ PDF generation requires either 'weasyprint' or 'playwright'")
                print("Install with: pip install weasyprint  OR  pip install playwright && playwright install chromium")
                return False
        except Exception as e:
            print(f"❌ Error generating PDF: {e}")
            return False
    
    # Main execution
    try:
        # Validate input file
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Input file not found: {filename}")
        
        # Parse the input file
        sections = parse_txt_file(filename)
        print(f"✅ Parsed {len(sections)} sections from {filename}")
        
        # Generate HTML
        html_content = generate_html(sections)
        
        # Determine output filename
        base_name = os.path.splitext(filename)[0]
        output_files = []
        
        # Generate HTML if requested
        if output_format in ['html', 'both']:
            html_output = f"{base_name}_presentation.html"
            with open(html_output, 'w', encoding='utf-8') as file:
                file.write(html_content)
            output_files.append(html_output)
            print(f"✅ HTML presentation generated: {html_output}")
        
        # Generate PDF if requested
        if output_format in ['pdf', 'both']:
            pdf_output = f"{base_name}_presentation.pdf"
            if generate_pdf_from_html(html_content, pdf_output):
                output_files.append(pdf_output)
                print(f"✅ PDF presentation generated: {pdf_output}")
            else:
                print("❌ PDF generation failed")
        
        return output_files[0] if len(output_files) == 1 else output_files
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Example with custom colors matching your design
    custom_colors = [
        "#1E3A8A",  # Primary - Blue
        "#059669",  # Secondary - Green  
        "#DC2626",  # Accent - Red
        "#7C3AED",  # Success - Purple
        "#F59E0B"   # Warning - Orange
    ]
    
    generate_presentation(
        "output.txt",
        "https://static.wixstatic.com/media/cb6b3d_5c8f2b020ebe48b69bc8c163cc480156~mv2.png/v1/fill/w_60,h_60,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/GrowthSutra%20Logo.png",
        custom_colors,
        'pdf'
    )