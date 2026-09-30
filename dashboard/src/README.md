# Fonte do dashboard

Arquivos usados para gerar `../pt-br-dashboard.html` e `../en-dashboard.html`.

| Arquivo | Conteúdo |
|---|---|
| `dashboard_data.json` | Números do artigo, pseudonimizados (LGPD). É a única fonte de dados; a chave `_fonte` indica a tabela/script de origem de cada bloco |
| `template_pt-br.html`, `template_en.html` | Texto e código das duas versões |
| `build.py` | Injeta os dados nos templates e grava as páginas em `dashboard/` (só biblioteca padrão; não lê nada fora de `dashboard/`) |

```bash
cd dashboard/src && python build.py
```

As páginas geradas são 100% ASCII (acentos como entidades HTML), então abrem corretamente em qualquer navegador.
