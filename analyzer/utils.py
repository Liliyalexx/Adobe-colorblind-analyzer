import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import base64
from PIL import Image
import io
import numpy as np
import colorsys

def simulate_colorblindness(color, colorblind_type):
    """Simulate color blindness by converting RGB colors (0-255 scale)"""
    r, g, b = [x/255.0 for x in color]  # Convert to 0-1 range
    
    if colorblind_type == 'protanopia':
        # Protanopia (red-blind) simulation
        new_r = 0.567 * g + 0.433 * b
        new_g = 0.558 * g + 0.442 * b
        new_b = 0.242 * g + 0.758 * b
    elif colorblind_type == 'deuteranopia':
        # Deuteranopia (green-blind) simulation
        new_r = 0.625 * r + 0.375 * b
        new_g = 0.7 * r + 0.3 * b
        new_b = 0.3 * r + 0.7 * b
    elif colorblind_type == 'tritanopia':
        # Tritanopia (blue-blind) simulation
        new_r = 0.95 * r + 0.05 * g
        new_g = 0.433 * r + 0.567 * g
        new_b = g  # Blue becomes green
    else:
        # Achromatomaly (color weakness) simulation - convert to grayscale
        gray = 0.299 * r + 0.587 * g + 0.114 * b
        new_r = new_g = new_b = gray
    
    # Convert back to 0-255 range and return as integers
    return (
        int(new_r * 255),
        int(new_g * 255),
        int(new_b * 255)
    )

def analyze_website_for_colorblindness(url, colorblind_type):
    # Set up Selenium WebDriver
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1200,800')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Load the webpage
        driver.get(url)
        time.sleep(3)  # Wait for page to load
        
        # Take screenshot
        screenshot = driver.get_screenshot_as_png()
        screenshot_base64 = f"data:image/png;base64,{base64.b64encode(screenshot).decode('utf-8')}"
        
        # Get page HTML
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # Analyze elements for color contrast issues
        issues = []
        elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'a', 'button', 'label'])
        
        for element in elements:
            # Get element properties (simplified - in real app you'd need to get actual styles)
            element_info = {
                'tag': element.name,
                'text': element.get_text(strip=True),
                'class': ' '.join(element.get('class', [])),
                'id': element.get('id'),
                'issues': []
            }
            
            # Simulate colorblindness and check contrast (simplified)
            # In a real app, you'd use the color-blind library to transform colors
            # and calculate actual contrast ratios
            if element.name in ['button', 'a']:
                element_info['issues'].append('Potential contrast issue for ' + colorblind_type)
            
            if element_info['issues']:
                issues.append(element_info)
        
        return {
            'url': url,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'colorblind_type': colorblind_type,
            'issues': issues,
            'elements_analyzed': len(elements)
        }, screenshot_base64
    
    finally:
        driver.quit()

def calculate_contrast_ratio(color1, color2):
    """Calculate WCAG contrast ratio between two colors"""
    def get_luminance(c):
        c = c / 255
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2] if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    
    luminance1 = get_luminance(color1)
    luminance2 = get_luminance(color2)
    
    lighter = max(luminance1, luminance2)
    darker = min(luminance1, luminance2)
    return (lighter + 0.05) / (darker + 0.05)