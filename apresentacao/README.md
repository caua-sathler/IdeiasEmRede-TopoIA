# Materiais de Apresentação — Ideias em Rede (1ª Edição)

Este diretório reúne todos os recursos necessários para a produção do **vídeo de apresentação de até 5 minutos**, exigido como entregável obrigatório da competição **Ideias em Rede (1ª Edição)**, organizada pelo **Instituto Kunumi**.

---

## 1. Regulamentação do Entregável de Vídeo

Conforme o **Regulamento Oficial da Competição**:
* **Duração Máxima:** Até 5 minutos (rigoroso: vídeos com mais de 5:00 podem sofrer penalização). Recomendamos gravar com **4min30s a 4min45s**.
* **Objetivo:** Apresentar a solução desenvolvida e, **sempre que possível, sua execução ou demonstração prática** (§7.2c).
* **Critério de Avaliação Associado:** *Qualidade da Apresentação e do Código (20%)* (§8.6d) — clareza do vídeo demonstrativo, didática e facilidade de compreensão da solução.
* **Formato Sugerido:** Resolução 1080p (1920x1080), proporção 16:9, áudio limpo e claro, formato `.mp4` ou link privado/não listado (YouTube / Google Drive).

---

## 2. Conteúdo deste diretório

1. **`ROTEIRO_VIDEO_5MIN.md`**: roteiro em 6 blocos, com falas prontas e indicação de tela (slide ou painel).
2. **`slides.tex` / `slides.pdf`**: 12 slides em Beamer, alinhados ao artigo; ver `SLIDES_ESTRUTURA.md`.
3. **`dashboard/`**: painel interativo com dados reais, em seis etapas: quem disse, empates, somar ou desempatar, custo, fila e previsão. Abra `dashboard/index.html` no navegador. Para regenerar: `codigo/k3_dashboard_dados.py` e depois `dashboard/build.py`.
4. **`DEMO_TERMINAL.md`**: guia da demonstração (painel e, opcionalmente, terminal), com as saídas reais dos scripts.

## 3. Checklist Rápido de Gravação

- [ ] Abrir `dashboard/index.html` em tela cheia e ensaiar as seis etapas.
- [ ] (Opcional) Instalar as dependências para a gravação do terminal.
- [ ] Testar o áudio com microfone dedicado (evitar eco de sala).
- [ ] Configurar gravador de tela (OBS Studio, QuickTime ou Loom) em 1080p 60fps.
- [ ] Fazer 1 ensaio cronometrado: conferir se a fala fica entre **4m15s e 4m45s**.
- [ ] Renderizar em `.mp4` e hospedar no Google Drive com permissão de visualização aberta ou link não listado no YouTube.
