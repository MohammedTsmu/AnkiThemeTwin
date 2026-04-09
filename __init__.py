# AnkiThemeTwin/__init__.py — Anki 25.x (Qt6/PyQt6) — v1.2.0
# 10 high-readability themes + follow-system mode + instant updates + configurable font size
# Tools > Theme: AnkiThemeTwin  |  Help > About AnkiThemeTwin

from aqt import mw, gui_hooks
from aqt.qt import (
    QAction, QActionGroup, QApplication, QMenu,
    QDialog, QVBoxLayout, QLabel, QPushButton, Qt,
)
from aqt.utils import openLink
from typing import Literal, Any

VERSION = "1.3.0"

Theme = Literal[
    "sepia_word", "sepia_paper", "gray_word", "gray_paper",
    "sepia_special", "blue_light", "olive_green"
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

PALETTES = {
    "sepia_word": SEPIA_WORD,
    "sepia_paper": SEPIA_PAPER,
    "gray_word": GRAY_WORD,
    "gray_paper": GRAY_PAPER,
    "sepia_special": SEPIA_SPECIAL,
    "blue_light": BLUE_LIGHT,
    "olive_green": OLIVE_GREEN,
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

def css_vars(p):
    """Generate comprehensive CSS for all webview contexts."""
    font_size = get_font_size()
    return (
        # Base styles
        "html, body {"
        f"  background:{p['bg']} !important; color:{p['fg']} !important;"
        '  font-family:"Segoe UI","Amiri","Arial",sans-serif !important;'
        f"  line-height:1.58; font-size:{font_size}px;"
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

# ---------------- About Dialog ----------------
def show_about_dialog():
    dlg = QDialog(mw)
    dlg.setWindowTitle("About — AnkiThemeTwin")
    layout = QVBoxLayout(dlg)
    lbl = QLabel(
        '<div style="font-size:14px;">'
        f'<b>AnkiThemeTwin</b> v{VERSION}<br>'
        '7 eye-comfort light themes with high readability.<br>'
        'Configurable font sizes and comprehensive styling.<br><br>'
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
    dlg.resize(520, 280)
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

    # ---- Font Size submenu ----
    font_menu = QMenu("Font Size", m)
    font_group = QActionGroup(font_menu)
    font_group.setExclusive(True)
    current_size = get_font_size()
    font_sizes = [
        ("Small (14px)", 14),
        ("Medium (16px)", 16),
        ("Large (18px)", 18),
        ("Extra Large (20px)", 20),
    ]
    for label, size in font_sizes:
        act = QAction(label, font_menu, checkable=True)
        act.setChecked(current_size == size)
        act.triggered.connect(lambda _, s=size: set_font_size(s))
        font_group.addAction(act)
        font_menu.addAction(act)
    m.addMenu(font_menu)

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

def on_profile_open():
    if not getattr(mw, "_ankitwin_menu", False):
        add_menu()
        mw._ankitwin_menu = True
    apply_theme_everywhere(get_active_theme())

gui_hooks.profile_did_open.append(on_profile_open)
gui_hooks.webview_will_set_content.append(inject_css)
