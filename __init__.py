# AnkiThemeTwin/__init__.py — Anki 25.x (Qt6/PyQt6) — v1.6.0
# Enhanced theming with keyboard shortcuts, more font sizes, theme presets, and custom theme creator
# Tools > Theme: AnkiThemeTwin  |  Help > About AnkiThemeTwin

from aqt import mw, gui_hooks
from aqt.qt import (
    QAction, QActionGroup, QApplication, QMenu,
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, Qt,
    QSlider, QColorDialog, QLineEdit, QSpinBox, QScrollArea,
    QWidget, QGridLayout, QComboBox, QCheckBox, QTextEdit,
    QShortcut, QKeySequence, QFrame, QTimeEdit, QButtonGroup,
    QRadioButton, QPalette, QColor, QTimer,
    QPixmap, QPainter, QPen, QBrush,
)
from aqt.utils import openLink, showInfo, tooltip
from typing import Literal, Any, Optional
import json
import os
import random
import math
from datetime import datetime, time

VERSION = "1.6.0"

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
    "input":"#000000","inputText":"#FFFFFF","hover":"#2A2A2A","selection":"#FFFF00",
    "stateNew":"#93C5FD","stateLearn":"#F87171","stateReview":"#4ADE80",
    "stateBuried":"#F59E0B","stateSuspended":"#FEF9C3","stateMarked":"#A855F7"}
DYSLEXIA_FRIENDLY = {"bg":"#FFFACD","fg":"#2F2F2F","muted":"#696969","border":"#E6DB8F",
    "accent":"#008B8B","button":"#FFF8B0","buttonText":"#2F2F2F",
    "input":"#FFFFF0","inputText":"#2F2F2F","hover":"#FFF48F","selection":"#FFE680"}

# Color blindness support themes
DEUTERANOPIA = {"bg":"#F0F0E8","fg":"#003366","muted":"#666699","border":"#9999CC",
    "accent":"#CC6600","button":"#E8E8E0","buttonText":"#003366",
    "input":"#FAFAF5","inputText":"#003366","hover":"#E0E0D8","selection":"#CCCCBB"}
PROTANOPIA = {"bg":"#EFF5FF","fg":"#004080","muted":"#5577AA","border":"#99BBDD",
    "accent":"#CC7700","button":"#E7EDF5","buttonText":"#004080",
    "input":"#F7FBFF","inputText":"#004080","hover":"#DFE9F5","selection":"#CCDDFF"}
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

def is_follow_system_theme() -> bool:
    """Return True if the user wants Anki's native theme (no addon override)."""
    cfg = get_config()
    return cfg.get("followSystemTheme", False)

def set_follow_system_theme(enabled: bool):
    """Enable or disable follow-system-theme mode."""
    cfg = get_config()
    cfg["followSystemTheme"] = enabled
    write_config(cfg)
    if enabled:
        _restore_system_theme()
    else:
        apply_theme_everywhere(get_active_theme())

def _restore_system_theme():
    """Remove all addon styling and let Anki/OS control the theme."""
    # Clear application-level QSS
    app = QApplication.instance()
    if app:
        try:
            app.setStyleSheet("")
        except (RuntimeError, AttributeError):
            pass
    # Clear main window QSS
    try:
        mw.setStyleSheet("")
    except (RuntimeError, AttributeError):
        pass
    # Reset Anki's theme to follow system
    try:
        from aqt.theme import theme_manager
        theme_manager.night_mode = theme_manager.default_night_mode()
    except (ImportError, AttributeError):
        pass  # Leave night_mode as-is, Anki will fix on next theme change
    # Clear QSS from all open top-level widgets
    try:
        for widget in QApplication.instance().topLevelWidgets():
            try:
                if widget.isVisible():
                    widget.setStyleSheet("")
            except (RuntimeError, AttributeError):
                continue
    except (RuntimeError, AttributeError):
        pass
    # Refresh webviews to remove our injected CSS
    _remove_addon_css_from_webviews()

# ---------------- CSS / QSS ----------------
_STYLE_ID = "ankithemetwin-style"

def _remove_addon_css_from_webviews():
    """Remove our injected CSS from all open webviews (used when follow-system-theme is on)."""
    remove_js = (
        "(function(){"
        f"var el=document.getElementById('{_STYLE_ID}');"
        "if(el){el.remove();}"
        "})();"
    )
    for attr in ("web", "bottomWeb"):
        wv = getattr(mw, attr, None)
        if wv:
            try:
                wv.eval(remove_js)
            except (RuntimeError, AttributeError):
                pass
    app = QApplication.instance()
    if app:
        try:
            from aqt.qt import QWebEngineView
            for widget in app.topLevelWidgets():
                try:
                    for wv in widget.findChildren(QWebEngineView):
                        try:
                            wv.page().runJavaScript(remove_js)
                        except (RuntimeError, AttributeError):
                            pass
                except (RuntimeError, AttributeError):
                    pass
        except (ImportError, RuntimeError):
            pass

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

# ====== Feature 1: Pomodoro / Break Reminder ======
def get_pomodoro_settings() -> dict:
    """Get Pomodoro timer settings."""
    cfg = get_config()
    return cfg.get("pomodoroSettings", {
        "enabled": False,
        "studyMinutes": 25,
        "breakMinutes": 5,
        "autoStart": False,
    })

def save_pomodoro_settings(settings: dict):
    """Save Pomodoro timer settings."""
    cfg = get_config()
    cfg["pomodoroSettings"] = settings
    write_config(cfg)

def _start_pomodoro_timer():
    """Start (or restart) the Pomodoro study timer."""
    settings = get_pomodoro_settings()
    if not settings.get("enabled"):
        return
    study_ms = settings.get("studyMinutes", 25) * 60 * 1000
    if not hasattr(mw, "_ankitwin_pomodoro_timer"):
        mw._ankitwin_pomodoro_timer = QTimer(mw)
        mw._ankitwin_pomodoro_timer.setSingleShot(True)
        mw._ankitwin_pomodoro_timer.timeout.connect(_show_break_reminder)
    mw._ankitwin_pomodoro_timer.start(study_ms)
    mw._ankitwin_pomodoro_studying = True

def _stop_pomodoro_timer():
    """Stop the Pomodoro timer."""
    if hasattr(mw, "_ankitwin_pomodoro_timer"):
        mw._ankitwin_pomodoro_timer.stop()
    mw._ankitwin_pomodoro_studying = False

def _show_break_reminder():
    """Show a break reminder dialog."""
    settings = get_pomodoro_settings()
    break_min = settings.get("breakMinutes", 5)
    theme = get_active_theme()
    p = palette_for(theme)

    dlg = QDialog(mw)
    dlg.setWindowTitle("Break Time!")
    dlg.resize(400, 250)
    layout = QVBoxLayout(dlg)
    dlg.setStyleSheet(f"background:{p['bg']}; color:{p['fg']};")

    icon_lbl = QLabel("☕")
    icon_lbl.setStyleSheet("font-size:48px;")
    icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(icon_lbl)

    msg = QLabel(
        f"<div style='text-align:center;font-size:16px;'>"
        f"<b>Time for a {break_min}-minute break!</b><br><br>"
        f"Rest your eyes, stretch, and hydrate.<br>"
        f"Your study session will continue after.</div>"
    )
    msg.setWordWrap(True)
    layout.addWidget(msg)

    def end_break():
        dlg.accept()
        if settings.get("autoStart", False):
            _start_pomodoro_timer()
            tooltip("⏱️ Pomodoro: New study session started!", period=2000)

    btn = QPushButton(f"I'm Back! (Start Next Session)")
    btn.clicked.connect(end_break)
    layout.addWidget(btn)

    skip_btn = QPushButton("Skip (Don't Restart Timer)")
    skip_btn.clicked.connect(dlg.accept)
    layout.addWidget(skip_btn)

    dlg.exec()

# ====== Feature 2: Blue Light Filter ======
def get_blue_light_filter() -> int:
    """Get blue light filter intensity (0-100)."""
    cfg = get_config()
    return max(0, min(100, cfg.get("blueLightFilter", 0)))

def set_blue_light_filter(value: int):
    """Set blue light filter intensity (0-100)."""
    cfg = get_config()
    cfg["blueLightFilter"] = max(0, min(100, value))
    write_config(cfg)
    apply_theme_everywhere(get_active_theme())

def _get_blue_light_filter_css() -> str:
    """Generate CSS for the blue light filter overlay."""
    intensity = get_blue_light_filter()
    if intensity <= 0:
        return ""
    # Scale opacity from 0.0 to 0.35 based on 0-100 slider
    opacity = intensity / 100.0 * 0.35
    return (
        "#ankithemetwin-bluelight-overlay {"
        "  position:fixed; top:0; left:0; width:100%; height:100%;"
        f"  background:rgba(255, 180, 50, {opacity});"
        "  pointer-events:none; z-index:99999; mix-blend-mode:multiply;"
        "}"
    )

# ====== Feature 3: Theme Sync via collection.media ======
_SYNC_FILENAME = "_ankithemetwin_sync.json"

def get_sync_enabled() -> bool:
    """Check if theme sync is enabled."""
    cfg = get_config()
    return cfg.get("syncEnabled", False)

def _get_sync_file_path() -> Optional[str]:
    """Get path to sync file in collection.media."""
    try:
        media_dir = mw.col.media.dir()
        return os.path.join(media_dir, _SYNC_FILENAME)
    except (AttributeError, Exception):
        return None

def sync_config_to_media():
    """Write current config to collection.media for AnkiWeb sync."""
    if not get_sync_enabled():
        return
    path = _get_sync_file_path()
    if not path:
        return
    try:
        cfg = get_config()
        sync_data = {
            "version": VERSION,
            "synced_at": datetime.now().isoformat(),
            "configuration": cfg,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(sync_data, f, indent=2)
    except (OSError, IOError):
        pass

def sync_config_from_media():
    """Import config from collection.media if newer than current."""
    if not get_sync_enabled():
        return
    path = _get_sync_file_path()
    if not path or not os.path.exists(path):
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            sync_data = json.load(f)
        synced_cfg = sync_data.get("configuration", {})
        if synced_cfg:
            for key, value in synced_cfg.items():
                current_cfg = get_config()
                current_cfg[key] = value
                write_config(current_cfg)
            # Reload custom themes
            custom_themes = get_custom_themes()
            for name, palette in custom_themes.items():
                PALETTES[name] = palette
            tooltip("🔄 Settings synced from another device!", period=2000)
    except (OSError, IOError, json.JSONDecodeError):
        pass

# ====== Feature 4: Note-Type Specific Styling ======
def get_note_type_styles() -> dict:
    """Get per-note-type styling overrides."""
    cfg = get_config()
    return cfg.get("noteTypeStyles", {})

def set_note_type_style(note_type: str, styles: dict):
    """Set styling overrides for a specific note type."""
    cfg = get_config()
    nts = get_note_type_styles()
    nts[note_type] = styles
    cfg["noteTypeStyles"] = nts
    write_config(cfg)
    tooltip(f"Style for '{note_type}' saved!")

def delete_note_type_style(note_type: str):
    """Remove styling overrides for a note type."""
    cfg = get_config()
    nts = get_note_type_styles()
    if note_type in nts:
        del nts[note_type]
        cfg["noteTypeStyles"] = nts
        write_config(cfg)

def _get_note_type_css(note_type_name: str) -> str:
    """Generate CSS overrides for a specific note type."""
    styles = get_note_type_styles()
    if note_type_name not in styles:
        return ""
    s = styles[note_type_name]
    css = ""
    if "fontSize" in s:
        css += f".card {{ font-size:{s['fontSize']}px !important; }}"
    if "fontFamily" in s:
        css += f".card {{ font-family:{s['fontFamily']} !important; }}"
    if "lineHeight" in s:
        css += f".card {{ line-height:{s['lineHeight']} !important; }}"
    if "theme" in s and s["theme"] in PALETTES:
        p = PALETTES[s["theme"]]
        css += (
            f".card {{ background:{p['bg']} !important; color:{p['fg']} !important; }}"
        )
    return css

# ====== Feature 5: Zen Mode ======
def get_zen_mode() -> bool:
    """Get zen mode state."""
    cfg = get_config()
    return cfg.get("zenMode", False)

def toggle_zen_mode():
    """Toggle zen mode on/off."""
    cfg = get_config()
    new_state = not cfg.get("zenMode", False)
    cfg["zenMode"] = new_state
    write_config(cfg)
    apply_theme_everywhere(get_active_theme())
    if new_state:
        tooltip("🧘 Zen Mode enabled — distraction-free review", period=2000)
    else:
        tooltip("🧘 Zen Mode disabled", period=2000)

def _get_zen_mode_css() -> str:
    """CSS to hide UI elements for zen mode."""
    return (
        "/* Zen Mode: hide distracting elements */"
        "#header, .header, .toolbar, .deck-info, .deckname, nav,"
        "#studycount, #cardcount, .stat, .stattxt {"
        "  display:none !important;"
        "}"
        ".card, .card1, .card2, .card3 {"
        "  max-width:800px; margin:40px auto !important;"
        "  padding:40px !important; min-height:60vh;"
        "}"
        "#qa { max-width:800px; margin:0 auto; padding:20px; }"
        "body { display:flex; flex-direction:column;"
        "  justify-content:center; min-height:100vh; }"
    )

# ====== Feature 6: Theme Rotation ======
def get_rotation_settings() -> dict:
    """Get theme rotation settings."""
    cfg = get_config()
    return cfg.get("themeRotation", {
        "enabled": False,
        "themes": [],
        "intervalCards": 10,
        "intervalMinutes": 0,
    })

def save_rotation_settings(settings: dict):
    """Save theme rotation settings."""
    cfg = get_config()
    cfg["themeRotation"] = settings
    write_config(cfg)

def _check_theme_rotation():
    """Check if it's time to rotate the theme (card-based)."""
    settings = get_rotation_settings()
    if not settings.get("enabled") or not settings.get("themes"):
        return
    interval = settings.get("intervalCards", 10)
    if interval <= 0:
        return
    count = getattr(mw, "_ankitwin_rotation_count", 0) + 1
    mw._ankitwin_rotation_count = count
    if count >= interval:
        mw._ankitwin_rotation_count = 0
        themes = settings["themes"]
        # Filter to valid themes
        valid = [t for t in themes if t in PALETTES]
        if valid:
            current = get_active_theme()
            choices = [t for t in valid if t != current] or valid
            new_theme = random.choice(choices)
            set_theme(new_theme)
            tooltip(f"🔄 Theme rotated to {new_theme.replace('_', ' ').title()}", period=1500)

def _start_rotation_timer():
    """Start timer-based theme rotation if configured."""
    settings = get_rotation_settings()
    if not settings.get("enabled"):
        return
    minutes = settings.get("intervalMinutes", 0)
    if minutes <= 0:
        return
    if not hasattr(mw, "_ankitwin_rotation_timer"):
        mw._ankitwin_rotation_timer = QTimer(mw)
        mw._ankitwin_rotation_timer.timeout.connect(_rotate_theme_by_timer)
    mw._ankitwin_rotation_timer.start(minutes * 60 * 1000)

def _rotate_theme_by_timer():
    """Rotate theme on timer interval."""
    settings = get_rotation_settings()
    if not settings.get("enabled") or not settings.get("themes"):
        return
    valid = [t for t in settings["themes"] if t in PALETTES]
    if valid:
        current = get_active_theme()
        choices = [t for t in valid if t != current] or valid
        new_theme = random.choice(choices)
        set_theme(new_theme)
        tooltip(f"🔄 Theme rotated to {new_theme.replace('_', ' ').title()}", period=1500)

# ====== Feature 7: Custom CSS Injection ======
def get_custom_css() -> str:
    """Get user's custom CSS string."""
    cfg = get_config()
    return cfg.get("customCSS", "")

def set_custom_css(css: str):
    """Set user's custom CSS."""
    cfg = get_config()
    cfg["customCSS"] = css
    write_config(cfg)
    apply_theme_everywhere(get_active_theme())

# ====== Feature 9: Ambient Light Auto-Adjust ======
def get_ambient_light_settings() -> dict:
    """Get ambient light auto-adjust settings."""
    cfg = get_config()
    return cfg.get("ambientLightAuto", {
        "enabled": False,
        "minFilter": 0,
        "maxFilter": 60,
    })

def save_ambient_light_settings(settings: dict):
    """Save ambient light settings."""
    cfg = get_config()
    cfg["ambientLightAuto"] = settings
    write_config(cfg)

def _calculate_ambient_filter() -> int:
    """Calculate blue light filter based on time of day (solar position estimate).

    Returns a value 0-100 representing blue light filter intensity.
    Peaks at night (around midnight), lowest at midday.
    """
    settings = get_ambient_light_settings()
    if not settings.get("enabled"):
        return get_blue_light_filter()  # Return manual setting

    min_filter = settings.get("minFilter", 0)
    max_filter = settings.get("maxFilter", 60)

    now = datetime.now()
    # Hour as fraction (0-24)
    hour_frac = now.hour + now.minute / 60.0

    # Cosine curve: peaks at midnight (hour 0/24), valley at noon (hour 12)
    # cos(0) = 1 (midnight, max filter), cos(pi) = -1 (noon, min filter)
    radians = (hour_frac / 24.0) * 2 * math.pi
    factor = (math.cos(radians) + 1) / 2  # Normalized 0-1
    filter_value = int(min_filter + factor * (max_filter - min_filter))
    return max(0, min(100, filter_value))

def _apply_ambient_light():
    """Apply time-based blue light filter adjustment."""
    settings = get_ambient_light_settings()
    if not settings.get("enabled"):
        return
    new_filter = _calculate_ambient_filter()
    current = get_blue_light_filter()
    if abs(new_filter - current) >= 2:  # Only update if meaningful change
        cfg = get_config()
        cfg["blueLightFilter"] = new_filter
        write_config(cfg)
        refresh_all_webviews()

# ====== Feature 12: Match Card Background ======
def get_match_card_background() -> bool:
    """Check if match card background is enabled."""
    cfg = get_config()
    return cfg.get("matchCardBackground", False)

def toggle_match_card_background():
    """Toggle match card background feature."""
    cfg = get_config()
    new_state = not cfg.get("matchCardBackground", False)
    cfg["matchCardBackground"] = new_state
    write_config(cfg)
    apply_theme_everywhere(get_active_theme())
    tooltip(f"Match Card Background: {'enabled' if new_state else 'disabled'}")

# ====== Feature 13: Status Bar Indicator ======
def get_status_bar_enabled() -> bool:
    """Check if status bar indicator is enabled."""
    cfg = get_config()
    return cfg.get("statusBarIndicator", True)

def _update_status_bar():
    """Update the status bar with current theme info."""
    if not get_status_bar_enabled():
        return
    try:
        theme = get_active_theme()
        theme_name = theme.replace("_", " ").title()
        font_size = get_font_size()
        zen = " | 🧘 Zen" if get_zen_mode() else ""
        bl = get_blue_light_filter()
        bl_text = f" | 🔆 BL:{bl}%" if bl > 0 else ""
        msg = f"🎨 {theme_name} | {font_size}px{bl_text}{zen}"

        if not hasattr(mw, "_ankitwin_status_label"):
            mw._ankitwin_status_label = QLabel()
            mw.statusBar().addPermanentWidget(mw._ankitwin_status_label)
        mw._ankitwin_status_label.setText(msg)
        mw._ankitwin_status_label.setVisible(True)
    except (RuntimeError, AttributeError):
        pass

def _hide_status_bar():
    """Hide the status bar indicator."""
    if hasattr(mw, "_ankitwin_status_label"):
        try:
            mw._ankitwin_status_label.setVisible(False)
        except (RuntimeError, AttributeError):
            pass

# ====== Feature 15: Seasonal Themes ======
SEASONAL_THEMES = {
    "spring": {"months": [3, 4, 5], "theme": "olive_green", "label": "Spring (March-May)"},
    "summer": {"months": [6, 7, 8], "theme": "blue_light", "label": "Summer (June-August)"},
    "autumn": {"months": [9, 10, 11], "theme": "sepia_special", "label": "Autumn (September-November)"},
    "winter": {"months": [12, 1, 2], "theme": "gray_word", "label": "Winter (December-February)"},
}

def get_seasonal_themes_enabled() -> bool:
    """Check if seasonal themes are enabled."""
    cfg = get_config()
    return cfg.get("seasonalThemes", {}).get("enabled", False)

def _check_seasonal_theme():
    """Apply seasonal theme if enabled."""
    if not get_seasonal_themes_enabled():
        return
    cfg = get_config()
    seasonal_cfg = cfg.get("seasonalThemes", {})
    month = datetime.now().month
    for season, data in SEASONAL_THEMES.items():
        if month in data["months"]:
            # Use user-configured theme or fall back to default
            target = seasonal_cfg.get(season, data["theme"])
            if target not in PALETTES:
                target = data["theme"]
            current = get_active_theme()
            if current != target:
                cfg["currentTheme"] = target
                write_config(cfg)
                apply_theme_everywhere(target)
                tooltip(f"🌿 Seasonal theme: {data['label']}", period=2000)
            break

# ====== Feature 14: Community Theme Gallery (bundled themes) ======
COMMUNITY_THEMES = {
    "Solarized Light": {
        "bg": "#FDF6E3", "fg": "#657B83", "muted": "#93A1A1", "border": "#EEE8D5",
        "accent": "#268BD2", "button": "#EEE8D5", "buttonText": "#657B83",
        "input": "#FDF6E3", "inputText": "#657B83", "hover": "#EEE8D5", "selection": "#D6DBDF",
    },
    "Nord Light": {
        "bg": "#ECEFF4", "fg": "#2E3440", "muted": "#4C566A", "border": "#D8DEE9",
        "accent": "#5E81AC", "button": "#E5E9F0", "buttonText": "#2E3440",
        "input": "#ECEFF4", "inputText": "#2E3440", "hover": "#D8DEE9", "selection": "#C0C8D8",
    },
    "Rosé Pine Dawn": {
        "bg": "#FAF4ED", "fg": "#575279", "muted": "#9893A5", "border": "#DFDAD9",
        "accent": "#D7827E", "button": "#F2E9E1", "buttonText": "#575279",
        "input": "#FFFAF3", "inputText": "#575279", "hover": "#F2E9E1", "selection": "#DFDAD9",
    },
    "Gruvbox Light": {
        "bg": "#FBF1C7", "fg": "#3C3836", "muted": "#928374", "border": "#EBDBB2",
        "accent": "#D65D0E", "button": "#EBDBB2", "buttonText": "#3C3836",
        "input": "#FBF1C7", "inputText": "#3C3836", "hover": "#EBDBB2", "selection": "#D5C4A1",
    },
    "Catppuccin Latte": {
        "bg": "#EFF1F5", "fg": "#4C4F69", "muted": "#9CA0B0", "border": "#CCD0DA",
        "accent": "#1E66F5", "button": "#E6E9EF", "buttonText": "#4C4F69",
        "input": "#EFF1F5", "inputText": "#4C4F69", "hover": "#CCD0DA", "selection": "#BCC0CC",
    },
    "Tokyo Night Light": {
        "bg": "#D5D6DB", "fg": "#343B58", "muted": "#9699A3", "border": "#C0C1C8",
        "accent": "#34548A", "button": "#C8C9D0", "buttonText": "#343B58",
        "input": "#D5D6DB", "inputText": "#343B58", "hover": "#C0C1C8", "selection": "#B0B1BA",
    },
    "Everforest Light": {
        "bg": "#FDF6E3", "fg": "#5C6A72", "muted": "#829181", "border": "#E0DCC7",
        "accent": "#8DA101", "button": "#EFE8CF", "buttonText": "#5C6A72",
        "input": "#FDF6E3", "inputText": "#5C6A72", "hover": "#E0DCC7", "selection": "#D4CCAD",
    },
    "Dracula Light": {
        "bg": "#F8F8F2", "fg": "#282A36", "muted": "#6272A4", "border": "#E0E0E0",
        "accent": "#BD93F9", "button": "#E8E8E4", "buttonText": "#282A36",
        "input": "#F8F8F2", "inputText": "#282A36", "hover": "#E0E0E0", "selection": "#D0D0CE",
    },
}

def css_vars(p):
    """Generate comprehensive CSS for all webview contexts."""
    font_size = get_font_size()
    font_family = get_font_family()
    line_height = get_line_height()
    letter_spacing = get_letter_spacing()
    anim_settings = get_animation_settings()

    # Animation CSS based on settings
    transitions = ""
    if anim_settings.get("enabled", True):
        duration = anim_settings.get("duration", 300)
        style = anim_settings.get("style", "fade")
        if style == "fade":
            transitions = f"transition: all {duration}ms ease-in-out;"
        elif style == "slide":
            transitions = f"transition: all {duration}ms cubic-bezier(0.4, 0, 0.2, 1);"
        elif style == "morph":
            transitions = f"transition: all {duration}ms cubic-bezier(0.68, -0.55, 0.265, 1.55);"
        elif style == "zoom":
            transitions = f"transition: all {duration}ms cubic-bezier(0.175, 0.885, 0.32, 1.275);"
        else:
            transitions = f"transition: all {duration}ms ease-in-out;"

    # Blue light filter CSS
    blue_light_css = _get_blue_light_filter_css()

    # Custom user CSS
    user_css = get_custom_css()

    # Zen mode CSS
    zen_css = _get_zen_mode_css() if get_zen_mode() else ""

    # Card template helper variables (--att-* prefix)
    template_helper_css = (
        f"  --att-bg: {p['bg']};"
        f"  --att-fg: {p['fg']};"
        f"  --att-muted: {p['muted']};"
        f"  --att-border: {p['border']};"
        f"  --att-accent: {p['accent']};"
        f"  --att-button: {p['button']};"
        f"  --att-button-text: {p['buttonText']};"
        f"  --att-input: {p['input']};"
        f"  --att-input-text: {p['inputText']};"
        f"  --att-hover: {p['hover']};"
        f"  --att-selection: {p['selection']};"
        f"  --att-font-size: {font_size}px;"
        f"  --att-font-family: {font_family};"
        f"  --att-line-height: {line_height};"
        f"  --att-letter-spacing: {letter_spacing}px;"
    )

    return (
        # Override Anki's built-in CSS custom properties used by Svelte components
        # This ensures ThemeManager colors are replaced with our theme colors
        ":root {"
        f"  --canvas: {p['bg']} !important;"
        f"  --canvas-elevated: {p['input']} !important;"
        f"  --canvas-overlay: {p['bg']} !important;"
        f"  --canvas-inset: {p['input']} !important;"
        f"  --canvas-glass: {p['bg']}ee !important;"
        f"  --canvas-code: {p['input']} !important;"
        f"  --fg: {p['fg']} !important;"
        f"  --fg-subtle: {p['muted']} !important;"
        f"  --fg-disabled: {p['muted']} !important;"
        f"  --fg-faint: {p['border']} !important;"
        f"  --fg-link: {p['accent']} !important;"
        f"  --shadow: {p['border']} !important;"
        f"  --shadow-inset: {p['muted']} !important;"
        f"  --shadow-subtle: {p['hover']} !important;"
        f"  --shadow-focus: {p['accent']} !important;"
        f"  --border: {p['border']} !important;"
        f"  --border-subtle: {p['border']} !important;"
        f"  --border-strong: {p['muted']} !important;"
        f"  --border-focus: {p['accent']} !important;"
        f"  --button-bg: {p['button']} !important;"
        f"  --button-hover: {p['hover']} !important;"
        f"  --button-hover-border: {p['accent']} !important;"
        f"  --button-active: {p['selection']} !important;"
        f"  --button-disabled: {p['border']} !important;"
        f"  --button-gradient-start: {p['button']} !important;"
        f"  --button-gradient-end: {p['hover']} !important;"
        f"  --button-primary-bg: {p['accent']} !important;"
        f"  --button-primary-fg: {p['bg']} !important;"
        f"  --button-primary-gradient-start: {p['accent']} !important;"
        f"  --button-primary-gradient-end: {p['accent']} !important;"
        f"  --button-primary-disabled: {p['muted']} !important;"
        f"  --scrollbar-bg: {p['bg']} !important;"
        f"  --scrollbar-bg-hover: {p['hover']} !important;"
        f"  --scrollbar-bg-active: {p['selection']} !important;"
        f"  --accent-card: {p['accent']} !important;"
        f"  --accent-note: {p['accent']} !important;"
        f"  --accent-danger: #E74C3C !important;"
        f"  --badge-bg: {p['button']} !important;"
        f"  --badge-fg: {p['buttonText']} !important;"
        f"  --highlight-bg: {p['selection']} !important;"
        f"  --highlight-fg: {p['fg']} !important;"
        f"  --selected-bg: {p['selection']} !important;"
        f"  --selected-fg: {p['fg']} !important;"
        f"  --frame-bg: {p['input']} !important;"
        f"  --window-bg: {p['bg']} !important;"
        f"  --window-fg: {p['fg']} !important;"
        # Additional properties used by Anki's editor/browser Svelte components
        f"  --pane-bg: {p['bg']} !important;"
        f"  --surface-bg: {p['bg']} !important;"
        # Editor text color properties
        f"  --text-fg: {p['fg']} !important;"
        f"  --editor-fg: {p['inputText']} !important;"
        f"  --field-bg: {p['input']} !important;"
        f"  --flag-1: #E74C3C !important;"
        f"  --flag-2: #E67E22 !important;"
        f"  --flag-3: #2ECC71 !important;"
        f"  --flag-4: #3498DB !important;"
        f"  --flag-5: #FF69B4 !important;"
        f"  --flag-6: #40E0D0 !important;"
        f"  --flag-7: #9B59B6 !important;"
        # Card state colors used by Anki's browser table and deck views
        f"  --state-new: {p.get('stateNew', '#3B82F6')} !important;"
        f"  --state-learn: {p.get('stateLearn', '#DC2626')} !important;"
        f"  --state-review: {p.get('stateReview', '#16A34A')} !important;"
        f"  --state-buried: {p.get('stateBuried', '#D97706')} !important;"
        f"  --state-suspended: {p.get('stateSuspended', '#EAB308')} !important;"
        f"  --state-marked: {p.get('stateMarked', '#6366F1')} !important;"
        # Feature 8: Theme-aware card template helper variables
        + template_helper_css +
        "}"
        # Override nightMode/night_mode body classes that Anki applies in dark mode
        # This ensures our theme colors win even when OS is in dark mode
        f"body.nightMode, body.night_mode, .nightMode, .night_mode {{"
        f"  background:{p['bg']} !important; color:{p['fg']} !important;"
        "}}"
        f".nightMode .card, .night_mode .card {{"
        f"  background:{p['bg']} !important; color:{p['fg']} !important;"
        "}}"
        f".nightMode a, .night_mode a {{ color:{p['accent']} !important; }}"
        f".nightMode button, .night_mode button {{"
        f"  background:{p['button']} !important; color:{p['buttonText']} !important;"
        f"  border-color:{p['border']} !important;"
        "}}"
        f".nightMode input, .nightMode textarea, .nightMode select,"
        f".night_mode input, .night_mode textarea, .night_mode select {{"
        f"  background:{p['input']} !important; color:{p['inputText']} !important;"
        f"  border-color:{p['border']} !important;"
        "}}"
        f".nightMode table, .night_mode table {{ background:{p['bg']} !important; }}"
        f".nightMode th, .night_mode th {{ background:{p['button']} !important; color:{p['buttonText']} !important; }}"
        f".nightMode td, .night_mode td {{ color:{p['fg']} !important; border-color:{p['border']} !important; }}"
        f".nightMode tr:hover, .night_mode tr:hover {{ background:{p['hover']} !important; }}"
        f".nightMode .field, .night_mode .field {{"
        f"  background:{p['input']} !important; color:{p['inputText']} !important;"
        f"  border-color:{p['border']} !important;"
        "}}"
        f".nightMode [contenteditable], .night_mode [contenteditable] {{"
        f"  background:{p['input']} !important; color:{p['inputText']} !important;"
        "}}"
        # Base styles with smooth transitions
        "html, body {"
        f"  background:{p['bg']} !important; color:{p['fg']} !important;"
        f'  font-family:{font_family} !important;'
        f"  line-height:{line_height}; font-size:{font_size}px;"
        f"  letter-spacing:{letter_spacing}px;"
        "  -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility;"
        f"  {transitions}"
        "}"
        # All text elements
        f"p, span, div, li, label {{ color:{p['fg']} !important; }}"
        # Links and selection with transitions
        f"a {{ color:{p['accent']} !important; text-decoration:underline; {transitions} }}"
        f"a:hover {{ color:{p['hover']} !important; text-shadow:0 0 8px {p['accent']}44; }}"
        f"::selection {{ background:{p['selection']}; color:{p['fg']}; }}"
        # Buttons with enhanced visual effects
        f"button, .btn, input[type='button'], input[type='submit'] {{"
        f"  background:linear-gradient(180deg, {p['button']} 0%, {p['hover']} 100%) !important;"
        f"  color:{p['buttonText']} !important;"
        f"  border:1px solid {p['border']} !important; border-radius:6px;"
        f"  padding:6px 12px; cursor:pointer;"
        f"  box-shadow:0 2px 4px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06);"
        f"  {transitions}"
        "}"
        f"button:hover, .btn:hover {{"
        f"  background:linear-gradient(180deg, {p['hover']} 0%, {p['button']} 100%) !important;"
        f"  box-shadow:0 4px 8px rgba(0,0,0,0.15), 0 2px 4px rgba(0,0,0,0.1);"
        f"  transform:translateY(-1px);"
        "}}"
        f"button:active, .btn:active {{"
        f"  transform:translateY(1px);"
        f"  box-shadow:0 1px 2px rgba(0,0,0,0.1) inset;"
        "}}"
        # Input fields with enhanced focus effects
        f"input, textarea, select {{"
        f"  background:{p['input']} !important; color:{p['inputText']} !important;"
        f"  border:1px solid {p['border']} !important; border-radius:4px;"
        f"  padding:4px 8px;"
        f"  {transitions}"
        "}"
        f"input:focus, textarea:focus, select:focus {{"
        f"  border-color:{p['accent']} !important; outline:none;"
        f"  box-shadow:0 0 0 3px {p['accent']}33, 0 4px 6px rgba(0,0,0,0.1);"
        f"  transform:scale(1.01);"
        "}}"
        # Contenteditable divs (Anki editor fields) with enhanced styling
        f"[contenteditable='true'], [contenteditable='plaintext-only'] {{"
        f"  background:{p['input']} !important; color:{p['inputText']} !important;"
        f"  border:1px solid {p['border']} !important; border-radius:4px;"
        f"  padding:8px !important; min-height:60px !important;"
        f"  {transitions}"
        f"  box-shadow:0 1px 3px rgba(0,0,0,0.05);"
        "}"
        f"[contenteditable='true']:focus, [contenteditable='plaintext-only']:focus {{"
        f"  border-color:{p['accent']} !important; outline:none !important;"
        f"  box-shadow:0 0 0 3px {p['accent']}33, 0 4px 6px rgba(0,0,0,0.1) !important;"
        "}"
        # Checkboxes and radio buttons with transitions
        f"input[type='checkbox'], input[type='radio'] {{"
        f"  border:2px solid {p['border']} !important; background:{p['input']} !important;"
        f"  {transitions}"
        "}"
        # Card content (reviewer) with depth and animation
        f".card, .card1, .card2, .card3 {{"
        f"  background:{p['bg']} !important; color:{p['fg']} !important;"
        f"  border-radius:8px; padding:20px;"
        f"  box-shadow:0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.05);"
        f"  {transitions}"
        "}}"
        # Card fade-in animation
        "@keyframes cardFadeIn {"
        "  from { opacity:0; transform:translateY(10px); }"
        "  to { opacity:1; transform:translateY(0); }"
        "}"
        f".card {{ animation:cardFadeIn 0.3s ease-out; }}"
        # Editor fields with subtle shadow
        f".field {{"
        f"  background:{p['input']} !important; color:{p['inputText']} !important;"
        f"  border:1px solid {p['border']} !important;"
        f"  border-radius:4px; padding:8px;"
        f"  box-shadow:0 1px 3px rgba(0,0,0,0.05);"
        f"  {transitions}"
        "}}"
        # Tables with enhanced styling
        f"table {{ background:{p['bg']} !important; color:{p['fg']} !important; border-collapse:separate; border-spacing:0; }}"
        f"th {{ background:linear-gradient(180deg, {p['button']} 0%, {p['hover']} 100%) !important; color:{p['buttonText']} !important;"
        f"  border:1px solid {p['border']} !important; padding:8px; font-weight:600; }}"
        f"td {{ border:1px solid {p['border']} !important; padding:6px; color:{p['fg']} !important; {transitions} }}"
        f"tr:hover {{ background:{p['hover']} !important; box-shadow:0 2px 4px rgba(0,0,0,0.05); }}"
        f"tr.drag-hover {{ background:{p['selection']} !important; }}"
        # Lists
        f"ul, ol {{ color:{p['fg']} !important; }}"
        f"li {{ color:{p['fg']} !important; }}"
        # Code blocks with enhanced styling
        f"code, pre {{"
        f"  background:{p['input']} !important; color:{p['fg']} !important;"
        f"  border:1px solid {p['border']} !important; border-radius:4px;"
        f"  padding:2px 4px; font-family:monospace;"
        f"  box-shadow:0 1px 2px rgba(0,0,0,0.05);"
        "}"
        # Headings with subtle accents
        f"h1, h2, h3, h4, h5, h6 {{ color:{p['fg']} !important; font-weight:600; }}"
        f"h1 {{ border-bottom:2px solid {p['accent']}; padding-bottom:8px; }}"
        f"h2 {{ border-bottom:1px solid {p['border']}; padding-bottom:6px; }}"
        # Horizontal rules
        f"hr {{ border:0; height:2px; background:linear-gradient(90deg, transparent, {p['border']}, transparent); }}"
        # Scrollbars with enhanced styling
        f"::-webkit-scrollbar {{ width:12px; height:12px; }}"
        f"::-webkit-scrollbar-track {{ background:{p['bg']}; border-radius:6px; }}"
        f"::-webkit-scrollbar-thumb {{"
        f"  background:linear-gradient(180deg, {p['border']} 0%, {p['muted']} 100%);"
        f"  border-radius:6px; border:2px solid {p['bg']};"
        f"  {transitions}"
        "}}"
        f"::-webkit-scrollbar-thumb:hover {{"
        f"  background:linear-gradient(180deg, {p['muted']} 0%, {p['accent']} 100%);"
        f"  box-shadow:0 0 6px {p['accent']}33;"
        "}}"
        # Dropdown menus and autocomplete with animations
        f".autocomplete, .dropdown-menu {{"
        f"  background:{p['input']} !important; color:{p['inputText']} !important;"
        f"  border:1px solid {p['border']} !important;"
        f"  box-shadow:0 4px 12px rgba(0,0,0,0.15), 0 2px 4px rgba(0,0,0,0.1);"
        f"  border-radius:6px; overflow:hidden;"
        "}"
        f".autocomplete-item, .dropdown-item {{"
        f"  color:{p['fg']} !important; padding:8px 12px;"
        f"  {transitions}"
        "}"
        f".autocomplete-item:hover, .dropdown-item:hover {{"
        f"  background:{p['hover']} !important; color:{p['fg']} !important;"
        f"  padding-left:16px;"
        "}"
        f".autocomplete-item.selected, .dropdown-item.selected {{"
        f"  background:{p['selection']} !important; color:{p['fg']} !important;"
        f"  border-left:3px solid {p['accent']};"
        "}"
        # Modal dialogs with enhanced depth
        "@keyframes modalFadeIn {"
        "  from { opacity:0; transform:scale(0.95); }"
        "  to { opacity:1; transform:scale(1); }"
        "}"
        f".modal, .overlay {{"
        f"  background:{p['bg']} !important; color:{p['fg']} !important;"
        f"  border:1px solid {p['border']} !important; border-radius:8px;"
        f"  box-shadow:0 10px 25px rgba(0,0,0,0.2), 0 6px 12px rgba(0,0,0,0.15);"
        "  animation:modalFadeIn 0.2s ease-out;"
        "}"
        f".modal-header {{"
        f"  background:linear-gradient(180deg, {p['button']} 0%, {p['hover']} 100%) !important;"
        f"  color:{p['buttonText']} !important; border-bottom:1px solid {p['border']} !important;"
        f"  border-radius:8px 8px 0 0; padding:12px 16px;"
        "}}"
        f".modal-footer {{"
        f"  background:{p['button']} !important; border-top:1px solid {p['border']} !important;"
        f"  border-radius:0 0 8px 8px; padding:12px 16px;"
        "}}"
        # Additional animation keyframes (Feature 11)
        "@keyframes slideIn {"
        "  from { opacity:0; transform:translateX(-20px); }"
        "  to { opacity:1; transform:translateX(0); }"
        "}"
        "@keyframes zoomIn {"
        "  from { opacity:0; transform:scale(0.8); }"
        "  to { opacity:1; transform:scale(1); }"
        "}"
        "@keyframes morphIn {"
        "  0% { opacity:0; transform:scale(0.95) rotate(-1deg); }"
        "  50% { opacity:0.8; transform:scale(1.02) rotate(0.5deg); }"
        "  100% { opacity:1; transform:scale(1) rotate(0); }"
        "}"
        # Blue light filter overlay (Feature 2)
        + blue_light_css
        # Zen mode CSS (Feature 5)
        + zen_css
        # User custom CSS (Feature 7)
        + user_css
    )

def inject_css(web_content, ctx):
    """Inject CSS into webviews with context-specific enhancements."""
    if is_follow_system_theme():
        return
    theme = get_active_theme()
    p = palette_for(theme)

    # Base CSS for all contexts
    base_css = css_vars(p)

    # Add background pattern CSS if enabled
    pattern = get_background_pattern()
    pattern_css = get_pattern_css(p, pattern)

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
        /* Reviewer specific - override nightMode comprehensively */
        #qa {{ background:{p['bg']} !important; color:{p['fg']} !important; }}
        .nightMode .card, .night_mode .card {{ background:{p['bg']} !important; color:{p['fg']} !important; }}
        .nightMode #qa, .night_mode #qa {{ background:{p['bg']} !important; color:{p['fg']} !important; }}
        .nightMode #answer, .night_mode #answer {{ color:{p['fg']} !important; }}
        .nightMode .replay-button, .night_mode .replay-button {{ background:{p['button']} !important; border:1px solid {p['border']} !important; }}
        #answer {{ color:{p['fg']} !important; }}
        .replay-button {{ background:{p['button']} !important; border:1px solid {p['border']} !important; }}
        .typeGood {{ color:{p['accent']} !important; }}
        .typeBad {{ color:#E74C3C !important; }}
        .typeMissed {{ color:#F39C12 !important; }}
        /* Ensure all text in reviewer is visible */
        .nightMode p, .nightMode span, .nightMode div, .nightMode li,
        .night_mode p, .night_mode span, .night_mode div, .night_mode li {{
            color:{p['fg']} !important;
        }}
        /* Bottom bar answer buttons */
        .nightMode .stattxt, .night_mode .stattxt {{ color:{p['fg']} !important; }}
        """

    # Editor or AddCards - note editing
    elif "Editor" in ctx_name or "AddCards" in ctx_name or "NoteEditor" in ctx_name:
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
        /* Svelte NoteEditor component overrides */
        .editor-toolbar {{ background:{p['bg']} !important; border-bottom:1px solid {p['border']} !important; }}
        .editor-toolbar button {{ background:{p['button']} !important; color:{p['buttonText']} !important; border:1px solid {p['border']} !important; }}
        .editor-toolbar button:hover {{ background:{p['hover']} !important; }}
        .editor-toolbar button.active, .editor-toolbar button[class*="active"] {{ background:{p['accent']} !important; color:{p['bg']} !important; }}
        /* Field labels (Front, Back, etc.) */
        .label-name, .field-label, [class*="label"] {{ color:{p['muted']} !important; }}
        /* Collapsible field headers */
        .collapse-icon {{ color:{p['muted']} !important; }}
        .fields-collapse {{ background:{p['bg']} !important; }}
        /* Tag editor Svelte component */
        .tag-editor {{ background:{p['bg']} !important; border:1px solid {p['border']} !important; }}
        .tag-editor input {{ background:{p['input']} !important; color:{p['inputText']} !important; border:none !important; }}
        .tag-editor .tag-container {{ background:{p['bg']} !important; }}
        .tag-editor .tag-chip, .tag-pill {{ background:{p['button']} !important; color:{p['buttonText']} !important; border:1px solid {p['border']} !important; border-radius:3px; }}
        .tag-editor .tag-chip:hover, .tag-pill:hover {{ background:{p['hover']} !important; }}
        /* Note type / deck selector buttons in editor */
        .note-type-selector, .deck-selector {{ background:{p['button']} !important; color:{p['buttonText']} !important; border:1px solid {p['border']} !important; }}
        .note-type-selector:hover, .deck-selector:hover {{ background:{p['hover']} !important; }}
        /* Plain/rich text toggle and field expansion buttons */
        .plain-text-badge {{ background:{p['button']} !important; color:{p['muted']} !important; border:1px solid {p['border']} !important; }}
        .plain-text-badge:hover {{ background:{p['hover']} !important; }}
        /* Editor field containers */
        .editor-field {{ background:{p['input']} !important; border:1px solid {p['border']} !important; border-radius:4px; }}
        .editor-field:focus-within {{ border-color:{p['accent']} !important; box-shadow:0 0 0 3px {p['accent']}33 !important; }}
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
        /* Browser specific webview styling */
        .browser-table {{ background:{p['bg']} !important; }}
        .search {{ background:{p['input']} !important; color:{p['inputText']} !important; border:1px solid {p['border']} !important; }}
        .cell {{ color:{p['fg']} !important; }}
        .browserRow {{ background:{p['bg']} !important; }}
        .browserRow:hover {{ background:{p['hover']} !important; }}
        /* Browser sidebar webview elements */
        .sidebar {{ background:{p['bg']} !important; color:{p['fg']} !important; }}
        .sidebar-item {{ color:{p['fg']} !important; padding:4px 8px; }}
        .sidebar-item:hover {{ background:{p['hover']} !important; }}
        .sidebar-item.selected, .sidebar-item.highlighted {{ background:{p['selection']} !important; color:{p['fg']} !important; }}
        /* Browser toolbar */
        #searchEdit {{ background:{p['input']} !important; color:{p['inputText']} !important; border:1px solid {p['border']} !important; }}
        /* Card preview/details in browser right panel */
        #previewArea {{ background:{p['bg']} !important; color:{p['fg']} !important; }}
        /* Editor fields/labels on right side of browser */
        .fname {{ color:{p['muted']} !important; font-size:12px; }}
        .field {{ min-height:40px !important; background:{p['input']} !important; color:{p['inputText']} !important; }}
        .EditorField {{ background:{p['input']} !important; color:{p['inputText']} !important; }}
        .editor-field {{ background:{p['input']} !important; border:1px solid {p['border']} !important; border-radius:4px; color:{p['inputText']} !important; }}
        .editor-field:focus-within {{ border-color:{p['accent']} !important; }}
        .editor-toolbar {{ background:{p['bg']} !important; border-bottom:1px solid {p['border']} !important; }}
        .editor-toolbar button {{ background:{p['button']} !important; color:{p['buttonText']} !important; }}
        .editor-toolbar button:hover {{ background:{p['hover']} !important; }}
        .label-name, .field-label, [class*="label"] {{ color:{p['muted']} !important; }}
        .collapse-icon {{ color:{p['muted']} !important; }}
        .fields-collapse {{ background:{p['bg']} !important; }}
        /* Rich-text-input container (Anki's Svelte component) */
        .rich-text-input {{ background-color:{p['input']} !important; color:{p['inputText']} !important; }}
        .rich-text-editable {{ color:{p['inputText']} !important; }}
        /* Force ALL text inside editor fields to use theme color */
        .field *, .EditorField *, .editor-field *, .rich-text-input *, .rich-text-editable * {{ color:{p['inputText']} !important; }}
        /* Override content with inline style colors (from card templates) */
        .field *[style], .EditorField *[style], .editor-field *[style] {{ color:{p['inputText']} !important; }}
        .field font, .EditorField font, .editor-field font {{ color:{p['inputText']} !important; }}
        /* Tag editor in browser */
        .tag-editor {{ background:{p['bg']} !important; border:1px solid {p['border']} !important; }}
        .tag-editor input {{ background:{p['input']} !important; color:{p['inputText']} !important; border:none !important; }}
        .tag-editor .tag-chip, .tag-pill {{ background:{p['button']} !important; color:{p['buttonText']} !important; border:1px solid {p['border']} !important; border-radius:3px; }}
        .tag-editor .tag-chip:hover, .tag-pill:hover {{ background:{p['hover']} !important; }}
        /* Note type/deck selectors in browser editor */
        .note-type-selector, .deck-selector {{ background:{p['button']} !important; color:{p['buttonText']} !important; border:1px solid {p['border']} !important; }}
        .note-type-selector:hover, .deck-selector:hover {{ background:{p['hover']} !important; }}
        .plain-text-badge {{ background:{p['button']} !important; color:{p['muted']} !important; border:1px solid {p['border']} !important; }}
        .plain-text-badge:hover {{ background:{p['hover']} !important; }}
        /* Suspended and marked cards */
        .suspended {{ color:{p['muted']} !important; opacity:0.7; }}
        .marked {{ color:{p['accent']} !important; }}
        /* Column headers */
        th.browser-header {{ background:{p['button']} !important; color:{p['buttonText']} !important; border:1px solid {p['border']} !important; }}
        /* Filter bar */
        .filterBar {{ background:{p['bg']} !important; border:1px solid {p['border']} !important; padding:8px; }}
        /* Pane/panel backgrounds for card details */
        .pane {{ background:{p['bg']} !important; color:{p['fg']} !important; }}
        [class*="pane"] {{ background:{p['bg']} !important; color:{p['fg']} !important; }}
        /* Rich text buttons in browser editor */
        .richTextButton {{ background:{p['button']} !important; color:{p['buttonText']} !important; border:1px solid {p['border']} !important; }}
        .richTextButton:hover {{ background:{p['hover']} !important; }}
        .richTextButton.highlighted {{ background:{p['accent']} !important; color:{p['bg']} !important; }}
        /* Svelte component overrides */
        .tag {{ background:{p['button']} !important; color:{p['buttonText']} !important; }}
        .fieldButton {{ background:{p['button']} !important; color:{p['buttonText']} !important; border:1px solid {p['border']} !important; }}
        #notetype {{ background:{p['input']} !important; color:{p['inputText']} !important; border:1px solid {p['border']} !important; }}
        #deck {{ background:{p['input']} !important; color:{p['inputText']} !important; border:1px solid {p['border']} !important; }}
        """

    # Toolbar and bottom bars
    elif "Toolbar" in ctx_name or "BottomBar" in ctx_name:
        context_css += f"""
        /* Toolbar/BottomBar specific */
        .bottom {{ background:{p['bg']} !important; border-top:1px solid {p['border']} !important; }}
        """

    # Combine all CSS
    full_css = base_css + pattern_css + context_css

    # Inject into page
    web_content.head += f'<style id="{_STYLE_ID}">{full_css}</style>'

    # Feature 2: Blue light filter overlay element
    bl_intensity = get_blue_light_filter()
    if bl_intensity > 0:
        opacity = bl_intensity / 100.0 * 0.35
        web_content.body += (
            f'<div id="ankithemetwin-bluelight-overlay" style="'
            f'position:fixed;top:0;left:0;width:100%;height:100%;'
            f'background:rgba(255,180,50,{opacity});'
            f'pointer-events:none;z-index:99999;mix-blend-mode:multiply;'
            f'"></div>'
        )

    # Feature 12: Match card background JS (reviewer only)
    if get_match_card_background() and ("Reviewer" in ctx_name or "Review" in ctx_name):
        match_bg_js = (
            "<script>"
            "(function(){"
            "  function matchBg(){"
            "    var card=document.querySelector('.card,.card1,.card2,.card3');"
            "    if(!card)return;"
            "    var cs=window.getComputedStyle(card);"
            "    var bg=cs.backgroundColor;"
            "    if(bg && bg!=='rgba(0, 0, 0, 0)'){"
            "      document.body.style.backgroundColor=bg;"
            "    }"
            "  }"
            "  setTimeout(matchBg,200);"
            "  setTimeout(matchBg,800);"
            "  var obs=new MutationObserver(function(){setTimeout(matchBg,100);});"
            "  obs.observe(document.body||document.documentElement,{childList:true,subtree:true});"
            "})();"
            "</script>"
        )
        web_content.head += match_bg_js

    # For Editor/AddCards/Browser contexts, inject JavaScript to style Shadow DOM elements
    # (Browser has an editor panel on the right side with shadow DOM fields)
    if "Editor" in ctx_name or "AddCards" in ctx_name or "Browser" in ctx_name or "NoteEditor" in ctx_name:
        shadow_css_content = (
            f":host {{ background:{p['input']} !important; "
            f"color:{p['inputText']} !important; "
            f"font-family:{get_font_family()} !important; "
            f"font-size:{get_font_size()}px !important; "
            f"line-height:{get_line_height()} !important; "
            f"letter-spacing:{get_letter_spacing()}px !important; "
            f"caret-color:{p['fg']} !important; "
            f"padding:8px !important; }} "
            # Force color on all elements, including inline-styled content
            f"*, *[style] {{ color:{p['inputText']} !important; }} "
            # Override Anki's own anki-editable rule (RichTextStyles sets color:white in dark mode)
            f"anki-editable {{ color:{p['inputText']} !important; background:{p['input']} !important; }} "
            f"::selection {{ background:{p['selection']} !important; color:{p['fg']} !important; }} "
            # Override legacy font tags and inline color spans from card content
            f"font, font[color] {{ color:{p['inputText']} !important; }} "
            f"span[style*='color'] {{ color:{p['inputText']} !important; }}"
        )
        shadow_css_json = json.dumps(shadow_css_content)
        input_text_json = json.dumps(p['inputText'])
        input_bg_json = json.dumps(p['input'])
        shadow_js = (
            "<script>"
            "(function(){"
            "  function styleShadowRoots(){"
            "    document.querySelectorAll('anki-editable').forEach(function(el){"
            "      if(el.shadowRoot){"
            "        var sid='ankithemetwin-shadow';"
            "        var existing=el.shadowRoot.getElementById(sid);"
            "        if(existing){existing.remove();}"
            "        var s=document.createElement('style');"
            "        s.id=sid;"
            f"        s.textContent={shadow_css_json};"
            "        el.shadowRoot.appendChild(s);"
            # Also patch Anki's own CSSStyleRules that target anki-editable
            "        try{"
            "          var sheets=el.shadowRoot.styleSheets||[];"
            "          for(var i=0;i<sheets.length;i++){"
            "            try{"
            "              var rules=sheets[i].cssRules||[];"
            "              for(var j=0;j<rules.length;j++){"
            "                if(rules[j].selectorText&&rules[j].selectorText.indexOf('anki-editable')>=0){"
            f"                  rules[j].style.color={input_text_json};"
            f"                  rules[j].style.background={input_bg_json};"
            "                }"
            "              }"
            "            }catch(e2){}"
            "          }"
            "        }catch(e1){}"
            "      }"
            "    });"
            "  }"
            "  /* Run after DOM is ready and observe for dynamically added fields */"
            "  if(document.readyState==='complete'){"
            "    setTimeout(styleShadowRoots,100);"
            "    setTimeout(styleShadowRoots,500);"
            "    setTimeout(styleShadowRoots,1000);"
            "  }else{"
            "    window.addEventListener('load',function(){"
            "      setTimeout(styleShadowRoots,100);"
            "      setTimeout(styleShadowRoots,500);"
            "      setTimeout(styleShadowRoots,1000);"
            "    });"
            "  }"
            "  var obs=new MutationObserver(function(){setTimeout(styleShadowRoots,50);});"
            "  obs.observe(document.body||document.documentElement,{childList:true,subtree:true});"
            "})();"
            "</script>"
        )
        web_content.head += shadow_js

def qss(p):
    """Generate comprehensive Qt Style Sheets for all Qt widgets."""
    return f"""
    /* Main widget styling */
    QWidget {{
        background:{p['bg']};
        color:{p['fg']};
        font-size:14px;
    }}

    /* Main window and stacked layouts */
    QMainWindow, QStackedWidget, QStackedLayout {{
        background:{p['bg']};
        color:{p['fg']};
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
    QTableView::item, QListView::item, QTreeView::item {{
        color:{p['fg']};
        padding:4px 2px;
    }}
    QTableView::item:hover, QListView::item:hover, QTreeView::item:hover {{
        background:{p['hover']};
    }}
    QTableView::item:selected, QListView::item:selected, QTreeView::item:selected {{
        background:{p['selection']};
        color:{p['fg']};
    }}
    /* QTreeView branch indicators for sidebar tree */
    QTreeView::branch {{
        background:{p['bg']};
    }}
    QTreeView::branch:hover {{
        background:{p['hover']};
    }}
    QTreeView::branch:selected {{
        background:{p['selection']};
    }}
    QTreeView::branch:has-children:!has-siblings:closed,
    QTreeView::branch:closed:has-children:has-siblings {{
        border-image:none;
        image:none;
    }}
    QTreeView::branch:open:has-children:!has-siblings,
    QTreeView::branch:open:has-children:has-siblings {{
        border-image:none;
        image:none;
    }}
    QHeaderView::section {{
        background:{p['button']};
        color:{p['buttonText']};
        border:1px solid {p['border']};
        padding:6px;
        font-weight:bold;
    }}
    QHeaderView::section:hover {{
        background:{p['hover']};
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

    /* Frames — critical for AddCards/EditCurrent toolbar areas */
    QFrame {{
        background:{p['bg']};
        color:{p['fg']};
    }}

    /* Labels */
    QLabel {{
        color:{p['fg']};
        background:transparent;
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

def _build_qt_palette(p: dict) -> QPalette:
    """Build a QPalette from our theme colors to override the OS/Qt dark palette.

    Sets colors for ALL color groups (Active, Inactive, Disabled) to ensure
    the OS theme cannot override any state of our widgets.
    """
    pal = QPalette()

    # Define all color role mappings
    color_map = {
        QPalette.ColorRole.Window: QColor(p['bg']),
        QPalette.ColorRole.WindowText: QColor(p['fg']),
        QPalette.ColorRole.Base: QColor(p['input']),
        QPalette.ColorRole.AlternateBase: QColor(p['bg']),
        QPalette.ColorRole.ToolTipBase: QColor(p['button']),
        QPalette.ColorRole.ToolTipText: QColor(p['buttonText']),
        QPalette.ColorRole.Text: QColor(p['inputText']),
        QPalette.ColorRole.Button: QColor(p['button']),
        QPalette.ColorRole.ButtonText: QColor(p['buttonText']),
        QPalette.ColorRole.BrightText: QColor(p['accent']),
        QPalette.ColorRole.Link: QColor(p['accent']),
        QPalette.ColorRole.Highlight: QColor(p['selection']),
        QPalette.ColorRole.HighlightedText: QColor(p['fg']),
        QPalette.ColorRole.PlaceholderText: QColor(p['muted']),
        QPalette.ColorRole.Light: QColor(p['hover']),
        QPalette.ColorRole.Midlight: QColor(p['border']),
        QPalette.ColorRole.Mid: QColor(p['muted']),
        QPalette.ColorRole.Dark: QColor(p['muted']),
        QPalette.ColorRole.Shadow: QColor(p['border']),
    }

    # Apply to all color groups so OS theme can't override any state
    groups = [
        QPalette.ColorGroup.Active,
        QPalette.ColorGroup.Inactive,
        QPalette.ColorGroup.Disabled,
    ]
    for group in groups:
        for role, color in color_map.items():
            if group == QPalette.ColorGroup.Disabled:
                # Use muted colors for disabled state
                if role in (QPalette.ColorRole.WindowText, QPalette.ColorRole.Text,
                            QPalette.ColorRole.ButtonText):
                    pal.setColor(group, role, QColor(p['muted']))
                else:
                    pal.setColor(group, role, color)
            else:
                pal.setColor(group, role, color)

    return pal

def force_anki_theme_mode(theme: Theme):
    """Force Anki's ThemeManager to use the correct mode for our theme.

    When Windows switches between dark/light mode, Anki's ThemeManager detects
    this and overrides our colors. We must force night_mode to match our theme
    and override the Qt application palette to prevent OS theme from bleeding in.
    """
    p = palette_for(theme)

    # Determine if our theme is dark or light based on background luminance
    bg = p['bg']
    # Parse hex color to get luminance
    r, g, b = int(bg[1:3], 16), int(bg[3:5], 16), int(bg[5:7], 16)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    is_dark_theme = luminance < 0.5

    # Force Anki's ThemeManager night_mode to match our theme
    try:
        from aqt.theme import theme_manager
        theme_manager.night_mode = is_dark_theme
        # Also try to set the default palette on theme_manager if it has one,
        # preventing Anki from using its own calculated palette
        if hasattr(theme_manager, '_default_palette'):
            theme_manager._default_palette = _build_qt_palette(p)
    except (ImportError, AttributeError):
        pass

    # Force Qt application palette to use our colors
    app = QApplication.instance()
    if app:
        try:
            app.setPalette(_build_qt_palette(p))
        except (RuntimeError, AttributeError):
            pass

def on_theme_did_change():
    """Called when Anki's theme changes (e.g. OS dark/light switch).

    Re-assert our addon theme to prevent Anki's ThemeManager from
    overriding our colors when the OS theme changes.

    Uses delayed re-assertions because Anki continues to reload webviews
    and re-apply its own styles AFTER this hook fires.
    """
    if is_follow_system_theme():
        return
    # Guard against recursive calls
    if getattr(mw, "_ankitwin_theme_changing", False):
        return
    mw._ankitwin_theme_changing = True

    def _reapply_theme():
        """Re-assert our theme over Anki's."""
        try:
            apply_theme_everywhere(get_active_theme())
        except (RuntimeError, AttributeError):
            pass

    try:
        # Immediate re-assertion
        _reapply_theme()

        # Delayed re-assertions to catch Anki's own reloads that happen
        # AFTER theme_did_change fires. Anki reloads webviews, re-applies
        # its QPalette, and resets its QSS at various points after the hook.
        from aqt.qt import QTimer
        QTimer.singleShot(200, _reapply_theme)
        QTimer.singleShot(800, _reapply_theme)
        QTimer.singleShot(1500, _reapply_theme)
    finally:
        # Reset guard after all re-assertions have had time to complete
        from aqt.qt import QTimer
        QTimer.singleShot(2000, lambda: setattr(mw, "_ankitwin_theme_changing", False))

# ---------------- Browser-specific Qt widget theming ----------------
def _style_qt_children(parent_widget, p: dict):
    """Apply QSS directly to individual child widgets.

    Qt6 does NOT reliably cascade parent QSS to children when Anki's own
    ThemeManager applies styles after our hook. The only reliable way is
    to find each child widget and set its stylesheet directly.
    """
    from aqt.qt import QTreeView, QTableView, QHeaderView

    # Style all QTreeView widgets (sidebar)
    tree_qss = f"""
    QTreeView {{
        background:{p['bg']};
        color:{p['fg']};
        border:1px solid {p['border']};
        selection-background-color:{p['selection']};
        selection-color:{p['fg']};
        outline:none;
    }}
    QTreeView::item {{
        color:{p['fg']};
        padding:4px 2px;
    }}
    QTreeView::item:hover {{
        background:{p['hover']};
        color:{p['fg']};
    }}
    QTreeView::item:selected {{
        background:{p['selection']};
        color:{p['fg']};
    }}
    QTreeView::branch {{
        background:{p['bg']};
    }}
    QTreeView::branch:hover {{
        background:{p['hover']};
    }}
    QTreeView::branch:selected {{
        background:{p['selection']};
    }}
    """
    for w in parent_widget.findChildren(QTreeView):
        try:
            w.setStyleSheet(tree_qss)
            # Also force palette on the widget for Qt6 robustness
            pal = w.palette()
            pal.setColor(QPalette.ColorRole.Base, QColor(p['bg']))
            pal.setColor(QPalette.ColorRole.Text, QColor(p['fg']))
            pal.setColor(QPalette.ColorRole.Window, QColor(p['bg']))
            pal.setColor(QPalette.ColorRole.WindowText, QColor(p['fg']))
            pal.setColor(QPalette.ColorRole.Highlight, QColor(p['selection']))
            pal.setColor(QPalette.ColorRole.HighlightedText, QColor(p['fg']))
            pal.setColor(QPalette.ColorRole.AlternateBase, QColor(p['input']))
            w.setPalette(pal)
        except (RuntimeError, AttributeError):
            pass

    # Style all QTableView widgets (card list)
    table_qss = f"""
    QTableView {{
        background:{p['bg']};
        color:{p['fg']};
        alternate-background-color:{p['input']};
        gridline-color:{p['border']};
        border:1px solid {p['border']};
        selection-background-color:{p['selection']};
        selection-color:{p['fg']};
    }}
    QTableView::item {{
        color:{p['fg']};
        padding:4px 2px;
    }}
    QTableView::item:hover {{
        background:{p['hover']};
        color:{p['fg']};
    }}
    QTableView::item:selected {{
        background:{p['selection']};
        color:{p['fg']};
    }}
    """
    for w in parent_widget.findChildren(QTableView):
        try:
            w.setStyleSheet(table_qss)
            pal = w.palette()
            pal.setColor(QPalette.ColorRole.Base, QColor(p['bg']))
            pal.setColor(QPalette.ColorRole.Text, QColor(p['fg']))
            pal.setColor(QPalette.ColorRole.AlternateBase, QColor(p['input']))
            pal.setColor(QPalette.ColorRole.Highlight, QColor(p['selection']))
            pal.setColor(QPalette.ColorRole.HighlightedText, QColor(p['fg']))
            w.setPalette(pal)
            w.setAlternatingRowColors(True)
        except (RuntimeError, AttributeError):
            pass

    # Style all QHeaderView sections (column headers)
    header_qss = f"""
    QHeaderView::section {{
        background:{p['button']};
        color:{p['buttonText']};
        border:1px solid {p['border']};
        padding:6px;
        font-weight:bold;
    }}
    QHeaderView::section:hover {{
        background:{p['hover']};
    }}
    """
    for w in parent_widget.findChildren(QHeaderView):
        try:
            w.setStyleSheet(header_qss)
        except (RuntimeError, AttributeError):
            pass

    # Style all QLineEdit (filter bar, search bar)
    line_edit_qss = f"""
    QLineEdit {{
        background:{p['input']};
        color:{p['inputText']};
        border:1px solid {p['border']};
        border-radius:3px;
        padding:4px 8px;
        selection-background-color:{p['selection']};
        selection-color:{p['fg']};
    }}
    QLineEdit:focus {{
        border:2px solid {p['accent']};
    }}
    """
    for w in parent_widget.findChildren(QLineEdit):
        try:
            w.setStyleSheet(line_edit_qss)
        except (RuntimeError, AttributeError):
            pass

    # Style all QPushButton
    button_qss = f"""
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
    """
    for w in parent_widget.findChildren(QPushButton):
        try:
            w.setStyleSheet(button_qss)
        except (RuntimeError, AttributeError):
            pass

    # Style all QComboBox
    combo_qss = f"""
    QComboBox {{
        background:{p['input']};
        color:{p['inputText']};
        border:1px solid {p['border']};
        border-radius:3px;
        padding:4px 8px;
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
    """
    for w in parent_widget.findChildren(QComboBox):
        try:
            w.setStyleSheet(combo_qss)
        except (RuntimeError, AttributeError):
            pass

    # Style all QLabel (make text visible)
    for w in parent_widget.findChildren(QLabel):
        try:
            w.setStyleSheet(f"QLabel {{ color:{p['fg']}; background:transparent; }}")
        except (RuntimeError, AttributeError):
            pass

    # Style all QFrame (containers)
    for w in parent_widget.findChildren(QFrame):
        try:
            # Skip webview containers — only style plain QFrame/QWidget instances.
            # Check the exact type to avoid styling QWebEngineView or its wrappers.
            cls = type(w)
            if cls is QFrame or cls is QWidget:
                w.setStyleSheet(f"background:{p['bg']}; color:{p['fg']};")
        except (RuntimeError, AttributeError):
            pass

    # Style all QCheckBox
    for w in parent_widget.findChildren(QCheckBox):
        try:
            w.setStyleSheet(f"""
            QCheckBox {{ color:{p['fg']}; spacing:8px; }}
            QCheckBox::indicator {{ width:18px; height:18px; border:1px solid {p['border']}; background:{p['input']}; }}
            QCheckBox::indicator:checked {{ background:{p['accent']}; border-color:{p['accent']}; }}
            """)
        except (RuntimeError, AttributeError):
            pass


def on_browser_will_show(browser):
    """Apply targeted QSS to Browser window's Qt widgets (sidebar, table, filter).

    Uses two strategies for Qt6 reliability:
    1. Set QSS on the parent Browser window (cascading)
    2. Find and style each child widget DIRECTLY (overrides Anki's own styles)
    """
    if is_follow_system_theme():
        return
    theme = get_active_theme()
    p = palette_for(theme)

    # Strategy 1: Parent-level QSS for general styling and any widgets
    # not caught by direct child styling
    browser_qss = f"""
    /* Splitter between sidebar and table */
    QSplitter::handle {{
        background:{p['border']};
    }}
    QSplitter::handle:hover {{
        background:{p['muted']};
    }}
    /* Search bar area */
    QToolBar {{
        background:{p['bg']};
        border:1px solid {p['border']};
    }}
    QToolBar > QWidget {{
        background:{p['bg']};
        color:{p['fg']};
    }}
    QMenuBar {{
        background:{p['bg']};
        color:{p['fg']};
    }}
    QMenuBar::item:selected {{
        background:{p['hover']};
    }}
    QStatusBar {{
        background:{p['bg']};
        color:{p['muted']};
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
    /* Tab bar */
    QTabBar::tab {{
        background:{p['button']};
        color:{p['buttonText']};
        border:1px solid {p['border']};
        padding:6px 12px;
    }}
    QTabBar::tab:selected {{
        background:{p['bg']};
        border-bottom-color:{p['bg']};
    }}
    QTabBar::tab:hover {{
        background:{p['hover']};
    }}
    """

    try:
        browser.setStyleSheet(browser_qss)
    except (RuntimeError, AttributeError):
        pass

    # Strategy 2: Direct child widget styling (most reliable in Qt6)
    _style_qt_children(browser, p)

# ---------------- Shadow DOM refresh for editor ----------------
def _build_shadow_dom_js(theme: Theme) -> str:
    """Build JavaScript to inject styles into Shadow DOM elements (anki-editable).

    Anki's RichTextStyles.svelte sets color on anki-editable via a CSSStyleRule
    inserted into the shadow DOM's adopted stylesheets. When Windows is in dark mode,
    Anki sets color:"white" even if our addon forces night_mode=False, because the
    Svelte component may have already rendered. We override this by:
    1. Injecting a <style> with !important rules into each shadowRoot
    2. Also patching any existing CSSStyleRules that target anki-editable
    3. Re-running on a MutationObserver so dynamically added fields get styled
    """
    p = palette_for(theme)
    font_family = get_font_family()
    font_size = get_font_size()
    line_height = get_line_height()
    letter_spacing = get_letter_spacing()

    shadow_css = (
        f"background:{p['input']} !important;"
        f"color:{p['inputText']} !important;"
        f"font-family:{font_family} !important;"
        f"font-size:{font_size}px !important;"
        f"line-height:{line_height} !important;"
        f"letter-spacing:{letter_spacing}px !important;"
        f"caret-color:{p['fg']} !important;"
        f"padding:8px !important;"
    )
    inner_css = (
        # Force color on all elements inside shadow DOM, including inline-styled content
        f"*, *[style] {{ color:{p['inputText']} !important; }}"
        # Override Anki's own anki-editable rule that sets color:white in dark mode
        f"anki-editable {{ color:{p['inputText']} !important; background:{p['input']} !important; }}"
        f"::selection {{ background:{p['selection']} !important; color:{p['fg']} !important; }}"
        # Override any font tags or spans with inline color styles
        f"font, font[color] {{ color:{p['inputText']} !important; }}"
        f"span[style*='color'] {{ color:{p['inputText']} !important; }}"
    )

    shadow_css_json = json.dumps(f":host {{ {shadow_css} }} {inner_css}")

    return (
        "(function(){"
        "  function styleShadowRoots(){"
        "    document.querySelectorAll('anki-editable').forEach(function(el){"
        "      if(el.shadowRoot){"
        "        var sid='ankithemetwin-shadow';"
        "        var existing=el.shadowRoot.getElementById(sid);"
        "        if(existing){existing.remove();}"
        "        var s=document.createElement('style');"
        "        s.id=sid;"
        f"        s.textContent={shadow_css_json};"
        "        el.shadowRoot.appendChild(s);"
        # Also patch Anki's own CSSStyleRules that target anki-editable
        # Anki's RichTextStyles.svelte inserts rules like "anki-editable { color: white; }"
        "        try{"
        "          var sheets=el.shadowRoot.styleSheets||[];"
        "          for(var i=0;i<sheets.length;i++){"
        "            try{"
        "              var rules=sheets[i].cssRules||[];"
        "              for(var j=0;j<rules.length;j++){"
        "                if(rules[j].selectorText&&rules[j].selectorText.indexOf('anki-editable')>=0){"
        f"                  rules[j].style.color={json.dumps(p['inputText'])};"
        f"                  rules[j].style.background={json.dumps(p['input'])};"
        "                }"
        "              }"
        "            }catch(e2){}"
        "          }"
        "        }catch(e1){}"
        "      }"
        "    });"
        "  }"
        "  styleShadowRoots();"
        # Also set up observer for dynamically added fields
        "  if(!window._ankitwin_shadow_obs){"
        "    window._ankitwin_shadow_obs=new MutationObserver(function(){setTimeout(styleShadowRoots,50);});"
        "    window._ankitwin_shadow_obs.observe(document.body||document.documentElement,{childList:true,subtree:true});"
        "  }"
        "})();"
    )

def on_editor_did_load_note(editor):
    """Inject shadow DOM styles when editor loads a note.

    Uses multiple delayed injections because:
    1. Anki's Svelte RichTextStyles component may set color AFTER our initial injection
    2. The field rendering is async — fields may not have shadowRoot immediately
    3. Anki may re-apply its own color rules after the note loads
    """
    if is_follow_system_theme():
        return
    theme = get_active_theme()
    js = _build_shadow_dom_js(theme)
    try:
        # Multiple delays to catch Anki's async field rendering
        # 100ms: initial attempt (fields may not be ready)
        # 300ms: after Svelte components mount
        # 600ms: after Anki's RichTextStyles applies its color rule
        # 1200ms: final catch-all for slow renders
        editor.web.eval(f"setTimeout(function(){{{js}}}, 100);")
        editor.web.eval(f"setTimeout(function(){{{js}}}, 300);")
        editor.web.eval(f"setTimeout(function(){{{js}}}, 600);")
        editor.web.eval(f"setTimeout(function(){{{js}}}, 1200);")
    except (RuntimeError, AttributeError):
        pass

# ---------------- Instant refresh ----------------
def _build_refresh_js(theme: Theme) -> str:
    """Build JavaScript to refresh CSS in webviews safely using JSON escaping."""
    import json
    p = palette_for(theme)
    css = css_vars(p)
    # Include background pattern CSS so pattern changes apply instantly
    pattern = get_background_pattern()
    pattern_css = get_pattern_css(p, pattern)
    full_css = css + pattern_css
    # Use JSON encoding for safe JavaScript string escaping
    css_json = json.dumps(full_css)
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
    """Push updated CSS into every open webview instantly.

    Covers: main window webviews, Browser, AddCards, EditCurrent,
    Stats, and any other open dialog with webviews or editors.
    """
    if is_follow_system_theme():
        return
    theme = get_active_theme()
    p = palette_for(theme)
    js = _build_refresh_js(theme)
    shadow_js = _build_shadow_dom_js(theme)

    # 1. Main window webviews (deck browser, reviewer, toolbar, bottom bar)
    for attr in ("web", "bottomWeb"):
        wv = getattr(mw, attr, None)
        if wv:
            try:
                wv.eval(js)
            except (RuntimeError, AttributeError):
                pass

    # 2. If reviewer is active, also refresh its webview explicitly
    reviewer = getattr(mw, "reviewer", None)
    if reviewer:
        wv = getattr(reviewer, "web", None)
        if wv:
            try:
                wv.eval(js)
            except (RuntimeError, AttributeError):
                pass
        bottom = getattr(reviewer, "bottom", None)
        if bottom:
            bwv = getattr(bottom, "web", None)
            if bwv:
                try:
                    bwv.eval(js)
                except (RuntimeError, AttributeError):
                    pass

    # 3. Scan ALL open top-level widgets for webviews and editors
    app = QApplication.instance()
    if not app:
        return

    try:
        from aqt.browser.browser import Browser
    except ImportError:
        Browser = None

    for widget in app.topLevelWidgets():
        try:
            if not widget.isVisible():
                continue
        except (RuntimeError, AttributeError):
            continue

        # Browser windows get special treatment — use targeted browser QSS only
        # (do NOT apply the full qss() which has a blanket QWidget rule that
        # conflicts with webview components and loses font/label colors)
        if Browser and isinstance(widget, Browser):
            on_browser_will_show(widget)
            if hasattr(widget, 'editor') and widget.editor and hasattr(widget.editor, 'web'):
                try:
                    widget.editor.web.eval(js)
                    # Multiple delayed injections to catch Anki's async Svelte rendering
                    # Anki's RichTextStyles.svelte sets color:white AFTER initial load in dark mode
                    widget.editor.web.eval(f"setTimeout(function(){{{shadow_js}}}, 100);")
                    widget.editor.web.eval(f"setTimeout(function(){{{shadow_js}}}, 400);")
                    widget.editor.web.eval(f"setTimeout(function(){{{shadow_js}}}, 800);")
                except (RuntimeError, AttributeError):
                    pass
            # Also refresh any other webviews inside the browser (e.g. card preview)
            try:
                from aqt.qt import QWebEngineView
                for wv in widget.findChildren(QWebEngineView):
                    try:
                        wv.page().runJavaScript(js)
                        # Also inject shadow DOM styles into all browser webviews
                        wv.page().runJavaScript(f"setTimeout(function(){{{shadow_js}}}, 100);")
                        wv.page().runJavaScript(f"setTimeout(function(){{{shadow_js}}}, 400);")
                        wv.page().runJavaScript(f"setTimeout(function(){{{shadow_js}}}, 800);")
                    except (RuntimeError, AttributeError):
                        pass
            except (ImportError, RuntimeError, AttributeError):
                pass
            continue

        # Re-apply QSS to every visible non-Browser top-level window
        try:
            widget.setStyleSheet(qss(p))
        except (RuntimeError, AttributeError):
            pass

        # Also style child widgets directly for Qt6 reliability
        # (ensures AddCards, EditCurrent, etc. have styled buttons/inputs)
        _style_qt_children(widget, p)

        # Find any webview (QWebEngineView) inside the widget and eval our CSS
        try:
            from aqt.qt import QWebEngineView
            for wv in widget.findChildren(QWebEngineView):
                try:
                    wv.page().runJavaScript(js)
                except (RuntimeError, AttributeError):
                    pass
        except (ImportError, RuntimeError, AttributeError):
            pass

        # Find any editor inside the widget (AddCards, EditCurrent, etc.)
        # and refresh its webview + shadow DOM
        if hasattr(widget, 'editor') and widget.editor:
            editor = widget.editor
            if hasattr(editor, 'web') and editor.web:
                try:
                    editor.web.eval(js)
                    editor.web.eval(f"setTimeout(function(){{{shadow_js}}}, 200);")
                except (RuntimeError, AttributeError):
                    pass

def apply_theme_everywhere(theme: Theme):
    """Apply QSS + force theme mode + refresh all webviews in one call."""
    if is_follow_system_theme():
        _restore_system_theme()
        return
    force_anki_theme_mode(theme)
    apply_qt_styles(theme)

    # Also apply QSS directly to the main window to override any per-widget
    # stylesheets Anki might set
    p = palette_for(theme)
    try:
        mw.setStyleSheet(qss(p))
    except (RuntimeError, AttributeError):
        pass

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
        try:
            with open(file_path, 'w') as f:
                json.dump(theme_data, f, indent=2)
            tooltip(f"Theme exported to {file_path}")
        except (OSError, IOError) as e:
            showInfo(f"Error exporting theme: {e}")
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

# ---------------- Background Patterns ----------------
def get_background_pattern() -> str:
    """Get background pattern setting."""
    cfg = get_config()
    return cfg.get("backgroundPattern", "none")  # none, dots, grid, lines, subtle, diagonal, crosshatch, paper, linen, diamond, waves

def set_background_pattern(pattern: str):
    """Set background pattern."""
    cfg = get_config()
    cfg["backgroundPattern"] = pattern
    write_config(cfg)
    apply_theme_everywhere(get_active_theme())
    tooltip(f"Background pattern: {pattern}")

def get_pattern_css(p: dict, pattern: str) -> str:
    """Generate CSS for background patterns."""
    if pattern == "none":
        return ""
    elif pattern == "dots":
        return f"""
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: radial-gradient(circle, {p['border']}55 1px, transparent 1px);
            background-size: 20px 20px;
            pointer-events: none;
            z-index: -1;
        }}
        """
    elif pattern == "grid":
        return f"""
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image:
                linear-gradient(0deg, {p['border']}40 1px, transparent 1px),
                linear-gradient(90deg, {p['border']}40 1px, transparent 1px);
            background-size: 30px 30px;
            pointer-events: none;
            z-index: -1;
        }}
        """
    elif pattern == "lines":
        return f"""
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: repeating-linear-gradient(
                0deg,
                transparent,
                transparent 2px,
                {p['border']}35 2px,
                {p['border']}35 4px
            );
            pointer-events: none;
            z-index: -1;
        }}
        """
    elif pattern == "subtle":
        return f"""
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: radial-gradient(circle at 20% 50%, {p['accent']}25 0%, transparent 50%),
                              radial-gradient(circle at 80% 80%, {p['accent']}25 0%, transparent 50%);
            pointer-events: none;
            z-index: -1;
        }}
        """
    elif pattern == "diagonal":
        return f"""
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: repeating-linear-gradient(
                45deg,
                transparent,
                transparent 10px,
                {p['border']}38 10px,
                {p['border']}38 11px
            );
            pointer-events: none;
            z-index: -1;
        }}
        """
    elif pattern == "crosshatch":
        return f"""
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image:
                repeating-linear-gradient(
                    45deg,
                    transparent,
                    transparent 10px,
                    {p['border']}30 10px,
                    {p['border']}30 11px
                ),
                repeating-linear-gradient(
                    -45deg,
                    transparent,
                    transparent 10px,
                    {p['border']}30 10px,
                    {p['border']}30 11px
                );
            pointer-events: none;
            z-index: -1;
        }}
        """
    elif pattern == "paper":
        return f"""
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image:
                linear-gradient(0deg, {p['border']}28 1px, transparent 1px),
                linear-gradient(90deg, {p['border']}28 1px, transparent 1px),
                radial-gradient(ellipse at 30% 40%, {p['accent']}18 0%, transparent 70%),
                radial-gradient(ellipse at 70% 60%, {p['border']}18 0%, transparent 70%);
            background-size: 25px 25px, 25px 25px, 100% 100%, 100% 100%;
            pointer-events: none;
            z-index: -1;
        }}
        """
    elif pattern == "linen":
        return f"""
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image:
                repeating-linear-gradient(
                    0deg,
                    {p['border']}30,
                    {p['border']}30 1px,
                    transparent 1px,
                    transparent 4px
                ),
                repeating-linear-gradient(
                    90deg,
                    {p['border']}30,
                    {p['border']}30 1px,
                    transparent 1px,
                    transparent 4px
                );
            pointer-events: none;
            z-index: -1;
        }}
        """
    elif pattern == "diamond":
        return f"""
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image:
                linear-gradient(45deg, {p['border']}35 25%, transparent 25%),
                linear-gradient(-45deg, {p['border']}35 25%, transparent 25%),
                linear-gradient(45deg, transparent 75%, {p['border']}35 75%),
                linear-gradient(-45deg, transparent 75%, {p['border']}35 75%);
            background-size: 30px 30px;
            background-position: 0 0, 0 15px, 15px -15px, -15px 0;
            pointer-events: none;
            z-index: -1;
        }}
        """
    elif pattern == "waves":
        return f"""
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image:
                radial-gradient(ellipse at 0% 50%, {p['border']}35 0%, transparent 60%),
                radial-gradient(ellipse at 100% 50%, {p['border']}35 0%, transparent 60%),
                repeating-linear-gradient(
                    0deg,
                    transparent,
                    transparent 18px,
                    {p['border']}28 18px,
                    {p['border']}28 20px
                );
            pointer-events: none;
            z-index: -1;
        }}
        """
    return ""


# ---------------- Study Session Modes ----------------
def get_study_mode() -> str:
    """Get current study mode."""
    cfg = get_config()
    return cfg.get("studyMode", "normal")

def set_study_mode(mode: str):
    """Set study mode and apply associated settings."""
    cfg = get_config()
    cfg["studyMode"] = mode

    # Apply mode-specific settings
    if mode == "focus":
        # Focus mode: larger text, higher contrast
        cfg["fontSize"] = 20
        cfg["lineHeight"] = 1.8
        cfg["letterSpacing"] = 0.5
    elif mode == "speed":
        # Speed mode: compact layout, smaller text
        cfg["fontSize"] = 14
        cfg["lineHeight"] = 1.4
        cfg["letterSpacing"] = 0.0
    elif mode == "detail":
        # Detail mode: maximum readability
        cfg["fontSize"] = 18
        cfg["lineHeight"] = 2.0
        cfg["letterSpacing"] = 1.0
    # normal mode keeps current settings

    write_config(cfg)
    apply_theme_everywhere(get_active_theme())
    tooltip(f"Study mode: {mode}")

# ---------------- Theme Tags & Favorites ----------------
def get_favorite_themes() -> list:
    """Get list of favorite theme names."""
    cfg = get_config()
    return cfg.get("favoriteThemes", [])

def toggle_favorite_theme(theme_name: str):
    """Add or remove theme from favorites."""
    cfg = get_config()
    favorites = get_favorite_themes()

    if theme_name in favorites:
        favorites.remove(theme_name)
        tooltip(f"Removed {theme_name} from favorites")
    else:
        favorites.append(theme_name)
        tooltip(f"Added {theme_name} to favorites")

    cfg["favoriteThemes"] = favorites
    write_config(cfg)

def get_theme_tags() -> dict:
    """Get theme tags mapping."""
    cfg = get_config()
    return cfg.get("themeTags", {})

def add_theme_tag(theme_name: str, tag: str):
    """Add a tag to a theme."""
    cfg = get_config()
    tags = get_theme_tags()

    if theme_name not in tags:
        tags[theme_name] = []

    if tag not in tags[theme_name]:
        tags[theme_name].append(tag)
        cfg["themeTags"] = tags
        write_config(cfg)
        tooltip(f"Added tag '{tag}' to {theme_name}")

# ---------------- Configuration Backup/Restore ----------------
def backup_configuration() -> str:
    """Backup current configuration to JSON string."""
    cfg = get_config()
    backup_data = {
        "version": VERSION,
        "backup_date": datetime.now().isoformat(),
        "configuration": cfg
    }
    return json.dumps(backup_data, indent=2)

def restore_configuration(backup_json: str) -> bool:
    """Restore configuration from JSON string."""
    try:
        backup_data = json.loads(backup_json)
        cfg = backup_data.get("configuration", {})

        # Restore configuration
        for key, value in cfg.items():
            current_cfg = get_config()
            current_cfg[key] = value
            write_config(current_cfg)

        # Reload custom themes
        custom_themes = get_custom_themes()
        for name, palette in custom_themes.items():
            PALETTES[name] = palette

        apply_theme_everywhere(get_active_theme())
        tooltip("Configuration restored successfully!")
        return True
    except Exception as e:
        showInfo(f"Error restoring configuration: {e}")
        return False

def export_configuration_to_file(file_path: str):
    """Export configuration to file."""
    try:
        backup_json = backup_configuration()
        with open(file_path, 'w') as f:
            f.write(backup_json)
        tooltip(f"Configuration exported to {file_path}")
    except (OSError, IOError) as e:
        showInfo(f"Error exporting configuration: {e}")

def import_configuration_from_file(file_path: str):
    """Import configuration from file."""
    try:
        with open(file_path, 'r') as f:
            backup_json = f.read()
        restore_configuration(backup_json)
    except Exception as e:
        showInfo(f"Error importing configuration: {e}")

# ---------------- Theme Statistics ----------------
def get_theme_statistics() -> dict:
    """Get local theme usage statistics."""
    cfg = get_config()
    return cfg.get("themeStats", {})

def record_theme_usage(theme_name: str):
    """Record theme usage (called when theme is applied)."""
    cfg = get_config()
    stats = get_theme_statistics()

    if theme_name not in stats:
        stats[theme_name] = {"count": 0, "last_used": None}

    stats[theme_name]["count"] += 1
    stats[theme_name]["last_used"] = datetime.now().isoformat()

    cfg["themeStats"] = stats
    write_config(cfg)

# ---------------- About Dialog ----------------
def show_about_dialog():
    dlg = QDialog(mw)
    dlg.setWindowTitle("About — AnkiThemeTwin")
    layout = QVBoxLayout(dlg)
    lbl = QLabel(
        '<div style="font-size:14px;">'
        f'<b>AnkiThemeTwin</b> v{VERSION}<br>'
        '21+ themes including accessibility and community themes.<br>'
        'Full theming engine with eye-comfort tools.<br><br>'
        '<b>Features:</b><br>'
        '• 7 eye-comfort themes + 6 accessibility themes<br>'
        '• 8 community themes (Solarized, Nord, Catppuccin, etc.)<br>'
        '• Custom theme creator with color picker<br>'
        '• Theme presets, import/export, and community gallery<br>'
        '• Keyboard shortcuts (Ctrl+Shift+1-7, Ctrl+Shift+Z)<br>'
        '• Advanced font customization<br>'
        '• 🔆 Blue light filter with intensity slider<br>'
        '• 🌅 Ambient light auto-adjust (time-based)<br>'
        '• 🧘 Zen Mode — distraction-free review<br>'
        '• ⏱️ Pomodoro break reminders<br>'
        '• 🔄 Theme rotation and seasonal themes<br>'
        '• 📝 Per-note-type styling<br>'
        '• 🎨 Custom CSS injection<br>'
        '• 🎯 Match card background<br>'
        '• 🔄 Theme sync across devices via AnkiWeb<br>'
        '• Right-click context menu for quick switching<br>'
        '• 4 animation styles (fade, slide, morph, zoom)<br>'
        '• Status bar theme indicator<br><br>'
        '<b>Card Template Helper Variables:</b><br>'
        '<code>--att-bg, --att-fg, --att-accent, --att-border,<br>'
        '--att-button, --att-input, --att-hover, --att-selection,<br>'
        '--att-font-size, --att-font-family, --att-line-height</code><br><br>'
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
    dlg.resize(650, 550)
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

    slide_rb = QRadioButton("Slide")
    slide_rb.setChecked(settings.get("style", "fade") == "slide")
    style_group.addButton(slide_rb)
    style_layout.addWidget(slide_rb)

    morph_rb = QRadioButton("Morph (Elastic)")
    morph_rb.setChecked(settings.get("style", "fade") == "morph")
    style_group.addButton(morph_rb)
    style_layout.addWidget(morph_rb)

    zoom_rb = QRadioButton("Zoom")
    zoom_rb.setChecked(settings.get("style", "fade") == "zoom")
    style_group.addButton(zoom_rb)
    style_layout.addWidget(zoom_rb)

    none_rb = QRadioButton("None (Instant)")
    none_rb.setChecked(settings.get("style", "fade") == "none")
    style_group.addButton(none_rb)
    style_layout.addWidget(none_rb)

    layout.addLayout(style_layout)

    # Save button
    def save_settings():
        if fade_rb.isChecked():
            style = "fade"
        elif slide_rb.isChecked():
            style = "slide"
        elif morph_rb.isChecked():
            style = "morph"
        elif zoom_rb.isChecked():
            style = "zoom"
        else:
            style = "none"
        new_settings = {
            "enabled": enabled_cb.isChecked(),
            "duration": duration_spin.value(),
            "style": style,
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

# ---------------- Visual Enhancements Dialog ----------------

def _create_pattern_preview(pattern_key: str, bg_color: str, line_color: str, accent_color: str, size: int = 48) -> QPixmap:
    """Create a small preview pixmap showing what a background pattern looks like."""
    pixmap = QPixmap(size, size)
    bg = QColor(bg_color)
    line = QColor(line_color)
    accent = QColor(accent_color)

    pixmap.fill(bg)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    if pattern_key == "none":
        # Just the solid background — already filled
        pass

    elif pattern_key == "dots":
        line.setAlpha(85)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(line))
        for x in range(4, size, 8):
            for y in range(4, size, 8):
                painter.drawEllipse(x - 1, y - 1, 2, 2)

    elif pattern_key == "grid":
        line.setAlpha(64)
        pen = QPen(line, 1)
        painter.setPen(pen)
        for x in range(0, size, 10):
            painter.drawLine(x, 0, x, size)
        for y in range(0, size, 10):
            painter.drawLine(0, y, size, y)

    elif pattern_key == "lines":
        line.setAlpha(53)
        pen = QPen(line, 1)
        painter.setPen(pen)
        for y in range(0, size, 4):
            painter.drawLine(0, y, size, y)

    elif pattern_key == "subtle":
        accent.setAlpha(37)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(accent))
        painter.drawEllipse(4, 8, 24, 24)
        painter.drawEllipse(24, 24, 20, 20)

    elif pattern_key == "diagonal":
        line.setAlpha(56)
        pen = QPen(line, 1)
        painter.setPen(pen)
        for i in range(-size, size * 2, 8):
            painter.drawLine(i, 0, i + size, size)

    elif pattern_key == "crosshatch":
        line.setAlpha(48)
        pen = QPen(line, 1)
        painter.setPen(pen)
        for i in range(-size, size * 2, 8):
            painter.drawLine(i, 0, i + size, size)
            painter.drawLine(i + size, 0, i, size)

    elif pattern_key == "paper":
        line.setAlpha(40)
        pen = QPen(line, 1)
        painter.setPen(pen)
        for x in range(0, size, 10):
            painter.drawLine(x, 0, x, size)
        for y in range(0, size, 10):
            painter.drawLine(0, y, size, y)
        accent.setAlpha(24)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(accent))
        painter.drawEllipse(6, 6, 20, 20)
        painter.drawEllipse(26, 26, 18, 18)

    elif pattern_key == "linen":
        line.setAlpha(48)
        pen = QPen(line, 1)
        painter.setPen(pen)
        for y in range(0, size, 4):
            painter.drawLine(0, y, size, y)
        line.setAlpha(40)
        pen = QPen(line, 1)
        painter.setPen(pen)
        for x in range(0, size, 4):
            painter.drawLine(x, 0, x, size)

    elif pattern_key == "diamond":
        line.setAlpha(53)
        pen = QPen(line, 1)
        painter.setPen(pen)
        for i in range(-size, size * 2, 12):
            painter.drawLine(i, 0, i + size, size)
            painter.drawLine(i + size, 0, i, size)

    elif pattern_key == "waves":
        line.setAlpha(53)
        pen = QPen(line, 1)
        painter.setPen(pen)
        for y in range(4, size, 10):
            painter.drawLine(0, y, size, y)
        line.setAlpha(40)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(line))
        painter.drawRect(0, 0, 8, size)
        painter.drawRect(size - 8, 0, 8, size)

    painter.end()
    return pixmap

def show_visual_enhancements_dialog():
    """Show dialog to configure visual enhancements with pattern previews."""
    dlg = QDialog(mw)
    dlg.setWindowTitle("Visual Enhancements")
    dlg.resize(500, 580)
    layout = QVBoxLayout(dlg)

    # Header
    header = QLabel("<h3>Visual Enhancements</h3>")
    layout.addWidget(header)

    # Get current theme palette for preview colors
    theme = get_active_theme()
    p = palette_for(theme)

    # Background pattern selection
    pattern_label = QLabel("<b>Background Texture:</b>")
    layout.addWidget(pattern_label)

    # Scrollable area for the pattern list
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll_widget = QWidget()
    pattern_group = QVBoxLayout(scroll_widget)
    pattern_group.setContentsMargins(4, 4, 4, 4)

    current_pattern = get_background_pattern()
    pattern_bg = QButtonGroup(dlg)

    patterns = [
        ("none", "None (Solid)", "No texture — just a flat solid color background"),
        ("subtle", "Subtle Gradient", "Soft color blobs in the background"),
        ("dots", "Dots", "Small repeating dots across the background"),
        ("grid", "Grid", "Light grid lines forming small squares"),
        ("lines", "Horizontal Lines", "Thin horizontal ruled lines"),
        ("diagonal", "Diagonal Lines", "Lines tilted at 45°"),
        ("crosshatch", "Crosshatch", "Crisscrossing diagonal lines"),
        ("paper", "Paper", "Faint grid with subtle color wash"),
        ("linen", "Linen", "Tight woven fabric-like texture"),
        ("diamond", "Diamond", "Repeating diamond / argyle shapes"),
        ("waves", "Waves", "Horizontal bands with soft edges"),
    ]

    for value, label, desc in patterns:
        row = QHBoxLayout()
        row.setContentsMargins(2, 2, 2, 2)

        # Preview square
        preview = QLabel()
        pix = _create_pattern_preview(value, p['bg'], p['border'], p['accent'], 48)
        preview.setPixmap(pix)
        preview.setFixedSize(52, 52)
        preview.setStyleSheet(
            f"border: 1px solid {p['border']}; border-radius: 4px; padding: 1px;"
        )
        row.addWidget(preview)

        # Radio + description
        text_col = QVBoxLayout()
        text_col.setContentsMargins(4, 0, 0, 0)
        text_col.setSpacing(0)
        rb = QRadioButton(label)
        rb.setChecked(current_pattern == value)
        rb.setProperty("pattern_value", value)
        pattern_bg.addButton(rb)
        text_col.addWidget(rb)

        desc_label = QLabel(f"<span style='color:gray; font-size:10px;'>{desc}</span>")
        text_col.addWidget(desc_label)
        row.addLayout(text_col)
        row.addStretch()

        row_widget = QWidget()
        row_widget.setLayout(row)
        pattern_group.addWidget(row_widget)

    pattern_group.addStretch()
    scroll.setWidget(scroll_widget)
    layout.addWidget(scroll)

    # Info text
    info = QLabel(
        "💡 <b>Where do textures appear?</b> Textures are visible on <b>all Anki screens</b>: "
        "the deck list, reviewer, card editor, and browser. They overlay on top of your current "
        "theme color. All textures are pure CSS — no images needed."
    )
    info.setWordWrap(True)
    info.setStyleSheet("color: gray; font-size: 11px; padding: 8px; background: palette(base); border-radius: 4px;")
    layout.addWidget(info)

    # Buttons
    btn_row = QHBoxLayout()
    def save_settings():
        for button in pattern_bg.buttons():
            if button.isChecked():
                pattern_value = button.property("pattern_value")
                set_background_pattern(pattern_value)
                break
        dlg.accept()

    save_btn = QPushButton("Apply")
    save_btn.clicked.connect(save_settings)
    btn_row.addWidget(save_btn)

    cancel_btn = QPushButton("Cancel")
    cancel_btn.clicked.connect(dlg.reject)
    btn_row.addWidget(cancel_btn)
    layout.addLayout(btn_row)

    dlg.exec()

# ---------------- Study Mode Dialog ----------------
def show_study_mode_dialog():
    """Show dialog to select study mode."""
    dlg = QDialog(mw)
    dlg.setWindowTitle("Study Session Modes")
    dlg.resize(500, 400)
    layout = QVBoxLayout(dlg)

    info = QLabel(
        "<b>Study Session Modes</b><br><br>"
        "Choose a mode optimized for different study scenarios:"
    )
    layout.addWidget(info)

    current_mode = get_study_mode()

    # Mode buttons
    mode_group = QButtonGroup(dlg)

    normal_rb = QRadioButton("Normal - Balanced settings")
    normal_rb.setChecked(current_mode == "normal")
    mode_group.addButton(normal_rb)
    layout.addWidget(normal_rb)

    focus_rb = QRadioButton("Focus - Larger text, higher contrast, fewer distractions")
    focus_rb.setChecked(current_mode == "focus")
    mode_group.addButton(focus_rb)
    layout.addWidget(focus_rb)

    speed_rb = QRadioButton("Speed - Compact layout for rapid reviews")
    speed_rb.setChecked(current_mode == "speed")
    mode_group.addButton(speed_rb)
    layout.addWidget(speed_rb)

    detail_rb = QRadioButton("Detail - Maximum readability for careful study")
    detail_rb.setChecked(current_mode == "detail")
    mode_group.addButton(detail_rb)
    layout.addWidget(detail_rb)

    # Mode descriptions
    desc_label = QLabel(
        "<br><b>Mode Details:</b><br>"
        "• <b>Normal</b>: Your current custom settings<br>"
        "• <b>Focus</b>: Font 20px, Line height 1.8, Letter spacing 0.5px<br>"
        "• <b>Speed</b>: Font 14px, Line height 1.4, Letter spacing 0px<br>"
        "• <b>Detail</b>: Font 18px, Line height 2.0, Letter spacing 1.0px<br>"
    )
    layout.addWidget(desc_label)

    # Apply button
    def apply_mode():
        if normal_rb.isChecked():
            set_study_mode("normal")
        elif focus_rb.isChecked():
            set_study_mode("focus")
        elif speed_rb.isChecked():
            set_study_mode("speed")
        elif detail_rb.isChecked():
            set_study_mode("detail")
        dlg.accept()

    apply_btn = QPushButton("Apply Mode")
    apply_btn.clicked.connect(apply_mode)
    layout.addWidget(apply_btn)

    close_btn = QPushButton("Cancel")
    close_btn.clicked.connect(dlg.reject)
    layout.addWidget(close_btn)

    dlg.exec()

# ---------------- Quick Settings Panel ----------------
def show_quick_settings_panel():
    """Show quick access panel for common settings."""
    dlg = QDialog(mw)
    dlg.setWindowTitle("Quick Settings")
    dlg.resize(400, 500)
    layout = QVBoxLayout(dlg)

    cfg = get_config()

    # Current theme
    theme_layout = QHBoxLayout()
    theme_layout.addWidget(QLabel("Theme:"))
    theme_combo = QComboBox()
    all_themes = [key for _, key in THEME_OPTIONS + ACCESSIBILITY_THEMES]
    theme_combo.addItems(all_themes)
    theme_combo.setCurrentText(cfg.get("currentTheme", "sepia_special"))
    theme_layout.addWidget(theme_combo)
    layout.addLayout(theme_layout)

    # Font size
    size_layout = QHBoxLayout()
    size_layout.addWidget(QLabel("Font Size:"))
    size_spin = QSpinBox()
    size_spin.setRange(8, 32)
    size_spin.setValue(cfg.get("fontSize", 16))
    size_spin.setSuffix("px")
    size_layout.addWidget(size_spin)
    layout.addLayout(size_layout)

    # Study mode
    mode_layout = QHBoxLayout()
    mode_layout.addWidget(QLabel("Study Mode:"))
    mode_combo = QComboBox()
    mode_combo.addItems(["normal", "focus", "speed", "detail"])
    mode_combo.setCurrentText(get_study_mode())
    mode_layout.addWidget(mode_combo)
    layout.addLayout(mode_layout)

    # Favorites
    layout.addWidget(QLabel("<br><b>Favorite Themes:</b>"))
    favorites = get_favorite_themes()
    fav_list = QTextEdit()
    fav_list.setReadOnly(True)
    fav_list.setMaximumHeight(100)
    if favorites:
        fav_list.setPlainText(", ".join(favorites))
    else:
        fav_list.setPlainText("No favorites yet")
    layout.addWidget(fav_list)

    # Quick actions
    layout.addWidget(QLabel("<br><b>Quick Actions:</b>"))

    actions_layout = QVBoxLayout()

    def apply_favorite(fav_theme):
        set_theme(fav_theme)
        dlg.accept()

    for fav in favorites[:5]:  # Show first 5 favorites
        btn = QPushButton(f"Apply: {fav}")
        btn.clicked.connect(lambda _, f=fav: apply_favorite(f))
        actions_layout.addWidget(btn)

    layout.addLayout(actions_layout)

    # Apply current selections
    def apply_quick_settings():
        set_theme(theme_combo.currentText())
        set_font_size(size_spin.value())
        set_study_mode(mode_combo.currentText())
        dlg.accept()

    apply_btn = QPushButton("Apply All Settings")
    apply_btn.clicked.connect(apply_quick_settings)
    layout.addWidget(apply_btn)

    close_btn = QPushButton("Close")
    close_btn.clicked.connect(dlg.reject)
    layout.addWidget(close_btn)

    dlg.exec()

# ---------------- Configuration Backup Dialog ----------------
def show_backup_restore_dialog():
    """Show dialog to backup/restore configuration."""
    dlg = QDialog(mw)
    dlg.setWindowTitle("Backup & Restore Configuration")
    dlg.resize(600, 400)
    layout = QVBoxLayout(dlg)

    info = QLabel(
        "<b>Backup & Restore</b><br>"
        "Save and restore all your AnkiThemeTwin settings."
    )
    layout.addWidget(info)

    # Backup section
    backup_layout = QVBoxLayout()
    backup_layout.addWidget(QLabel("<br><b>Backup Configuration:</b>"))

    backup_text = QTextEdit()
    backup_text.setPlaceholderText("Backup JSON will appear here...")
    backup_text.setMaximumHeight(150)
    backup_layout.addWidget(backup_text)

    def create_backup():
        backup_json = backup_configuration()
        backup_text.setPlainText(backup_json)
        tooltip("Backup created! Copy or save to file.")

    backup_btn = QPushButton("Create Backup")
    backup_btn.clicked.connect(create_backup)
    backup_layout.addWidget(backup_btn)

    layout.addLayout(backup_layout)

    # Restore section
    restore_layout = QVBoxLayout()
    restore_layout.addWidget(QLabel("<br><b>Restore Configuration:</b>"))

    restore_text = QTextEdit()
    restore_text.setPlaceholderText("Paste backup JSON here to restore...")
    restore_text.setMaximumHeight(150)
    restore_layout.addWidget(restore_text)

    def restore_backup():
        backup_json = restore_text.toPlainText()
        if backup_json.strip():
            if restore_configuration(backup_json):
                dlg.accept()
        else:
            showInfo("Please paste a backup JSON first!")

    restore_btn = QPushButton("Restore from Backup")
    restore_btn.clicked.connect(restore_backup)
    restore_layout.addWidget(restore_btn)

    layout.addLayout(restore_layout)

    close_btn = QPushButton("Close")
    close_btn.clicked.connect(dlg.reject)
    layout.addWidget(close_btn)

    dlg.exec()

# ---------------- Theme Statistics Dialog ----------------
def show_statistics_dialog():
    """Show theme usage statistics."""
    dlg = QDialog(mw)
    dlg.setWindowTitle("Theme Usage Statistics")
    dlg.resize(600, 400)
    layout = QVBoxLayout(dlg)

    info = QLabel("<b>Your Theme Usage (Local Only)</b>")
    layout.addWidget(info)

    stats = get_theme_statistics()

    if not stats:
        layout.addWidget(QLabel("<br>No usage data yet. Start using themes to see statistics!"))
    else:
        # Sort by usage count
        sorted_stats = sorted(stats.items(), key=lambda x: x[1]["count"], reverse=True)

        stats_text = QTextEdit()
        stats_text.setReadOnly(True)

        text = "<table width='100%'><tr><th>Theme</th><th>Uses</th><th>Last Used</th></tr>"
        for theme, data in sorted_stats:
            count = data.get("count", 0)
            last_used = data.get("last_used", "Never")
            if last_used != "Never":
                # Format datetime
                try:
                    dt = datetime.fromisoformat(last_used)
                    last_used = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    pass
            text += f"<tr><td>{theme}</td><td>{count}</td><td>{last_used}</td></tr>"
        text += "</table>"

        stats_text.setHtml(text)
        layout.addWidget(stats_text)

        # Most used theme
        most_used = sorted_stats[0]
        summary = QLabel(
            f"<br><b>Most Used:</b> {most_used[0]} ({most_used[1]['count']} times)"
        )
        layout.addWidget(summary)

    close_btn = QPushButton("Close")
    close_btn.clicked.connect(dlg.accept)
    layout.addWidget(close_btn)

    dlg.exec()

# ====== Feature 1: Pomodoro Timer Dialog ======
def show_pomodoro_dialog():
    """Show Pomodoro timer configuration and control dialog."""
    dlg = QDialog(mw)
    dlg.setWindowTitle("Pomodoro Timer")
    dlg.resize(450, 350)
    layout = QVBoxLayout(dlg)

    settings = get_pomodoro_settings()

    header = QLabel("<h3>⏱️ Pomodoro Timer</h3>"
                    "<p>Take regular breaks to protect your eyes and maintain focus.</p>")
    header.setWordWrap(True)
    layout.addWidget(header)

    # Enable
    enabled_cb = QCheckBox("Enable Pomodoro Timer")
    enabled_cb.setChecked(settings.get("enabled", False))
    layout.addWidget(enabled_cb)

    # Study duration
    study_layout = QHBoxLayout()
    study_layout.addWidget(QLabel("Study duration:"))
    study_spin = QSpinBox()
    study_spin.setRange(5, 120)
    study_spin.setValue(settings.get("studyMinutes", 25))
    study_spin.setSuffix(" min")
    study_layout.addWidget(study_spin)
    layout.addLayout(study_layout)

    # Break duration
    break_layout = QHBoxLayout()
    break_layout.addWidget(QLabel("Break duration:"))
    break_spin = QSpinBox()
    break_spin.setRange(1, 30)
    break_spin.setValue(settings.get("breakMinutes", 5))
    break_spin.setSuffix(" min")
    break_layout.addWidget(break_spin)
    layout.addLayout(break_layout)

    # Auto start
    auto_cb = QCheckBox("Auto-start next session after break")
    auto_cb.setChecked(settings.get("autoStart", False))
    layout.addWidget(auto_cb)

    # Status
    is_running = getattr(mw, "_ankitwin_pomodoro_studying", False)
    status = QLabel(f"Status: {'🟢 Running' if is_running else '⭕ Stopped'}")
    layout.addWidget(status)

    layout.addStretch()

    # Buttons
    btn_layout = QHBoxLayout()

    def save_and_start():
        new_settings = {
            "enabled": enabled_cb.isChecked(),
            "studyMinutes": study_spin.value(),
            "breakMinutes": break_spin.value(),
            "autoStart": auto_cb.isChecked(),
        }
        save_pomodoro_settings(new_settings)
        if enabled_cb.isChecked():
            _start_pomodoro_timer()
            tooltip("⏱️ Pomodoro timer started!", period=2000)
        else:
            _stop_pomodoro_timer()
        dlg.accept()

    def stop_timer():
        _stop_pomodoro_timer()
        tooltip("⏱️ Pomodoro timer stopped", period=1500)
        dlg.accept()

    save_btn = QPushButton("Save & Start")
    save_btn.clicked.connect(save_and_start)
    btn_layout.addWidget(save_btn)

    stop_btn = QPushButton("Stop Timer")
    stop_btn.clicked.connect(stop_timer)
    btn_layout.addWidget(stop_btn)

    cancel_btn = QPushButton("Cancel")
    cancel_btn.clicked.connect(dlg.reject)
    btn_layout.addWidget(cancel_btn)

    layout.addLayout(btn_layout)
    dlg.exec()

# ====== Feature 2: Blue Light Filter Dialog ======
def show_blue_light_dialog():
    """Show blue light filter adjustment dialog."""
    dlg = QDialog(mw)
    dlg.setWindowTitle("Blue Light Filter")
    dlg.resize(450, 250)
    layout = QVBoxLayout(dlg)

    header = QLabel("<h3>🔆 Blue Light Filter</h3>"
                    "<p>Reduce blue light to ease eye strain during evening study.</p>")
    header.setWordWrap(True)
    layout.addWidget(header)

    current = get_blue_light_filter()

    slider_layout = QVBoxLayout()
    value_label = QLabel(f"Intensity: {current}%")
    slider_layout.addWidget(value_label)

    slider = QSlider(Qt.Orientation.Horizontal)
    slider.setRange(0, 100)
    slider.setValue(current)

    def update_label(val):
        value_label.setText(f"Intensity: {val}%")

    slider.valueChanged.connect(update_label)
    slider_layout.addWidget(slider)

    desc = QLabel("0% = Off | 50% = Moderate | 100% = Maximum warmth")
    desc.setStyleSheet("font-size:11px; color:gray;")
    slider_layout.addWidget(desc)
    layout.addLayout(slider_layout)

    layout.addStretch()

    def apply_filter():
        set_blue_light_filter(slider.value())
        tooltip(f"🔆 Blue light filter: {slider.value()}%", period=1500)
        dlg.accept()

    apply_btn = QPushButton("Apply")
    apply_btn.clicked.connect(apply_filter)
    layout.addWidget(apply_btn)

    cancel_btn = QPushButton("Cancel")
    cancel_btn.clicked.connect(dlg.reject)
    layout.addWidget(cancel_btn)

    dlg.exec()

# ====== Feature 3: Theme Sync Dialog ======
def show_sync_dialog():
    """Show theme sync configuration dialog."""
    dlg = QDialog(mw)
    dlg.setWindowTitle("Theme Sync")
    dlg.resize(500, 350)
    layout = QVBoxLayout(dlg)

    header = QLabel("<h3>🔄 Theme Sync via AnkiWeb</h3>"
                    "<p>Sync your theme settings across devices using Anki's media sync.<br>"
                    "Settings are stored in collection.media and synced by AnkiWeb.</p>")
    header.setWordWrap(True)
    layout.addWidget(header)

    cfg = get_config()
    enabled_cb = QCheckBox("Enable theme sync")
    enabled_cb.setChecked(cfg.get("syncEnabled", False))
    layout.addWidget(enabled_cb)

    sync_path = _get_sync_file_path()
    if sync_path and os.path.exists(sync_path):
        try:
            mod_time = datetime.fromtimestamp(os.path.getmtime(sync_path))
            status = QLabel(f"Last synced: {mod_time.strftime('%Y-%m-%d %H:%M')}")
        except (OSError, ValueError):
            status = QLabel("Sync file exists")
    else:
        status = QLabel("No sync file found yet")
    layout.addWidget(status)

    layout.addStretch()

    btn_layout = QHBoxLayout()

    def save_settings():
        cfg = get_config()
        cfg["syncEnabled"] = enabled_cb.isChecked()
        write_config(cfg)
        if enabled_cb.isChecked():
            sync_config_to_media()
            tooltip("🔄 Sync enabled and settings exported!", period=2000)
        dlg.accept()

    def force_push():
        sync_config_to_media()
        tooltip("🔄 Settings pushed to sync!", period=1500)

    def force_pull():
        sync_config_from_media()
        apply_theme_everywhere(get_active_theme())
        dlg.accept()

    save_btn = QPushButton("Save")
    save_btn.clicked.connect(save_settings)
    btn_layout.addWidget(save_btn)

    push_btn = QPushButton("Push to Sync")
    push_btn.clicked.connect(force_push)
    btn_layout.addWidget(push_btn)

    pull_btn = QPushButton("Pull from Sync")
    pull_btn.clicked.connect(force_pull)
    btn_layout.addWidget(pull_btn)

    layout.addLayout(btn_layout)

    close_btn = QPushButton("Close")
    close_btn.clicked.connect(dlg.reject)
    layout.addWidget(close_btn)

    dlg.exec()

# ====== Feature 4: Note-Type Styling Dialog ======
def show_note_type_styling_dialog():
    """Show dialog to configure per-note-type styling."""
    dlg = QDialog(mw)
    dlg.setWindowTitle("Note Type Styling")
    dlg.resize(600, 500)
    layout = QVBoxLayout(dlg)

    header = QLabel("<h3>📝 Note Type Specific Styling</h3>"
                    "<p>Set different fonts, sizes, or themes for each note type.</p>")
    header.setWordWrap(True)
    layout.addWidget(header)

    # Current styles
    styles = get_note_type_styles()
    styles_list = QTextEdit()
    styles_list.setReadOnly(True)
    styles_list.setMaximumHeight(120)

    def refresh_list():
        if not styles:
            styles_list.setPlainText("No note-type styles configured yet.")
        else:
            text = ""
            for nt, s in styles.items():
                parts = []
                if "fontSize" in s:
                    parts.append(f"{s['fontSize']}px")
                if "fontFamily" in s:
                    parts.append(s["fontFamily"])
                if "theme" in s:
                    parts.append(f"theme:{s['theme']}")
                text += f"• {nt}: {', '.join(parts)}\n"
            styles_list.setPlainText(text)

    refresh_list()
    layout.addWidget(styles_list)

    # Add new style
    grid = QGridLayout()
    grid.addWidget(QLabel("Note Type Name:"), 0, 0)
    nt_input = QLineEdit()
    nt_input.setPlaceholderText("e.g., Basic, Cloze, Basic (and reversed)")
    grid.addWidget(nt_input, 0, 1)

    grid.addWidget(QLabel("Font Size (px):"), 1, 0)
    fs_spin = QSpinBox()
    fs_spin.setRange(0, 48)
    fs_spin.setValue(0)
    fs_spin.setSpecialValueText("Default")
    grid.addWidget(fs_spin, 1, 1)

    grid.addWidget(QLabel("Font Family:"), 2, 0)
    ff_input = QLineEdit()
    ff_input.setPlaceholderText("Leave empty for default")
    grid.addWidget(ff_input, 2, 1)

    grid.addWidget(QLabel("Override Theme:"), 3, 0)
    theme_combo = QComboBox()
    theme_combo.addItem("(No Override)", "")
    for label, key in THEME_OPTIONS + ACCESSIBILITY_THEMES:
        theme_combo.addItem(label, key)
    grid.addWidget(theme_combo, 3, 1)

    layout.addLayout(grid)

    btn_layout = QHBoxLayout()

    def save_style():
        nt = nt_input.text().strip()
        if not nt:
            showInfo("Please enter a note type name!")
            return
        style = {}
        if fs_spin.value() > 0:
            style["fontSize"] = fs_spin.value()
        if ff_input.text().strip():
            style["fontFamily"] = ff_input.text().strip()
        theme_key = theme_combo.currentData()
        if theme_key:
            style["theme"] = theme_key
        if style:
            set_note_type_style(nt, style)
            styles[nt] = style
            refresh_list()
            nt_input.clear()

    def remove_style():
        nt = nt_input.text().strip()
        if nt and nt in styles:
            delete_note_type_style(nt)
            del styles[nt]
            refresh_list()
            nt_input.clear()
            tooltip(f"Removed style for '{nt}'")

    save_btn = QPushButton("Save Style")
    save_btn.clicked.connect(save_style)
    btn_layout.addWidget(save_btn)

    remove_btn = QPushButton("Remove Style")
    remove_btn.clicked.connect(remove_style)
    btn_layout.addWidget(remove_btn)

    layout.addLayout(btn_layout)

    close_btn = QPushButton("Close")
    close_btn.clicked.connect(dlg.accept)
    layout.addWidget(close_btn)

    dlg.exec()

# ====== Feature 6: Theme Rotation Dialog ======
def show_rotation_dialog():
    """Show theme rotation configuration dialog."""
    dlg = QDialog(mw)
    dlg.setWindowTitle("Theme Rotation")
    dlg.resize(550, 450)
    layout = QVBoxLayout(dlg)

    header = QLabel("<h3>🔄 Theme Rotation</h3>"
                    "<p>Auto-rotate through selected themes to keep study sessions fresh.</p>")
    header.setWordWrap(True)
    layout.addWidget(header)

    settings = get_rotation_settings()

    enabled_cb = QCheckBox("Enable theme rotation")
    enabled_cb.setChecked(settings.get("enabled", False))
    layout.addWidget(enabled_cb)

    # Interval
    interval_layout = QHBoxLayout()
    interval_layout.addWidget(QLabel("Rotate every:"))
    cards_spin = QSpinBox()
    cards_spin.setRange(0, 1000)
    cards_spin.setValue(settings.get("intervalCards", 10))
    cards_spin.setSuffix(" cards")
    cards_spin.setSpecialValueText("Disabled")
    interval_layout.addWidget(cards_spin)

    minutes_spin = QSpinBox()
    minutes_spin.setRange(0, 120)
    minutes_spin.setValue(settings.get("intervalMinutes", 0))
    minutes_spin.setSuffix(" min")
    minutes_spin.setSpecialValueText("Disabled")
    interval_layout.addWidget(minutes_spin)
    layout.addLayout(interval_layout)

    # Theme selection
    layout.addWidget(QLabel("Themes to rotate through:"))
    theme_checkboxes = {}
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll_widget = QWidget()
    scroll_layout = QVBoxLayout(scroll_widget)

    selected = settings.get("themes", [])
    all_themes = list(THEME_OPTIONS) + list(ACCESSIBILITY_THEMES)
    for label, key in all_themes:
        cb = QCheckBox(label)
        cb.setChecked(key in selected)
        cb.setProperty("theme_key", key)
        theme_checkboxes[key] = cb
        scroll_layout.addWidget(cb)

    scroll.setWidget(scroll_widget)
    layout.addWidget(scroll)

    def save_settings():
        themes = [k for k, cb in theme_checkboxes.items() if cb.isChecked()]
        new_settings = {
            "enabled": enabled_cb.isChecked(),
            "themes": themes,
            "intervalCards": cards_spin.value(),
            "intervalMinutes": minutes_spin.value(),
        }
        save_rotation_settings(new_settings)
        if enabled_cb.isChecked() and minutes_spin.value() > 0:
            _start_rotation_timer()
        tooltip("🔄 Rotation settings saved!")
        dlg.accept()

    save_btn = QPushButton("Save")
    save_btn.clicked.connect(save_settings)
    layout.addWidget(save_btn)

    cancel_btn = QPushButton("Cancel")
    cancel_btn.clicked.connect(dlg.reject)
    layout.addWidget(cancel_btn)

    dlg.exec()

# ====== Feature 7: Custom CSS Dialog ======
def show_custom_css_dialog():
    """Show dialog for custom CSS injection."""
    dlg = QDialog(mw)
    dlg.setWindowTitle("Custom CSS")
    dlg.resize(650, 500)
    layout = QVBoxLayout(dlg)

    header = QLabel("<h3>🎨 Custom CSS Injection</h3>"
                    "<p>Add your own CSS rules that are injected alongside the theme.<br>"
                    "This CSS is applied after all theme styles.</p>")
    header.setWordWrap(True)
    layout.addWidget(header)

    css_edit = QTextEdit()
    css_edit.setPlainText(get_custom_css())
    css_edit.setPlaceholderText(
        "/* Example custom CSS */\n"
        ".card { border-radius: 12px; }\n"
        "h1 { font-size: 24px; }\n"
        "\n"
        "/* Use --att-* variables from your theme: */\n"
        ".myclass { color: var(--att-accent); }"
    )
    layout.addWidget(css_edit)

    hint = QLabel(
        "💡 Available theme variables: --att-bg, --att-fg, --att-accent, "
        "--att-border, --att-button, --att-input, --att-hover, --att-selection, "
        "--att-font-size, --att-font-family, --att-line-height"
    )
    hint.setWordWrap(True)
    hint.setStyleSheet("font-size:11px; color:gray; padding:4px;")
    layout.addWidget(hint)

    btn_layout = QHBoxLayout()

    def apply_css():
        set_custom_css(css_edit.toPlainText())
        tooltip("🎨 Custom CSS applied!")
        dlg.accept()

    def clear_css():
        css_edit.clear()
        set_custom_css("")
        tooltip("Custom CSS cleared")

    apply_btn = QPushButton("Apply & Save")
    apply_btn.clicked.connect(apply_css)
    btn_layout.addWidget(apply_btn)

    clear_btn = QPushButton("Clear All")
    clear_btn.clicked.connect(clear_css)
    btn_layout.addWidget(clear_btn)

    cancel_btn = QPushButton("Cancel")
    cancel_btn.clicked.connect(dlg.reject)
    btn_layout.addWidget(cancel_btn)

    layout.addLayout(btn_layout)
    dlg.exec()

# ====== Feature 9: Ambient Light Settings Dialog ======
def show_ambient_light_dialog():
    """Show ambient light auto-adjust settings dialog."""
    dlg = QDialog(mw)
    dlg.setWindowTitle("Ambient Light Auto-Adjust")
    dlg.resize(500, 380)
    layout = QVBoxLayout(dlg)

    header = QLabel("<h3>🌅 Ambient Light Auto-Adjust</h3>"
                    "<p>Automatically adjusts blue light filter based on time of day,<br>"
                    "similar to f.lux or Night Shift. Strongest at night, lightest at noon.</p>")
    header.setWordWrap(True)
    layout.addWidget(header)

    settings = get_ambient_light_settings()

    enabled_cb = QCheckBox("Enable automatic blue light adjustment")
    enabled_cb.setChecked(settings.get("enabled", False))
    layout.addWidget(enabled_cb)

    # Min filter
    min_layout = QHBoxLayout()
    min_layout.addWidget(QLabel("Minimum filter (noon):"))
    min_spin = QSpinBox()
    min_spin.setRange(0, 100)
    min_spin.setValue(settings.get("minFilter", 0))
    min_spin.setSuffix("%")
    min_layout.addWidget(min_spin)
    layout.addLayout(min_layout)

    # Max filter
    max_layout = QHBoxLayout()
    max_layout.addWidget(QLabel("Maximum filter (midnight):"))
    max_spin = QSpinBox()
    max_spin.setRange(0, 100)
    max_spin.setValue(settings.get("maxFilter", 60))
    max_spin.setSuffix("%")
    max_layout.addWidget(max_spin)
    layout.addLayout(max_layout)

    # Current calculation
    current_calc = _calculate_ambient_filter() if settings.get("enabled") else 0
    preview = QLabel(f"Current auto-calculated filter: {current_calc}%")
    layout.addWidget(preview)

    note = QLabel("Note: When enabled, this overrides the manual blue light filter slider.")
    note.setWordWrap(True)
    note.setStyleSheet("font-size:11px; color:gray;")
    layout.addWidget(note)

    layout.addStretch()

    def save_settings():
        new_settings = {
            "enabled": enabled_cb.isChecked(),
            "minFilter": min_spin.value(),
            "maxFilter": max_spin.value(),
        }
        save_ambient_light_settings(new_settings)
        if enabled_cb.isChecked():
            _apply_ambient_light()
        tooltip("🌅 Ambient light settings saved!")
        dlg.accept()

    save_btn = QPushButton("Save & Apply")
    save_btn.clicked.connect(save_settings)
    layout.addWidget(save_btn)

    cancel_btn = QPushButton("Cancel")
    cancel_btn.clicked.connect(dlg.reject)
    layout.addWidget(cancel_btn)

    dlg.exec()

# ====== Feature 14: Community Theme Gallery Dialog ======
def show_community_gallery_dialog():
    """Show community theme gallery with bundled popular themes."""
    dlg = QDialog(mw)
    dlg.setWindowTitle("Community Theme Gallery")
    dlg.resize(800, 600)
    layout = QVBoxLayout(dlg)

    header = QLabel("<h3>🌍 Community Theme Gallery</h3>"
                    "<p>Popular color schemes from the community. Click Install to add any theme.</p>")
    header.setWordWrap(True)
    layout.addWidget(header)

    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll_widget = QWidget()
    scroll_layout = QVBoxLayout(scroll_widget)

    for name, palette in COMMUNITY_THEMES.items():
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        frame_layout = QVBoxLayout(frame)

        name_label = QLabel(f"<b>{name}</b>")
        frame_layout.addWidget(name_label)

        # Color preview boxes
        colors_layout = QHBoxLayout()
        for ck in ["bg", "fg", "accent", "button", "input"]:
            cbox = QLabel(ck.upper())
            cbox.setStyleSheet(
                f"background:{palette.get(ck, '#FFF')};"
                f"color:{palette.get('fg', '#000')};"
                f"border:1px solid {palette.get('border', '#CCC')};"
                f"padding:8px; min-width:50px;"
            )
            cbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
            colors_layout.addWidget(cbox)
        frame_layout.addLayout(colors_layout)

        def install_theme(n=name, p=palette):
            save_custom_theme(n, p)
            tooltip(f"✅ '{n}' installed! Find it in Custom Themes.")

        def install_and_apply(n=name, p=palette):
            save_custom_theme(n, p)
            set_theme(n)
            tooltip(f"✅ '{n}' installed and applied!")
            dlg.accept()

        btn_layout = QHBoxLayout()
        inst_btn = QPushButton("Install")
        inst_btn.clicked.connect(install_theme)
        btn_layout.addWidget(inst_btn)

        apply_btn = QPushButton("Install & Apply")
        apply_btn.clicked.connect(install_and_apply)
        btn_layout.addWidget(apply_btn)

        frame_layout.addLayout(btn_layout)
        scroll_layout.addWidget(frame)

    scroll.setWidget(scroll_widget)
    layout.addWidget(scroll)

    # Import from URL section
    url_layout = QHBoxLayout()
    url_layout.addWidget(QLabel("Import from URL:"))
    url_input = QLineEdit()
    url_input.setPlaceholderText("https://example.com/theme.json")
    url_layout.addWidget(url_input)

    def import_from_url():
        url = url_input.text().strip()
        if not url:
            return
        try:
            import urllib.request
            with urllib.request.urlopen(url, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            name = data.get("name", "imported_theme")
            palette = data.get("palette")
            if palette:
                save_custom_theme(name, palette)
                tooltip(f"✅ '{name}' imported from URL!")
            else:
                showInfo("Invalid theme format!")
        except Exception as e:
            showInfo(f"Error importing: {e}")

    fetch_btn = QPushButton("Fetch & Install")
    fetch_btn.clicked.connect(import_from_url)
    url_layout.addWidget(fetch_btn)
    layout.addLayout(url_layout)

    close_btn = QPushButton("Close")
    close_btn.clicked.connect(dlg.reject)
    layout.addWidget(close_btn)

    dlg.exec()

# ====== Feature 15: Seasonal Themes Dialog ======
def show_seasonal_themes_dialog():
    """Show seasonal themes configuration dialog."""
    dlg = QDialog(mw)
    dlg.setWindowTitle("Seasonal Themes")
    dlg.resize(500, 400)
    layout = QVBoxLayout(dlg)

    header = QLabel("<h3>🌿 Seasonal Themes</h3>"
                    "<p>Automatically switch themes based on the current season.</p>")
    header.setWordWrap(True)
    layout.addWidget(header)

    cfg = get_config()
    seasonal = cfg.get("seasonalThemes", {"enabled": False})

    enabled_cb = QCheckBox("Enable seasonal theme switching")
    enabled_cb.setChecked(seasonal.get("enabled", False))
    layout.addWidget(enabled_cb)

    # Show current season
    month = datetime.now().month
    current_season = "Unknown"
    for season, data in SEASONAL_THEMES.items():
        if month in data["months"]:
            current_season = data["label"]
            break

    season_label = QLabel(f"<b>Current season:</b> {current_season}")
    layout.addWidget(season_label)

    # Season-theme mapping
    layout.addWidget(QLabel("<br><b>Season → Theme Mapping:</b>"))
    season_combos = {}
    grid = QGridLayout()
    all_theme_keys = [key for _, key in THEME_OPTIONS + ACCESSIBILITY_THEMES]

    for idx, (season, data) in enumerate(SEASONAL_THEMES.items()):
        grid.addWidget(QLabel(data["label"]), idx, 0)
        combo = QComboBox()
        combo.addItems(all_theme_keys)
        # Set current mapping
        current = seasonal.get(season, data["theme"])
        if current in all_theme_keys:
            combo.setCurrentText(current)
        else:
            combo.setCurrentText(data["theme"])
        season_combos[season] = combo
        grid.addWidget(combo, idx, 1)

    layout.addLayout(grid)

    note = QLabel("Note: When enabled, seasonal themes override your manual theme selection "
                  "and scheduled theme switching.")
    note.setWordWrap(True)
    note.setStyleSheet("font-size:11px; color:gray;")
    layout.addWidget(note)

    layout.addStretch()

    def save_settings():
        new_seasonal = {"enabled": enabled_cb.isChecked()}
        for season, combo in season_combos.items():
            new_seasonal[season] = combo.currentText()
        cfg = get_config()
        cfg["seasonalThemes"] = new_seasonal
        write_config(cfg)
        if enabled_cb.isChecked():
            _check_seasonal_theme()
        tooltip("🌿 Seasonal themes saved!")
        dlg.accept()

    save_btn = QPushButton("Save & Apply")
    save_btn.clicked.connect(save_settings)
    layout.addWidget(save_btn)

    cancel_btn = QPushButton("Cancel")
    cancel_btn.clicked.connect(dlg.reject)
    layout.addWidget(cancel_btn)

    dlg.exec()

def set_theme(theme: Theme):
    """Set the current theme."""
    theme = normalize_theme(theme)
    cfg = get_config()
    cfg["currentTheme"] = theme
    # Selecting a theme implicitly disables follow-system-theme
    cfg["followSystemTheme"] = False
    write_config(cfg)
    apply_theme_everywhere(theme)
    # Record usage statistics
    record_theme_usage(theme)
    # Feature 13: Update status bar
    _update_status_bar()
    # Feature 3: Sync config if enabled
    sync_config_to_media()

def set_font_size(size: int):
    """Set the font size and refresh all views. Valid range: 8-72px."""
    # Validate font size to prevent unreasonable values
    if not (8 <= size <= 72):
        size = 16  # Default fallback
    cfg = get_config()
    cfg["fontSize"] = size
    write_config(cfg)
    apply_theme_everywhere(get_active_theme())
    _update_status_bar()

def add_menu():
    m = mw.form.menuTools.addMenu("Theme: AnkiThemeTwin")

    # ---- Follow System Theme toggle ----
    actFollow = QAction("Follow System Theme (Disable Addon Theming)", mw, checkable=True)
    actFollow.setChecked(is_follow_system_theme())
    def toggle_follow_system(checked):
        set_follow_system_theme(checked)
        if checked:
            tooltip("🖥️ Following system/Anki theme — addon theming disabled", period=2000)
        else:
            tooltip("🎨 Addon theming enabled", period=2000)
    actFollow.triggered.connect(toggle_follow_system)
    m.addAction(actFollow)

    # Feature 5: Zen Mode toggle
    actZen = QAction("🧘 Zen Mode (Distraction-Free)", mw, checkable=True)
    actZen.setChecked(get_zen_mode())
    actZen.triggered.connect(lambda _: toggle_zen_mode())
    m.addAction(actZen)

    m.addSeparator()

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

    # Feature 14: Community Gallery
    actGallery = QAction("🌍 Community Theme Gallery...", mw)
    actGallery.triggered.connect(show_community_gallery_dialog)
    m.addAction(actGallery)

    m.addSeparator()

    # ---- Eye Comfort & Filters ----
    actBlueLight = QAction("🔆 Blue Light Filter...", mw)
    actBlueLight.triggered.connect(show_blue_light_dialog)
    m.addAction(actBlueLight)

    actAmbient = QAction("🌅 Ambient Light Auto-Adjust...", mw)
    actAmbient.triggered.connect(show_ambient_light_dialog)
    m.addAction(actAmbient)

    # Feature 12: Match Card Background toggle
    actMatchBg = QAction("🎯 Match Card Background", mw, checkable=True)
    actMatchBg.setChecked(get_match_card_background())
    actMatchBg.triggered.connect(lambda _: toggle_match_card_background())
    m.addAction(actMatchBg)

    m.addSeparator()

    # ---- Scheduling & Automation ----
    actScheduled = QAction("Scheduled Theme Switching...", mw)
    actScheduled.triggered.connect(show_scheduled_themes_dialog)
    m.addAction(actScheduled)

    actDeckThemes = QAction("Per-Deck Themes...", mw)
    actDeckThemes.triggered.connect(show_deck_themes_dialog)
    m.addAction(actDeckThemes)

    # Feature 4: Note-Type Styling
    actNoteType = QAction("📝 Note Type Styling...", mw)
    actNoteType.triggered.connect(show_note_type_styling_dialog)
    m.addAction(actNoteType)

    # Feature 6: Theme Rotation
    actRotation = QAction("🔄 Theme Rotation...", mw)
    actRotation.triggered.connect(show_rotation_dialog)
    m.addAction(actRotation)

    # Feature 15: Seasonal Themes
    actSeasonal = QAction("🌿 Seasonal Themes...", mw)
    actSeasonal.triggered.connect(show_seasonal_themes_dialog)
    m.addAction(actSeasonal)

    m.addSeparator()

    # ---- Visual & Animation ----
    actAnimations = QAction("Animation Settings...", mw)
    actAnimations.triggered.connect(show_animation_settings)
    m.addAction(actAnimations)

    actVisualEnhancements = QAction("Visual Enhancements...", mw)
    actVisualEnhancements.triggered.connect(show_visual_enhancements_dialog)
    m.addAction(actVisualEnhancements)

    # Feature 7: Custom CSS
    actCustomCSS = QAction("🎨 Custom CSS...", mw)
    actCustomCSS.triggered.connect(show_custom_css_dialog)
    m.addAction(actCustomCSS)

    m.addSeparator()

    # ---- Study & Quick Access ----
    actStudyMode = QAction("Study Session Modes...", mw)
    actStudyMode.triggered.connect(show_study_mode_dialog)
    m.addAction(actStudyMode)

    # Feature 1: Pomodoro Timer
    actPomodoro = QAction("⏱️ Pomodoro Timer...", mw)
    actPomodoro.triggered.connect(show_pomodoro_dialog)
    m.addAction(actPomodoro)

    actQuickSettings = QAction("Quick Settings Panel...", mw)
    actQuickSettings.triggered.connect(show_quick_settings_panel)
    m.addAction(actQuickSettings)

    m.addSeparator()

    # ---- Configuration & Sync ----
    actBackup = QAction("Backup & Restore...", mw)
    actBackup.triggered.connect(show_backup_restore_dialog)
    m.addAction(actBackup)

    # Feature 3: Theme Sync
    actSync = QAction("🔄 Theme Sync...", mw)
    actSync.triggered.connect(show_sync_dialog)
    m.addAction(actSync)

    actStatistics = QAction("Usage Statistics...", mw)
    actStatistics.triggered.connect(show_statistics_dialog)
    m.addAction(actStatistics)

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

# ---------------- Visual Feedback ----------------
def show_shortcut_feedback(message: str, icon: str = "⚡"):
    """Show enhanced visual feedback for keyboard shortcuts."""
    tooltip(f"{icon} {message}", period=1500)

def setup_keyboard_shortcuts():
    """Setup keyboard shortcuts for quick theme switching."""
    # Ctrl+Shift+1 through Ctrl+Shift+7 for the main themes
    theme_keys = [key for _, key in THEME_OPTIONS]
    for i, theme_key in enumerate(theme_keys[:7], 1):
        shortcut = QShortcut(QKeySequence(f"Ctrl+Shift+{i}"), mw)
        def activate_theme(k=theme_key, num=i):
            set_theme(k)
            show_shortcut_feedback(f"Theme {num}: {k.replace('_', ' ').title()}", "🎨")
        shortcut.activated.connect(activate_theme)

    # Ctrl+Shift+= for increasing font size
    increase_font = QShortcut(QKeySequence("Ctrl+Shift+="), mw)
    def increase_size():
        current = get_font_size()
        new_size = min(current + 2, 32)
        set_font_size(new_size)
        show_shortcut_feedback(f"Font size increased to {new_size}px", "📈")
    increase_font.activated.connect(increase_size)

    # Ctrl+Shift+- for decreasing font size
    decrease_font = QShortcut(QKeySequence("Ctrl+Shift+-"), mw)
    def decrease_size():
        current = get_font_size()
        new_size = max(current - 2, 8)
        set_font_size(new_size)
        show_shortcut_feedback(f"Font size decreased to {new_size}px", "📉")
    decrease_font.activated.connect(decrease_size)

    # Feature 5: Ctrl+Shift+Z for Zen Mode toggle
    zen_shortcut = QShortcut(QKeySequence("Ctrl+Shift+Z"), mw)
    zen_shortcut.activated.connect(toggle_zen_mode)

# ====== Feature 10: Right-Click Context Menu ======
def _on_webview_context_menu(webview, menu):
    """Add theme switching options to webview right-click context menu."""
    if is_follow_system_theme():
        return

    theme_menu = QMenu("🎨 AnkiThemeTwin", menu)

    # Quick theme options
    for label, key in THEME_OPTIONS[:5]:
        act = QAction(label, theme_menu)
        act.triggered.connect(lambda _, k=key: set_theme(k))
        theme_menu.addAction(act)

    theme_menu.addSeparator()

    # Favorite themes
    favorites = get_favorite_themes()
    if favorites:
        for fav in favorites[:5]:
            if fav in PALETTES:
                act = QAction(f"★ {fav.replace('_', ' ').title()}", theme_menu)
                act.triggered.connect(lambda _, f=fav: set_theme(f))
                theme_menu.addAction(act)
        theme_menu.addSeparator()

    # Quick toggles
    zen_act = QAction("🧘 Toggle Zen Mode", theme_menu)
    zen_act.triggered.connect(toggle_zen_mode)
    theme_menu.addAction(zen_act)

    # Font size submenu
    font_sub = QMenu("Font Size", theme_menu)
    for label, size in [("Small (14px)", 14), ("Medium (16px)", 16), ("Large (20px)", 20), ("Huge (24px)", 24)]:
        act = QAction(label, font_sub)
        act.triggered.connect(lambda _, s=size: set_font_size(s))
        font_sub.addAction(act)
    theme_menu.addMenu(font_sub)

    # Blue light filter quick options
    bl_sub = QMenu("🔆 Blue Light Filter", theme_menu)
    for label, val in [("Off", 0), ("Light (20%)", 20), ("Medium (40%)", 40), ("Strong (60%)", 60), ("Max (80%)", 80)]:
        act = QAction(label, bl_sub)
        act.triggered.connect(lambda _, v=val: set_blue_light_filter(v))
        bl_sub.addAction(act)
    theme_menu.addMenu(bl_sub)

    menu.addSeparator()
    menu.addMenu(theme_menu)

# ====== Feature 4: Reviewer hook for note-type CSS ======
def _on_reviewer_did_show_answer(card):
    """Apply note-type specific styling when reviewing."""
    _apply_note_type_styling_for_card(card)

def _on_reviewer_did_show_question(card):
    """Apply note-type specific styling when question is shown."""
    _apply_note_type_styling_for_card(card)
    # Feature 6: Check theme rotation on each card
    _check_theme_rotation()

def _apply_note_type_styling_for_card(card):
    """Apply note-type specific CSS for the current card."""
    styles = get_note_type_styles()
    if not styles:
        return
    try:
        note = card.note()
        model = note.note_type()
        if model:
            nt_name = model.get("name", "")
            css = _get_note_type_css(nt_name)
            if css:
                js = (
                    "(function(){"
                    "var sid='ankithemetwin-notetype';"
                    "var el=document.getElementById(sid);"
                    "if(!el){el=document.createElement('style');el.id=sid;document.head.appendChild(el);}"
                    f"el.textContent={json.dumps(css)};"
                    "})();"
                )
                mw.reviewer.web.eval(js)
    except (AttributeError, Exception):
        pass

def on_profile_open():
    if not getattr(mw, "_ankitwin_menu", False):
        add_menu()
        setup_keyboard_shortcuts()
        # Load custom themes from config
        custom_themes = get_custom_themes()
        for name, palette in custom_themes.items():
            PALETTES[name] = palette
        mw._ankitwin_menu = True

    # Feature 3: Sync config from media if available
    sync_config_from_media()

    # Feature 15: Check seasonal theme
    _check_seasonal_theme()

    # Check scheduled theme on startup
    check_scheduled_theme()

    # Feature 9: Apply ambient light filter
    _apply_ambient_light()

    # Apply current theme
    apply_theme_everywhere(get_active_theme())

    # Feature 13: Update status bar
    _update_status_bar()

    # Feature 1: Start Pomodoro timer if enabled
    settings = get_pomodoro_settings()
    if settings.get("enabled"):
        _start_pomodoro_timer()

    # Feature 6: Start rotation timer if enabled
    _start_rotation_timer()

    # Set up timer to check scheduled themes every 5 minutes
    if not hasattr(mw, "_ankitwin_timer"):
        timer = QTimer(mw)
        timer.timeout.connect(check_scheduled_theme)
        timer.start(300000)  # 5 minutes in milliseconds
        mw._ankitwin_timer = timer

    # Feature 9: Timer for ambient light updates every 10 minutes
    if not hasattr(mw, "_ankitwin_ambient_timer"):
        ambient_timer = QTimer(mw)
        ambient_timer.timeout.connect(_apply_ambient_light)
        ambient_timer.start(600000)  # 10 minutes
        mw._ankitwin_ambient_timer = ambient_timer

gui_hooks.profile_did_open.append(on_profile_open)
gui_hooks.webview_will_set_content.append(inject_css)
gui_hooks.browser_will_show.append(on_browser_will_show)
gui_hooks.editor_did_load_note.append(on_editor_did_load_note)
gui_hooks.theme_did_change.append(on_theme_did_change)

# Feature 10: Right-click context menu
try:
    gui_hooks.webview_will_show_context_menu.append(_on_webview_context_menu)
except AttributeError:
    pass  # Hook not available in older Anki versions

# Feature 4/6: Reviewer card hooks for note-type styling and rotation
try:
    gui_hooks.reviewer_did_show_question.append(_on_reviewer_did_show_question)
    gui_hooks.reviewer_did_show_answer.append(_on_reviewer_did_show_answer)
except AttributeError:
    pass
