# Interactive Dashboard

This directory contains standalone, interactive HTML dashboards illustrating the core findings, empirical cases, and theoretical mechanisms of the paper:
**"Who Said It? Speaker-Conditioned Verification and Lexicographic Tie-Breaking for Low-Cost Hallucination Detection in Legislative Hearings"**.

## Available Dashboards

Two self-contained, bilingual dashboards are provided at the root of this folder:
- **[`en-dashboard.html`](en-dashboard.html)**: English version.
- **[`pt-br-dashboard.html`](pt-br-dashboard.html)**: Portuguese (pt-BR) version.

Both pages require **zero dependencies**, run completely offline, and can be opened directly in any modern web browser (`double-click` or `file:///`).

---

## Directory Structure

```
dashboard/
├── en-dashboard.html       # Compiled English standalone interactive dashboard
├── pt-br-dashboard.html    # Compiled Portuguese standalone interactive dashboard
└── src/
    ├── template_en.html    # HTML/JS template for the English dashboard
    ├── template_pt-br.html # HTML/JS template for the Portuguese dashboard
    ├── dashboard_data.json # Pseudonymised (LGPD) snapshot of the paper's data
    ├── deck.css, deck.js   # Presentation mode (#slides), injected into both pages
    ├── build.py            # Standard-library Python compiler script
    └── README.md           # Source and build documentation
```

---

## Interactive Modules Included

The dashboards provide interactive visualizations for all seven key claims of the paper:
1. **Misattribution Walkthrough (Turn-by-Turn)**: Interactive speech strip showing why global cosine matching fails on Deputy B ($0.783$) while the attributed speaker's turns (Deputy A) drop to $0.386$ (Figure 1).
2. **Committee Tie Structure**: 13-level vote distribution histogram showing why the tie fraction $\tau = 4.65\%$ is concentrated in the 0-vote class (Figure 3).
3. **AUROC Decomposition & Reversals**: Interactive breakdown of the $1.31\text{M}$ pairs, demonstrating why stacking loses AUROC through reversals ($1.33\%$) while lexicographic tie-breaking safely preserves committee order (Table 2).
4. **Judge Budget Ladder**: Interactive slider showing committee performance from 1 to 12 judges, illustrating that 8 judges with lexicographic tie-breaking match the full 12-judge committee (Table 5).
5. **CPU Cost vs. Token Savings**: Measured CPU runtimes (0 calls for cosine features) vs. LLM token consumption.
6. **Human Review Queue**: Interactive risk-coverage curve displaying hallucination recall at different audit budget percentages (Figure 4).
7. **Gain Forecast Validation**: Interactive scatterplot validating the theoretical gain identity $\tau(\alpha - \frac{1}{2})$ across 50 held-out splits (Table 6).

---

## Presentation Mode

Open either page with `#slides` at the end of the URL (e.g. `pt-br-dashboard.html#slides`), click **Presentation mode** in the header, or press `P`. The same page becomes a horizontal slide deck in the order of [`../video/pitch_script.md`](../video/pitch_script.md): title, the seven modules (the forecast comes right after the combination rule) and a closing slide. Charts animate in on every visit, and each slide has scripted steps that replay the interactions of the pitch (sweeping the committee size, switching sum ↔ lexicographic, moving the review budget from 10% to 20%, etc.). Everything stays interactive with the mouse.

| Key | Action |
|---|---|
| `→` / `Space` / `PageDown` | next scripted step, then next slide (works with a presentation clicker) |
| `←` / `PageUp` | previous slide (state is reset) |
| `1`–`9`, `Home`, `End` | jump to a slide (`#slides/5` opens slide 5 directly) |
| `C` | camera area: frame + reserved space → reserved space only → off |
| `H` | hide the slide counter, step dots and progress bar |
| `T` | toggle light/dark theme |
| `F` | fullscreen |
| `P` | leave the presentation mode |

The deck is designed on a 1600 px canvas and scaled to the window, so recording at 1920×1080 in fullscreen gives the intended layout. With the camera area on, the text column is kept clear of the bottom-left corner where the webcam overlay goes. `prefers-reduced-motion` disables the animations.

---

## How to Build & Recompile

To rebuild the compiled `.html` files from the templates and data snapshot:

```bash
cd src
python build.py
```

### Compiler Details (`src/build.py`)
- **No external dependencies**: Uses only Python standard library (`json`, `re`, `pathlib`).
- **Encodings**: Generated HTML files are encoded in pure **ASCII** (non-ASCII characters are converted to HTML numeric entities and JavaScript `\uXXXX` escapes). This ensures consistent rendering across any browser, server, or operating system regardless of default charset handling.
- **Data Source**: Data is strictly loaded from `src/dashboard_data.json` (which records the origin table/script for every data block).
