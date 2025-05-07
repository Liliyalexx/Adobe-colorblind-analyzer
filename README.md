# Adobe Colorblind Analyzer 🌈

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Adobe_Systems_logo_and_wordmark.svg/60px-Adobe_Systems_logo_and_wordmark.svg.png" width="30" alt="Adobe Logo">

**An internal tool for web developers & UX/UI designers to create accessible content for colorblind users**

---

## 🎯 Why This Matters for me
"As someone who is 80% deaf and cannot hear high-frequency sounds like children’s or women’s voices, I understand what it’s like to miss important information others take for granted. Colorblind users experience a similar kind of ‘invisible barrier’ — they can’t perceive certain colors that designers often rely on. This tool helps bridge that perceptual gap and ensures no one is left out of the experience."

<ul>
  <li><strong style="font-size: 1.1rem;">👨‍👩‍👧 1 in 12 men and 1 in 200 women</strong> have color vision deficiency</li>
  <li><strong style="font-size: 1.1rem;">🚦 Colorblind users</strong> may miss critical UI elements</li>
  <li><strong style="font-size: 1.1rem;">♿ Accessible design</strong> benefits ALL users</li>
</ul>


## 🔍 Project Overview

Colorblind Analyzer simulates how websites appear to individuals with:

- 🔴 **Protanopia** (red-blind)
- 🟢 **Deuteranopia** (green-blind)
- 🔵 **Tritanopia** (blue-blind)
- ⚪ **Achromatomaly** (color weakness)

```mermaid
graph TD
    A[Website URL] --> B(Colorblind Simulation)
    B --> C[Protanopia]
    B --> D[Deuteranopia]
    B --> E[Tritanopia]
    B --> F[Achromatomaly]
    C --> G[Accessibility Report]
    D --> G
    E --> G
    F --> G

```
## ✨ Key Features

<ul>
  <li><strong style="font-size: 1.1rem;">👁️ Color Simulation:</strong> See designs through colorblind eyes</li>
  <li><strong style="font-size: 1.1rem;">🤖 Automated Testing:</strong> Detect contrast issues in UI elements</li>
  <li><strong style="font-size: 1.1rem;">✅ WCAG Compliance:</strong> Identify accessibility violations</li>
  <li><strong style="font-size: 1.1rem;">📊 Project Tracking:</strong> Monitor improvements over time</li>
  <li><strong style="font-size: 1.1rem;">👥 Team Collaboration:</strong> Share findings with your team</li>
</ul>

## 🛠 Technical Implementation

def simulate_colorblindness(color, colorblind_type):
    r, g, b = [x / 255.0 for x in color]
    
    if colorblind_type == 'protanopia':
        new_r = 0.567 * g + 0.433 * b
        new_g = 0.558 * g + 0.442 * b
        new_b = 0.242 * g + 0.758 * b
    elif colorblind_type == 'deuteranopia':
        new_r = 0.625 * r + 0.375 * b
        new_g = 0.7 * r + 0.3 * b
        new_b = 0.3 * r + 0.7 * b
    elif colorblind_type == 'tritanopia':
        new_r = 0.95 * r + 0.05 * g
        new_g = 0.433 * r + 0.567 * g
        new_b = g
    else:
        gray = 0.299 * r + 0.587 * g + 0.114 * b
        new_r = new_g = new_b = gray
    
    return (int(new_r * 255), int(new_g * 255), int(new_b * 255))

## 🖥 Tech Stack
Frontend: Django Templates, Bootstrap 5

Backend: Python, Django

Vision: Selenium, PIL (via Pillow), Colorsys

Deployment: Heroku with Selenium buildpacks

## 📸 Screenshots
**Home Page**
![Home Page](analyzer/static/analyzer/images/1.png)


**Analysis Dashboard**
![Analysis Dashboard](analyzer/static/analyzer/images/3.png)

**Project View**

![Project View](analyzer/static/analyzer/images/4.png)

**Projects Page**

![Progects Page](analyzer/static/analyzer/images/5.png)
		

## 🚀 Getting Started
📋 Prerequisites
Python 3.9+

Chrome Browser

Heroku CLI (for deployment)

## ⚙️ Installation

git clone https://github.com/liliyalexx/adobe-colorblind-analyzer.git
cd adobe-colorblind-analyzer
pip install -r requirements.txt

## 💻 Run Locally

python manage.py migrate 
python manage.py runserver

## ☁️ Deploy to Heroku

heroku create
heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-chromedriver
heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-google-chrome
heroku buildpacks:add --index 3 heroku/python
git push heroku main

## 📜 Compliance Standards

✅ WCAG 2.1 AA (4.5:1 contrast ratio)

✅ Section 508

✅ Adobe Accessibility Guidelines

## 🔗 Resources
🔍 Colour Blind Awareness

🎨 WebAIM Contrast Checker

🅰️ Adobe Accessibility

## 💡 Future Enhancements

🤖 AI-Powered Colorblind Check
Integrate machine learning to automatically analyze color patterns and generate accessible alternatives for problematic color combinations.

🎨 Professional CSS Styling
Refactor and enhance CSS for better maintainability, consistency, and responsiveness using custom themes and modern UI principles.
