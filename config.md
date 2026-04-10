# AnkiThemeTwin Config

- `currentTheme`: The selected theme. One of `"sepia_word"`, `"sepia_paper"`, `"sepia_special"`, `"gray_word"`, `"gray_paper"`, `"blue_light"`, `"olive_green"`, `"high_contrast_light"`, `"high_contrast_dark"`, `"dyslexia_friendly"`, `"deuteranopia"`, `"protanopia"`, `"tritanopia"`, or any custom theme name. Default: `"sepia_special"`.

- `fontSize`: Font size in pixels for webview content. Range: 8–72. Default: `16`.

- `followSystemTheme`: When `true`, addon theming is disabled and Anki's native dark/light mode controls the appearance. Default: `false`.

- `fontFamily`: CSS font-family string for webview content. Default: `"Segoe UI,Amiri,Arial,sans-serif"`.

- `lineHeight`: Line height multiplier for webview text. Range: 1.0–3.0. Default: `1.58`.

- `letterSpacing`: Letter spacing in pixels. Range: -5 to 10. Default: `0.0`.

- `presets`: List of saved theme preset objects (each with name, theme, font settings). Default: `[]`.

- `customThemes`: Dictionary of user-created themes. Keys are theme names, values are palette color dictionaries. Default: `{}`.

- `scheduledThemes`: Configuration for automatic time-based theme switching. Contains `enabled` (bool) and four period objects (`morning`, `afternoon`, `evening`, `night`), each with `time` (HH:MM) and `theme` (theme name). Default: disabled.

- `deckThemes`: Dictionary mapping deck names to theme names for per-deck theming. Default: `{}`.

- `animations`: Animation settings object with `enabled` (bool), `duration` (ms, 100–2000), and `style` (`"fade"` or `"none"`). Default: enabled at 300ms with fade.

- `backgroundPattern`: Background pattern overlay. One of `"none"`, `"subtle"`, `"dots"`, `"grid"`, or `"lines"`. Default: `"none"`.

- `studyMode`: Study session display mode. One of `"normal"`, `"focus"`, `"speed"`, or `"detail"`. Default: `"normal"`.

- `favoriteThemes`: List of theme names marked as favorites. Default: `[]`.

- `themeTags`: Dictionary mapping theme names to lists of user-defined tags. Default: `{}`.

- `themeStats`: Local usage statistics. Dictionary mapping theme names to objects with `count` and `last_used`. Default: `{}`.
