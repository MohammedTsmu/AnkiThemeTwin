# Changelog

All notable changes to AnkiThemeTwin will be documented in this file.

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
