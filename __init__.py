# AnkiThemeTwin/__init__.py — Anki 25.x (Qt6/PyQt6) — v1.4.0
# Enhanced theming with keyboard shortcuts, more font sizes, theme presets, and custom theme creator
# Tools > Theme: AnkiThemeTwin  |  Help > About AnkiThemeTwin

from aqt import mw, gui_hooks
from aqt.qt import (
    QAction, QActionGroup, QApplication, QMenu,
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, Qt,
    QSlider, QColorDialog, QLineEdit, QSpinBox, QScrollArea,
    QWidget, QGridLayout, QComboBox, QCheckBox, QTextEdit,
    QShortcut, QKeySequence, QFrame, QTimeEdit, QButtonGroup,
    QRadioButton,
)
from aqt.utils import openLink, showInfo, tooltip
from typing import Literal, Any, Optional
import json
import os
from datetime import datetime, time

VERSION = "1.4.0"

Theme = Literal[
    "sepia_word", "sepia_paper", "gray_word", "gray_paper",
    "sepia_special", "blue_light", "olive_green",
    "high_contrast_light", "high_contrast_dark", "dyslexia_friendly",
    "deuteranopia", "protanopia", "tritanopia"
]

THEME_OPTIONS = [
    ("Sepia (Word-like)", "sepia_word"),
    ("Sepia (Paper)", "sepia_paper"),
    ("Sepia (Special • Dr. M)", "sepia_special"),
    ("Gray (Word-like)", "gray_word"),
    ("Gray (Paper)", "gray_paper"),
    ("Blue Light (Evening)", "blue_light"),
    ("Olive Green (Natural)", "olive_green"),
]

ACCESSIBILITY_THEMES = [
    ("High Contrast Light", "high_contrast_light"),
    ("High Contrast Dark", "high_contrast_dark"),
    ("Dyslexia Friendly", "dyslexia_friendly"),
    ("Deuteranopia Support", "deuteranopia"),
    ("Protanopia Support", "protanopia"),
    ("Tritanopia Support", "tritanopia"),
]

def get_config():
    return mw.addonManager.getConfig(__name__) or {}

def write_config(cfg: dict):
    mw.addonManager.writeConfig(__name__, cfg)

# ---------------- Palettes (readability-first) ----------------
SEPIA_WORD = {"bg":"#F9F5E9","fg":"#2A2420","muted":"#5C524A","border":"#D9D0C2",
    "accent":"#7B5F4B","button":"#EDE5D6","buttonText":"#2A2420",
    "input":"#FCF9F1","inputText":"#2A2420","hover":"#E6DECF","selection":"#DACCB7"}
SEPIA_PAPER = {"bg":"#F3E7D3","fg":"#29231F","muted":"#5B4E44","border":"#CFBEA7",
    "accent":"#715843","button":"#E9DFC9","buttonText":"#29231F",
    "input":"#FBF4E8","inputText":"#29231F","hover":"#E2D5BF","selection":"#D7C6AC"}
GRAY_WORD = {"bg":"#E6E6E6","fg":"#1E1E1E","muted":"#454545","border":"#CFCFCF",
    "accent":"#0F5AA6","button":"#F2F2F2","buttonText":"#1E1E1E",
    "input":"#FFFFFF","inputText":"#1E1E1E","hover":"#E0E0E0","selection":"#CFCFCF"}
GRAY_PAPER = {"bg":"#D9D9D9","fg":"#1C1C1C","muted":"#3F3F3F","border":"#BFBFBF",
    "accent":"#0F5AA6","button":"#E9E9E9","buttonText":"#1C1C1C",
    "input":"#F7F7F7","inputText":"#1C1C1C","hover":"#D2D2D2","selection":"#C5C5C5"}
SEPIA_SPECIAL = {"bg":"#EEDFC6","fg":"#201A16","muted":"#54483F","border":"#CDB99F",
    "accent":"#6D523F","button":"#E6D3B7","buttonText":"#201A16",
    "input":"#FAF2E4","inputText":"#201A16","hover":"#DFC9A9","selection":"#D2BC9C"}
BLUE_LIGHT = {"bg":"#E8F0F8","fg":"#1A2330","muted":"#4A5568","border":"#C5D5E5",
    "accent":"#2C5AA0","button":"#DDE8F5","buttonText":"#1A2330",
    "input":"#F5F8FC","inputText":"#1A2330","hover":"#D5E3F2","selection":"#C0D8ED"}
OLIVE_GREEN = {"bg":"#EBF0E4","fg":"#2A2F24","muted":"#4F5449","border":"#D0D9C5",
    "accent":"#5A7A3C","button":"#E2EAD8","buttonText":"#2A2F24",
    "input":"#F5F8F0","inputText":"#2A2F24","hover":"#DDE7D0","selection":"#D0DFBC"}

# Accessibility themes
HIGH_CONTRAST_LIGHT = {"bg":"#FFFFFF","fg":"#000000","muted":"#404040","border":"#000000",
    "accent":"#0000FF","button":"#F0F0F0","buttonText":"#000000",
    "input":"#FFFFFF","inputText":"#000000","hover":"#E0E0E0","selection":"#FFFF00"}
HIGH_CONTRAST_DARK = {"bg":"#000000","fg":"#FFFFFF","muted":"#C0C0C0","border":"#FFFFFF",
    "accent":"#FFFF00","button":"#1A1A1A","buttonText":"#FFFFFF",
    "input":"#000000","inputText":"#FFFFFF","hover":"#2A2A2A","selection":"#FFFF00"}
DYSLEXIA_FRIENDLY = {"bg":"#FFFACD","fg":"#2F2F2F","muted":"#696969","border":"#E6DB8F",
    "accent":"#008B8B","button":"#FFF8B0","buttonText":"#2F2F2F",
    "input":"#FFFFF0","inputText":"#2F2F2F","hover":"#FFF48F","selection":"#FFE680"}

# Color blindness support themes
DEUTERANOPIA = {"bg":"#F0F0E8","fg":"#003366","muted":"#666699","border":"#9999CC",
    "accent":"#CC6600","button":"#E8E8E0","buttonText":"#003366",
    "input":"#FAFAF5","inputText":"#003366","hover":"#E0E0D8","selection":"#CCCCBB"}
PROTANOPIA = {"bg":"#EFF5FF","fg":"#004080","muted":"#5577AA","border":"#99BBDD",
    "accent":"#CC7700","button":"#E7EDF5","buttonText":"#004080",
    "input":"#F7FBFF","inputText":"#004080","hover":"#DFE9F5","selection":"#CCDDF"}
TRITANOPIA = {"bg":"#FFF0F0","fg":"#330022","muted":"#775566","border":"#CCAACC",
    "accent":"#CC3366","button":"#FFE8E8","buttonText":"#330022",
    "input":"#FFF8F8","inputText":"#330022","hover":"#FFE0E0","selection":"#FFCCDD"}

PALETTES = {
    "sepia_word": SEPIA_WORD,
    "sepia_paper": SEPIA_PAPER,
    "gray_word": GRAY_WORD,
    "gray_paper": GRAY_PAPER,
    "sepia_special": SEPIA_SPECIAL,
    "blue_light": BLUE_LIGHT,
    "olive_green": OLIVE_GREEN,
    "high_contrast_light": HIGH_CONTRAST_LIGHT,
    "high_contrast_dark": HIGH_CONTRAST_DARK,
    "dyslexia_friendly": DYSLEXIA_FRIENDLY,
    "deuteranopia": DEUTERANOPIA,
    "protanopia": PROTANOPIA,
    "tritanopia": TRITANOPIA,
}

def palette_for(theme: Theme) -> dict:
    """Return the color palette dictionary for the given theme."""
    return PALETTES[theme]

def normalize_theme(t: str) -> Theme:
    legacy = {"sepia":"sepia_word","gray":"gray_word"}
    v = legacy.get(t, t)
    return v if v in PALETTES else "sepia_special"

def get_active_theme() -> Theme:
    """Return the currently configured theme."""
    cfg = get_config()
    return normalize_theme(cfg.get("currentTheme", "sepia_special"))

# ---------------- CSS / QSS ----------------
_STYLE_ID = "ankithemetwin-style"

def get_font_size() -> int:
    """Get configured font size, default 16px."""
    cfg = get_config()
    return cfg.get("fontSize", 16)

def get_font_family() -> str:
    """Get configured font family."""
    cfg = get_config()
    return cfg.get("fontFamily", "Segoe UI,Amiri,Arial,sans-serif")

def get_line_height() -> float:
    """Get configured line height, default 1.58."""
    cfg = get_config()
    return cfg.get("lineHeight", 1.58)

def get_letter_spacing() -> float:
    """Get configured letter spacing, default 0."""
    cfg = get_config()
    return cfg.get("letterSpacing", 0.0)

def css_vars(p):
    """Generate comprehensive CSS for all webview contexts."""
    font_size = get_font_size()
    font_family = get_font_family()
    line_height = get_line_height()
    letter_spacing = get_letter_spacing()
    return (
        # Base styles
        "html, body {"
        f"  background:{p['bg']} !important; color:{p['fg']} !important;"
        f'  font-family:{font_family} !important;'
        f"  line-height:{line_height}; font-size:{font_size}px;"
        f"  letter-spacing:{letter_spacing}px;"
        "  -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility;"
        "}"
        # All text elements
        f"p, span, div, li, label {{ color:{p['fg']} !important; }}"
        # Links and selection
        f"a {{ color:{p['accent']} !important; text-decoration:underline; }}"
        f"a:hover {{ color:{p['hover']} !important; }}"
        f"::selection {{ background:{p['selection']}; color:{p['fg']}; }}"
        # Buttons and inputs in webviews
        f"button, .btn, input[type='button'], input[type='submit'] {{"
        f"  background:{p['button']} !important; color:{p['buttonText']} !important;"
        f"  border:1px solid {p['border']} !important; border-radius:4px;"
        f"  padding:6px 12px; cursor:pointer;"
        "}"
        f"button:hover, .btn:hover {{ background:{p['hover']} !important; }}"
        # Input fields
        f"input, textarea, select {{"
        f"  background:{p['input']} !important; color:{p['inputText']} !important;"
        f"  border:1px solid {p['border']} !important; border-radius:3px;"
        f"  padding:4px 8px;"
        "}"
        f"input:focus, textarea:focus, select:focus {{"
        f"  border-color:{p['accent']} !important; outline:none;"
        f"  box-shadow:0 0 0 2px {p['accent']}33;"
        "}"
        # Contenteditable divs (Anki editor fields)
        f"[contenteditable='true'], [contenteditable='plaintext-only'] {{"
        f"  background:{p['input']} !important; color:{p['inputText']} !important;"
        f"  border:1px solid {p['border']} !important; border-radius:3px;"
        f"  padding:8px !important; min-height:60px !important;"
        "}"
        f"[contenteditable='true']:focus, [contenteditable='plaintext-only']:focus {{"
        f"  border-color:{p['accent']} !important; outline:none !important;"
        f"  box-shadow:0 0 0 2px {p['accent']}33 !important;"
        "}"
        # Checkboxes and radio buttons
        f"input[type='checkbox'], input[type='radio'] {{"
        f"  border:2px solid {p['border']} !important; background:{p['input']} !important;"
        "}"
        # Card content (reviewer)
        f".card, .card1, .card2, .card3 {{"
        f"  background:{p['bg']} !important; color:{p['fg']} !important;"
        "}"
        # Editor fields
        f".field {{"
        f"  background:{p['input']} !important; color:{p['inputText']} !important;"
        f"  border:1px solid {p['border']} !important;"
        "}"
        # Tables
        f"table {{ background:{p['bg']} !important; color:{p['fg']} !important; }}"
        f"th {{ background:{p['button']} !important; color:{p['buttonText']} !important;"
        f"  border:1px solid {p['border']} !important; padding:8px; }}"
        f"td {{ border:1px solid {p['border']} !important; padding:6px; color:{p['fg']} !important; }}"
        f"tr:hover {{ background:{p['hover']} !important; }}"
        f"tr.drag-hover {{ background:{p['selection']} !important; }}"
        # Lists
        f"ul, ol {{ color:{p['fg']} !important; }}"
        f"li {{ color:{p['fg']} !important; }}"
        # Code blocks
        f"code, pre {{"
        f"  background:{p['input']} !important; color:{p['fg']} !important;"
        f"  border:1px solid {p['border']} !important; border-radius:3px;"
        f"  padding:2px 4px; font-family:monospace;"
        "}"
        # Headings
        f"h1, h2, h3, h4, h5, h6 {{ color:{p['fg']} !important; }}"
        # Horizontal rules
        f"hr {{ border-color:{p['border']} !important; }}"
        # Scrollbars (webkit)
        f"::-webkit-scrollbar {{ width:12px; height:12px; }}"
        f"::-webkit-scrollbar-track {{ background:{p['bg']}; }}"
        f"::-webkit-scrollbar-thumb {{ background:{p['border']}; border-radius:6px; }}"
        f"::-webkit-scrollbar-thumb:hover {{ background:{p['muted']}; }}"
        # Dropdown menus and autocomplete
        f".autocomplete, .dropdown-menu {{"
        f"  background:{p['input']} !important; color:{p['inputText']} !important;"
        f"  border:1px solid {p['border']} !important; box-shadow:0 2px 8px rgba(0,0,0,0.2);"
        "}"
        f".autocomplete-item, .dropdown-item {{"
        f"  color:{p['fg']} !important; padding:6px 12px;"
        "}"
        f".autocomplete-item:hover, .dropdown-item:hover {{"
        f"  background:{p['hover']} !important; color:{p['fg']} !important;"
        "}"
        f".autocomplete-item.selected, .dropdown-item.selected {{"
        f"  background:{p['selection']} !important; color:{p['fg']} !important;"
        "}"
        # Modal dialogs and overlays
        f".modal, .overlay {{"
        f"  background:{p['bg']} !important; color:{p['fg']} !important;"
        f"  border:1px solid {p['border']} !important;"
        "}"
        f".modal-header {{ background:{p['button']} !important; color:{p['buttonText']} !important; border-bottom:1px solid {p['border']} !important; }}"
        f".modal-footer {{ background:{p['button']} !important; border-top:1px solid {p['border']} !important; }}"
    )

def inject_css(web_content, ctx):
    """Inject CSS into webviews with context-specific enhancements."""
    theme = get_active_theme()
    p = palette_for(theme)

    # Base CSS for all contexts
    base_css = css_vars(p)

    # Context-specific CSS additions
    context_css = ""

    # Check context type and add specific styling
    ctx_name = ctx.__class__.__name__ if hasattr(ctx, '__class__') else str(ctx)

    # DeckBrowser - main deck list
    if "DeckBrowser" in ctx_name:
        context_css += f"""
        /* Deck browser specific */
        .deck {{ color:{p['fg']} !important; }}
        .deck-current {{ background:{p['hover']} !important; }}
        tr.deck td {{ padding:8px !important; color:{p['fg']} !important; }}
        .collapse {{ color:{p['muted']} !important; }}
        .filtered {{ color:{p['accent']} !important; }}
        .gears {{ color:{p['muted']} !important; }}
        """

    # Reviewer - card display
    elif "Reviewer" in ctx_name or "Review" in ctx_name:
        context_css += f"""
        /* Reviewer specific */
        #qa {{ background:{p['bg']} !important; color:{p['fg']} !important; }}
        .nightMode .card {{ background:{p['bg']} !important; color:{p['fg']} !important; }}
        #answer {{ color:{p['fg']} !important; }}
        .replay-button {{ background:{p['button']} !important; border:1px solid {p['border']} !important; }}
        .typeGood {{ color:{p['accent']} !important; }}
        .typeBad {{ color:#E74C3C !important; }}
        .typeMissed {{ color:#F39C12 !important; }}
        """

    # Editor - note editing
    elif "Editor" in ctx_name:
        context_css += f"""
        /* Editor specific */
        .fname {{ color:{p['muted']} !important; font-size:12px; }}
        .field {{ min-height:60px !important; background:{p['input']} !important; color:{p['inputText']} !important; }}
        .EditorField {{ background:{p['input']} !important; color:{p['inputText']} !important; }}
        .fieldButton {{ background:{p['button']} !important; color:{p['buttonText']} !important; border:1px solid {p['border']} !important; }}
        .tag {{ background:{p['button']} !important; color:{p['buttonText']} !important; border:1px solid {p['border']} !important; padding:2px 6px; border-radius:3px; }}
        .tagAdd {{ background:{p['input']} !important; color:{p['inputText']} !important; }}
        /* Note type and deck selectors */
        #notetype {{ background:{p['input']} !important; color:{p['inputText']} !important; border:1px solid {p['border']} !important; }}
        #deck {{ background:{p['input']} !important; color:{p['inputText']} !important; border:1px solid {p['border']} !important; }}
        /* Editor toolbar */
        .topbut, .linkb {{ background:{p['button']} !important; color:{p['buttonText']} !important; border:1px solid {p['border']} !important; }}
        .topbut:hover, .linkb:hover {{ background:{p['hover']} !important; }}
        /* Dupes area */
        #dupes {{ background:{p['input']} !important; color:{p['muted']} !important; border:1px solid {p['border']} !important; padding:4px; }}
        .dupes {{ color:{p['accent']} !important; }}
        /* Placeholder text in fields */
        .field:empty:before {{ color:{p['muted']} !important; }}
        /* Rich text controls */
        .richTextButton {{ background:{p['button']} !important; color:{p['buttonText']} !important; border:1px solid {p['border']} !important; }}
        .richTextButton:hover {{ background:{p['hover']} !important; }}
        .richTextButton.highlighted {{ background:{p['accent']} !important; color:{p['bg']} !important; }}
        """

    # Overview - deck overview
    elif "Overview" in ctx_name:
        context_css += f"""
        /* Overview specific */
        .descfont {{ color:{p['fg']} !important; }}
        """

    # Browser - card browser
    elif "Browser" in ctx_name:
        context_css += f"""
        /* Browser specific */
        .browser-table {{ background:{p['bg']} !important; }}
        .search {{ background:{p['input']} !important; color:{p['inputText']} !important; border:1px solid {p['border']} !important; }}
        .cell {{ color:{p['fg']} !important; }}
        .browserRow {{ background:{p['bg']} !important; }}
        .browserRow:hover {{ background:{p['hover']} !important; }}
        /* Browser sidebar */
        .sidebar {{ background:{p['bg']} !important; color:{p['fg']} !important; }}
        .sidebar-item {{ color:{p['fg']} !important; padding:4px 8px; }}
        .sidebar-item:hover {{ background:{p['hover']} !important; }}
        .sidebar-item.selected {{ background:{p['selection']} !important; }}
        /* Browser toolbar */
        #searchEdit {{ background:{p['input']} !important; color:{p['inputText']} !important; border:1px solid {p['border']} !important; }}
        /* Card preview in browser */
        #previewArea {{ background:{p['bg']} !important; color:{p['fg']} !important; }}
        /* Suspended and marked cards */
        .suspended {{ color:{p['muted']} !important; opacity:0.7; }}
        .marked {{ color:{p['accent']} !important; }}
        /* Column headers */
        th.browser-header {{ background:{p['button']} !important; color:{p['buttonText']} !important; border:1px solid {p['border']} !important; }}
        /* Filter bar */
        .filterBar {{ background:{p['bg']} !important; border:1px solid {p['border']} !important; padding:8px; }}
        """

    # Toolbar and bottom bars
    elif "Toolbar" in ctx_name or "BottomBar" in ctx_name:
        context_css += f"""
        /* Toolbar/BottomBar specific */
        .bottom {{ background:{p['bg']} !important; border-top:1px solid {p['border']} !important; }}
        """

    # Combine all CSS
    full_css = base_css + context_css

    # Inject into page
    web_content.head += f'<style id="{_STYLE_ID}">{full_css}</style>'

def qss(p):
    """Generate comprehensive Qt Style Sheets for all Qt widgets."""
    return f"""
    /* Main widget styling */
    QWidget {{
        background:{p['bg']};
        color:{p['fg']};
        font-size:14px;
    }}

    /* Buttons */
    QPushButton {{
        background:{p['button']};
        color:{p['buttonText']};
        border:1px solid {p['border']};
        border-radius:4px;
        padding:6px 12px;
        min-height:24px;
    }}
    QPushButton:hover {{
        background:{p['hover']};
        border-color:{p['accent']};
    }}
    QPushButton:pressed {{
        background:{p['selection']};
    }}
    QPushButton:disabled {{
        background:{p['border']};
        color:{p['muted']};
    }}

    /* Input fields */
    QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox {{
        background:{p['input']};
        color:{p['inputText']};
        border:1px solid {p['border']};
        border-radius:3px;
        padding:4px 8px;
        selection-background-color:{p['selection']};
        selection-color:{p['fg']};
    }}
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
        border:2px solid {p['accent']};
    }}

    /* Combo boxes (dropdowns) */
    QComboBox {{
        background:{p['input']};
        color:{p['inputText']};
        border:1px solid {p['border']};
        border-radius:3px;
        padding:4px 8px;
        min-height:24px;
    }}
    QComboBox:hover {{
        border-color:{p['accent']};
    }}
    QComboBox::drop-down {{
        border:none;
        width:20px;
    }}
    QComboBox QAbstractItemView {{
        background:{p['input']};
        color:{p['inputText']};
        selection-background-color:{p['selection']};
        selection-color:{p['fg']};
        border:1px solid {p['border']};
    }}

    /* Tables and lists */
    QTableView, QListView, QTreeView {{
        background:{p['bg']};
        color:{p['fg']};
        alternate-background-color:{p['input']};
        gridline-color:{p['border']};
        border:1px solid {p['border']};
        selection-background-color:{p['selection']};
        selection-color:{p['fg']};
    }}
    QTableView::item:hover, QListView::item:hover, QTreeView::item:hover {{
        background:{p['hover']};
    }}
    QHeaderView::section {{
        background:{p['button']};
        color:{p['buttonText']};
        border:1px solid {p['border']};
        padding:6px;
        font-weight:bold;
    }}

    /* Menus */
    QMenuBar {{
        background:{p['bg']};
        color:{p['fg']};
        border-bottom:1px solid {p['border']};
    }}
    QMenuBar::item {{
        background:transparent;
        padding:4px 12px;
    }}
    QMenuBar::item:selected {{
        background:{p['hover']};
    }}
    QMenuBar::item:pressed {{
        background:{p['selection']};
    }}
    QMenu {{
        background:{p['bg']};
        color:{p['fg']};
        border:1px solid {p['border']};
    }}
    QMenu::item {{
        padding:6px 24px 6px 8px;
        min-width:120px;
    }}
    QMenu::item:selected {{
        background:{p['hover']};
    }}
    QMenu::separator {{
        height:1px;
        background:{p['border']};
        margin:4px 0;
    }}

    /* Scrollbars */
    QScrollBar:vertical {{
        background:{p['bg']};
        width:12px;
        border:none;
    }}
    QScrollBar::handle:vertical {{
        background:{p['border']};
        border-radius:6px;
        min-height:20px;
    }}
    QScrollBar::handle:vertical:hover {{
        background:{p['muted']};
    }}
    QScrollBar:horizontal {{
        background:{p['bg']};
        height:12px;
        border:none;
    }}
    QScrollBar::handle:horizontal {{
        background:{p['border']};
        border-radius:6px;
        min-width:20px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background:{p['muted']};
    }}
    QScrollBar::add-line, QScrollBar::sub-line {{
        border:none;
        background:none;
    }}

    /* Tabs */
    QTabWidget::pane {{
        border:1px solid {p['border']};
        background:{p['bg']};
    }}
    QTabBar::tab {{
        background:{p['button']};
        color:{p['buttonText']};
        border:1px solid {p['border']};
        padding:6px 12px;
        margin-right:2px;
    }}
    QTabBar::tab:selected {{
        background:{p['bg']};
        border-bottom-color:{p['bg']};
    }}
    QTabBar::tab:hover {{
        background:{p['hover']};
    }}

    /* Checkboxes and radio buttons */
    QCheckBox, QRadioButton {{
        color:{p['fg']};
        spacing:8px;
    }}
    QCheckBox::indicator, QRadioButton::indicator {{
        width:18px;
        height:18px;
        border:1px solid {p['border']};
        background:{p['input']};
    }}
    QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
        background:{p['accent']};
        border-color:{p['accent']};
    }}
    QRadioButton::indicator {{
        border-radius:9px;
    }}

    /* Sliders */
    QSlider::groove:horizontal {{
        background:{p['border']};
        height:4px;
        border-radius:2px;
    }}
    QSlider::handle:horizontal {{
        background:{p['accent']};
        width:16px;
        height:16px;
        margin:-6px 0;
        border-radius:8px;
    }}
    QSlider::handle:horizontal:hover {{
        background:{p['hover']};
    }}

    /* Toolbars */
    QToolBar {{
        background:{p['bg']};
        border:1px solid {p['border']};
        spacing:4px;
        padding:4px;
    }}
    QToolButton {{
        background:transparent;
        color:{p['fg']};
        border:none;
        border-radius:3px;
        padding:4px;
    }}
    QToolButton:hover {{
        background:{p['hover']};
    }}
    QToolButton:pressed {{
        background:{p['selection']};
    }}

    /* Status bar */
    QStatusBar {{
        background:{p['bg']};
        color:{p['muted']};
        border-top:1px solid {p['border']};
    }}

    /* Progress bars */
    QProgressBar {{
        background:{p['input']};
        border:1px solid {p['border']};
        border-radius:3px;
        text-align:center;
        color:{p['fg']};
    }}
    QProgressBar::chunk {{
        background:{p['accent']};
        border-radius:2px;
    }}

    /* Dialogs */
    QDialog {{
        background:{p['bg']};
        color:{p['fg']};
    }}

    /* Tooltips */
    QToolTip {{
        background:{p['button']};
        color:{p['buttonText']};
        border:1px solid {p['border']};
        padding:4px;
    }}

    /* Group boxes */
    QGroupBox {{
        color:{p['fg']};
        border:1px solid {p['border']};
        border-radius:4px;
        margin-top:8px;
        padding-top:12px;
    }}
    QGroupBox::title {{
        subcontrol-origin:margin;
        subcontrol-position:top left;
        padding:0 4px;
        color:{p['accent']};
    }}

    /* Splitters */
    QSplitter::handle {{
        background:{p['border']};
    }}
    QSplitter::handle:hover {{
        background:{p['muted']};
    }}

    /* Labels */
    QLabel {{
        color:{p['fg']};
    }}

    /* Spin boxes */
    QSpinBox::up-button, QDoubleSpinBox::up-button {{
        background:{p['button']};
        border:1px solid {p['border']};
    }}
    QSpinBox::down-button, QDoubleSpinBox::down-button {{
        background:{p['button']};
        border:1px solid {p['border']};
    }}

    /* Text browser (for help/preview) */
    QTextBrowser {{
        background:{p['bg']};
        color:{p['fg']};
        border:1px solid {p['border']};
        selection-background-color:{p['selection']};
        selection-color:{p['fg']};
    }}

    /* Disabled widgets */
    QWidget:disabled {{
        color:{p['muted']};
    }}
    """

def apply_qt_styles(theme: Theme):
    app = QApplication.instance()
    if app:
        app.setStyleSheet(qss(palette_for(theme)))

# ---------------- Instant refresh ----------------
def _build_refresh_js(theme: Theme) -> str:
    """Build JavaScript to refresh CSS in webviews safely using JSON escaping."""
    import json
    css = css_vars(palette_for(theme))
    # Use JSON encoding for safe JavaScript string escaping
    css_json = json.dumps(css)
    style_id_json = json.dumps(_STYLE_ID)
    return (
        "(function(){"
        f"var id={style_id_json};"
        "var el=document.getElementById(id);"
        "if(!el){el=document.createElement('style');el.id=id;document.head.appendChild(el);}"
        f"el.textContent={css_json};"
        "})();"
    )

def refresh_all_webviews():
    """Push updated CSS into every open webview instantly."""
    theme = get_active_theme()
    js = _build_refresh_js(theme)
    for attr in ("web", "bottomWeb"):
        wv = getattr(mw, attr, None)
        if wv:
            try:
                wv.eval(js)
            except (RuntimeError, AttributeError) as e:
                # WebView might be closed or not ready - safe to ignore
                # Uncomment for debugging: print(f"AnkiThemeTwin: {e}")
                pass

def apply_theme_everywhere(theme: Theme):
    """Apply QSS + refresh all webviews in one call."""
    apply_qt_styles(theme)
    refresh_all_webviews()

# ---------------- Theme Presets ----------------
def get_presets() -> list:
    """Get saved theme presets."""
    cfg = get_config()
    return cfg.get("presets", [])

def save_preset(name: str):
    """Save current theme and settings as a preset."""
    cfg = get_config()
    preset = {
        "name": name,
        "theme": cfg.get("currentTheme", "sepia_special"),
        "fontSize": cfg.get("fontSize", 16),
        "fontFamily": cfg.get("fontFamily", "Segoe UI,Amiri,Arial,sans-serif"),
        "lineHeight": cfg.get("lineHeight", 1.58),
        "letterSpacing": cfg.get("letterSpacing", 0.0),
    }
    presets = get_presets()
    # Remove existing preset with same name
    presets = [p for p in presets if p.get("name") != name]
    presets.append(preset)
    cfg["presets"] = presets
    write_config(cfg)
    tooltip(f"Preset '{name}' saved!")

def load_preset(preset: dict):
    """Load a theme preset."""
    cfg = get_config()
    cfg["currentTheme"] = preset.get("theme", "sepia_special")
    cfg["fontSize"] = preset.get("fontSize", 16)
    cfg["fontFamily"] = preset.get("fontFamily", "Segoe UI,Amiri,Arial,sans-serif")
    cfg["lineHeight"] = preset.get("lineHeight", 1.58)
    cfg["letterSpacing"] = preset.get("letterSpacing", 0.0)
    write_config(cfg)
    apply_theme_everywhere(get_active_theme())
    tooltip(f"Preset '{preset.get('name')}' loaded!")

def delete_preset(name: str):
    """Delete a preset."""
    cfg = get_config()
    presets = [p for p in get_presets() if p.get("name") != name]
    cfg["presets"] = presets
    write_config(cfg)
    tooltip(f"Preset '{name}' deleted!")

# ---------------- Custom Themes ----------------
def get_custom_themes() -> dict:
    """Get user-created custom themes."""
    cfg = get_config()
    return cfg.get("customThemes", {})

def save_custom_theme(name: str, palette: dict):
    """Save a custom theme."""
    cfg = get_config()
    custom_themes = get_custom_themes()
    custom_themes[name] = palette
    cfg["customThemes"] = custom_themes
    write_config(cfg)
    # Add to PALETTES dynamically
    PALETTES[name] = palette
    tooltip(f"Custom theme '{name}' saved!")

def delete_custom_theme(name: str):
    """Delete a custom theme."""
    cfg = get_config()
    custom_themes = get_custom_themes()
    if name in custom_themes:
        del custom_themes[name]
        cfg["customThemes"] = custom_themes
        write_config(cfg)
        if name in PALETTES:
            del PALETTES[name]
        tooltip(f"Custom theme '{name}' deleted!")

def export_theme(theme_name: str, file_path: str):
    """Export a theme to JSON file."""
    if theme_name in PALETTES:
        theme_data = {
            "name": theme_name,
            "palette": PALETTES[theme_name],
            "version": VERSION,
        }
        with open(file_path, 'w') as f:
            json.dump(theme_data, f, indent=2)
        tooltip(f"Theme exported to {file_path}")
    else:
        showInfo(f"Theme '{theme_name}' not found!")

def import_theme(file_path: str):
    """Import a theme from JSON file."""
    try:
        with open(file_path, 'r') as f:
            theme_data = json.load(f)
        name = theme_data.get("name", "imported_theme")
        palette = theme_data.get("palette")
        if palette:
            save_custom_theme(name, palette)
            tooltip(f"Theme '{name}' imported successfully!")
        else:
            showInfo("Invalid theme file!")
    except Exception as e:
        showInfo(f"Error importing theme: {e}")

# ---------------- Scheduled Theme Switching ----------------
def get_scheduled_themes() -> dict:
    """Get scheduled theme switching configuration."""
    cfg = get_config()
    return cfg.get("scheduledThemes", {
        "enabled": False,
        "morning": {"time": "07:00", "theme": "sepia_word"},
        "afternoon": {"time": "12:00", "theme": "sepia_special"},
        "evening": {"time": "18:00", "theme": "blue_light"},
        "night": {"time": "23:00", "theme": "gray_word"}
    })

def save_scheduled_themes(schedule: dict):
    """Save scheduled theme configuration."""
    cfg = get_config()
    cfg["scheduledThemes"] = schedule
    write_config(cfg)

def check_scheduled_theme():
    """Check and apply scheduled theme if enabled."""
    schedule = get_scheduled_themes()
    if not schedule.get("enabled"):
        return

    now = datetime.now().time()
    current_theme = None

    # Parse times and find the appropriate theme
    times = []
    for period in ["morning", "afternoon", "evening", "night"]:
        if period in schedule:
            time_str = schedule[period].get("time", "00:00")
            hour, minute = map(int, time_str.split(":"))
            times.append((time(hour, minute), schedule[period].get("theme")))

    # Sort by time
    times.sort(key=lambda x: x[0])

    # Find the current theme based on time
    for t, theme in reversed(times):
        if now >= t:
            current_theme = theme
            break

    # If no match, use the last time period (wraps around to night)
    if current_theme is None and times:
        current_theme = times[-1][1]

    # Apply if different from current
    if current_theme and current_theme != get_active_theme():
        set_theme(current_theme)
        tooltip(f"Auto-switched to {current_theme}")

# ---------------- Per-Deck Themes ----------------
def get_deck_themes() -> dict:
    """Get per-deck theme configuration."""
    cfg = get_config()
    return cfg.get("deckThemes", {})

def set_deck_theme(deck_name: str, theme: str):
    """Set theme for a specific deck."""
    cfg = get_config()
    deck_themes = get_deck_themes()
    deck_themes[deck_name] = theme
    cfg["deckThemes"] = deck_themes
    write_config(cfg)
    tooltip(f"Theme for deck '{deck_name}' set to {theme}")

def get_theme_for_deck(deck_name: str) -> Optional[str]:
    """Get theme for a specific deck, or None if not set."""
    deck_themes = get_deck_themes()
    return deck_themes.get(deck_name)

def apply_deck_theme_if_set(deck_name: str):
    """Apply theme for deck if configured."""
    theme = get_theme_for_deck(deck_name)
    if theme and theme in PALETTES:
        set_theme(theme)
        tooltip(f"Loaded theme for {deck_name}")

# ---------------- Theme Animations ----------------
def get_animation_settings() -> dict:
    """Get animation settings."""
    cfg = get_config()
    return cfg.get("animations", {
        "enabled": True,
        "duration": 300,  # milliseconds
        "style": "fade"  # fade, slide, none
    })

def save_animation_settings(settings: dict):
    """Save animation settings."""
    cfg = get_config()
    cfg["animations"] = settings
    write_config(cfg)

# ---------------- About Dialog ----------------
def show_about_dialog():
    dlg = QDialog(mw)
    dlg.setWindowTitle("About — AnkiThemeTwin")
    layout = QVBoxLayout(dlg)
    lbl = QLabel(
        '<div style="font-size:14px;">'
        f'<b>AnkiThemeTwin</b> v{VERSION}<br>'
        '13+ themes including accessibility themes.<br>'
        'Custom theme creator, presets, keyboard shortcuts.<br>'
        'Configurable fonts, sizes, and comprehensive styling.<br><br>'
        '<b>Features:</b><br>'
        '• 7 eye-comfort themes + 6 accessibility themes<br>'
        '• Custom theme creator with color picker<br>'
        '• Theme presets and import/export<br>'
        '• Keyboard shortcuts (Ctrl+Shift+1-7)<br>'
        '• Advanced font customization<br><br>'
        'Author: <b>Dr. Mohammed</b><br>'
        '<a href="https://github.com/MohammedTsmu/AnkiThemeTwin">'
        'GitHub: MohammedTsmu/AnkiThemeTwin</a>'
        '</div>'
    )
    lbl.setOpenExternalLinks(True)
    layout.addWidget(lbl)
    btn = QPushButton("Open GitHub")
    btn.clicked.connect(lambda: openLink("https://github.com/MohammedTsmu/AnkiThemeTwin"))
    layout.addWidget(btn)
    closeBtn = QPushButton("Close")
    closeBtn.clicked.connect(dlg.accept)
    layout.addWidget(closeBtn)
    dlg.setLayout(layout)
    dlg.resize(600, 400)
    dlg.exec()

# ---------------- Custom Theme Creator Dialog ----------------
def show_custom_theme_creator():
    """Show dialog to create custom themes."""
    dlg = QDialog(mw)
    dlg.setWindowTitle("Custom Theme Creator")
    dlg.resize(700, 600)
    layout = QVBoxLayout(dlg)

    # Theme name
    name_layout = QHBoxLayout()
    name_layout.addWidget(QLabel("Theme Name:"))
    name_input = QLineEdit()
    name_input.setPlaceholderText("my_custom_theme")
    name_layout.addWidget(name_input)
    layout.addLayout(name_layout)

    # Scroll area for color pickers
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll_widget = QWidget()
    scroll_layout = QGridLayout(scroll_widget)

    color_inputs = {}
    color_keys = ["bg", "fg", "muted", "border", "accent", "button",
                  "buttonText", "input", "inputText", "hover", "selection"]
    color_labels = {
        "bg": "Background", "fg": "Foreground/Text", "muted": "Muted Text",
        "border": "Borders", "accent": "Accent Color", "button": "Button Background",
        "buttonText": "Button Text", "input": "Input Background", "inputText": "Input Text",
        "hover": "Hover State", "selection": "Selection"
    }

    row = 0
    for key in color_keys:
        label = QLabel(f"{color_labels.get(key, key)}:")
        color_input = QLineEdit("#FFFFFF")
        color_btn = QPushButton("Pick")

        def make_picker(inp=color_input):
            def pick_color():
                color = QColorDialog.getColor()
                if color.isValid():
                    inp.setText(color.name())
            return pick_color

        color_btn.clicked.connect(make_picker())
        color_inputs[key] = color_input

        scroll_layout.addWidget(label, row, 0)
        scroll_layout.addWidget(color_input, row, 1)
        scroll_layout.addWidget(color_btn, row, 2)
        row += 1

    scroll.setWidget(scroll_widget)
    layout.addWidget(scroll)

    # Buttons
    btn_layout = QHBoxLayout()

    def save_theme():
        name = name_input.text().strip()
        if not name:
            showInfo("Please enter a theme name!")
            return
        palette = {key: inp.text() for key, inp in color_inputs.items()}
        save_custom_theme(name, palette)
        dlg.accept()

    save_btn = QPushButton("Save Theme")
    save_btn.clicked.connect(save_theme)
    cancel_btn = QPushButton("Cancel")
    cancel_btn.clicked.connect(dlg.reject)

    btn_layout.addWidget(save_btn)
    btn_layout.addWidget(cancel_btn)
    layout.addLayout(btn_layout)

    dlg.exec()

# ---------------- Presets Manager Dialog ----------------
def show_presets_manager():
    """Show dialog to manage theme presets."""
    dlg = QDialog(mw)
    dlg.setWindowTitle("Theme Presets Manager")
    dlg.resize(600, 400)
    layout = QVBoxLayout(dlg)

    # Current settings info
    cfg = get_config()
    info = QLabel(
        f"Current: {cfg.get('currentTheme', 'sepia_special')} | "
        f"Font: {cfg.get('fontSize', 16)}px"
    )
    layout.addWidget(info)

    # Presets list
    presets_list = QTextEdit()
    presets_list.setReadOnly(True)

    def refresh_list():
        presets = get_presets()
        if not presets:
            presets_list.setPlainText("No presets saved yet.")
        else:
            text = ""
            for preset in presets:
                text += f"• {preset.get('name')}: {preset.get('theme')} | {preset.get('fontSize')}px\n"
            presets_list.setPlainText(text)

    refresh_list()
    layout.addWidget(presets_list)

    # Save current as preset
    save_layout = QHBoxLayout()
    save_layout.addWidget(QLabel("Save current as:"))
    preset_name = QLineEdit()
    preset_name.setPlaceholderText("My Preset")
    save_layout.addWidget(preset_name)

    def save_current():
        name = preset_name.text().strip()
        if name:
            save_preset(name)
            refresh_list()
            preset_name.clear()

    save_btn = QPushButton("Save")
    save_btn.clicked.connect(save_current)
    save_layout.addWidget(save_btn)
    layout.addLayout(save_layout)

    # Load/Delete preset
    action_layout = QHBoxLayout()
    action_layout.addWidget(QLabel("Preset name:"))
    action_name = QLineEdit()
    action_layout.addWidget(action_name)

    def load_preset_by_name():
        name = action_name.text().strip()
        presets = get_presets()
        preset = next((p for p in presets if p.get("name") == name), None)
        if preset:
            load_preset(preset)
            dlg.accept()
        else:
            showInfo(f"Preset '{name}' not found!")

    def delete_preset_by_name():
        name = action_name.text().strip()
        if name:
            delete_preset(name)
            refresh_list()
            action_name.clear()

    load_btn = QPushButton("Load")
    load_btn.clicked.connect(load_preset_by_name)
    delete_btn = QPushButton("Delete")
    delete_btn.clicked.connect(delete_preset_by_name)
    action_layout.addWidget(load_btn)
    action_layout.addWidget(delete_btn)
    layout.addLayout(action_layout)

    # Close button
    close_btn = QPushButton("Close")
    close_btn.clicked.connect(dlg.accept)
    layout.addWidget(close_btn)

    dlg.exec()

# ---------------- Advanced Settings Dialog ----------------
def show_advanced_settings():
    """Show advanced font and typography settings."""
    dlg = QDialog(mw)
    dlg.setWindowTitle("Advanced Settings")
    dlg.resize(500, 400)
    layout = QVBoxLayout(dlg)

    cfg = get_config()

    # Font family
    font_layout = QHBoxLayout()
    font_layout.addWidget(QLabel("Font Family:"))
    font_input = QLineEdit(cfg.get("fontFamily", "Segoe UI,Amiri,Arial,sans-serif"))
    font_layout.addWidget(font_input)
    layout.addLayout(font_layout)

    # Font size slider
    size_layout = QVBoxLayout()
    size_layout.addWidget(QLabel(f"Font Size: {cfg.get('fontSize', 16)}px"))
    size_slider = QSlider(Qt.Orientation.Horizontal)
    size_slider.setMinimum(8)
    size_slider.setMaximum(32)
    size_slider.setValue(cfg.get("fontSize", 16))
    size_label = QLabel(f"{cfg.get('fontSize', 16)}px")

    def update_size_label(val):
        size_label.setText(f"{val}px")

    size_slider.valueChanged.connect(update_size_label)
    size_layout.addWidget(size_slider)
    size_layout.addWidget(size_label)
    layout.addLayout(size_layout)

    # Line height
    lh_layout = QHBoxLayout()
    lh_layout.addWidget(QLabel("Line Height:"))
    lh_spin = QSpinBox()
    lh_spin.setMinimum(100)
    lh_spin.setMaximum(300)
    lh_spin.setValue(int(cfg.get("lineHeight", 1.58) * 100))
    lh_spin.setSuffix("%")
    lh_layout.addWidget(lh_spin)
    layout.addLayout(lh_layout)

    # Letter spacing
    ls_layout = QHBoxLayout()
    ls_layout.addWidget(QLabel("Letter Spacing:"))
    ls_spin = QSpinBox()
    ls_spin.setMinimum(-5)
    ls_spin.setMaximum(10)
    ls_spin.setValue(int(cfg.get("letterSpacing", 0.0)))
    ls_spin.setSuffix("px")
    ls_layout.addWidget(ls_spin)
    layout.addLayout(ls_layout)

    # Save button
    def save_settings():
        cfg["fontFamily"] = font_input.text()
        cfg["fontSize"] = size_slider.value()
        cfg["lineHeight"] = lh_spin.value() / 100.0
        cfg["letterSpacing"] = float(ls_spin.value())
        write_config(cfg)
        apply_theme_everywhere(get_active_theme())
        tooltip("Settings saved!")
        dlg.accept()

    save_btn = QPushButton("Save & Apply")
    save_btn.clicked.connect(save_settings)
    layout.addWidget(save_btn)

    cancel_btn = QPushButton("Cancel")
    cancel_btn.clicked.connect(dlg.reject)
    layout.addWidget(cancel_btn)

    dlg.exec()

# ---------------- Theme Preview Dialog ----------------
def show_theme_preview():
    """Show visual preview of all themes."""
    dlg = QDialog(mw)
    dlg.setWindowTitle("Theme Preview")
    dlg.resize(800, 600)
    layout = QVBoxLayout(dlg)

    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll_widget = QWidget()
    scroll_layout = QVBoxLayout(scroll_widget)

    # Get all available themes
    all_themes = list(THEME_OPTIONS) + list(ACCESSIBILITY_THEMES)
    custom_themes = get_custom_themes()
    for name in custom_themes.keys():
        all_themes.append((name.replace("_", " ").title(), name))

    for label, theme_key in all_themes:
        if theme_key not in PALETTES:
            continue

        # Create preview frame
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        frame_layout = QVBoxLayout(frame)

        palette = PALETTES[theme_key]

        # Theme name
        name_label = QLabel(f"<b>{label}</b>")
        frame_layout.addWidget(name_label)

        # Color preview boxes
        colors_layout = QHBoxLayout()
        for color_key in ["bg", "fg", "accent", "button", "input"]:
            color_box = QLabel(color_key.upper())
            color_box.setStyleSheet(
                f"background: {palette.get(color_key, '#FFF')}; "
                f"color: {palette.get('fg', '#000')}; "
                f"border: 1px solid {palette.get('border', '#CCC')}; "
                f"padding: 10px; min-width: 60px;"
            )
            color_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
            colors_layout.addWidget(color_box)
        frame_layout.addLayout(colors_layout)

        # Apply button
        apply_btn = QPushButton("Apply This Theme")
        apply_btn.clicked.connect(lambda _, t=theme_key: (set_theme(t), dlg.accept()))
        frame_layout.addWidget(apply_btn)

        scroll_layout.addWidget(frame)

    scroll.setWidget(scroll_widget)
    layout.addWidget(scroll)

    close_btn = QPushButton("Close")
    close_btn.clicked.connect(dlg.reject)
    layout.addWidget(close_btn)

    dlg.exec()

# ---------------- Scheduled Themes Dialog ----------------
def show_scheduled_themes_dialog():
    """Show dialog to configure scheduled theme switching."""
    dlg = QDialog(mw)
    dlg.setWindowTitle("Scheduled Theme Switching")
    dlg.resize(600, 500)
    layout = QVBoxLayout(dlg)

    schedule = get_scheduled_themes()

    # Enable/disable checkbox
    enabled_cb = QCheckBox("Enable scheduled theme switching")
    enabled_cb.setChecked(schedule.get("enabled", False))
    layout.addWidget(enabled_cb)

    # Time periods
    periods_layout = QGridLayout()
    periods_layout.addWidget(QLabel("<b>Period</b>"), 0, 0)
    periods_layout.addWidget(QLabel("<b>Time</b>"), 0, 1)
    periods_layout.addWidget(QLabel("<b>Theme</b>"), 0, 2)

    time_inputs = {}
    theme_combos = {}
    periods = ["morning", "afternoon", "evening", "night"]
    period_labels = ["Morning", "Afternoon", "Evening", "Night"]

    for idx, (period, label) in enumerate(zip(periods, period_labels), 1):
        periods_layout.addWidget(QLabel(label), idx, 0)

        # Time input
        time_edit = QLineEdit(schedule.get(period, {}).get("time", "00:00"))
        time_edit.setPlaceholderText("HH:MM")
        time_inputs[period] = time_edit
        periods_layout.addWidget(time_edit, idx, 1)

        # Theme combo
        theme_combo = QComboBox()
        all_themes = [key for _, key in THEME_OPTIONS + ACCESSIBILITY_THEMES]
        theme_combo.addItems(all_themes)
        current_theme = schedule.get(period, {}).get("theme", "sepia_word")
        if current_theme in all_themes:
            theme_combo.setCurrentText(current_theme)
        theme_combos[period] = theme_combo
        periods_layout.addWidget(theme_combo, idx, 2)

    layout.addLayout(periods_layout)

    # Save button
    def save_schedule():
        new_schedule = {
            "enabled": enabled_cb.isChecked()
        }
        for period in periods:
            new_schedule[period] = {
                "time": time_inputs[period].text(),
                "theme": theme_combos[period].currentText()
            }
        save_scheduled_themes(new_schedule)
        tooltip("Scheduled themes saved!")
        dlg.accept()

    save_btn = QPushButton("Save")
    save_btn.clicked.connect(save_schedule)
    layout.addWidget(save_btn)

    cancel_btn = QPushButton("Cancel")
    cancel_btn.clicked.connect(dlg.reject)
    layout.addWidget(cancel_btn)

    dlg.exec()

# ---------------- Deck Themes Dialog ----------------
def show_deck_themes_dialog():
    """Show dialog to configure per-deck themes."""
    dlg = QDialog(mw)
    dlg.setWindowTitle("Per-Deck Themes")
    dlg.resize(600, 400)
    layout = QVBoxLayout(dlg)

    info = QLabel("Set different themes for different decks.")
    layout.addWidget(info)

    # Current deck themes
    deck_themes = get_deck_themes()
    themes_list = QTextEdit()
    themes_list.setReadOnly(True)

    def refresh_list():
        if not deck_themes:
            themes_list.setPlainText("No deck-specific themes set.")
        else:
            text = ""
            for deck, theme in deck_themes.items():
                text += f"• {deck}: {theme}\n"
            themes_list.setPlainText(text)

    refresh_list()
    layout.addWidget(themes_list)

    # Set deck theme
    set_layout = QGridLayout()
    set_layout.addWidget(QLabel("Deck Name:"), 0, 0)
    deck_input = QLineEdit()
    set_layout.addWidget(deck_input, 0, 1)

    set_layout.addWidget(QLabel("Theme:"), 1, 0)
    theme_combo = QComboBox()
    all_themes = [key for _, key in THEME_OPTIONS + ACCESSIBILITY_THEMES]
    theme_combo.addItems(all_themes)
    set_layout.addWidget(theme_combo, 1, 1)

    def set_theme_for_deck():
        deck = deck_input.text().strip()
        theme = theme_combo.currentText()
        if deck:
            set_deck_theme(deck, theme)
            deck_themes[deck] = theme
            refresh_list()
            deck_input.clear()

    set_btn = QPushButton("Set Theme for Deck")
    set_btn.clicked.connect(set_theme_for_deck)
    set_layout.addWidget(set_btn, 2, 0, 1, 2)
    layout.addLayout(set_layout)

    close_btn = QPushButton("Close")
    close_btn.clicked.connect(dlg.accept)
    layout.addWidget(close_btn)

    dlg.exec()

# ---------------- Animation Settings Dialog ----------------
def show_animation_settings():
    """Show dialog to configure theme animations."""
    dlg = QDialog(mw)
    dlg.setWindowTitle("Animation Settings")
    dlg.resize(400, 300)
    layout = QVBoxLayout(dlg)

    settings = get_animation_settings()

    # Enable animations
    enabled_cb = QCheckBox("Enable theme transition animations")
    enabled_cb.setChecked(settings.get("enabled", True))
    layout.addWidget(enabled_cb)

    # Duration
    duration_layout = QHBoxLayout()
    duration_layout.addWidget(QLabel("Duration (ms):"))
    duration_spin = QSpinBox()
    duration_spin.setMinimum(100)
    duration_spin.setMaximum(2000)
    duration_spin.setValue(settings.get("duration", 300))
    duration_layout.addWidget(duration_spin)
    layout.addLayout(duration_layout)

    # Style
    style_layout = QVBoxLayout()
    style_layout.addWidget(QLabel("Animation Style:"))
    style_group = QButtonGroup(dlg)

    fade_rb = QRadioButton("Fade")
    fade_rb.setChecked(settings.get("style", "fade") == "fade")
    style_group.addButton(fade_rb)
    style_layout.addWidget(fade_rb)

    none_rb = QRadioButton("None (Instant)")
    none_rb.setChecked(settings.get("style", "fade") == "none")
    style_group.addButton(none_rb)
    style_layout.addWidget(none_rb)

    layout.addLayout(style_layout)

    # Save button
    def save_settings():
        new_settings = {
            "enabled": enabled_cb.isChecked(),
            "duration": duration_spin.value(),
            "style": "fade" if fade_rb.isChecked() else "none"
        }
        save_animation_settings(new_settings)
        tooltip("Animation settings saved!")
        dlg.accept()

    save_btn = QPushButton("Save")
    save_btn.clicked.connect(save_settings)
    layout.addWidget(save_btn)

    cancel_btn = QPushButton("Cancel")
    cancel_btn.clicked.connect(dlg.reject)
    layout.addWidget(cancel_btn)

    dlg.exec()

# ---------------- Menu ----------------

def set_theme(theme: Theme):
    """Set the current theme."""
    theme = normalize_theme(theme)
    cfg = get_config()
    cfg["currentTheme"] = theme
    write_config(cfg)
    apply_theme_everywhere(theme)

def set_font_size(size: int):
    """Set the font size and refresh all views. Valid range: 8-72px."""
    # Validate font size to prevent unreasonable values
    if not (8 <= size <= 72):
        size = 16  # Default fallback
    cfg = get_config()
    cfg["fontSize"] = size
    write_config(cfg)
    apply_theme_everywhere(get_active_theme())

def add_menu():
    m = mw.form.menuTools.addMenu("Theme: AnkiThemeTwin")

    # ---- Direct theme choices ----
    for label, key in THEME_OPTIONS:
        act = QAction(label, mw)
        act.triggered.connect(lambda _, k=key: set_theme(k))
        m.addAction(act)

    m.addSeparator()

    # ---- Accessibility Themes submenu ----
    accessibility_menu = QMenu("Accessibility Themes", m)
    for label, key in ACCESSIBILITY_THEMES:
        act = QAction(label, mw)
        act.triggered.connect(lambda _, k=key: set_theme(k))
        accessibility_menu.addAction(act)
    m.addMenu(accessibility_menu)

    m.addSeparator()

    # ---- Font Size submenu ----
    font_menu = QMenu("Font Size", m)
    font_group = QActionGroup(font_menu)
    font_group.setExclusive(True)
    current_size = get_font_size()
    font_sizes = [
        ("Very Small (12px)", 12),
        ("Small (14px)", 14),
        ("Medium (16px)", 16),
        ("Large (18px)", 18),
        ("Extra Large (20px)", 20),
        ("Huge (22px)", 22),
        ("Massive (24px)", 24),
    ]
    for label, size in font_sizes:
        act = QAction(label, font_menu, checkable=True)
        act.setChecked(current_size == size)
        act.triggered.connect(lambda _, s=size: set_font_size(s))
        font_group.addAction(act)
        font_menu.addAction(act)
    m.addMenu(font_menu)

    m.addSeparator()

    # ---- Advanced Features ----
    actPreview = QAction("Theme Preview Gallery...", mw)
    actPreview.triggered.connect(show_theme_preview)
    m.addAction(actPreview)

    actAdvanced = QAction("Advanced Settings...", mw)
    actAdvanced.triggered.connect(show_advanced_settings)
    m.addAction(actAdvanced)

    actCustomTheme = QAction("Create Custom Theme...", mw)
    actCustomTheme.triggered.connect(show_custom_theme_creator)
    m.addAction(actCustomTheme)

    actPresets = QAction("Manage Presets...", mw)
    actPresets.triggered.connect(show_presets_manager)
    m.addAction(actPresets)

    m.addSeparator()

    # ---- Scheduling & Per-Deck ----
    actScheduled = QAction("Scheduled Theme Switching...", mw)
    actScheduled.triggered.connect(show_scheduled_themes_dialog)
    m.addAction(actScheduled)

    actDeckThemes = QAction("Per-Deck Themes...", mw)
    actDeckThemes.triggered.connect(show_deck_themes_dialog)
    m.addAction(actDeckThemes)

    actAnimations = QAction("Animation Settings...", mw)
    actAnimations.triggered.connect(show_animation_settings)
    m.addAction(actAnimations)

    m.addSeparator()

    # ---- Links / About ----
    actGitHub = QAction("Visit Project GitHub", mw)
    actGitHub.triggered.connect(lambda: openLink("https://github.com/MohammedTsmu/AnkiThemeTwin"))
    m.addAction(actGitHub)

    actAbout = QAction("About AnkiThemeTwin", mw)
    actAbout.triggered.connect(show_about_dialog)
    m.addAction(actAbout)

    help_menu = mw.form.menuHelp
    actAboutHelp = QAction("About AnkiThemeTwin", mw)
    actAboutHelp.triggered.connect(show_about_dialog)
    help_menu.addAction(actAboutHelp)

def setup_keyboard_shortcuts():
    """Setup keyboard shortcuts for quick theme switching."""
    # Ctrl+Shift+1 through Ctrl+Shift+7 for the main themes
    theme_keys = [key for _, key in THEME_OPTIONS]
    for i, theme_key in enumerate(theme_keys[:7], 1):
        shortcut = QShortcut(QKeySequence(f"Ctrl+Shift+{i}"), mw)
        shortcut.activated.connect(lambda k=theme_key: (set_theme(k), tooltip(f"Switched to {k}")))

    # Ctrl+Shift+= for increasing font size
    increase_font = QShortcut(QKeySequence("Ctrl+Shift+="), mw)
    def increase_size():
        current = get_font_size()
        new_size = min(current + 2, 32)
        set_font_size(new_size)
        tooltip(f"Font size: {new_size}px")
    increase_font.activated.connect(increase_size)

    # Ctrl+Shift+- for decreasing font size
    decrease_font = QShortcut(QKeySequence("Ctrl+Shift+-"), mw)
    def decrease_size():
        current = get_font_size()
        new_size = max(current - 2, 8)
        set_font_size(new_size)
        tooltip(f"Font size: {new_size}px")
    decrease_font.activated.connect(decrease_size)

def on_profile_open():
    if not getattr(mw, "_ankitwin_menu", False):
        add_menu()
        setup_keyboard_shortcuts()
        # Load custom themes from config
        custom_themes = get_custom_themes()
        for name, palette in custom_themes.items():
            PALETTES[name] = palette
        mw._ankitwin_menu = True

    # Check scheduled theme on startup
    check_scheduled_theme()

    # Apply current theme
    apply_theme_everywhere(get_active_theme())

    # Set up timer to check scheduled themes every 5 minutes
    if not hasattr(mw, "_ankitwin_timer"):
        from aqt.qt import QTimer
        timer = QTimer(mw)
        timer.timeout.connect(check_scheduled_theme)
        timer.start(300000)  # 5 minutes in milliseconds
        mw._ankitwin_timer = timer

gui_hooks.profile_did_open.append(on_profile_open)
gui_hooks.webview_will_set_content.append(inject_css)
