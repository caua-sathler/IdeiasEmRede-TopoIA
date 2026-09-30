# Dashboard Source Files

Source templates and build scripts used to compile [`../pt-br-dashboard.html`](../pt-br-dashboard.html) and [`../en-dashboard.html`](../en-dashboard.html).

## Files

| File | Content |
|---|---|
| `dashboard_data.json` | Pseudonymised (LGPD) snapshot of the paper's data. Serves as the single data input for the build; the `_fonte` key indicates the source script/table for each block. |
| `template_pt-br.html`, `template_en.html` | Page markup, CSS styles, and vanilla JavaScript visualization logic for both language versions. |
| `deck.css`, `deck.js` | Presentation mode (`#slides`): horizontal deck, entrance animations and scripted steps for the pitch video. Shared by both languages; the UI strings live in `L.deck` inside each template. Must stay ASCII. |
| `build.py` | Injects `dashboard_data.json`, `deck.css` and `deck.js` into both templates and writes the standalone ASCII pages to `../` (uses only Python standard library; reads nothing outside `dashboard/`). |

## Compilation

```bash
python build.py
```

Generated HTML pages are 100% ASCII-compatible (accents converted to HTML entities and JS unicode escapes), ensuring identical rendering across all browsers and file servers.
