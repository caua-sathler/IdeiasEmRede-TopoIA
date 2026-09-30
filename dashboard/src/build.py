"""Build the two dashboards from the templates and the pseudonymised paper data.

    cd dashboard/src && python build.py

Self-contained: the only inputs are the files in this folder, and nothing outside
dashboard/ is read.
  dashboard_data.json                      pseudonymised (LGPD) snapshot of the paper's numbers
                                           (the "_fonte" key lists the paper table / script of origin)
  template_pt-br.html, template_en.html    page templates
  deck.css, deck.js                        presentation mode (#slides) shared by both pages

Outputs (written to dashboard/, one level up)
  pt-br-dashboard.html, en-dashboard.html

Encoding: every output is written as pure ASCII. Non-ASCII characters become HTML numeric
entities in markup and \\uXXXX escapes inside <script>, and each page also declares
<meta charset="utf-8">. The pages therefore render the same whatever encoding a browser or
server assumes (Safari opening a local file, a server sending latin-1, etc.).
Standard library only.
"""
import json
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent
OUT = SRC.parent
PAGES = [("template_pt-br.html", "pt-br-dashboard.html"), ("template_en.html", "en-dashboard.html")]
REQUIRED = {"exemplos", "comite", "totais", "escada", "previsao", "custo", "fila", "mecanismo"}


def load_data():
    d = json.loads((SRC / "dashboard_data.json").read_text(encoding="utf-8"))
    d.pop("_fonte", None)
    missing = REQUIRED - d.keys()
    assert not missing, f"dashboard_data.json is missing {sorted(missing)}"
    return d


def ascii_page(html):
    """Return an ASCII-only equivalent of an HTML page (entities outside scripts, \\u escapes inside)."""
    def ent(s):
        return "".join(c if ord(c) < 128 else f"&#{ord(c)};" for c in s)

    def js(s):
        out = []
        for c in s:
            o = ord(c)
            if o < 128:
                out.append(c)
            elif o <= 0xFFFF:
                out.append(f"\\u{o:04x}")
            else:                                            # astral plane: UTF-16 surrogate pair
                o -= 0x10000
                out.append(f"\\u{0xD800 + (o >> 10):04x}\\u{0xDC00 + (o & 0x3FF):04x}")
        return "".join(out)

    style = re.search(r"<style>(.*?)</style>", html, re.S)
    assert style is None or style.group(1).isascii(), "non-ASCII inside <style>: use CSS escapes"
    parts, pos = [], 0
    for m in re.finditer(r"(<script\b[^>]*>)(.*?)(</script>)", html, re.S | re.I):
        parts.append(ent(html[pos:m.start(2)]))
        parts.append(js(m.group(2)))
        pos = m.end(2)
    parts.append(ent(html[pos:]))
    out = "".join(parts)
    assert out.isascii()
    return out


def main():
    blob = json.dumps(load_data(), ensure_ascii=True, separators=(",", ":")).replace("</", "<\\/")
    deck_css = (SRC / "deck.css").read_text(encoding="utf-8")
    deck_js = (SRC / "deck.js").read_text(encoding="utf-8")
    assert deck_css.isascii() and deck_js.isascii(), "deck.css / deck.js must be ASCII"
    for tpl, dst in PAGES:
        html = (SRC / tpl).read_text(encoding="utf-8")
        assert html.count("/*__DECK_CSS__*/") == 1 and html.count("/*__DECK_JS__*/") == 1
        html = html.replace("/*__DECK_CSS__*/", deck_css).replace("/*__DECK_JS__*/", deck_js)
        assert html.count("__DATA__") == 1
        page = ascii_page(html.replace("__DATA__", blob))
        (OUT / dst).write_text(page, encoding="ascii", newline="\n")
        print(f"{dst}: {len(page) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
