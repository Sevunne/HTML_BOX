# HTML BOX 🎯

A dark-themed HTML editor developed based on PyQt5, offering real-time preview, syntax highlighting, and code export functionality.

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.4+-green.svg)
![License](https://img.shields.io/badge/License-Proprietary-red.svg)

🌐 Language
**English** | [中文](README.md)

## ✨ Functional Features

### 🎨 Editor Features
- **Live Preview** - View the effect while writing code
- **Syntax Highlighting** - Supports syntax highlighting for HTML, CSS, and JavaScript
- **Dark Theme** - Eye-friendly dark interface, preventing fatigue during prolonged coding sessions
- **Intelligent prompts** - auto-completion and code formatting

### 📁 File Management
- **New/Open/Save** - Complete file operation functions
- **Multi-format Export** - Supports single HTML, complete project ZIP, and compressed HTML
- **Project Template** - Export standard project structure (HTML + CSS + JS)

### ⚙️ Custom Settings
- **Font Settings** - Customize the editor font and size
- **Preview delay** - Adjust the response speed of real-time preview
- **Theme Configuration** - Personalized Interface Appearance

### 🎮 Fun Features
- **Version History** - Complete update log records
- **Easter Egg** - Discover it yourself (WvW)
## 🚀 Quick Start

### Environmental requirements
- Python 3.6+
- Pyside6
- Other dependent packages

### Installation steps

1. **Clone project** 
```bash 
git clone https://github.com/Sevunne/html-box.git 
cd html-box 
```
2. **Install all dependencies with one click** 
```bash 
pip install pyside6 pyside6-qtwebengine 
```
## 📖 Instructions for Use
1. The left side of the top toolbar houses basic file functions such as New, Open, Save, and Export, while the right side, divided by flexible white space, concentrates on placing mode switching and project operation buttons.
2. Click on "📝 Professional Code Mode" to switch to the code editing panel, where you can manually write HTML/CSS/JS code. The editor comes with built-in syntax highlighting.
3. Click on "🧩 Block Mode" to switch to the visual block panel, and drag and drop components to quickly build a webpage.
4. The mode switch has a built-in caching mechanism, so manually written code will not be overwritten or lost by the content of the building blocks. Data is bidirectionally interchangeable between the two editing modes.
5. Supports the `.htbx` proprietary project format, which allows for the saving of the entire set of block layouts and code content, enabling complete restoration of the project upon next opening.
6. The "Preview" button at the top allows for manual refreshing of the webpage, and also supports automatic scheduled previewing. The preview delay can be customized in the settings panel.
7. Equipped with full-featured shortcut keys, the bottom status bar displays the current editing mode and program status in real-time.

## 📜 Copyright Notice
Copyright © 2026 
All Rights Reserved.

The project is currently not open-sourced, and the copyright of all the project's code, interface design, and logic of the building block editor belongs to the author.
Without the written authorization of the author, it is prohibited to copy, forward, modify, or commercially use any content of this project. Any infringement will be subject to legal action.
If an open-source version is launched in the future, we will announce it separately.
