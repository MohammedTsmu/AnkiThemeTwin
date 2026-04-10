# AnkiThemeTwin Config

- `currentTheme`: The selected theme. One of `"sepia_word"`, `"sepia_paper"`, `"sepia_special"`, `"gray_word"`, `"gray_paper"`, `"blue_light"`, `"olive_green"`, `"high_contrast_light"`, `"high_contrast_dark"`, `"dyslexia_friendly"`, `"deuteranopia"`, `"protanopia"`, `"tritanopia"`, or any custom theme name. Default: `"sepia_special"`.

- `fontSize`: Font size in pixels for webview content. Range: 8–32. Default: `16`.

- `followSystemTheme`: When `true`, addon theming is disabled and Anki's native dark/light mode controls the appearance. Default: `false`.

- `fontFamily`: CSS font-family string for webview content. Default: `"Segoe UI,Amiri,Arial,sans-serif"`.

- `lineHeight`: Line height multiplier for webview text. Range: 1.0–3.0. Default: `1.58`.

- `letterSpacing`: Letter spacing in pixels. Range: -5 to 10. Default: `0.0`.

- `presets`: List of saved theme preset objects (each with name, theme, font settings). Default: `[]`.

- `customThemes`: Dictionary of user-created themes. Keys are theme names, values are palette color dictionaries. Default: `{}`.

- `scheduledThemes`: Configuration for automatic time-based theme switching. Contains `enabled` (bool, default: `false`) and four period objects (`morning`, `afternoon`, `evening`, `night`), each with `time` (HH:MM) and `theme` (theme name). See `config.json` for the full default structure.

- `deckThemes`: Dictionary mapping deck names to theme names for per-deck theming. Default: `{}`.

- `animations`: Animation settings object with `enabled` (bool), `duration` (ms, 100–2000), and `style` (`"fade"`, `"slide"`, `"morph"`, `"zoom"`, or `"none"`). Default: enabled at 300ms with fade.

- `backgroundPattern`: Background pattern overlay. One of `"none"`, `"subtle"`, `"dots"`, `"grid"`, or `"lines"`. Default: `"none"`.

- `studyMode`: Study session display mode. One of `"normal"`, `"focus"`, `"speed"`, or `"detail"`. Default: `"normal"`.

- `favoriteThemes`: List of theme names marked as favorites. Default: `[]`.

- `themeTags`: Dictionary mapping theme names to lists of user-defined tags. Default: `{}`.

- `themeStats`: Local usage statistics. Dictionary mapping theme names to objects with `count` and `last_used`. Default: `{}`.

- `pomodoroSettings`: Pomodoro break reminder timer. Object with `enabled` (bool), `studyMinutes` (5–120, default: 25), `breakMinutes` (1–30, default: 5), and `autoStart` (bool, default: false). Default: disabled.

- `blueLightFilter`: Blue light filter intensity percentage. Range: 0–100. 0 = off, 100 = maximum warm tint. Default: `0`.

- `syncEnabled`: When `true`, theme settings are synced across devices via AnkiWeb's media sync (stored in `collection.media/_ankithemetwin_sync.json`). Default: `false`.

- `noteTypeStyles`: Dictionary mapping note type names to style override objects. Each override may contain `fontSize` (int), `fontFamily` (string), `lineHeight` (float), and `theme` (theme name). Default: `{}`.

- `zenMode`: When `true`, enables distraction-free review mode — hides toolbars, card counts, and centers the card. Toggle with Ctrl+Shift+Z. Default: `false`.

- `themeRotation`: Theme rotation settings. Object with `enabled` (bool), `themes` (list of theme names to rotate through), `intervalCards` (rotate every N cards, 0 = disabled), and `intervalMinutes` (rotate every N minutes, 0 = disabled). Default: disabled.

- `customCSS`: User-provided CSS string injected after theme styles. Use `--att-*` CSS custom properties to reference theme colors in your CSS. Default: `""`.

- `ambientLightAuto`: Automatic blue light filter based on time of day. Object with `enabled` (bool), `minFilter` (0–100, applied at noon), and `maxFilter` (0–100, applied at midnight). Uses cosine interpolation. Default: disabled with 0–60 range.

- `matchCardBackground`: When `true`, detects the card template's background color and adapts the page background to match. Default: `false`.

- `statusBarIndicator`: When `true`, shows current theme name, font size, and active features in Anki's status bar. Default: `true`.

- `seasonalThemes`: Automatic seasonal theme switching. Object with `enabled` (bool) and optional per-season theme overrides (`spring`, `summer`, `autumn`, `winter`). Default themes: Spring→olive_green, Summer→blue_light, Autumn→sepia_special, Winter→gray_word. Default: disabled.
