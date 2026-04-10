# Changelog

All notable changes to AnkiThemeTwin will be documented in this file.

## [1.6.0] - 2026-04-10

### Added - 15 New Features + Background Textures

#### Background Textures (Visual Enhancements)
- Added 6 new CSS-only background textures: Diagonal Lines, Crosshatch, Paper, Linen, Diamond, Waves
- All textures are subtle, study-friendly, and use no external images
- Accessible via Tools > Theme: AnkiThemeTwin > Visual Enhancements
- Extends existing patterns (Dots, Grid, Horizontal Lines, Subtle Gradient)

#### Feature 1: Pomodoro / Break Reminder
- Configurable study timer with break reminders
- Adjustable study duration (5–120 min) and break duration (1–30 min)
- Auto-restart option after breaks
- Dialog with start/stop controls
- Menu: ⏱️ Pomodoro Timer...

#### Feature 2: Blue Light Filter
- Adjustable warm tint overlay (0–100% intensity)
- Uses CSS overlay with `mix-blend-mode:multiply` for eye comfort
- Slider-based control dialog
- Quick access via right-click context menu
- Menu: 🔆 Blue Light Filter...

#### Feature 3: Theme Sync via AnkiWeb
- Sync settings across devices using Anki's media sync
- Stores config in `collection.media/_ankithemetwin_sync.json`
- Push/Pull controls for manual sync
- Auto-imports on profile open if newer sync file found
- Menu: 🔄 Theme Sync...

#### Feature 4: Note-Type Specific Styling
- Set per-note-type font size, font family, and theme overrides
- Automatically applies when reviewing cards of that note type
- Hooks into `reviewer_did_show_question` and `reviewer_did_show_answer`
- Menu: 📝 Note Type Styling...

#### Feature 5: Zen Mode
- Distraction-free review mode
- Hides toolbar, deck name, card counts, and stats
- Centers card content with generous padding
- Toggle via menu or Ctrl+Shift+Z shortcut
- Menu: 🧘 Zen Mode (Distraction-Free)

#### Feature 6: Theme Rotation
- Auto-rotate through selected themes
- Card-based interval (every N cards reviewed)
- Time-based interval (every N minutes)
- Select which themes to include in rotation
- Menu: 🔄 Theme Rotation...

#### Feature 7: Custom CSS Injection
- Textarea for user CSS that's injected after theme styles
- Supports `--att-*` CSS custom properties from current theme
- Syntax hints and variable reference in dialog
- Menu: 🎨 Custom CSS...

#### Feature 8: Theme-Aware Card Template Helper
- Exposes `--att-*` CSS custom properties for card templates
- Variables: `--att-bg`, `--att-fg`, `--att-accent`, `--att-border`, `--att-button`, `--att-input`, `--att-hover`, `--att-selection`, `--att-font-size`, `--att-font-family`, `--att-line-height`, `--att-letter-spacing`
- Allows card templates to adapt to the user's chosen theme
- Documented in About dialog

#### Feature 9: Ambient Light Auto-Adjust
- Automatic blue light filter based on time of day
- Cosine interpolation: strongest at midnight, lightest at noon
- Configurable min/max filter range
- Updates every 10 minutes automatically
- Menu: 🌅 Ambient Light Auto-Adjust...

#### Feature 10: Right-Click Context Menu
- Quick theme switching from any webview right-click menu
- Shows top 5 themes and favorite themes
- Quick toggles for Zen Mode
- Font size submenu
- Blue light filter presets
- Uses `webview_will_show_context_menu` hook

#### Feature 11: More Transition Animations
- 4 animation styles: Fade, Slide, Morph (Elastic), Zoom
- Each uses distinct CSS easing curves
- New CSS keyframes: slideIn, zoomIn, morphIn
- Updated Animation Settings dialog with all options

#### Feature 12: Match Card Background
- Detects card template's background color via JavaScript
- Adapts page background to match the card
- Useful for cards with custom backgrounds
- Toggle via menu checkbox
- Menu: 🎯 Match Card Background

#### Feature 13: Status Bar Indicator
- Shows current theme name, font size, and active features
- Updates when theme changes, font size changes, etc.
- Shows blue light filter and Zen mode status
- Persistent QLabel in Anki's status bar
- Configurable via `statusBarIndicator` setting

#### Feature 14: Community Theme Gallery
- 8 bundled community themes (Solarized Light, Nord Light, Rosé Pine Dawn, Gruvbox Light, Catppuccin Latte, Tokyo Night Light, Everforest Light, Dracula Light)
- One-click install or install & apply
- Import themes from URL (JSON format)
- Menu: 🌍 Community Theme Gallery...

#### Feature 15: Seasonal Themes
- Automatic theme switching based on season
- Spring → Olive Green, Summer → Blue Light, Autumn → Sepia Special, Winter → Gray Word
- Customizable season-to-theme mapping
- Menu: 🌿 Seasonal Themes...

### Changed
- Updated to version 1.6.0
- Menu reorganized with new sections: Eye Comfort & Filters, Scheduling & Automation, Visual & Animation, Configuration & Sync
- About dialog updated with all new features
- Animation Settings dialog updated with 4 animation styles
- Status bar integration for live theme info

## [1.5.2] - 2026-04-10

### Fixed - OS Theme Override on All Windows (Not Just Browser)

#### Delayed Theme Re-assertion
- **Multiple timer re-assertions (200ms, 800ms, 1500ms)**: When OS theme switches, Anki reloads webviews AFTER firing the `theme_did_change` hook. Our handler now re-applies the addon theme at multiple delays to ensure it wins the race against Anki's own reload cycle.

#### Comprehensive Window Refresh
- **All open windows refreshed**: `refresh_all_webviews()` now scans ALL visible top-level windows (AddCards, EditCurrent, Stats, Preferences, etc.) and re-applies QSS and webview CSS - not just the Browser window.
- **QWebEngineView scan**: Finds and re-injects CSS into any QWebEngineView inside open dialogs.
- **Editor detection in all dialogs**: Finds editor components in any dialog (AddCards, EditCurrent) and re-injects Shadow DOM styles.
- **Main window QSS**: `apply_theme_everywhere()` now also sets QSS directly on the main window to override per-widget stylesheets Anki may set.
- **Reviewer refresh**: Explicitly refreshes reviewer webview and bottom bar when active.

#### QPalette for All Color Groups
- **Active/Inactive/Disabled color groups**: The Qt QPalette now sets colors for all three color groups, preventing the OS from overriding any widget state with dark colors.

## [1.5.1] - 2026-04-10

### Fixed - Windows 11 Dark/Light Theme Override

#### Anki ThemeManager Override
- **`force_anki_theme_mode()`**: Forces `theme_manager.night_mode` to match our theme (light/dark), preventing Windows 11 dark mode from overriding addon colors
- **Qt `QPalette` override**: Forces the Qt application palette to use our theme colors, preventing OS dark palette from bleeding into native widgets (sidebar, table, inputs)
- **`theme_did_change` hook**: Re-applies addon theme whenever Anki detects an OS theme change (Windows dark↔light switch), so the addon always retains control

#### Night Mode CSS Neutralization
- **`.nightMode` / `.night_mode` body class overrides**: Added comprehensive CSS rules that override Anki's dark mode body class styling for all elements (cards, inputs, tables, fields, text, buttons)
- **Reviewer night mode overrides**: Ensures card content, answer text, and bottom bar remain visible with correct font colors in dark OS mode
- **All webview contexts**: Night mode overrides apply to all contexts (DeckBrowser, Reviewer, Editor, Overview, Browser, Toolbar)

## [1.5.0] - 2026-04-10

### Fixed - Browser Window Complete Theming

#### Browser Sidebar & Qt Widget Theming
- **`browser_will_show` hook**: Added targeted QSS styling that applies directly to the Browser window's native Qt widgets (sidebar QTreeView, card table QTableView, filter QLineEdit), overriding Anki's ThemeManager
- **Enhanced QTreeView styling**: Added item, branch, selected, and hover state QSS rules for the sidebar tree (Saved Searches, Today, Flags, Card State, Decks, Tags sections)
- **QHeaderView section hover**: Added hover state for column headers in the card table

#### Editor Fields & Shadow DOM Theming
- **Shadow DOM injection**: Added JavaScript injection to penetrate `<anki-editable>` Shadow DOM elements, styling the actual editable content inside editor fields (Front, Back, PageInfo, Tags)
- **`editor_did_load_note` hook**: Added hook to re-inject shadow DOM styles whenever a note is loaded in the editor
- **MutationObserver**: Added automatic re-injection when new fields are dynamically added to the editor
- **Svelte component overrides**: Added CSS targeting for Svelte-based editor components: field labels, tag editor, toolbar buttons, note-type/deck selectors, collapse icons, plain-text badges, editor-field containers

#### Anki CSS Custom Property Overrides
- **50+ CSS custom properties**: Override Anki's built-in CSS variables at `:root` level (`--canvas`, `--fg`, `--border`, `--button-bg`, `--frame-bg`, `--window-bg`, `--selected-bg`, `--badge-bg`, `--highlight-bg`, etc.) so Svelte components inherit theme colors
- **ThemeManager conflict resolution**: Theme colors now override Anki's ThemeManager CSS variables with `!important`, ensuring consistent theming across all rendering layers

#### Live Theme Refresh
- **Browser window refresh**: Theme switching now re-applies QSS to any open Browser windows and refreshes editor webviews inside them
- **Shadow DOM refresh**: Theme switching re-injects styles into Shadow DOM elements in open editors

## [1.4.0] - 2026-04-09

### Added - Major Feature Release

#### Phase 1: Accessibility & Customization
- **6 New Accessibility Themes**:
  - High Contrast Light - Maximum contrast for visual impairments
  - High Contrast Dark - Dark mode with high contrast
  - Dyslexia Friendly - Yellow background optimized for dyslexic readers
  - Deuteranopia Support - Color blindness optimized (red-green)
  - Protanopia Support - Color blindness optimized (red-green variant)
  - Tritanopia Support - Color blindness optimized (blue-yellow)

- **Custom Theme Creator**:
  - Visual color picker for all theme elements
  - Create unlimited custom themes
  - Export themes as JSON files
  - Import themes from JSON files
  - Share themes with other users

- **Theme Presets System**:
  - Save favorite theme + font combinations
  - Quick-load presets
  - Manage multiple presets
  - Perfect for switching between study environments

- **Theme Preview Gallery**:
  - Visual preview of all themes before applying
  - See color palettes at a glance
  - One-click theme application

- **Advanced Font Customization**:
  - Custom font family selection
  - Font size slider (8-32px)
  - Line height adjustment (100-300%)
  - Letter spacing control (-5px to +10px)
  - 7 font size presets (12, 14, 16, 18, 20, 22, 24px)

#### Phase 2: Intelligent Features
- **Scheduled Theme Switching**:
  - Auto-switch themes based on time of day
  - Configure 4 time periods (morning, afternoon, evening, night)
  - Each period can have its own theme
  - Perfect for adapting to lighting conditions

- **Per-Deck Themes**:
  - Set different themes for different decks
  - Auto-switch when reviewing specific decks
  - Great for context switching between subjects

- **Keyboard Shortcuts**:
  - Ctrl+Shift+1-7: Quick theme switching
  - Ctrl+Shift+=: Increase font size
  - Ctrl+Shift+-: Decrease font size
  - Enhanced visual feedback with icons

- **Animation Settings**:
  - Configurable theme transition animations
  - Adjustable animation duration (100-2000ms)
  - Multiple animation styles (fade, instant)

#### Phase 3: Power User Features
- **Study Session Modes**:
  - Normal Mode - Standard settings
  - Focus Mode - Larger text, higher contrast for concentration
  - Speed Mode - Compact layout for rapid reviews
  - Detail Mode - Maximum readability for complex material

- **Quick Settings Panel**:
  - Combined controls for theme, font, and mode
  - Favorite theme quick access
  - One-click preset application

- **Configuration Backup & Restore**:
  - Export complete configuration to JSON
  - Import configuration from backup
  - Versioned backups with timestamps
  - Safely migrate settings between devices

- **Theme Usage Statistics**:
  - Track theme usage patterns
  - View most-used themes
  - Last used timestamps
  - Usage count per theme

- **Theme Organization**:
  - Mark themes as favorites
  - Add tags to themes for categorization
  - Quick filter by favorites

#### Phase 4: Visual Enhancements
- **CSS Transitions & Animations**:
  - Smooth transitions on all interactive elements
  - Configurable animation duration
  - Card fade-in animations
  - Modal dialog entrance effects
  - Hover state transitions

- **Enhanced Visual Depth**:
  - Card shadows for depth perception
  - Layered shadow effects on buttons
  - Elevated focus states
  - Gradient overlays on buttons and headers

- **Button Press Effects**:
  - Transform animations on click
  - Inset shadows for pressed state
  - Elevation changes on hover
  - Smooth state transitions

- **Advanced Focus Indicators**:
  - Multi-layer box shadows
  - Scale transformations on focus
  - Accent color glow effects
  - Enhanced visibility for accessibility

- **Gradient Enhancements**:
  - Linear gradients on buttons
  - Gradient scrollbar thumbs
  - Gradient table headers
  - Subtle accent gradients

- **Background Patterns**:
  - 5 pattern options: None, Subtle, Dots, Grid, Lines
  - Subtle texture without affecting readability
  - Configurable via Visual Enhancements dialog
  - Pattern colors adapt to current theme

- **Scrollbar Enhancements**:
  - Gradient scrollbar thumbs
  - Hover glow effects
  - Rounded, modern design
  - Border spacing for clarity

- **Improved Typography**:
  - Heading underlines with accent colors
  - Font weight adjustments
  - Gradient horizontal rules
  - Better text hierarchy

- **Modal & Dropdown Improvements**:
  - Entrance animations
  - Enhanced shadows for depth
  - Rounded corners
  - Slide-in effects on dropdown items
  - Border accent on selected items

- **Enhanced Keyboard Shortcut Feedback**:
  - Icon-based visual notifications
  - Themed notification messages
  - Extended display duration (1500ms)
  - Descriptive action feedback

### Changed
- Updated to version 1.4.0
- Menu reorganized with new submenus for better organization
- About dialog updated with new features list
- Theme count increased from 7 to 13+ (plus unlimited custom themes)

### Improved
- Better accessibility for users with visual impairments
- More flexible theming options
- Enhanced user experience with previews and presets
- Automatic theme adaptation with scheduling
- More control over typography

## [1.3.0] - 2026-04-09

### Removed
- **Dark Themes**: Removed all dark themes to focus on light, eye-comfort themes
  - Removed Dark • Warm (Soft)
  - Removed Dark • Neutral (Soft)
  - Removed True Black (OLED)
- **System Theme Detection**: Removed automatic dark/light mode switching
  - Removed "Follow System Theme" toggle
  - Removed system color scheme detection
  - Removed "Light Mode Theme" and "Dark Mode Theme" submenus
- Simplified configuration by removing `followSystem`, `lightTheme`, and `darkTheme` options

### Changed
- Updated to version 1.3.0
- Simplified menu structure - direct theme selection only
- Updated About dialog to reflect 7 light themes
- Updated README with light-theme-only recommendations
- Streamlined configuration to `currentTheme` and `fontSize` only

### Benefits
- Cleaner, more focused user experience
- Simplified codebase (removed ~130 lines of code)
- Faster theme application without system detection overhead
- All themes now optimized for readability and eye comfort in various lighting conditions

## [1.2.0] - 2026-04-09

### Added
- **3 New Themes**:
  - Blue Light (Evening) - Cool blue tones for evening study, reduces eye strain
  - Olive Green (Natural) - Warm natural tones for extended sessions
  - True Black (OLED) - Perfect for OLED screens with pure black background
- **Configurable Font Sizes**: Choose from Small (14px), Medium (16px), Large (18px), or Extra Large (20px)
- **Comprehensive CSS Styling** for webviews:
  - Enhanced buttons with hover states
  - Styled input fields with focus indicators
  - Table styling with header emphasis
  - Card content optimization
  - Editor field improvements
  - Code block styling
  - Custom scrollbar design
- **Enhanced Qt/QSS Styling** for native widgets:
  - All button types with states (hover, pressed, disabled)
  - Input fields (QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox)
  - Combo boxes with dropdown styling
  - Tables and lists with alternating colors
  - Menu bar and menu items
  - Scrollbars (vertical and horizontal)
  - Tabs with selection states
  - Checkboxes and radio buttons
  - Sliders with custom handles
  - Toolbars and tool buttons
  - Status bars
  - Progress bars
  - Dialogs
  - Tooltips
  - Group boxes
  - Splitters
- **Context-Specific Styling**: Different CSS for DeckBrowser, Reviewer, Editor, Overview, Browser, and Toolbars
- **Theme Recommendations Guide** in README:
  - By environment (sunlight, office, evening, night)
  - By device type (OLED, LCD, e-ink)
  - By preference (warm/cool tones, contrast)
  - Font size recommendations

### Changed
- Increased version to 1.2.0
- Updated About dialog to reflect new features
- Improved CSS injection to be context-aware
- Enhanced QSS to cover all major Qt widget types

### Improved
- Better readability across all Anki pages
- More consistent styling between webviews and native UI
- Better focus indicators for accessibility
- Smoother hover and interaction states

## [1.1.1] - 2026-04-09

### Fixed
- Compatibility with Anki standards
- Manifest.json structure updated

## [1.1.0] - Initial Release

### Added
- 7 high-readability themes (Sepia Word, Sepia Paper, Sepia Special, Gray Word, Gray Paper, and 2 dark themes)
- Follow System Theme feature
- Instant theme updates without restart
- System dark mode detection
- About dialog with project information
- Menu integration in Tools menu
