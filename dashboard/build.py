"""Build the dashboard: inject codigo/out/dashboard_dados.json into template.html.

    python ../../producao_de_artigos/artigo_unificado_sota/codigo/k3_dashboard_dados.py
    python build.py        # writes index.html
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / "producao_de_artigos/artigo_unificado_sota/codigo/out/dashboard_dados.json"
d = json.loads(DATA.read_text())
html = (HERE / "template.html").read_text().replace("__DATA__", json.dumps(d, ensure_ascii=False))
(HERE / "index.html").write_text(html)
print(f"index.html: {len(html)/1024:.0f} KB")
