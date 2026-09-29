# Código — Speaker-Conditioned Verification and Lexicographic Tie-Breaking

Pacote de reprodução do artigo (`../artigo/main.tex`). Todo número reportado
sai de algum script aqui.

## 1. O que este código faz

Duas peças, nessa ordem:

1. **Incidência por orador** (`h6_orador.py`, `h6b_controles.py`,
   `h6c_dowker_oradores.py`, `h7_nli_orador.py`) — em vez de comparar uma
   opinião com a transcrição inteira, compara com as falas do orador a quem
   ela foi atribuída. Sobe o AUROC de 0,57 (baseline global) para 0,78 (com
   NLI), **sem nenhuma chamada de LLM** até o `h7`, que só usa um modelo de
   NLI local.
2. **Fusão lexicográfica** (`j4_reticulado.py` em diante) — combina essas
   features com o comitê de 12 juízes LLM do dataset, usando-as só para
   desempatar opiniões que o comitê empatou. Nunca reverte uma decisão do
   comitê. É o resultado de manchete: comitê `0,9260 → 0,9300`.

Duas peças de apoio:

- **`i0`–`i4`** — features estruturais (homologia de Dowker, decomposição de
  Hodge, duplicação) que entram como **resultado negativo**: não melhoram a
  fusão (ver Negative Results no artigo). `i2`/`i3` ainda alimentam a cadeia
  de dados abaixo, porque o artigo compara "família" com "família + camada
  conjunta" e as duas precisam do mesmo pipeline.
- **`k1`–`k3`** — a auditoria de 50 opiniões positivas (má-atribuição ≈ 24%,
  §Results I) e a exportação de dados para o painel do vídeo.

## 2. Instalação

```bash
python -m venv .venv && source .venv/bin/activate     # Python 3.11
pip install -r requirements.txt
```

**Dados.** É preciso o `../dataset/` do PublicHearingBR já processado (ver
`../dataset/README.md`). Este pacote o localiza sozinho subindo a árvore de
diretórios; para apontar para outra cópia:

```bash
export PHBR_DATA=/caminho/para/dataset
python comum.py        # imprime OUT, CACHE e DATA — confira antes de rodar
python dados.py        # deve imprimir "audiencias utilizaveis: 206"
```

Os CSV intermediários da trilha C já vêm prontos em `out/` (§4), então **você
não precisa dos dados nem de nenhum modelo** para reproduzir o resultado de
manchete — só para regenerar os CSV do zero (trilha A).

## 3. Como rodar

Tudo é determinístico (`SEED = 42`). **Um script de NLI por vez** — o
mDeBERTa ocupa ~1 GB e dois processos simultâneos derrubam uma máquina de
8 GB.

### Trilha A — incidência por orador

| # | comando | ~tempo | modelo? |
|---|---|---|---|
| 1 | `python h6_orador.py` | 2 min | não |
| 2 | `python h6b_controles.py` | 3 min | não |
| 3 | `python h6c_dowker_oradores.py` | 3 min | não |
| 4 | `python h7_nli_orador.py` | 5 min (com cache) | NLI, 29k pares — já em `cache/h7_nli.npz` |

`h6b` é o passo que não se pula: é lá que estão os três controles (tamanho,
**identidade** — orador aleatório pareado em tamanho, AUROC 0,5209 — e
inferência agrupada por audiência). Sem eles o resultado é indefensável.

### Trilha C — fusão lexicográfica (resultado de manchete)

Nenhum destes chama modelo: leem CSV e rodam regressão logística. Os quatro
primeiros só são necessários se você quiser **regenerar** os CSV de `out/`;
como eles já vêm prontos, pule direto para o passo 5 (`j4`).

| # | comando | ~tempo | produz |
|---|---|---|---|
| 1 | `python h7_nli_orador.py` | 5 min | `out/h7_nli_orador.csv` |
| 2 | `python i2_hodge_audiencias.py` | 8 min | `out/i2_hodge.csv` |
| 3 | `python i3_duplicacao_guarda.py` | 3 min | `out/i3_dup.csv` |
| 4 | `python j1_continuidade.py` | 6 min | `out/j1_continuidade.csv` |
| 5 | `python j4_reticulado.py` | 1 min | teto `τ/2`, join vs. soma, por juiz |
| 6 | `python j5_join_condicional.py` | 1 min | nulo do desempate aleatório, join condicional |
| 7 | `python j6_estabilidade.py` | 10 s | 20 particionamentos + placar final |
| 8 | `python j7_mecanismo.py` | 30 s | decomposição exata do AUROC + anatomia do orçamento |
| 9 | `python j8_desempatador.py [--full]` | 30 s / 6 min | seis tentativas de melhorar o desempatador (todas falham — ver `j8_predicoes.md`) |
| 10 | `python j9_teto.py [--robustez]` | 2 min / 12 min | onde ainda há gap; equivalência de custo em chamadas de juiz |
| 11 | `python j10_portao.py` | 8 min | o portão `f_γ`: cota, detector clarividente, limiar de qualidade |
| 12 | `python j11_operacao.py` | 3 min | a fila de revisão (recall por orçamento de auditoria) |
| 13 | `python j12_histograma_comite.py` | 1 s | coordenadas da Fig. 2 (histograma do comitê) |
| 14 | `python j13_previsao.py` | 1 min | previsão do ganho em audiências não vistas |

Os passos 1→4 são uma **cadeia**: cada um lê o CSV do anterior. Rodar fora de
ordem falha com `FileNotFoundError` em `out/`. Os passos 5 em diante só leem
esses quatro CSV; rodam em qualquer ordem entre si.

## 4. O que já vem pronto, e por quê

**`cache/h7_nli.npz`** — o cache de NLI do `h7` (29k pares). Sem ele o `h7`
custaria alguns minutos de mDeBERTa em vez de segundos. É retomável: apagar o
arquivo faz o script recomputá-lo do zero.

**`out/`** — os CSV que uma trilha produz e a próxima lê, para você poder
começar em qualquer ponto da cadeia:

| arquivo | produzido por | lido por |
|---|---|---|
| `h6b_controles.csv` | `h6b_controles.py` | (informativo, Tab. `tab:orador`) |
| `h6c_dowker.csv` | `h6c_dowker_oradores.py` | `h7_nli_orador.py` |
| `h7_nli_orador.csv` | `h7_nli_orador.py` | `i2`, `i3`, `j1`–`j13`, `k1` |
| `i2_hodge.csv` | `i2_hodge_audiencias.py` | `i3`, `j1`–`j13` |
| `i3_dup.csv` | `i3_duplicacao_guarda.py` | `j1`–`j13` |
| `j1_continuidade.csv` | `j1_continuidade.py` | `j2`, `j4`–`j13` |
| `dashboard_dados.json` | `k3_dashboard_dados.py` | `../apresentacao/dashboard/build.py` |
| `k1_auditoria/*` | `k1_auditoria_planilha.py` | `k2_auditoria_concordancia.py` |

A cadeia `h7 → i2 → i3 → j1` é a que sustenta o resultado principal do
artigo. Com ela pronta (já vem), `j4`–`j7` rodam em menos de dois minutos no
total, sem tocar no dataset nem em nenhum modelo.

## 5. Correspondência artigo → script

Seções e teoremas são referenciados pelo `\label` do `.tex` (não pelo número
impresso, que pode mudar entre revisões).

| No artigo | Script |
|---|---|
| Fig. `fig:incidencia` — o exemplo real (Chinaglia/van Hattem) | dados medidos manualmente, não gerado por script |
| Tab. `tab:orador` — AUROC de cada feature, e os três controles | `h6_orador.py`, `h6b_controles.py`, `h6c_dowker_oradores.py`, `h7_nli_orador.py` |
| Auditoria de 50 positivos (`sec:auditoria`) | `k1_auditoria_planilha.py`, `k2_auditoria_concordancia.py` |
| Prop. `prop:soma` — a soma pode reverter o primário | `j4_reticulado.py` |
| Prop. `thm:lex` — a fusão lexicográfica, Eq. `eq:captura` | `j4_reticulado.py` (`join`, `deficit`) |
| Fig. `fig:comite` — histograma dos 13 níveis de voto, `τ` | `j12_histograma_comite.py` (citado no artigo) |
| Tab. `tab:mecanismo` — decomposição exata do AUROC por tipo de par | `j7_mecanismo.py` |
| Tab. `tab:estab` — 20 particionamentos de dobra | `j6_estabilidade.py` |
| Tab. `tab:scoreboard2` — escada de custo (0/1/3/5/8/12 juízes) | `j9_teto.py` (citado no artigo) |
| Tab. `tab:anatomia` — anatomia do orçamento (0,809 / 0,589 / 0,473) | `j7_mecanismo.py` |
| As seis tentativas de subir `α`, e "não deixe o desempatador ver o primário" | `j8_desempatador.py --full` (a sexta é o `j5`) |
| Limiar `α ≳ 0,58` para o *overrule* compensar | `j10_portao.py` (citado no artigo) |
| Remark `rem:portao` — o portão `f_γ = r₁ + γr₂` e sua cota | `j10_portao.py` |
| Fig. `fig:fila`, §Effect on a human review queue | `j11_operacao.py` (citado no artigo) |
| Tab. `tab:previsao` — previsão do ganho em audiências não vistas | `j13_previsao.py` (citado no artigo) |
| Nulo do desempate aleatório; controle com secundário fraco (`cos_g`) | `j5_join_condicional.py`, `j4_reticulado.py` |
| Negative Results — as construções estruturais não somam à combinação | `h6c_dowker_oradores.py`, `i2_hodge_audiencias.py`, `i3_duplicacao_guarda.py`, `j1_continuidade.py`, `j2_tipicidade.py` |
| Predições registradas **antes** de medir | `i0`, `j0`, `j8`, `j10`, `j11_predicoes.md` + cabeçalhos dos scripts |

Os números do artigo saem de **um único particionamento** (`GroupKFold`
natural), exceto a tabela de estabilidade, que é a distribuição sobre 20.
Particionamentos diferentes concordam na segunda casa decimal e variam na
terceira — é ruído de dobra, discutido no protocolo estatístico do artigo.

## 6. O que foi verificado

| verificação | esperado | obtido |
|---|---|---|
| `h6` — faixa dos 12 juízes LLM | 0,7340 – 0,8468 | idem |
| `h6b` — controle de identidade (orador aleatório pareado em tamanho) | ~0,52 (chance) | 0,5209 |
| `h7` — AUROC das features de incidência, todas + NLI | 0,7792 | idem |
| `j7` — decomposição por tipo de par (comitê / stacking / lex) | 0,9260 / 0,9262 / 0,9300 | idem, exato |
| `j7` — inversões da soma aditiva | 1,33% (0,74% danosas, 0,59% benignas) | idem |
| `j6` — 20 particionamentos (stacking e lex, família e família+tudo) | 0,9247 / 0,9218 / 0,9301 / 0,9302 | idem |
| `j5` — os três IC pareados do artigo | +0,0040 / +0,0054 / +0,0067 | idem, exato |
| `j5` — nulo do desempate (200 sorteios) | média 0,9259, dp 0,0020, máx 0,9308 | idem |
| `j4` — controle com secundário fraco (`cos_g`) | 0,9279 | idem |
| `j8` — as seis tentativas de subir `α` | todas piores que a família (0,489–0,520 vs. 0,589) | idem |
| `j9` — decomposição por desfecho do comitê | 0,809 / 0,589 / 0,473 | idem |
| `j10` — a cota do portão `f_γ` | 0 violações em 9 valores de γ | idem |
| `j11` — recall a 10% de orçamento (família+1 juiz vs. 1 juiz só) | +11,7 pp (52,2% vs. 40,5%) | idem |
| `j13` — previsão do ganho (1 e 12 juízes) | +0,0706/+0,0721 e +0,0041/+0,0042 (previsto/observado) | idem |

Cada linha acima é reproduzível rodando o script correspondente sobre os
CSV de `out/` — nenhuma depende do dataset bruto. Os vereditos completos
(inclusive as predições que falharam e por quê) estão nos `*_predicoes.md`
de cada script e em `diagnostico/RESULTADOS_J.md` do repositório de pesquisa
(§8 abaixo).

## 7. Notas

- **Infraestrutura, não os experimentos.** Os corpos dos experimentos vêm do
  repositório de pesquisa sem alteração. Só mudou o que é infraestrutura:
  `diagnostico/e0_common.py` virou `comum.py` (o original também
  materializava um acervo de ~400MB não usado por esta linha) e
  `diagnostico/e10_retrato.py` virou `dados.py` (o original era um
  experimento inteiro; esta linha usava só seis leitores). Os
  `sys.path.insert` para módulos do repositório de pesquisa foram
  removidos; tudo aqui é autocontido.
- **`h7` carrega o mDeBERTa na inicialização**, mesmo lendo tudo do cache —
  é o contrato de `make_nli()`, que devolve `None` quando o modelo não está
  disponível, para o script degradar com aviso em vez de quebrar. Na
  prática: a primeira execução baixa ~1GB do Hugging Face; depois disso o
  carregamento leva segundos e nenhuma inferência é feita se o cache estiver
  completo.
- **`i1_corrente_atribuicao.py` é biblioteca**, não um script — só o `i2` o
  importa.

## 8. Proveniência

A crônica completa da pesquisa (predições, o que falhou e por quê, becos sem
saída, e a trilha de consistência cortada do artigo) fica no repositório de
pesquisa, em `diagnostico/`, não neste repositório de entrega:

- Números e vereditos por fase: `RESULTADOS_H.md`, `RESULTADOS_I.md`, `RESULTADOS_J.md`
- Narrativa completa: `MEMORIAL_FASE_H.md`, `MEMORIAL_FASES_I_J.md`
- Teoria por trás da fusão lexicográfica: `TEORIA_RETICULADO.md`
