# Auditoria de rótulos — 50 opiniões marcadas como não suportadas

Universo: opiniões com rótulo humano e participante casado a um orador da transcrição (n=3630, 408 marcadas). Amostra aleatória de 50 (numpy default_rng, seed 20260923).

Cossenos no espaço MPNet (L2-normalizado). `cos_s` = maior cosseno nos turnos do orador atribuído; `best_other` = maior cosseno nos turnos de qualquer outro orador; Δ = best_other − cos_s; `cos_g` = maior cosseno na transcrição inteira. O orador de cada frase vem do último marcador `O SR./A SRA. NOME -` anterior (forward-fill). "Audiência" é a manchete da matéria da Agência Câmara pareada.

---
## Item 01 — `data_014#24`

- **Audiência (data_014):** Vítimas e autoridades divergem sobre reparações do crime socioambiental da Braskem em Maceió
- **Participante atribuído:** Alexandre Sampaio — Presidente da Associação dos Empreendedores e Vítimas da Mineração em Maceió
- **Orador casado na transcrição:** ALEXANDRE SAMPAIO (35 frases de 641; 11 oradores na audiência)
- **cos_s** = 0.303 · **best_other** = 0.835 · **Δ** = best_other − cos_s = +0.532 · cos_g = 0.835

**Opinião (PT original):**

> Mais de 70 mil pessoas foram deslocadas sem uma indenização adequada, apenas uma compensação limitada.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 299 | 0.303 | O Ministério Público argumenta que a nossa associação, que está há 5 anos lutando em favor das vítimas, não tem legitimidade para processar criminalmente a Braskem. |
| 2 | 315 | 0.299 | O primeiro acordo, que foi o de compensação financeira, deu a posse, a propriedade dos imóveis das pessoas atingidas. |
| 3 | 323 | 0.213 | Para coroar tudo isso, o IMA, do Governo Estadual, ainda este mês, há mais ou menos uns 10 dias, autorizou o uso de mosaicos de RPPN nos cerca de 3,5 quilômetros afetados pela mineradora Braskem. |
| 4 | 318 | 0.211 | A verdade é que ela tem condicionantes para fazer intervenções comerciais e uso comercial da área, e essas condicionantes podem se cumprir daqui a 10 anos, 15 anos, 20 anos, quando nem vamos mais estar militando. |
| 5 | 324 | 0.200 | Portanto, eu refuto, eu rechaço veementemente esses subterfúgios usados pelos colegas até agora, porque, de fato, o que aconteceu, em todas as instâncias, foi a legitimação da propriedade, inclusive uma licença prévia do IMA para que haja mosaicos de RPPN, e, nos outros lugares, consequentemente, poderia haver construções e tudo mais. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 606 | 0.835 | PRESIDENTE | Mais de 70 mil pessoas foram deslocadas. |
| 2 | 490 | 0.520 | PROFESSORA LUCIENE CAVALCANTE | São milhares e milhares de famílias impactadas, mais de 60 mil famílias, e mais de 14 mil residências já evacuadas. |
| 3 | 254 | 0.487 | PAULO CÉSAR PEREIRA MARQUES | Diante de todas essas situações, eu acho que muitas pessoas queriam mesmo ter uma indenização justa, sair daquele local, ter segurança, ter seu juízo no lugar, voltar a ter uma vida que já não tinham mais, o que é muito semelhante ao que acontece hoje com o Flexal e Bom Parto, que são outros bairros atingidos pela Braskem cujos moradores não foram realocados e brigam para entrar no mapa de criticidade e para poder sair do território com uma indenização justa e também a garantia dos direitos mínimos que foram tirados, como escola, saúde, educação, Uber, que não entra no território. |
| 4 | 607 | 0.483 | PRESIDENTE | Como disse um dos defensores do movimento, na verdade não houve indenização, houve compensação, e compensação limitada. |
| 5 | 213 | 0.433 | CÁSSIO ARAÚJO | As vítimas são detentoras dos direitos tratados por essas autoridades, e não estão sendo consideradas. |

**Contexto da melhor frase do orador** (frase 299)

- antes [ALEXANDRE SAMPAIO]: Entramos então com uma queixa-crime subsidiária.
- **frase [ALEXANDRE SAMPAIO]: O Ministério Público argumenta que a nossa associação, que está há 5 anos lutando em favor das vítimas, não tem legitimidade para processar criminalmente a Braskem.**
- depois [ALEXANDRE SAMPAIO]: E, apesar de já se terem passado 5 anos do início da prática do crime, o Ministério Público Federal ainda não processou criminalmente a empresa, o que nos causa muito estranhamento.

**Contexto da melhor frase global** (frase 606)

- antes [PRESIDENTE]: A verdade é a seguinte: essas pessoas foram vítimas de algo extremamente arrasante para a continuidade e busca de dignidade na vida.
- **frase [PRESIDENTE]: Mais de 70 mil pessoas foram deslocadas.**
- depois [PRESIDENTE]: Como disse um dos defensores do movimento, na verdade não houve indenização, houve compensação, e compensação limitada.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 02 — `data_017#8`

- **Audiência (data_017):** Em seminário na Câmara, especialistas discordam sobre ativismo judicial
- **Participante atribuído:** Sebastião Coelho — Desembargador aposentado do Tribunal de Justiça do Distrito Federal
- **Orador casado na transcrição:** SEBASTIÂO COELHO (127 frases de 1359; 13 oradores na audiência)
- **cos_s** = 0.626 · **best_other** = 0.722 · **Δ** = best_other − cos_s = +0.097 · cos_g = 0.722

**Opinião (PT original):**

> Criticou a relação de proximidade entre Ministros do STF e parlamentares, alegando que isso compromete a independência dos Poderes.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 250 | 0.626 | O STF coloca no ordenamento jurídico situações que o Parlamento, com a intervenção do Executivo, no caso de lei com sanção, não colocou no mundo jurídico, ou retira do mundo jurídico aquilo que o Parlamento e o Poder Executivo colocaram nele. |
| 2 | 307 | 0.587 | Mas, quando o Ministro se acha no direito de proferir falas infelizes, dizer que o partido tal... |
| 3 | 260 | 0.585 | Essa invasão de competência não é saudável para o relacionamento dos Poderes. |
| 4 | 271 | 0.561 | Qual é o sentido de um Ministro do Supremo Tribunal Federal interferir em nomeação de membros para o STJ, para os Tribunais Regionais Federais ou até mesmo para os Tribunais Estaduais. |
| 5 | 277 | 0.557 | Agora, quando o Ministro do Supremo interfere em indicação para outras Cortes... |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 474 | 0.722 | PEDRO ESTEVAM | Existem mecanismos para o Parlamento controlar e defender, aí, sim, o STF dos próprios Ministros? |
| 2 | 1133 | 0.644 | RODRIGO SARAIVA | Nesta visão, trazendo o ponto que a Deputada Chris Tonietto traz, de pesos e contrapesos, eu tenho muito problema naquilo que foi trazido na Constituinte por Michel Temer: os poderes devem ser independentes e harmônicos. |
| 3 | 250 | 0.626 | SEBASTIÂO COELHO | O STF coloca no ordenamento jurídico situações que o Parlamento, com a intervenção do Executivo, no caso de lei com sanção, não colocou no mundo jurídico, ou retira do mundo jurídico aquilo que o Parlamento e o Poder Executivo colocaram nele. |
| 4 | 1230 | 0.621 | SEBASTIÃO COELHO | Nós devemos salvar o STF dos abusos dos seus Ministros. |
| 5 | 997 | 0.620 | PRESIDENTE | Como preservar a independência entre os Poderes em um cenário político tão polarizado, com grande pressão e impacto social?" |

**Contexto da melhor frase do orador** (frase 250)

- antes [SEBASTIÂO COELHO]: O Supremo Tribunal Federal tomou para si essa atribuição que não lhe é devida.Então, o que nós temos visto, infelizmente, é o Supremo Tribunal Federal colocar no mundo jurídico normas inexistentes, como, por exemplo, normas relacionadas à injúria real, à homofobia, à transformação em crime hediondo.
- **frase [SEBASTIÂO COELHO]: O STF coloca no ordenamento jurídico situações que o Parlamento, com a intervenção do Executivo, no caso de lei com sanção, não colocou no mundo jurídico, ou retira do mundo jurídico aquilo que o Parlamento e o Poder Executivo colocaram nele.**
- depois [SEBASTIÂO COELHO]: Então, 594 Parlamentares debatem uma lei — é claro que as leis não são feitas por unanimidade, mas são aprovadas pela maioria, qualificada ou não —, e a um Ministro só se atribui o poder de retirar essa lei do ordenamento jurídico e, mais do que isso, de fazer a sua decisão vigorar por tempo indeterminado.

**Contexto da melhor frase global** (frase 474)

- antes [PEDRO ESTEVAM]: Que o Ministro Alexandre leve ou não em consideração isso.
- **frase [PEDRO ESTEVAM]: Existem mecanismos para o Parlamento controlar e defender, aí, sim, o STF dos próprios Ministros?**
- depois [PEDRO ESTEVAM]: Existe.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 03 — `data_022#10`

- **Audiência (data_022):** Debatedores apontam necessidade de mais regulamentação do e-commerce, especialmente para importações
- **Participante atribuído:** Igor Luna — Advogado e representante da Câmara Brasileira de Economia Digital (Camara-e.net)
- **Orador casado na transcrição:** IGOR LUNA (82 frases de 647; 6 oradores na audiência)
- **cos_s** = 0.600 · **best_other** = 0.592 · **Δ** = best_other − cos_s = -0.008 · cos_g = 0.600

**Opinião (PT original):**

> Sublinhou a necessidade de uma regulamentação equilibrada que não iniba o crescimento do setor.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 200 | 0.600 | Então, quando começamos a ter noção do impacto do comércio eletrônico na economia nacional, isso desperta a necessidade de que o tratamento regulatório e legislativo desse setor receba um cuidado compatível com a importância que tem. |
| 2 | 544 | 0.569 | Nós achamos que nós temos espaço para fazer a construção de um modelo que seja equilibrado. |
| 3 | 202 | 0.563 | E o comércio eletrônico vem se posicionando para ser também um dos grandes pilares da economia brasileira e exigir, em boa medida, um tratamento regulatório e legislativo compatível. |
| 4 | 177 | 0.552 | E esse setor, progressivamente, vem ganhando importância no contexto da economia nacional. |
| 5 | 547 | 0.532 | Defendemos uma tributação equilibrada e que observe a carga tributária que já existe no Brasil. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 200 | 0.600 | IGOR LUNA | Então, quando começamos a ter noção do impacto do comércio eletrônico na economia nacional, isso desperta a necessidade de que o tratamento regulatório e legislativo desse setor receba um cuidado compatível com a importância que tem. |
| 2 | 393 | 0.592 | GUILHERME HENRIQUE MARTINS SANTOS | Eu entendo que uma lei complementar regulamentando o tema em todo o território nacional traria previsibilidade, mitigaria essas discussões sobre formalidade e sobre norma adequada ou não para se regulamentar e também teria o condão de unificar o tratamento em todo o território nacional. |
| 3 | 462 | 0.588 | GUILHERME HENRIQUE MARTINS SANTOS | Será que o Ministério de Indústria e Comércio poderia consolidar aqui quais são as estratégias, as linhas de ação e os programas traçados para a melhoria desse ambiente de negócio? |
| 4 | 544 | 0.569 | IGOR LUNA | Nós achamos que nós temos espaço para fazer a construção de um modelo que seja equilibrado. |
| 5 | 632 | 0.563 | PRESIDENTE | Para a construção de uma legislação que torne esse ambiente favorável ao desenvolvimento de negócios, vamos precisar, necessariamente, repetir conversas ricas como esta. |

**Contexto da melhor frase do orador** (frase 200)

- antes [IGOR LUNA]: Isso, de fato, ampliou bastante os impactos de A a Z na economia nacional.
- **frase [IGOR LUNA]: Então, quando começamos a ter noção do impacto do comércio eletrônico na economia nacional, isso desperta a necessidade de que o tratamento regulatório e legislativo desse setor receba um cuidado compatível com a importância que tem.**
- depois [IGOR LUNA]: Atualmente, tomamos decisões de elevado nível técnico, muito ponderadas, políticas, técnicas, em grandes setores como o agro, o da indústria automotiva, porque reconhecemos a importância desses segmentos para a economia nacional.

**Contexto da melhor frase global** (frase 200)

- antes [IGOR LUNA]: Isso, de fato, ampliou bastante os impactos de A a Z na economia nacional.
- **frase [IGOR LUNA]: Então, quando começamos a ter noção do impacto do comércio eletrônico na economia nacional, isso desperta a necessidade de que o tratamento regulatório e legislativo desse setor receba um cuidado compatível com a importância que tem.**
- depois [IGOR LUNA]: Atualmente, tomamos decisões de elevado nível técnico, muito ponderadas, políticas, técnicas, em grandes setores como o agro, o da indústria automotiva, porque reconhecemos a importância desses segmentos para a economia nacional.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 04 — `data_023#14`

- **Audiência (data_023):** Debatedores defendem medidas para impulsionar uso do biometano no Brasil
- **Participante atribuído:** Tiago Samos Santovito — Gerente Executivo de Regulação, Transporte e Distribuição de Gás Natural do Instituto Brasileiro de Petróleo e Gás (IBP)
- **Orador casado na transcrição:** TIAGO SAMOS SANTOVITO (113 frases de 1220; 10 oradores na audiência)
- **cos_s** = 0.770 · **best_other** = 0.792 · **Δ** = best_other − cos_s = +0.022 · cos_g = 0.792

**Opinião (PT original):**

> Enfatizou a importância de se trabalhar com incrementos percentuais na descarbonização para expandir o uso do biometano.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 704 | 0.770 | O biometano tem o papel importantíssimo de promover a redução de emissões do nosso setor. |
| 2 | 717 | 0.768 | É importante sempre mencionar que o IBP reconhece a importância do biometano na transição energética e dos esforços que vêm sendo implementados em prol da descarbonização por meio de políticas públicas que visam trazer esse incentivo. |
| 3 | 698 | 0.652 | Muito se falou da integração do gás natural com o biometano. |
| 4 | 719 | 0.634 | O primeiro pilar é a criação do Regime Especial de Incentivos para o Desenvolvimento de Tecnologias Sustentáveis de Matriz Limpa do Gás Natural e Biometano. |
| 5 | 703 | 0.622 | Trazer essa segurança energética, tanto através do gás natural quanto do biometano, é fundamental. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 462 | 0.792 | GUSTAVO BONINI | Com o comprovado cumprimento dessa meta de descarbonização, conseguiremos avançar também no uso do gás e do biometano. |
| 2 | 308 | 0.776 | TULIO CORREA | E aqui eu acho que temos de enaltecer sim o papel do biometano, porque, com o gás natural, nós temos sim uma redução de emissões de CO2, e, com a utilização do biometano, essa redução pode chegar até 95%. |
| 3 | 704 | 0.770 | TIAGO SAMOS SANTOVITO | O biometano tem o papel importantíssimo de promover a redução de emissões do nosso setor. |
| 4 | 717 | 0.768 | TIAGO SAMOS SANTOVITO | É importante sempre mencionar que o IBP reconhece a importância do biometano na transição energética e dos esforços que vêm sendo implementados em prol da descarbonização por meio de políticas públicas que visam trazer esse incentivo. |
| 5 | 316 | 0.768 | TULIO CORREA | E, aqui, mais uma vez, quero enaltecer o biometano, porque, com o biometano, nós conseguimos uma redução, até na ordem do dobro, de 15% para 30%, pois, em geral, os clientes produzem o próprio combustível ou têm acesso a esse tipo de combustível com um custo mais baixo. |

**Contexto da melhor frase do orador** (frase 704)

- antes [TIAGO SAMOS SANTOVITO]: Trazer essa segurança energética, tanto através do gás natural quanto do biometano, é fundamental.
- **frase [TIAGO SAMOS SANTOVITO]: O biometano tem o papel importantíssimo de promover a redução de emissões do nosso setor.**
- depois [TIAGO SAMOS SANTOVITO]: Então, é extremamente necessário ele estar conectado ao gás natural.

**Contexto da melhor frase global** (frase 462)

- antes [GUSTAVO BONINI]: Isso é bastante importante.
- **frase [GUSTAVO BONINI]: Com o comprovado cumprimento dessa meta de descarbonização, conseguiremos avançar também no uso do gás e do biometano.**
- depois [GUSTAVO BONINI]: Aqui foram listados alguns pontos importantes sobre o preço que é determinado pelo mercado.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 05 — `data_029#18`

- **Audiência (data_029):** Debatedores apontam medidas para reduzir mortes violentas de jovens negros
- **Participante atribuído:** Silvio Conceição do Rosário — Major da Polícia Militar do Estado da Bahia, representante da Secretaria de Segurança Pública do Estado da Bahia
- **Orador casado na transcrição:** SILVIO CONCEIÇÃO DO ROSÁRIO (67 frases de 989; 14 oradores na audiência)
- **cos_s** = 0.618 · **best_other** = 0.680 · **Δ** = best_other − cos_s = +0.062 · cos_g = 0.680

**Opinião (PT original):**

> Compartilhou a importância de ressignificar a lógica da segurança pública no Brasil.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 364 | 0.618 | Então, eu entendo a luta que é feita no Congresso Nacional para que essa pauta se torne cada dia mais importante e cada dia mais essencial no cotidiano de todo brasileiro. |
| 2 | 390 | 0.611 | Nós como policiais precisamos ouvir o que a comunidade negra no Brasil tem a dizer. |
| 3 | 360 | 0.592 | De alguma forma, estou representando também um estrato da Secretaria de Segurança Pública do Estado da Bahia. |
| 4 | 521 | 0.584 | Este é o caminho para uma segurança pública de melhor qualidade, uma segurança pública cidadã. |
| 5 | 399 | 0.563 | Isso não só é uma chancela, mas também um projeto da Polícia Militar da Bahia, através do GTP. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 411 | 0.680 | PRESIDENTE | Foi muito importante a participação do major da Polícia Militar da Bahia, representando a Secretaria de Segurança Pública do Estado. |
| 2 | 137 | 0.670 | RAFAEL MOREIRA DA SILVA DE OLIVEIRA | Isso deveria motivar-nos a olhar com mais atenção, com mais prioridade e com mais especificidade para a letalidade, para a forma e para os aspectos como a violência se apresenta no Brasil. |
| 3 | 935 | 0.670 | JOÃO CARLOS DOS SANTOS | Entendemos que, assim como está sendo proposta, através do PRONASCI, a formação para os serviços de segurança estaduais, é necessário que se faça um projeto de formação antirracista para as empresas e os prestadores de serviços de segurança privada, a fim de que o combate a essa violência, no nível da segurança pública, aconteça de forma generalizada e atinja todas as formas de segurança existentes no regramento brasileiro. |
| 4 | 143 | 0.666 | RAFAEL MOREIRA DA SILVA DE OLIVEIRA | Começo lembrando alguns dados do Fórum Brasileiro de Segurança Pública, que fez uma ótima nota técnica sobre a desigualdade racial na segurança pública. |
| 5 | 351 | 0.659 | PRESIDENTE | Com a palavra, repito, o Major da Polícia Militar da Bahia Silvio Conceição do Rosário, representando a Secretaria de Segurança Pública da Bahia. |

**Contexto da melhor frase do orador** (frase 364)

- antes [SILVIO CONCEIÇÃO DO ROSÁRIO]: Quando estou trajado de branco, eu corro tanto risco de ser apedrejado e de ser vilipendiado quanto qualquer homem preto na minha condição.
- **frase [SILVIO CONCEIÇÃO DO ROSÁRIO]: Então, eu entendo a luta que é feita no Congresso Nacional para que essa pauta se torne cada dia mais importante e cada dia mais essencial no cotidiano de todo brasileiro.**
- depois [SILVIO CONCEIÇÃO DO ROSÁRIO]: Eu queria começar dizendo que eu, como o Pastor Martin Luther King, também tenho um sonho.

**Contexto da melhor frase global** (frase 411)

- antes [PRESIDENTE]: Inclusive, eu queria levantar aqui um questionamento sobre o qual acho importante refletirmos neste painel.
- **frase [PRESIDENTE]: Foi muito importante a participação do major da Polícia Militar da Bahia, representando a Secretaria de Segurança Pública do Estado.**
- depois [PRESIDENTE]: Ele, como disse, é filho de santo, negro, major, e sofre toda essa realidade.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 06 — `data_031#26`

- **Audiência (data_031):** Especialistas defendem transformação de programa de formação de professores em política de Estado
- **Participante atribuído:** Mariana Breim — Diretora de Políticas Educacionais do Instituto Península
- **Orador casado na transcrição:** MARIANA BREIM (91 frases de 736; 13 oradores na audiência)
- **cos_s** = 0.534 · **best_other** = 0.802 · **Δ** = best_other − cos_s = +0.269 · cos_g = 0.802

**Opinião (PT original):**

> Apoio ao diálogo com os municípios para melhorar a pactuação e colaboração no PARFOR.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 698 | 0.534 | Acho que concordo com tudo o que foi dito em relação ao PARFOR. |
| 2 | 701 | 0.485 | Aproveitando a presença da Marcia aqui, gostaria de dizer que precisamos trazer para discussão, Marcia, o PIBID — Programa Institucional de Bolsa de Iniciação à Docência. |
| 3 | 707 | 0.466 | Então, que possamos fazer um diálogo de adequação do programa às necessidades, às demandas dos professores e das redes. |
| 4 | 414 | 0.455 | E essa não deveria ser uma característica apenas do PARFOR, mas de qualquer programa que se proponha a formar professores, seja na formação inicial, seja na formação continuada. |
| 5 | 407 | 0.452 | Eles queriam participar da tomada de decisões. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 690 | 0.802 | ROMILSON MARTINS SIQUEIRA | Por fim, no regime de colaboração e pactuação com os Municípios, podemos quem sabe pensar a questão do PARFOR na perspectiva dos planos de carreira dos Municípios. |
| 2 | 691 | 0.707 | ROMILSON MARTINS SIQUEIRA | Quem sabe podemos ajudar os Municípios a pensar o PARFOR como um processo de progressão horizontal, por exemplo, nos planos de carreira, não apenas para adequação da formação, mas também para garantir que aqueles que fizerem o PARFOR tenham, no plano de carreira, ascensão e progressão horizontal ou vertical, como queiram os municípios. |
| 3 | 682 | 0.698 | ROMILSON MARTINS SIQUEIRA | Uma segunda questão que quero trazer é sobre o regime de pactuação e de colaboração com os Municípios. |
| 4 | 684 | 0.691 | ROMILSON MARTINS SIQUEIRA | Acho que há um novo Governo e uma nova política sendo pensada para o programa, então eu acho que vale a pena um diálogo com os Municípios para fazermos essa chamada de atenção para aquilo que é compromisso de cada ente nessa pactuação. |
| 5 | 625 | 0.679 | SUZANE DA ROCHA VIEIRA GONÇALVES | Finalizo as minhas contribuições e colocações nesta audiência destacando a importância da continuidade do PARFOR como um programa permanente, com ampliação de financiamento e com ampliação de vagas, a partir de um diagnóstico construído e dialogado entre os fóruns estaduais, as instituições de ensino superior, o Ministério da Educação, que é responsável por acompanhar os fóruns, e a CAPES. |

**Contexto da melhor frase do orador** (frase 698)

- antes [MARIANA BREIM]: A SRA. MARIANA BREIM- Quero agradecer as falas aos meus colegas de Mesa e à Deputada a oportunidade.
- **frase [MARIANA BREIM]: Acho que concordo com tudo o que foi dito em relação ao PARFOR.**
- depois [MARIANA BREIM]: Acho que ele está devidamente iluminado e defendido nesta manhã.

**Contexto da melhor frase global** (frase 690)

- antes [ROMILSON MARTINS SIQUEIRA]: Que seja um edital, mas que seja um edital amplo, a longo prazo, que nos permita, a curto, médio e longo prazo, entender como é que se faz e como é que as universidades, o MEC e os próprios Municípios vão a curto, médio e longo prazo, nesse planejamento, fazer ingressarem novas turmas no PARFOR, não apenas a cada edital.
- **frase [ROMILSON MARTINS SIQUEIRA]: Por fim, no regime de colaboração e pactuação com os Municípios, podemos quem sabe pensar a questão do PARFOR na perspectiva dos planos de carreira dos Municípios.**
- depois [ROMILSON MARTINS SIQUEIRA]: Quem sabe podemos ajudar os Municípios a pensar o PARFOR como um processo de progressão horizontal, por exemplo, nos planos de carreira, não apenas para adequação da formação, mas também para garantir que aqueles que fizerem o PARFOR tenham, no plano de carreira, ascensão e progressão horizontal ou vertical, como queiram os municípios.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 07 — `data_035#8`

- **Audiência (data_035):** Especialistas sugerem prazo maior para registro de candidaturas em minirreforma eleitoral
- **Participante atribuído:** Thiago Boverio — Coordenador do grupo de trabalho da Coordenação da Advocacia Partidária
- **Orador casado na transcrição:** THIAGO BOVERIO (111 frases de 1465; 14 oradores na audiência)
- **cos_s** = 0.622 · **best_other** = 0.757 · **Δ** = best_other − cos_s = +0.135 · cos_g = 0.757

**Opinião (PT original):**

> Destaca a importância da transparência e a necessidade de simplificação sem perder a garantia republicana.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 1056 | 0.622 | Mantendo esse contraponto, sobre as questões atinentes à prestação de contas, acredito que seja o tema mais falado aqui e acredito que tenha sido o que mais tenha acentuado essa lógica da simplificação. |
| 2 | 1063 | 0.544 | Isso, além de desburocratizar, alivia a tramitação desses processos na Justiça Eleitoral. |
| 3 | 1109 | 0.539 | Isso vai dar liquidez, vai dar fruição para a Justiça Eleitoral, porque analisa, aprofunda. |
| 4 | 1043 | 0.527 | A lógica sistemática constitucional hoje é a diminuição de partido político. |
| 5 | 1042 | 0.521 | Por meio dessa premissa de não retroação constitucional, quando se avança numa matéria no País, evita-se o retrocesso. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 352 | 0.757 | RODRIGO LOPES ZILIO | Nisso, acho, não temos espaço para retroceder.Na prestação de contas partidárias, não há oposição à simplificação, desde que não prejudique a transparência e a fiscalização dos recursos públicos. |
| 2 | 969 | 0.744 | VICTOR DURIGAN | A transparência deve ser considerada uma regra, com exceções específicas, explícitas e justificadas, e tem que ser considerada de forma transversal em toda a proposta de minirreforma. |
| 3 | 169 | 0.731 | WALBER AGRA | E a prestação de contas, volto a dizer, é uma garantia republicana, é uma medida de transparência. |
| 4 | 1026 | 0.704 | PRESIDENTE | Então, a transparência é fundamental. |
| 5 | 979 | 0.668 | VICTOR DURIGAN | Diante disso, nós ressaltamos que devem ser criados não apenas instrumentos de transparência sobre a remoção de informação dos canais oficiais de órgão público, mas também melhores definições de critérios que sirvam para orientar os servidores sobre a remoção apenas de conteúdos que promovam agentes públicos, sem que sejam removidas as informações sobre as políticas públicas e de Estado. |

**Contexto da melhor frase do orador** (frase 1056)

- antes [THIAGO BOVERIO]: A contribuição desse sistema de sobras para aqueles que atingirem o quociente é muito válida nesse sentido, assim como fomentar a formação de federação, criando mecanismos formais nas casas políticas para que funcione como uma federação, não como partido avulso, senão vira uma fraude ao sistema de coligação.
- **frase [THIAGO BOVERIO]: Mantendo esse contraponto, sobre as questões atinentes à prestação de contas, acredito que seja o tema mais falado aqui e acredito que tenha sido o que mais tenha acentuado essa lógica da simplificação.**
- depois [THIAGO BOVERIO]: Dentro dessa construção, fica, a título de sugestão ao eminente Relator, a possibilidade de se fazer a prestação de contas eleitoral dentro da anual, porque, em ano eleitoral, há duas prestações de contas do partido.

**Contexto da melhor frase global** (frase 352)

- antes [RODRIGO LOPES ZILIO]: Quero apenas falar sobre a questão da fraude de gênero, uma política afirmativa que veio para ficar.O TSE teve um papel essencial em relação aos critérios e às consequências das cassações, o que foi corroborado pela massificação do Supremo pela ADI 6.338.
- **frase [RODRIGO LOPES ZILIO]: Nisso, acho, não temos espaço para retroceder.Na prestação de contas partidárias, não há oposição à simplificação, desde que não prejudique a transparência e a fiscalização dos recursos públicos.**
- depois [RODRIGO LOPES ZILIO]: Acho que o Marcelo Issa, da Transparência Partidária, foi muito feliz nas observações que fez.A última observação diz respeito às federações partidárias.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 08 — `data_037#12`

- **Audiência (data_037):** Secretaria Nacional de Paradesporto pede mais orçamento e estrutura para os atletas com deficiência
- **Participante atribuído:** Augusto Puppio — Deputado Federal
- **Orador casado na transcrição:** AUGUSTO PUPPIO (22 frases de 443; 5 oradores na audiência)
- **cos_s** = 0.697 · **best_other** = 0.702 · **Δ** = best_other − cos_s = +0.005 · cos_g = 0.702

**Opinião (PT original):**

> A instituição da Subcomissão Permanente do Paradesporto é um passo importante para o reconhecimento e investimento no paradesporto.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 345 | 0.697 | Podem ter certeza de que vamos trabalhar, pelo menos enquanto estivermos aqui, Presidente, para colocar o paradesporto no local que merece, porque, mesmo sem o devido reconhecimento e investimento, o paradesporto proporciona um retorno muito maior do que outros temas aos quais, às vezes, damos um pouco mais de foco, por uma série de fatores. |
| 2 | 336 | 0.632 | Eu estou muito feliz, Presidente, porque conseguimos instituir aqui a Subcomissão Permanente do Paradesporto. |
| 3 | 341 | 0.506 | Eu sei que todo o mundo aqui sabe, tão bem quanto eu, da importância do esporte, não pelo esporte em si, mas por tudo que ele representa, por todas as muletas psicológicas e sociais que o esporte representa em todos os sentidos. |
| 4 | 335 | 0.302 | Eu queria cumprimentar o Secretário-Executivo Lindberg; a Nayara, a quem parabenizo pela sua história; e o Secretário Nacional de Paradesporto, Fábio, que eu estava querendo conhecer pessoalmente há muito tempo — a sua fama o precede. |
| 5 | 333 | 0.252 | Eu queria agradecer ao nosso Presidente Luiz Lima, nosso ídolo do esporte, pela gentileza de me ceder a oportunidade de falar primeiro. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 213 | 0.702 | PRESIDENTE | Esse seu comprometimento contribui bastante para o paradesporto. |
| 2 | 162 | 0.699 | FÁBIO AUGUSTO LIMA DE ARAUJO | Da mesma maneira, o Avança Paradesporto do Brasil, um programa que visa à excelência paradesportiva, também precisa ainda ser adequado ao que diz a Lei Geral do Esporte. |
| 3 | 345 | 0.697 | AUGUSTO PUPPIO | Podem ter certeza de que vamos trabalhar, pelo menos enquanto estivermos aqui, Presidente, para colocar o paradesporto no local que merece, porque, mesmo sem o devido reconhecimento e investimento, o paradesporto proporciona um retorno muito maior do que outros temas aos quais, às vezes, damos um pouco mais de foco, por uma série de fatores. |
| 4 | 95 | 0.680 | FÁBIO AUGUSTO LIMA DE ARAUJO | O eixo conceitual, que eu acho que é muito importante, é para diferenciar o paradesporto do esporte paralímpico. |
| 5 | 146 | 0.679 | FÁBIO AUGUSTO LIMA DE ARAUJO | É importantíssimo darmos essa visibilidade ao paradesporto. |

**Contexto da melhor frase do orador** (frase 345)

- antes [AUGUSTO PUPPIO]: Todo o mundo apoiou.
- **frase [AUGUSTO PUPPIO]: Podem ter certeza de que vamos trabalhar, pelo menos enquanto estivermos aqui, Presidente, para colocar o paradesporto no local que merece, porque, mesmo sem o devido reconhecimento e investimento, o paradesporto proporciona um retorno muito maior do que outros temas aos quais, às vezes, damos um pouco mais de foco, por uma série de fatores.**
- depois [AUGUSTO PUPPIO]: Muito obrigado pela oportunidade, Presidente.

**Contexto da melhor frase global** (frase 213)

- antes [PRESIDENTE]: Vemos que realmente é emocionante a sua atitude.
- **frase [PRESIDENTE]: Esse seu comprometimento contribui bastante para o paradesporto.**
- depois [PRESIDENTE]: Registro a presença — já foi anunciado aqui — do nosso colega Deputado Augusto Puppio e do Deputado Airton Faleiro, do Pará.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 09 — `data_048#8`

- **Audiência (data_048):** Proposta que proíbe a união de pessoas do mesmo sexo é criticada em audiência pública
- **Participante atribuído:** Rodrigo Pedroso — Procurador da Universidade de São Paulo — USP
- **Orador casado na transcrição:** RODRIGO PEDROSO (66 frases de 1745; 19 oradores na audiência)
- **cos_s** = 0.667 · **best_other** = 0.685 · **Δ** = best_other − cos_s = +0.018 · cos_g = 0.685

**Opinião (PT original):**

> Afirma que a decisão do STF sobre a ADI 4.277 foi correta em reconhecer a união estável como entidade familiar.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 480 | 0.667 | O art. 1.723 do Código Civil, que repete o texto da Constituição sobre a união estável, recebeu — entre aspas — "uma interpretação conforme a Constituição", como se ele já não repetisse o texto constitucional, para reconhecer-se a união estável como entidade familiar. |
| 2 | 476 | 0.615 | Este é um tema que se presta, infelizmente, a muita demagogia, mas o fato é que, quando o Supremo Tribunal Federal julgou a ADI 4.277, há 12 anos, em 2011, ele declarou inconstitucional o próprio texto do artigo da Constituição que define a união estável entre homem e mulher como entidade familiar, como já ressaltado antes de mim pelo Prof. Glauco e pelo Prof. Antonio. |
| 3 | 507 | 0.565 | Esse desenho da família era o que já existia antes, na legislação infraconstitucional, e foi confirmado no Código Civil, de 2002. |
| 4 | 506 | 0.546 | O que importa é que a Constituição desenhou a família de uma certa maneira. |
| 5 | 518 | 0.545 | O casamento é abrangido pelo direito, é regulado pelo direito, não por uma questão de felicidade individual, mas porque tem reflexos no bem comum, no interesse público, no interesse social. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 1364 | 0.685 | PASTOR HENRIQUE VIEIRA | Concordo com a unanimidade do STF, que diz que é constitucional o casamento civil entre pessoas do mesmo sexo. |
| 2 | 330 | 0.681 | GLAUCO BARREIRA | Fala da união estável. |
| 3 | 770 | 0.673 | PASTOR HENRIQUE VIEIRA | Nós queremos a manutenção do que já está garantido por um entendimento do STF a respeito do espírito constitucional. |
| 4 | 480 | 0.667 | RODRIGO PEDROSO | O art. 1.723 do Código Civil, que repete o texto da Constituição sobre a união estável, recebeu — entre aspas — "uma interpretação conforme a Constituição", como se ele já não repetisse o texto constitucional, para reconhecer-se a união estável como entidade familiar. |
| 5 | 1509 | 0.637 | GLAUCO BARREIRA | A união estável, mesmo entre homem e mulher, a Constituição chama de "entidade familiar", que é equiparável para a proteção, mas recebeu outro nome. |

**Contexto da melhor frase do orador** (frase 480)

- antes [RODRIGO PEDROSO]: E foi isso o que aconteceu no julgamento da ADI 4.277.
- **frase [RODRIGO PEDROSO]: O art. 1.723 do Código Civil, que repete o texto da Constituição sobre a união estável, recebeu — entre aspas — "uma interpretação conforme a Constituição", como se ele já não repetisse o texto constitucional, para reconhecer-se a união estável como entidade familiar.**
- depois [RODRIGO PEDROSO]: Como disse antes de mim o Prof. Glauco, a família não pode ser objeto de uma definição arbitrária.

**Contexto da melhor frase global** (frase 1364)

- antes [PASTOR HENRIQUE VIEIRA]: Eu até faço.
- **frase [PASTOR HENRIQUE VIEIRA]: Concordo com a unanimidade do STF, que diz que é constitucional o casamento civil entre pessoas do mesmo sexo.**
- depois [PASTOR HENRIQUE VIEIRA]: Mas chega uma hora que nem dá mais vontade de fazer debate técnico, jurídico, constitucional.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 10 — `data_057#18`

- **Audiência (data_057):** Guardas armados não resolvem problema de violência nas escolas, dizem especialistas
- **Participante atribuído:** Daniel Cara — Professor da Faculdade de Educação da Universidade de São Paulo
- **Orador casado na transcrição:** DANIEL CARA (92 frases de 810; 14 oradores na audiência)
- **cos_s** = 0.784 · **best_other** = 0.840 · **Δ** = best_other − cos_s = +0.056 · cos_g = 0.840

**Opinião (PT original):**

> Apresentou a necessidade de abordar a violência contra as escolas de maneira ampla e integrada.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 323 | 0.784 | Eu falei sobre a primeira grande contribuição do relatório, que foi descobrirmos o fenômeno que vai além da violência nas escolas, mas que se trata da violência às escolas. |
| 2 | 315 | 0.756 | O primeiro deles é a percepção de que saímos de uma perspectiva só de violência nas escolas para uma perspectiva de violência às escolas. |
| 3 | 300 | 0.750 | O Brasil precisava enfrentar o fenômeno da violência às escolas, ou seja, contra as escolas. |
| 4 | 349 | 0.698 | Por último, também estão previstas em nosso relatório campanhas de conscientização sobre o extremismo de direita e alternativas para a ação governamental na prevenção dos ataques às escolas. |
| 5 | 324 | 0.658 | A segunda grande contribuição para a literatura sobre o tema que esse relatório inaugura é a percepção de que essa violência às escolas é mobilizada também por um extremismo neonazista e fascista. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 772 | 0.840 | ARIEL DE CASTRO ALVES | A nossa Coordenação de Enfrentamento às Violências tem como prioridade a temática do enfrentamento à violência nas escolas. |
| 2 | 471 | 0.795 | ARIEL DE CASTRO ALVES | Também precisaríamos pensar em como ampliar essa experiência para o País todo, para que toda escola tenha a sua Comissão de Prevenção à Violência para tratar dos casos que ocorrem no interior das escolas e prevenir situações, com medidas de capacitação dos profissionais e medidas de discussão junto aos estudantes sobre direitos humanos, cidadania e cultura de paz. |
| 3 | 323 | 0.784 | DANIEL CARA | Eu falei sobre a primeira grande contribuição do relatório, que foi descobrirmos o fenômeno que vai além da violência nas escolas, mas que se trata da violência às escolas. |
| 4 | 91 | 0.767 | JOSEVANDA FRANCO | Agora nós estamos enfrentando a violência da sociedade contra a escola. |
| 5 | 556 | 0.756 | CATARINA DE ALMEIDA | E nós precisamos olhar esse número crescente, que inclusive ele já trouxe, de atentados contra as escolas a partir de questões vinculadas na sociedade. |

**Contexto da melhor frase do orador** (frase 323)

- antes [DANIEL CARA]: O SR. DANIEL CARA- Voltarei às questões do relatório.
- **frase [DANIEL CARA]: Eu falei sobre a primeira grande contribuição do relatório, que foi descobrirmos o fenômeno que vai além da violência nas escolas, mas que se trata da violência às escolas.**
- depois [DANIEL CARA]: A segunda grande contribuição para a literatura sobre o tema que esse relatório inaugura é a percepção de que essa violência às escolas é mobilizada também por um extremismo neonazista e fascista.

**Contexto da melhor frase global** (frase 772)

- antes [ARIEL DE CASTRO ALVES]: Essa é uma das ações.
- **frase [ARIEL DE CASTRO ALVES]: A nossa Coordenação de Enfrentamento às Violências tem como prioridade a temática do enfrentamento à violência nas escolas.**
- depois [ARIEL DE CASTRO ALVES]: Pretendemos que o Fundo da Criança e do Adolescente, também no seu edital, preveja projetos sociais para as entidades voltados à prevenção da violência nas escolas.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 11 — `data_060#14`

- **Audiência (data_060):** Especialistas apontam benefícios e desafios de novo programa do SUS para o atendimento a idosos
- **Participante atribuído:** Dra. Maíra Batista Botelho — Secretária de Atenção Especializada à Saúde do Ministério da Saúde
- **Orador casado na transcrição:** MAÍRA BATISTA BOTELHO (126 frases de 569; 7 oradores na audiência)
- **cos_s** = 0.595 · **best_other** = 0.778 · **Δ** = best_other − cos_s = +0.183 · cos_g = 0.778

**Opinião (PT original):**

> A Tabela SUS precisa de ajustes para refletir melhor os custos reais e permitir a compra de dispositivos médicos de qualidade.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 497 | 0.595 | Isso é o mais caro para nós, porque trata da qualidade do atendimento prestado ao usuário do SUS. |
| 2 | 550 | 0.583 | Nós trazemos para o SUS o conceito de valor em saúde, criamos várias comparações entre serviços e capacitações, promovemos a troca de experiências entre serviços, para ampliar e melhorar o acesso com qualidade assistencial. |
| 3 | 412 | 0.557 | A Portaria nº 3.904, de 2022, que regulamentou a Tabela do SUS, traz um atributo para a tabela, que é o valor de referência nacional. |
| 4 | 519 | 0.540 | Um dos critérios de contrapartida do hospital habilitado seria o preenchimento de todos os dados clínicos desse atendimento no Registro Nacional de Implantes. |
| 5 | 520 | 0.526 | Nós pagamos e oferecemos um custeio diferenciado. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 142 | 0.778 | FERNANDO SILVEIRA | Verifica-se claramente que, de acordo com a necessidade do paciente, produtos com características técnicas mais específicas podem ser adquiridos com preços bastante acima daqueles estabelecidos no SIGTAP, que é o sistema que gerencia a Tabela SUS. |
| 2 | 144 | 0.729 | FERNANDO SILVEIRA | De toda forma, o QualiSUS Cardio, por meio de portarias do Ministério da Saúde publicadas ao final de 2021 e em meados de 2022, estabeleceu os preços de reembolso para dispositivos usados em procedimentos cardiovasculares no âmbito do SUS e, com a eventual economia dessas reduções, estabeleceu uma política de remuneração dos serviços hospitalares e dos serviços profissionais dessa área da medicina, com base em métricas de desempenho e qualidade. |
| 3 | 140 | 0.680 | FERNANDO SILVEIRA | No contraste com os preços da Tabela SUS do Ministério da Saúde e o monitoramento dos preços da ANVISA, a ferramenta da ANVISA ainda permite obter a referência de preços mínimos, dois recortes em percentis médios de preço e o preço máximo encontrado em contas públicas de dispositivos médicos. |
| 4 | 150 | 0.666 | FERNANDO SILVEIRA | Portanto, embora os tópicos da Tabela SUS e do QualiSUS Cardio ofereçam ainda inúmeras possibilidades de discussão e de realinhamento entre todos os participantes do mercado e entes federativos, entendemos que a aplicação do QualiSUS Cardio na melhoria do atendimento à população idosa demanda uma retomada das conversações sobre metodologia, critérios e valores atribuídos aos dispositivos e procedimentos, de tal forma a ampliar o acesso da população-alvo a procedimentos e a dispositivos custo-efetivos com eficácia e segurança de nível adequado, tanto do ponto de vista técnico, como do de disponibilidade continuada e intempestiva em toda a cadeia produtiva e de atendimento. |
| 5 | 143 | 0.654 | FERNANDO SILVEIRA | A ferramenta de monitoramento dos preços praticados no mercado da ANVISA, de acordo com as características técnicas do dispositivo, tem se mostrado muito mais eficaz e fidedigna para estabelecer referência de preço para os repasses do Ministério da Saúde aos prestadores de serviço. |

**Contexto da melhor frase do orador** (frase 497)

- antes [MAÍRA BATISTA BOTELHO]: Nós partimos desse diagnóstico situacional de toda a rede de alta complexidade cardiovascular, estabelecemos um modelo de avaliação, uma metodologia de análise multicritério que considerou o volume de procedimentos e o acesso a esses centros, combinando os indicadores assistenciais.
- **frase [MAÍRA BATISTA BOTELHO]: Isso é o mais caro para nós, porque trata da qualidade do atendimento prestado ao usuário do SUS.**
- depois [MAÍRA BATISTA BOTELHO]: Nós estabelecemos uma relação, sim, de pactuação com o fortalecimento dos processos de gestão e aprimoramento dessa qualidade e focamos em capacitação profissional.

**Contexto da melhor frase global** (frase 142)

- antes [FERNANDO SILVEIRA]: Para os itens monitorados pela ANVISA, verificam-se alguns contrastes no que a Tabela SUS estabelece em termos de ressarcimento, nivelando todos os produtos usados no serviço público pelo menor preço.
- **frase [FERNANDO SILVEIRA]: Verifica-se claramente que, de acordo com a necessidade do paciente, produtos com características técnicas mais específicas podem ser adquiridos com preços bastante acima daqueles estabelecidos no SIGTAP, que é o sistema que gerencia a Tabela SUS.**
- depois [FERNANDO SILVEIRA]: A ferramenta de monitoramento dos preços praticados no mercado da ANVISA, de acordo com as características técnicas do dispositivo, tem se mostrado muito mais eficaz e fidedigna para estabelecer referência de preço para os repasses do Ministério da Saúde aos prestadores de serviço.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 12 — `data_062#16`

- **Audiência (data_062):** Debatedores cobram oferta gratuita de novos medicamentos para tratar amiloidose no SUS
- **Participante atribuído:** Fábio Almeida — Paciente de amiloidose hereditária
- **Orador casado na transcrição:** FÁBIO ALMEIDA (92 frases de 537; 7 oradores na audiência)
- **cos_s** = 0.543 · **best_other** = 0.721 · **Δ** = best_other − cos_s = +0.178 · cos_g = 0.721

**Opinião (PT original):**

> Relata os benefícios do uso do inotersena em comparação com o tafamidis.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 331 | 0.543 | E eu sabia do tratamento que já existia na Europa com o uso do tafamidis, e alguns países já estavam começando a dar acesso a ele à população. |
| 2 | 380 | 0.509 | A droga que está no SUS, o tafamidis, não é o suficiente. |
| 3 | 340 | 0.501 | Com relação ao meu tratamento, nesses 10 anos e meio que eu posso computar desde o início dos sintomas, eu usei tafamidis por 2 anos, recebendo o medicamento do Ministério da Saúde, através de ação judicial. |
| 4 | 343 | 0.491 | Naquela época, foi aberto um estudo para um medicamento novo, a inotersena, e nós tínhamos grande esperança nele. |
| 5 | 359 | 0.385 | Também fico muito contente porque, ao participar do estudo, eu ajudei a que essa droga fosse provada e outras pessoas pudessem ter acesso a ela. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 274 | 0.721 | LIANA FERRONATO | Ao mesmo tempo, tenho acompanhado pacientes que puderam entrar nos ensaios clínicos com a inotersena e que hoje têm um quadro clínico perceptivelmente melhor do que o daqueles que só tomam tafamidis 20mg. |
| 2 | 272 | 0.606 | LIANA FERRONATO | Ao longo dos últimos 2 anos à frente da ABPAR, enquanto a incorporação da inotersena se arrasta, eu tenho visto muitos casos de pacientes cujo estado de saúde se agravou e que hoje não respondem mais ao tafamidis 20mg. |
| 3 | 188 | 0.602 | MARCIA CRUZ | Depois, vieram as drogas, como as estabilizadoras — no caso, o tafamidis — e os silenciadores da transtirretina, que faz como se fosse um transplante, e veio mais tarde. |
| 4 | 67 | 0.594 | PRISCILA GEBRIM LOULY | Nós avaliamos recentemente o inotersena. |
| 5 | 331 | 0.543 | FÁBIO ALMEIDA | E eu sabia do tratamento que já existia na Europa com o uso do tafamidis, e alguns países já estavam começando a dar acesso a ele à população. |

**Contexto da melhor frase do orador** (frase 331)

- antes [FÁBIO ALMEIDA]: Eu fiquei com medo dessa opção, então não era minha alternativa primeira.
- **frase [FÁBIO ALMEIDA]: E eu sabia do tratamento que já existia na Europa com o uso do tafamidis, e alguns países já estavam começando a dar acesso a ele à população.**
- depois [FÁBIO ALMEIDA]: Na época, infelizmente não havia acesso a isso no Brasil.

**Contexto da melhor frase global** (frase 274)

- antes [LIANA FERRONATO]: Outros casos de demora no diagnóstico também descartam o uso desse medicamento.
- **frase [LIANA FERRONATO]: Ao mesmo tempo, tenho acompanhado pacientes que puderam entrar nos ensaios clínicos com a inotersena e que hoje têm um quadro clínico perceptivelmente melhor do que o daqueles que só tomam tafamidis 20mg.**
- depois [LIANA FERRONATO]: O Fábio, aqui presente, é um exemplo disso por ter participado de um estudo conduzido pela Dra. Marcia.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 13 — `data_063#17`

- **Audiência (data_063):** Entidades de defesa dos idosos cobram mais atenção do Estado com instituições de longa permanência
- **Participante atribuído:** Sandro Roberto Poleto — Coordenador Nacional do Departamento de Normatização e Orientação da Sociedade Vicente de Paulo
- **Orador casado na transcrição:** SANDRO ROBERTO POLETO (78 frases de 712; 9 oradores na audiência)
- **cos_s** = 0.567 · **best_other** = 0.744 · **Δ** = best_other − cos_s = +0.177 · cos_g = 0.744

**Opinião (PT original):**

> Reforçou que o Estado tem a obrigação de apoiar financeiramente essas instituições.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 567 | 0.567 | Sendo uma instituição filantrópica, como prevê a própria Constituição, toda essa assistência social, que é um direito do cidadão, assim como é um dever da caridade — porque a Sociedade São Vicente de Paulo faz pela caridade —, que hoje é assistência social, ela deveria ser feita em gestão, de forma articulada. |
| 2 | 569 | 0.538 | Por fazer parte da rede SUAS, que é um dever, somos fiscalizados pelo Ministério Público, pela vigilância sanitária, pelos conselhos, e geralmente essas fiscalizações agem com força desproporcional contra essas instituições filantrópicas. |
| 3 | 597 | 0.518 | Mas onde estão os direitos das instituições? |
| 4 | 581 | 0.509 | E eles não fecham por maus tratos, eles fecham por falta de recurso financeiro quando o Estado, o Governo Federal, o Governo Estadual e o Governo Municipal se omitem e não repassam o recurso financeiro, uma vez que é dever do Estado custear o idoso que está institucionalizado. |
| 5 | 598 | 0.488 | A Lei nº 10.741, o Estatuto do Idoso, fala dos deveres, sim, mas esqueceram-se de colocar ali que o Estado também tem suas obrigações. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 106 | 0.744 | VEJUSE ALENCAR DE OLIVEIRA | Mas o Estado tem uma obrigação e precisa assumi-la. |
| 2 | 522 | 0.721 | RENATO DA SILVA GOMES | O Estado tem que se colocar, sim, porque o Estado tem responsabilidade de fomentar isso. |
| 3 | 61 | 0.700 | KARLA GIACOMIN | É preciso apoiar as instituições privadas, porque elas estão fazendo o papel que o Estado deveria fazer. |
| 4 | 169 | 0.647 | VEJUSE ALENCAR DE OLIVEIRA | É dever do Estado, é dever do sistema da assistência social acolher qualquer cidadão que dele necessite. |
| 5 | 60 | 0.645 | KARLA GIACOMIN | É preciso apoiar as instituições filantrópicas. |

**Contexto da melhor frase do orador** (frase 567)

- antes [SANDRO ROBERTO POLETO]: Mas grande parte desses idosos que adentram nas nossas instituições não têm nem acesso a esse benefício ou, quando eles chegam, o benefício já está todo comprometido por empréstimos e por outras pessoas que se beneficiaram dessas pessoas idosas.
- **frase [SANDRO ROBERTO POLETO]: Sendo uma instituição filantrópica, como prevê a própria Constituição, toda essa assistência social, que é um direito do cidadão, assim como é um dever da caridade — porque a Sociedade São Vicente de Paulo faz pela caridade —, que hoje é assistência social, ela deveria ser feita em gestão, de forma articulada.**
- depois [SANDRO ROBERTO POLETO]: E qual é a maior dificuldade que temos hoje, como instituição filantrópica?

**Contexto da melhor frase global** (frase 106)

- antes [VEJUSE ALENCAR DE OLIVEIRA]: Esse é um desafio do Estado, da sociedade e da família, isso é um esforço conjunto.
- **frase [VEJUSE ALENCAR DE OLIVEIRA]: Mas o Estado tem uma obrigação e precisa assumi-la.**
- depois [VEJUSE ALENCAR DE OLIVEIRA]: A Casa do Povo tem suas atribuições.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 14 — `data_069#4`

- **Audiência (data_069):** Debatedores defendem engajamento de jovens na política para combater ataques à democracia
- **Participante atribuído:** Maria Claudia Bucchianeri Pinheiro — Ministra Substituta do Tribunal Superior Eleitoral
- **Orador casado na transcrição:** MINISTRA MARIA CLAUDIA BUCCHIANERI PINHEIRO (53 frases de 433; 7 oradores na audiência)
- **cos_s** = 0.741 · **best_other** = 0.673 · **Δ** = best_other − cos_s = -0.068 · cos_g = 0.741

**Opinião (PT original):**

> Desenvolveu o projeto Eleitor do Futuro para engajar crianças e jovens em diferentes níveis de ensino.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 42 | 0.741 | Já no ensino médio, o foco muitas vezes do projeto Eleitor do Futuro é a formação de lideranças. |
| 2 | 49 | 0.729 | Ele engaja crianças, engaja adolescentes e jovens, em gradação de formação cívica. |
| 3 | 35 | 0.717 | O projeto mais antigo das nossas escolas se chama Eleitor do Futuro. |
| 4 | 36 | 0.691 | Trata-se de um projeto voltado ao público do ensino infantil, ensino fundamental e também, Dr. Ricardo, do ensino médio e, a depender da idade, da escolaridade, o enfoque das atuações muda. |
| 5 | 37 | 0.667 | Então, por exemplo, com crianças, há um interessantíssimo trabalho de formação de consciência cívica, de engajamento eleitoral. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 42 | 0.741 | MINISTRA MARIA CLAUDIA BUCCHIANERI PINHEIRO | Já no ensino médio, o foco muitas vezes do projeto Eleitor do Futuro é a formação de lideranças. |
| 2 | 49 | 0.729 | MINISTRA MARIA CLAUDIA BUCCHIANERI PINHEIRO | Ele engaja crianças, engaja adolescentes e jovens, em gradação de formação cívica. |
| 3 | 35 | 0.717 | MINISTRA MARIA CLAUDIA BUCCHIANERI PINHEIRO | O projeto mais antigo das nossas escolas se chama Eleitor do Futuro. |
| 4 | 36 | 0.691 | MINISTRA MARIA CLAUDIA BUCCHIANERI PINHEIRO | Trata-se de um projeto voltado ao público do ensino infantil, ensino fundamental e também, Dr. Ricardo, do ensino médio e, a depender da idade, da escolaridade, o enfoque das atuações muda. |
| 5 | 90 | 0.673 | LUCAS FERNANDES HOOGERBRUGGE | Uma das coisas que percebemos muito nessa interação dos professores e especialmente dos estudantes é que há um desejo, uma necessidade muito forte dos jovens de participarem do debate sobre aquilo que é o projeto para o nosso País. |

**Contexto da melhor frase do orador** (frase 42)

- antes [MINISTRA MARIA CLAUDIA BUCCHIANERI PINHEIRO]: Há também, em muitos Estados — e sabemos da profundidade das diversidades regionais do Brasil —, a atuação de interiorização do projeto Eleitor do Futuro, levando a criança do interior, em escolas muitas vezes sem Internet, a este programa de formação de cidadania e de despertar interesse nas nossas crianças.
- **frase [MINISTRA MARIA CLAUDIA BUCCHIANERI PINHEIRO]: Já no ensino médio, o foco muitas vezes do projeto Eleitor do Futuro é a formação de lideranças.**
- depois [MINISTRA MARIA CLAUDIA BUCCHIANERI PINHEIRO]: Crianças são convidadas a ir ao Tribunal Eleitoral para entenderem os seus direitos; crianças são treinadas por professores, por servidores públicos da Justiça Eleitoral, a saber como fiscalizar a propaganda eleitoral.

**Contexto da melhor frase global** (frase 42)

- antes [MINISTRA MARIA CLAUDIA BUCCHIANERI PINHEIRO]: Há também, em muitos Estados — e sabemos da profundidade das diversidades regionais do Brasil —, a atuação de interiorização do projeto Eleitor do Futuro, levando a criança do interior, em escolas muitas vezes sem Internet, a este programa de formação de cidadania e de despertar interesse nas nossas crianças.
- **frase [MINISTRA MARIA CLAUDIA BUCCHIANERI PINHEIRO]: Já no ensino médio, o foco muitas vezes do projeto Eleitor do Futuro é a formação de lideranças.**
- depois [MINISTRA MARIA CLAUDIA BUCCHIANERI PINHEIRO]: Crianças são convidadas a ir ao Tribunal Eleitoral para entenderem os seus direitos; crianças são treinadas por professores, por servidores públicos da Justiça Eleitoral, a saber como fiscalizar a propaganda eleitoral.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 15 — `data_077#10`

- **Audiência (data_077):** Participantes de audiência defendem financiamento federal do transporte coletivo urbano
- **Participante atribuído:** Marcos Bicalho dos Santos — Diretor Administrativo e Institucional da Associação Nacional das Empresas de Transportes Urbanos (NTU)
- **Orador casado na transcrição:** MARCOS BICALHO DOS SANTOS (133 frases de 881; 4 oradores na audiência)
- **cos_s** = 0.667 · **best_other** = 0.721 · **Δ** = best_other − cos_s = +0.054 · cos_g = 0.721

**Opinião (PT original):**

> Agradece a oportunidade de debater e elogia a visão do Deputado Elias Vaz sobre o setor de transporte.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 224 | 0.667 | Eu gostaria de agradecer a oportunidade e o convite desta Comissão de Viação e Transportes para participar desta audiência pública, que trata de um assunto de suma importância tanto para a população, como para as empresas operadoras e a sociedade em geral. |
| 2 | 844 | 0.619 | A NTU — Associação Nacional das Empresas de Transportes Urbanos agradece por esta oportunidade e se coloca totalmente à disposição desta Casa para contribuir para esses debates e para tentar recuperar a atividade do transporte público coletivo urbano no Brasil, que realmente está muito sofrida nos dias de hoje. |
| 3 | 840 | 0.604 | Eu gostaria apenas, referindo-me à última fala do senhor, Deputado, sobre a conversa que teve com o candidato às eleições presidenciais que citou, de dizer que tive notícia de uma recente conversa entre os operadores de ônibus de Goiânia e o Governador sobre essa tratativa de subsídio ao sistema de transportes nesta época de pandemia.Um dos argumentos que foram utilizados e que deixaram o Governador realmente impressionado foi o de que os recursos que o Estado de Goiás gasta hoje subsidiando o IPVA dos automóveis novos seriam bastante significativos para esse subsídio ao transporte coletivo. |
| 4 | 302 | 0.598 | Ele tem apoio, é um projeto que foi muito bem discutido em todos os segmentos, com todos os agentes que fazem o transporte público. |
| 5 | 842 | 0.592 | Deputado, gostaria de lhe agradecer e de cumprimentá-lo pela visão clara e objetiva, pela sabedoria que o senhor tem sobre o nosso setor de atividade. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 63 | 0.721 | RAFAEL CALABRIA | Eu queria começar agradecendo o convite da Comissão e parabenizando o nobre Deputado Elias Vaz por abraçar esta pauta que é tão importante. |
| 2 | 65 | 0.716 | RAFAEL CALABRIA | Por isso, queria agradecer ao Deputado por abraçar esse tema dos usuários de transporte coletivo. |
| 3 | 826 | 0.668 | RAFAEL CALABRIA | Elogio a sua iniciativa, Deputado, de fazer um debate tão importante. |
| 4 | 224 | 0.667 | MARCOS BICALHO DOS SANTOS | Eu gostaria de agradecer a oportunidade e o convite desta Comissão de Viação e Transportes para participar desta audiência pública, que trata de um assunto de suma importância tanto para a população, como para as empresas operadoras e a sociedade em geral. |
| 5 | 54 | 0.625 | PRESIDENTE | E é com esse sentimento e com essa preocupação que nós trazemos esta discussão a esta audiência pública aqui hoje, através da nossa Comissão de Viação e Transportes. |

**Contexto da melhor frase do orador** (frase 224)

- antes [MARCOS BICALHO DOS SANTOS]: O SR. MARCOS BICALHO DOS SANTOS- Bom dia, Deputado Elias Vaz.
- **frase [MARCOS BICALHO DOS SANTOS]: Eu gostaria de agradecer a oportunidade e o convite desta Comissão de Viação e Transportes para participar desta audiência pública, que trata de um assunto de suma importância tanto para a população, como para as empresas operadoras e a sociedade em geral.**
- depois [MARCOS BICALHO DOS SANTOS]: Eu cumprimento os demais convidados, o Rafael Calabria e o Prefeito de Porto Alegre, Sebastião Melo, pela participação neste debate.

**Contexto da melhor frase global** (frase 63)

- antes [RAFAEL CALABRIA]: Eu fiz uma pequena apresentação para ser um pouco mais objetivo e até para não ser tão prolixo.
- **frase [RAFAEL CALABRIA]: Eu queria começar agradecendo o convite da Comissão e parabenizando o nobre Deputado Elias Vaz por abraçar esta pauta que é tão importante.**
- depois [RAFAEL CALABRIA]: No IDEC, nós atuamos em defesa do consumidor há mais de 30 anos.E eu coordeno essa área de mobilidade, tentando expressar, reunir e acumular visões dos usuários na defesa desse ponto, que é tão importante.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 16 — `data_084#26`

- **Audiência (data_084):** Serviço de famílias acolhedoras precisa ser ampliado no Brasil, defendem participantes de audiência
- **Participante atribuído:** Julia Salvagni — Psicóloga e Vice-Presidenta do Grupo Aconchego do Distrito Federal
- **Orador casado na transcrição:** JULIA SALVAGNI (94 frases de 841; 12 oradores na audiência)
- **cos_s** = 0.721 · **best_other** = 0.775 · **Δ** = best_other − cos_s = +0.053 · cos_g = 0.775

**Opinião (PT original):**

> Enfatizou a importância do vínculo afetivo para o desenvolvimento saudável das crianças acolhidas.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 413 | 0.721 | Não podemos falar em atender criança e em atender adolescente sem considerar a importância do vínculo e, como a Débora disse, do apego no desenvolvimento infantil. |
| 2 | 464 | 0.649 | Considerando todas essas relações, o cuidado com a criança é o cuidado com a família acolhedora, é o cuidado com a família de origem, é o cuidado com as equipes técnicas. |
| 3 | 431 | 0.624 | Eu tenho uma criança que, em um momento de extrema delicadeza, está vivendo intensamente as relações que a constituem. |
| 4 | 435 | 0.610 | E acolher essa criança é acolher, de alguma maneira, a sua família, é escutar as motivações do acolhimento e, a partir dessa escuta, traçar, de maneira articulada, com a rede de proteção do território, uma atuação. |
| 5 | 458 | 0.607 | E quando a equipe olha para esse contexto, com cuidado, com ética, com zelo e com responsabilidade, nós garantimos à criança o direito à convivência familiar e comunitária. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 337 | 0.775 | DÉBORA VIGEVANI | O apego é necessário para o desenvolvimento integral de qualquer ser humano, de qualquer criança, adolescente ou de um bebê. |
| 2 | 413 | 0.721 | JULIA SALVAGNI | Não podemos falar em atender criança e em atender adolescente sem considerar a importância do vínculo e, como a Débora disse, do apego no desenvolvimento infantil. |
| 3 | 339 | 0.663 | DÉBORA VIGEVANI | Então, crianças precisam de adultos que se importem com elas, com quem elas possam estabelecer relações de apego. |
| 4 | 779 | 0.658 | PRESIDENTE | Acho que a família acolhedora representa isto: amorosidade, afetividade, vínculos, permanência. |
| 5 | 325 | 0.654 | DÉBORA VIGEVANI | Entre esses objetivos, é preciso trabalhar para a preservação do vínculo e do contato da criança e do adolescente com sua família de origem. |

**Contexto da melhor frase do orador** (frase 413)

- antes [JULIA SALVAGNI]: A partir da minha vivência prática, cotidiana e dos estudos que já foram referenciados aqui, eu gostaria de sublinhar que discutir e debater o serviço em família acolhedora é falar sobre participação e corresponsabilização social no direito da criança e do adolescente, é considerar o vínculo afetivo como parte fundamental de um aparato técnico na execução da política pública da infância e da juventude.
- **frase [JULIA SALVAGNI]: Não podemos falar em atender criança e em atender adolescente sem considerar a importância do vínculo e, como a Débora disse, do apego no desenvolvimento infantil.**
- depois [JULIA SALVAGNI]: A alta complexidade é a UTI da assistência social.

**Contexto da melhor frase global** (frase 337)

- antes [DÉBORA VIGEVANI]: Para responder isso, em primeiro lugar, é preciso considerar que não tem cuidado verdadeiro sem apego.
- **frase [DÉBORA VIGEVANI]: O apego é necessário para o desenvolvimento integral de qualquer ser humano, de qualquer criança, adolescente ou de um bebê.**
- depois [DÉBORA VIGEVANI]: É uma via de mão dupla: cuidar gera apego, e só sentimos o ímpeto de cuidar de alguém por quem nós nos importamos.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 17 — `data_096#14`

- **Audiência (data_096):** Participantes de audiência pública divergem sobre proposta que enquadra TDAH como deficiência
- **Participante atribuído:** Cely Matthiesen Granja — Mãe de uma adolescente com TDAH
- **Orador casado na transcrição:** CELY MATTHIESEN GRANJA (144 frases de 987; 8 oradores na audiência)
- **cos_s** = 0.543 · **best_other** = 0.656 · **Δ** = best_other − cos_s = +0.113 · cos_g = 0.656

**Opinião (PT original):**

> Compartilhou a experiência de gestão da condição de sua filha, destacando a importância do diagnóstico precoce e tratamento contínuo.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 384 | 0.543 | E esse tratamento tinha acompanhamento da psicóloga. |
| 2 | 397 | 0.518 | Eu quis deixar bem claro que ela podia ter TOD e TDAH, porque eu não queria chegar a uma escola, mentir e depois não ter o acompanhamento correto. |
| 3 | 347 | 0.496 | Depois, elas me falavam que ela ficava melhor e tudo o mais, mas era um dia a dia de muita crise. |
| 4 | 340 | 0.494 | No caso, a minha filha chegou com 10 meses apenas. |
| 5 | 408 | 0.479 | Ela teve uma crise severíssima no começo. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 894 | 0.656 | ERIKA KOKAY | Há, portanto, a necessidade de diagnóstico precoce, de nível de informação e capacitação. |
| 2 | 905 | 0.620 | ERIKA KOKAY | Nesse sentido, penso serem necessários o diagnóstico precoce, as informações acerca do que isso significa, a capacitação dos educadores e profissionais de saúde, o atendimento multidisciplinar e intersetorial, que é absolutamente fundamental, porque as políticas públicas se engancham umas nas outras, não caminham sozinhas, como os direitos também se engancham. |
| 3 | 891 | 0.602 | ERIKA KOKAY | Portanto, penso que é preciso o diagnóstico precoce e, ao mesmo tempo, as informações necessárias em todas as políticas públicas. |
| 4 | 885 | 0.587 | ERIKA KOKAY | Por isso, é importante uma política nacional que pressuponha atenção à saúde, que pressuponha atenção à educação, que pressuponha a capacidade de termos diagnósticos precoces. |
| 5 | 804 | 0.562 | CAPITÃO FÁBIO ABREU | Eu vejo isso como um fator importante para que a família dessas crianças, desses jovens, desses adultos sejam também esclarecidas e sejam sempre tratadas, para que possam enfrentar esse problema juntamente com aquela pessoa. |

**Contexto da melhor frase do orador** (frase 384)

- antes [CELY MATTHIESEN GRANJA]: Passados os 6 meses, ela começou a ter uma regressão, a medicação começou a não fazer efeito.
- **frase [CELY MATTHIESEN GRANJA]: E esse tratamento tinha acompanhamento da psicóloga.**
- depois [CELY MATTHIESEN GRANJA]: Ela começou a regredir muito, começou a bater nos alunos.

**Contexto da melhor frase global** (frase 894)

- antes [ERIKA KOKAY]: E, a partir daí, se constrói a possibilidade de adaptação da política pública à lógica que cada uma e cada um de nós carrega nas nossas individualidades.
- **frase [ERIKA KOKAY]: Há, portanto, a necessidade de diagnóstico precoce, de nível de informação e capacitação.**
- depois [ERIKA KOKAY]: Penso que educadores e educadoras têm que, na sua formação, analisar as singularidades que vão fazer parte da sua própria vida num contato que é um dos mais intensos na condição de gente com gente.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 18 — `data_101#20`

- **Audiência (data_101):** Torcidas organizadas pedem mudanças na Lei Geral do Esporte
- **Participante atribuído:** Mario Sarrubbo — Secretário Nacional de Segurança Pública
- **Orador casado na transcrição:** MARIO LUIZ SARRUBBO (95 frases de 918; 15 oradores na audiência)
- **cos_s** = 0.604 · **best_other** = 0.790 · **Δ** = best_other − cos_s = +0.186 · cos_g = 0.790

**Opinião (PT original):**

> Capacitação das forças de segurança é crucial para combater a violência nos estádios.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 327 | 0.604 | Esse projeto promove apoio às políticas sociais e assegura a paz e a segurança nos estádios e nas imediações, antes, durante e depois dos jogos. |
| 2 | 307 | 0.594 | E é isso que nós temos que preservar sempre, a volta das famílias aos estádios, a frequência das mulheres, e ali tem que ser um ambiente da mais absoluta segurança. |
| 3 | 330 | 0.578 | E esse centro terá atribuições como coletar e analisar informações relevantes para a segurança dos estádios, produzir conhecimento em segurança pública. |
| 4 | 349 | 0.559 | A partir desses canais, construiremos os alicerces de uma política de segurança para os estádios, de forma que possamos levar ainda mais as famílias para os estádios, para as arenas esportivas. |
| 5 | 309 | 0.535 | Este é um diálogo, essa questão da violência dos estádios, nós temos que encontrar uma diretriz no nosso Brasil, através do diálogo com todas as partes envolvidas, com as torcidas organizadas, com os clubes, com as confederações, com a CBF, com as federações estaduais. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 248 | 0.790 | BEBETO | Queria falar aqui que combater a violência nos estádios de futebol é crucial, pois a violência nos estádios representa uma ameaça à segurança e ao bem-estar dos torcedores. |
| 2 | 214 | 0.769 | ALCINO REIS ROCHA | As forças de segurança precisam se capacitar, precisam entender esse fenômeno para ver qual a melhor forma de fazer o seu devido combate. |
| 3 | 224 | 0.738 | ALCINO REIS ROCHA | Os estádios têm contribuído, as torcidas organizadas têm contribuído, mas nós temos que ter aqui uma capacitação grande no que diz respeito às forças públicas que agem no estádio, ou nas suas mediações, ou no deslocamento dos times, para que sejam adotados, como dito aqui, procedimentos, protocolos que sejam seguros e eficientes para se combater isso daí. |
| 4 | 47 | 0.678 | CLEOMAR MARQUES DE PAULA | Deveria haver uma padronização do trabalho das Polícias Militares nesses grandes eventos. |
| 5 | 22 | 0.650 | PRESIDENTE | Essa parte do combate à violência precisa ser mais bem trabalhada. |

**Contexto da melhor frase do orador** (frase 327)

- antes [MARIO LUIZ SARRUBBO]: Nós temos um acordo de cooperação, o Ministério da Justiça, o Ministério dos Esportes e a CBF.
- **frase [MARIO LUIZ SARRUBBO]: Esse projeto promove apoio às políticas sociais e assegura a paz e a segurança nos estádios e nas imediações, antes, durante e depois dos jogos.**
- depois [MARIO LUIZ SARRUBBO]: Mas ele prevê algo que nos parece muito importante, que são, na verdade, os centros de segurança.

**Contexto da melhor frase global** (frase 248)

- antes [BEBETO]: Conheço muito bem torcida organizada, da qual eu também já participei.
- **frase [BEBETO]: Queria falar aqui que combater a violência nos estádios de futebol é crucial, pois a violência nos estádios representa uma ameaça à segurança e ao bem-estar dos torcedores.**
- depois [BEBETO]: Os incidentes e a violência física, o vandalismo e o confronto entre as torcidas organizadas podem resultar em ferimento grave, até mesmo em morte.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 19 — `data_102#0`

- **Audiência (data_102):** Governo reforça importância comercial de reduzir emissões de carbono em terminais marítimos
- **Participante atribuído:** Arnaldo Jardim — Presidente da Comissão e Deputado Federal (CIDADANIA-SP)
- **Orador casado na transcrição:** ARNALDO JARDIM (11 frases de 738; 8 oradores na audiência)
- **cos_s** = 0.467 · **best_other** = 0.740 · **Δ** = best_other − cos_s = +0.273 · cos_g = 0.740

**Opinião (PT original):**

> Apoia as iniciativas de transição energética e a redução da pegada de carbono no setor de navegação.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 724 | 0.467 | Dentro daquilo que é o espectro de energias do ponto de vista de energia limpa, o mundo todo vive um debate hoje em torno da utilização da energia nuclear. |
| 2 | 728 | 0.465 | A proposta é que esta Comissão, que trata da transição energética, programe, então, uma audiência especificamente sobre a questão da energia nuclear. |
| 3 | 723 | 0.459 | A proposta que eu apresento hoje é a realização de uma audiência pública para discutir a importância da energia nuclear no processo de transição energética. |
| 4 | 730 | 0.399 | Acho que essa audiência será muito valiosa para que nós possamos ter um cenário de discussão do uso da energia nuclear, razão pela qual eu peço o apoiamento dos Srs. Parlamentares a este nosso requerimento. |
| 5 | 729 | 0.375 | Nós estamos propondo que sejam convidados: o Sr. Ernest Moniz, CEO da Energy Futures Initiative e ex-Secretário de Energia dos Estados Unidos; o Sr. Celso Cunha, Presidente da Associação Brasileira para o Desenvolvimento de Atividades Nucleares — ABDAN; a Sra. Isabelle Boemeke, influenciadora digital na área de energia nuclear; o Sr. Raul Lycurgo Leite, Presidente da ELETRONUCLEAR; um representante da Marinha do Brasil; e um representante da Agência Internacional de Energia. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 520 | 0.740 | DINO ANTUNES DIAS BATISTA | Há a preocupação de uma quantidade de energia certamente muito menor do que as grandes embarcações, mas que já começa a fazer a diferença no processo de descarbonização e redução da pegada de carbono das atividades portuárias. |
| 2 | 287 | 0.727 | PRESIDENTE | Nós estamos discutindo como diminuir também esse impacto ambiental do combustível marítimo. |
| 3 | 354 | 0.722 | FRANCIELLE CARVALHO | Esse trabalho vai alimentar muito essas regulações que estão em discussão e que provavelmente vão forçar a redução de emissões desses combustíveis ao longo do tempo, de acordo com as metas da Organização Marítima Internacional. |
| 4 | 388 | 0.693 | PRESIDENTE | O que queremos, ao final, é um combustível de acordo com esse compromisso de redução da pegada de carbono, do impacto ambiental. |
| 5 | 681 | 0.689 | EDUARDO NERY MACHADO FILHO | No mais, quero só reafirmar aqui, Presidente, o nosso compromisso com a pauta da sustentabilidade, enfatizando estas prioridades, que são: os estudos já mencionados da transição energética; o nosso inventário de emissões de carbono, que entendemos que vai ser um marco para que o setor possa medir as suas emissões e, a partir daí, formular políticas públicas e poder realmente acompanhar se estamos melhorando ou não em termos de descarbonização; e, por fim, o desenvolvimento das nossas hidrovias, que, como o Deputado Leônidas Cristino falou, claro, está totalmente inserido no objeto da transição energética pelo apelo de sustentabilidade que ele carrega, o que é outra superprioridade da agência. |

**Contexto da melhor frase do orador** (frase 724)

- antes [ARNALDO JARDIM]: A proposta que eu apresento hoje é a realização de uma audiência pública para discutir a importância da energia nuclear no processo de transição energética.
- **frase [ARNALDO JARDIM]: Dentro daquilo que é o espectro de energias do ponto de vista de energia limpa, o mundo todo vive um debate hoje em torno da utilização da energia nuclear.**
- depois [ARNALDO JARDIM]: Eu, particularmente, defendo que essa matriz que nós já temos, essa fonte que nós já temos presente, através de Angra e outras iniciativas, possa adquirir outra dimensão com o avanço tecnológico que tem acontecido.

**Contexto da melhor frase global** (frase 520)

- antes [DINO ANTUNES DIAS BATISTA]: Apesar de a operação ter muita lógica, hoje os portos não estão preparados para fornecer essa energia.
- **frase [DINO ANTUNES DIAS BATISTA]: Há a preocupação de uma quantidade de energia certamente muito menor do que as grandes embarcações, mas que já começa a fazer a diferença no processo de descarbonização e redução da pegada de carbono das atividades portuárias.**
- depois [DINO ANTUNES DIAS BATISTA]: Este é só um exemplo, Deputado, das ações que nós temos no Ministério.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 20 — `data_104#7`

- **Audiência (data_104):** Deputados reafirmam interesse da Câmara em participar de definição das regras de renovação das concessões das distribuidoras
- **Participante atribuído:** Sandoval de Araújo Feitosa Neto — Diretor-Geral da Agência Nacional de Energia Elétrica (ANEEL)
- **Orador casado na transcrição:** SANDOVAL DE ARAÚJO FEITOSA NETO (157 frases de 1359; 20 oradores na audiência)
- **cos_s** = 0.696 · **best_other** = 0.683 · **Δ** = best_other − cos_s = -0.012 · cos_g = 0.696

**Opinião (PT original):**

> Comentou sobre a sobrecarga da tarifa elétrica e a necessidade de reconhecer e resolver esse problema.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 1225 | 0.696 | O grande problema é que, entre a produção de energia elétrica, seja nas nossas hidrelétricas, seja nos painéis solares, seja nas hélices das usinas eólicas, seja nas usinas termoelétricas, até a chegada na tomada do consumidor, a tarifa está extremamente sobrecarregada. |
| 2 | 913 | 0.694 | No que se refere aos desafios da tarifa de energia elétrica, temos que modernizar o sistema. |
| 3 | 1249 | 0.675 | Eu acho que uma boa saída, Deputado, seria o reconhecimento, que nós já estamos vendo que existe, e um grande projeto para reformar o setor elétrico. |
| 4 | 1229 | 0.649 | Só que há um efeito colateral, o custo da energia elétrica. |
| 5 | 1244 | 0.608 | E essa forma necessariamente é alocar um recurso maior para os Municípios, sobrecarregando aqueles entes que pagam e recolhem essa compensação, as usinas hidrelétricas no caso, que vão repassar isso para o preço final de energia elétrica. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 1225 | 0.696 | SANDOVAL DE ARAÚJO FEITOSA NETO | O grande problema é que, entre a produção de energia elétrica, seja nas nossas hidrelétricas, seja nos painéis solares, seja nas hélices das usinas eólicas, seja nas usinas termoelétricas, até a chegada na tomada do consumidor, a tarifa está extremamente sobrecarregada. |
| 2 | 913 | 0.694 | SANDOVAL DE ARAÚJO FEITOSA NETO | No que se refere aos desafios da tarifa de energia elétrica, temos que modernizar o sistema. |
| 3 | 365 | 0.683 | RENATA ALBUQUERQUE RIBEIRO | No entanto, existem outros pontos que nos preocupam, principalmente a possibilidade de aumento do custo da conta de luz para o consumidor. |
| 4 | 1249 | 0.675 | SANDOVAL DE ARAÚJO FEITOSA NETO | Eu acho que uma boa saída, Deputado, seria o reconhecimento, que nós já estamos vendo que existe, e um grande projeto para reformar o setor elétrico. |
| 5 | 1335 | 0.661 | RENATA ALBUQUERQUE RIBEIRO | Nós estamos falando aqui de um processo urgente, da reforma do setor elétrico, mas não deve caber ao pequeno consumidor assumir e pagar essa conta. |

**Contexto da melhor frase do orador** (frase 1225)

- antes [SANDOVAL DE ARAÚJO FEITOSA NETO]: Na fala trazida aqui pelo Deputado Julio Lopes — vou começar por ela —, foi destacada a importância de nós termos um plano, um projeto, para que possamos reorientar o desenvolvimento do País a partir da energia elétrica, como, vamos dizer assim, a grande base para que isso ocorra, considerada a nossa grande competitividade relacionada à produção de energia elétrica.
- **frase [SANDOVAL DE ARAÚJO FEITOSA NETO]: O grande problema é que, entre a produção de energia elétrica, seja nas nossas hidrelétricas, seja nos painéis solares, seja nas hélices das usinas eólicas, seja nas usinas termoelétricas, até a chegada na tomada do consumidor, a tarifa está extremamente sobrecarregada.**
- depois [SANDOVAL DE ARAÚJO FEITOSA NETO]: E, claro, o setor elétrico é tão perfeito na sua composição de receita e despesa que o Parlamento o escolheu para ser o grande indutor das políticas públicas, exatamente em função da volatilidade do orçamento público ou de outras questões, que aqui não me compete descrever.

**Contexto da melhor frase global** (frase 1225)

- antes [SANDOVAL DE ARAÚJO FEITOSA NETO]: Na fala trazida aqui pelo Deputado Julio Lopes — vou começar por ela —, foi destacada a importância de nós termos um plano, um projeto, para que possamos reorientar o desenvolvimento do País a partir da energia elétrica, como, vamos dizer assim, a grande base para que isso ocorra, considerada a nossa grande competitividade relacionada à produção de energia elétrica.
- **frase [SANDOVAL DE ARAÚJO FEITOSA NETO]: O grande problema é que, entre a produção de energia elétrica, seja nas nossas hidrelétricas, seja nos painéis solares, seja nas hélices das usinas eólicas, seja nas usinas termoelétricas, até a chegada na tomada do consumidor, a tarifa está extremamente sobrecarregada.**
- depois [SANDOVAL DE ARAÚJO FEITOSA NETO]: E, claro, o setor elétrico é tão perfeito na sua composição de receita e despesa que o Parlamento o escolheu para ser o grande indutor das políticas públicas, exatamente em função da volatilidade do orçamento público ou de outras questões, que aqui não me compete descrever.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 21 — `data_108#16`

- **Audiência (data_108):** Representantes do setor de turismo pedem manutenção de incentivos
- **Participante atribuído:** Jorge Goetten — Deputado Federal (PL - SC)
- **Orador casado na transcrição:** JORGE GOETTEN (57 frases de 1139; 20 oradores na audiência)
- **cos_s** = 0.513 · **best_other** = 0.628 · **Δ** = best_other − cos_s = +0.115 · cos_g = 0.628

**Opinião (PT original):**

> Criticou a necessidade de discutir um direito adquirido do setor de eventos.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 306 | 0.513 | Esta semana, Deputado Bibo, na Frente Parlamentar do Empreendedorismo, eu abordei a necessidade de o Congresso discutir qual é o papel das agências reguladoras. |
| 2 | 312 | 0.510 | Então, é isso que nós deveríamos estar discutindo, mas nós estamos discutindo, envergonhadamente, a manutenção do PERSE. |
| 3 | 331 | 0.428 | Como nós não vamos fazer justiça e manter o PERSE para os parques temáticos, para os operadores turísticos? |
| 4 | 318 | 0.410 | Lá nós tínhamos uma política pública dessa forma e não temos mais". |
| 5 | 308 | 0.406 | Nós deveríamos discutir o que vocês precisam! |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 729 | 0.628 | DORENI CARAMORI JUNIOR | Ainda que o programa tenha sido desenhado inicialmente para o setor de eventos, não acho justo deixarmos nossos coirmãos fora do programa. |
| 2 | 730 | 0.595 | DORENI CARAMORI JUNIOR | Quero deixar registrado que inúmeras CNAEs do setor de eventos ficaram fora desse PL. |
| 3 | 1093 | 0.582 | MILTON SÉRGIO SILVEIRA ZUANAZZI | Às vezes, uma discussão que envolve CNAEs pode criar um ambiente de divisão. |
| 4 | 1071 | 0.579 | MILTON SÉRGIO SILVEIRA ZUANAZZI | Seria necessário outro debate. |
| 5 | 739 | 0.559 | DORENI CARAMORI JUNIOR | Por último, manifesto a nossa — do setor de eventos — total não concordância com a necessidade de um cadastro prévio para usufruir o benefício. |

**Contexto da melhor frase do orador** (frase 306)

- antes [JORGE GOETTEN]: Eu me sinto muito envergonhado, porque nós deveríamos estar discutindo...
- **frase [JORGE GOETTEN]: Esta semana, Deputado Bibo, na Frente Parlamentar do Empreendedorismo, eu abordei a necessidade de o Congresso discutir qual é o papel das agências reguladoras.**
- depois [JORGE GOETTEN]: Nós deveríamos estar discutindo aqui o que a ANAC está fazendo para ajudar o turismo, o que a ANTT está fazendo quanto à melhoria das rodovias para ajudar o turismo, o que a ANEEL está fazendo para ajudar o turismo.

**Contexto da melhor frase global** (frase 729)

- antes [DORENI CARAMORI JUNIOR]: Não entendo que nenhum elo dessa cadeia deveria ficar de fora.
- **frase [DORENI CARAMORI JUNIOR]: Ainda que o programa tenha sido desenhado inicialmente para o setor de eventos, não acho justo deixarmos nossos coirmãos fora do programa.**
- depois [DORENI CARAMORI JUNIOR]: Quero deixar registrado que inúmeras CNAEs do setor de eventos ficaram fora desse PL.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 22 — `data_123#3`

- **Audiência (data_123):** Deputado defende aumento de orçamento para combater a tuberculose no Brasil
- **Participante atribuído:** Ethel Leonor Noia Maciel — Secretária de Vigilância em Saúde e Ambiente
- **Orador casado na transcrição:** ETHEL LEONOR NOIA MACIEL (171 frases de 778; 13 oradores na audiência)
- **cos_s** = 0.756 · **best_other** = 0.779 · **Δ** = best_other − cos_s = +0.023 · cos_g = 0.779

**Opinião (PT original):**

> Destacou a importância de acabar com a epidemia de AIDS, tuberculose e malária.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 74 | 0.756 | Nos nossos Objetivos de Desenvolvimento Sustentável, uma das nossas metas pós-2015, especificamente, é: acabar com a epidemia de AIDS, tuberculose, malária e doenças tropicais negligenciadas. |
| 2 | 118 | 0.726 | Então, lutar pela união dos diagnósticos de HIV e de tuberculose e pela prevenção no grupo com HIV é fundamental. |
| 3 | 204 | 0.687 | A nossa maior arma agora é fazermos a prevenção, interrompermos a cadeia, a progressão para a doença e a possível transmissão. |
| 4 | 123 | 0.687 | Eu quero aqui também destacar a nossa Coordenadora do Programa Nacional de Controle da Tuberculose, a Fernanda, e o Dr. Draurio, que é o Diretor do Departamento de HIV/Aids, Tuberculose, Hepatites Virais e Infecções Sexualmente Transmissíveis e que tem feito essa ponte muito importante entre tuberculose e HIV/AIDS, para que possamos intensificar as ações. |
| 5 | 184 | 0.652 | O Comitê Interministerial visa à eliminação da tuberculose e de outras doenças determinadas socialmente. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 266 | 0.779 | MIGUEL ANGEL ARAGÓN LÓPEZ | Conhecemos a Meta 3, que é a de eliminar a epidemia de AIDS, tuberculose e malária. |
| 2 | 74 | 0.756 | ETHEL LEONOR NOIA MACIEL | Nos nossos Objetivos de Desenvolvimento Sustentável, uma das nossas metas pós-2015, especificamente, é: acabar com a epidemia de AIDS, tuberculose, malária e doenças tropicais negligenciadas. |
| 3 | 118 | 0.726 | ETHEL LEONOR NOIA MACIEL | Então, lutar pela união dos diagnósticos de HIV e de tuberculose e pela prevenção no grupo com HIV é fundamental. |
| 4 | 758 | 0.693 | MARCIA DE ÁVILA BERNI LEÃO | E voltamos a falar que a principal causa de óbito na AIDS se dá por tuberculose. |
| 5 | 204 | 0.687 | ETHEL LEONOR NOIA MACIEL | A nossa maior arma agora é fazermos a prevenção, interrompermos a cadeia, a progressão para a doença e a possível transmissão. |

**Contexto da melhor frase do orador** (frase 74)

- antes [ETHEL LEONOR NOIA MACIEL]: Vou falar um pouquinho do cenário atual e das perspectivas.
- **frase [ETHEL LEONOR NOIA MACIEL]: Nos nossos Objetivos de Desenvolvimento Sustentável, uma das nossas metas pós-2015, especificamente, é: acabar com a epidemia de AIDS, tuberculose, malária e doenças tropicais negligenciadas.**
- depois [ETHEL LEONOR NOIA MACIEL]: Aqui está a nossa estratégia — eu vou falar um pouquinho dos números —: nós queremos reduzir em 90% a incidência e em 95% o número de mortes por tuberculose no Brasil e que nenhuma família sofra por custos catastróficos.

**Contexto da melhor frase global** (frase 266)

- antes [MIGUEL ANGEL ARAGÓN LÓPEZ]: Já foram abordadas as determinantes sociais no contexto dos Objetivos de Desenvolvimento Sustentável.
- **frase [MIGUEL ANGEL ARAGÓN LÓPEZ]: Conhecemos a Meta 3, que é a de eliminar a epidemia de AIDS, tuberculose e malária.**
- depois [MIGUEL ANGEL ARAGÓN LÓPEZ]: O País entende perfeitamente que só a atuação do setor de saúde ou só a abordagem da Meta 3 não vai ser suficiente.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 23 — `data_130#4`

- **Audiência (data_130):** Representantes do audiovisual sugerem a deputados medidas para estimular o setor
- **Participante atribuído:** Márcio — Desconhecido
- **Orador casado na transcrição:** MARCIO FRACCAROLI (63 frases de 1521; 19 oradores na audiência)
- **cos_s** = 0.871 · **best_other** = 0.729 · **Δ** = best_other − cos_s = -0.142 · cos_g = 0.871

**Opinião (PT original):**

> O desafio é distribuir filmes nacionais e colocá-los nas principais telas do VOD.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 450 | 0.871 | Nós temos como desafio distribuir filmes, colocar os nossos filmes na principal tela do VOD. |
| 2 | 439 | 0.590 | Temos que saber quem vai ajudar o cinema nacional, quem vai nos ajudar, quem vai ter um intercâmbio, quem vai nos colocar no lugar do mundo onde o jogo está sendo jogado. |
| 3 | 428 | 0.586 | O que eu posso dizer para este Parlamento é que um filme brasileiro tem a escravidão de pertencer a uma plataforma, enquanto um filme estrangeiro pode circular. |
| 4 | 401 | 0.533 | Eu tenho dividido com os meus pares o desejo de conquistar outros mercados que não sejam só o mercado brasileiro e que eu possa ser um representante da obra audiovisual brasileira no BRICS ou em outros lugares que têm desejo de ter o nosso cinema e o nosso audiovisual. |
| 5 | 399 | 0.500 | Trabalho com filmes brasileiros e filmes estrangeiros. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 450 | 0.871 | MARCIO FRACCAROLI | Nós temos como desafio distribuir filmes, colocar os nossos filmes na principal tela do VOD. |
| 2 | 827 | 0.729 | LÚCIO OTONI | Obviamente, o cinema também precisa do conteúdo nacional! |
| 3 | 601 | 0.713 | FELIPE LOPES | Nós lançamos filmes de todo o País em diversas telas, incluindo ostreaming. |
| 4 | 790 | 0.680 | LÚCIO OTONI | Nós queremos muito que o cinema nacional retorne, que o fomento melhore cada vez mais para o filme nacional. |
| 5 | 521 | 0.670 | SIMONE DE OLIVEIRA | Nós sabemos que o filme nacional é o que impulsiona também o mercado exibidor, é o que faz a diferença para o mercado exibidor. |

**Contexto da melhor frase do orador** (frase 450)

- antes [MARCIO FRACCAROLI]: Então, sou muito voltado para o cinema, que infelizmente vive hoje umsharede mercado pequeno.
- **frase [MARCIO FRACCAROLI]: Nós temos como desafio distribuir filmes, colocar os nossos filmes na principal tela do VOD.**
- depois [MARCIO FRACCAROLI]: Esse é um desafio muito grande.

**Contexto da melhor frase global** (frase 450)

- antes [MARCIO FRACCAROLI]: Então, sou muito voltado para o cinema, que infelizmente vive hoje umsharede mercado pequeno.
- **frase [MARCIO FRACCAROLI]: Nós temos como desafio distribuir filmes, colocar os nossos filmes na principal tela do VOD.**
- depois [MARCIO FRACCAROLI]: Esse é um desafio muito grande.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 24 — `data_132#8`

- **Audiência (data_132):** Governo conclui plano para garantir rádios comunitárias em todos os municípios do País
- **Participante atribuído:** Taís Ladeira — Representante da Associação Mundial de Rádios Comunitárias (AMARC) no Brasil
- **Orador casado na transcrição:** TAÍS LADEIRA (121 frases de 711; 7 oradores na audiência)
- **cos_s** = 0.621 · **best_other** = 0.804 · **Δ** = best_other − cos_s = +0.184 · cos_g = 0.804

**Opinião (PT original):**

> Reitera a necessidade de um novo decreto para garantir melhores condições de funcionamento para as rádios comunitárias.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 542 | 0.621 | No momento que começamos, por exemplo, a fazer uma legislação comparada com a América Latina, nós percebemos que quem tem que ter o poder de decisão de qual é a frequência que quer utilizar e qual é o tamanho da rádio que quer assumir é a comunidade. |
| 2 | 265 | 0.612 | O movimento de rádios comunitárias está junto com outros movimentos do campo do direito à comunicação, para exigir do Governo Federal uma nova Conferência Nacional de Comunicação. |
| 3 | 270 | 0.578 | E, para finalizar a minha apresentação, quero reiterar que nós da AMARC, junto com outras organizações e movimentos, estamos lado a lado da Abraço na exigência de que o decreto seja entregue, para que consigamos, por parte do Executivo, o mínimo e do executivo o mínimo: um novo decreto que nos dê respiro para que consigamos trabalhar no nosso dia a dia. |
| 4 | 221 | 0.561 | É um verdadeiro acinte virem com um argumento sem nexo algum, dizendo que isso iria abrir uma competição, uma competitividade entre rádios comerciais e rádios comunitárias. |
| 5 | 215 | 0.551 | Essa associação cita os números das rádios comunitárias. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 27 | 0.804 | PRESIDENTE | Estamos prestes a testemunhar a publicação de um novo decreto, que, sem dúvida, precisa estabelecer condições mínimas para a criação e manutenção das rádios comunitárias brasileiras desempenhando um papel fundamental na vida das pessoas. |
| 2 | 427 | 0.779 | DANIELA NAUFEL SCHETTINO | Tecnicamente, nós temos tentado melhorar as condições para prestação do serviço e autorização das rádios comunitárias. |
| 3 | 442 | 0.771 | DANIELA NAUFEL SCHETTINO | Depois veio o decreto que regulamentou a lei, que fala que, quanto ao tipo de modulação, as rádios comunitárias vão operar na faixa de frequência modulada. |
| 4 | 678 | 0.730 | DANIELA NAUFEL SCHETTINO | Então, precisamos colocar regras para regulamentar o espectro para que todos tenham vez e oportunidade."Ah, mas eu acho que deveria haver mais canais para as rádios comunitárias".O.k., se a lei alterar, nem eu e nem o Renato vamos fazer nada diferente disso, muito pelo contrário. |
| 5 | 343 | 0.711 | HIGINO ÍTALO GERMANI | Para respeitar os critérios de proteção e interferência, serão necessários canais de FM. |

**Contexto da melhor frase do orador** (frase 542)

- antes [TAÍS LADEIRA]: Porque anos depois a Abraço foi fundada, e eu fui participar da Associação Mundial de Rádios Comunitárias.
- **frase [TAÍS LADEIRA]: No momento que começamos, por exemplo, a fazer uma legislação comparada com a América Latina, nós percebemos que quem tem que ter o poder de decisão de qual é a frequência que quer utilizar e qual é o tamanho da rádio que quer assumir é a comunidade.**
- depois [TAÍS LADEIRA]: É claro que o Estado brasileiro, nas pessoas da ANATEL e também do Ministério das Comunicações, tem como coordenar esse processo, mas a autonomia tem que ser da comunidade.

**Contexto da melhor frase global** (frase 27)

- antes [PRESIDENTE]: A democracia exige que ouçamos todos, que falemos com todos, para que todos sejam de fato representados na maioria.
- **frase [PRESIDENTE]: Estamos prestes a testemunhar a publicação de um novo decreto, que, sem dúvida, precisa estabelecer condições mínimas para a criação e manutenção das rádios comunitárias brasileiras desempenhando um papel fundamental na vida das pessoas.**
- depois [PRESIDENTE]: O momento é de debate, e unidos vamos quebrar todas as barreiras que existem e exigir de mais, punir de mais e proteger de menos.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 25 — `data_133#29`

- **Audiência (data_133):** Deputados criticam ausência de presidente da Enel Brasil em audiência na Câmara
- **Participante atribuído:** Aureo Ribeiro — Deputado (Bloco/SOLIDARIEDADE - RJ)
- **Orador casado na transcrição:** AUREO RIBEIRO (59 frases de 628; 13 oradores na audiência)
- **cos_s** = 0.615 · **best_other** = 0.637 · **Δ** = best_other − cos_s = +0.022 · cos_g = 0.637

**Opinião (PT original):**

> Expressa preocupação com a falta de respostas às reclamações dos consumidores.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 333 | 0.615 | Primeiro, eu quero externar que não estou satisfeito com o serviço ofertado pela companhia elétrica no nosso País. |
| 2 | 380 | 0.549 | Concordo que o serviço ofertado ao brasileiro é de péssima qualidade, mas acho que não podemos deixar de fazer esse debate na data de hoje, porque quem está perdendo é o consumidor brasileiro. |
| 3 | 334 | 0.532 | Não atende à necessidade que temos. |
| 4 | 349 | 0.493 | Podemos perder a grande oportunidade de ampliar este debate, entender o que está acontecendo, recebendo informações da agência. |
| 5 | 382 | 0.476 | Eu queria perguntar à ANEEL quantos consumidores fizeram a reclamação de que estavam sem luz no momento da interrupção de energia elétrica. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 129 | 0.637 | ALEX MANENTE | Em vez de aumentar, diminuiu, e não houve nenhuma eficiência, nenhuma resposta ao consumidor. |
| 2 | 333 | 0.615 | AUREO RIBEIRO | Primeiro, eu quero externar que não estou satisfeito com o serviço ofertado pela companhia elétrica no nosso País. |
| 3 | 18 | 0.569 | PRESIDENTE | Em muitos casos, temos assistido um desserviço das distribuidoras, que cobram tarifas altas e não prestam serviço. |
| 4 | 380 | 0.549 | AUREO RIBEIRO | Concordo que o serviço ofertado ao brasileiro é de péssima qualidade, mas acho que não podemos deixar de fazer esse debate na data de hoje, porque quem está perdendo é o consumidor brasileiro. |
| 5 | 301 | 0.540 | CELSO RUSSOMANNO | Está difícil conviver com uma empresa que tem a quantidade de reclamações que eu tenho aqui. |

**Contexto da melhor frase do orador** (frase 333)

- antes [AUREO RIBEIRO]: Foi aqui apresentado um requerimento para a realização de uma audiência pública, para que se pudesse debater esse tema, mas temos que ter clareza do que estamos discutindo aqui.
- **frase [AUREO RIBEIRO]: Primeiro, eu quero externar que não estou satisfeito com o serviço ofertado pela companhia elétrica no nosso País.**
- depois [AUREO RIBEIRO]: Não atende à necessidade que temos.

**Contexto da melhor frase global** (frase 129)

- antes [ALEX MANENTE]: É importante ressaltar que a ENEL diminuiu 36% do número de funcionários, enquanto nós tivemos 7% de aumento do número de residências.
- **frase [ALEX MANENTE]: Em vez de aumentar, diminuiu, e não houve nenhuma eficiência, nenhuma resposta ao consumidor.**
- depois [ALEX MANENTE]: Nós precisamos é estimular, principalmente por causa da falta de compromisso e de respeito da ENEL com esta Casa, a criação da CPI que está sendo proposta, para que façamos avançar sua instalaçãoe possamos ter o desdobramento adequado, com as punições devidas e o ressarcimento à população brasileira de tudo o que foi causado.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 26 — `data_145#9`

- **Audiência (data_145):** Desempenho atual na segurança pública supera 2022, diz ministro da Justiça
- **Participante atribuído:** Flávio Dino — Ministro da Justiça e Segurança Pública
- **Orador casado na transcrição:** MINISTRO FLÁVIO DINO DE CASTRO E COSTA (664 frases de 1829; 23 oradores na audiência)
- **cos_s** = 0.777 · **best_other** = 0.718 · **Δ** = best_other − cos_s = -0.060 · cos_g = 0.777

**Opinião (PT original):**

> Destacou que não há redução no orçamento de segurança pública para 2024 e que as emendas parlamentares ainda não foram apresentadas.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 330 | 0.777 | Em resumo à sua perquirição, eu informo que não há corte de orçamento para 2024. |
| 2 | 116 | 0.762 | Como não há ainda prazo para as emendas ao Orçamento de 2024, nós fizemos uma comparação, sem levar em conta as emendas parlamentares. |
| 3 | 112 | 0.757 | Lembro que o Orçamento de 2024 ainda não foi votado, portanto não é possível aquilatar se haverá ou não redução em relação a um item fundamental, que são as emendas parlamentares. |
| 4 | 113 | 0.668 | As senhoras e os senhores ainda não apresentaram emendas parlamentares. |
| 5 | 128 | 0.633 | Portanto, respondendo ao segundo requerimento, na proposta orçamentária de 2024, elaborada pelo nosso Ministério, não há em absoluto a redução de 700 milhões de reais. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 330 | 0.777 | MINISTRO FLÁVIO DINO DE CASTRO E COSTA | Em resumo à sua perquirição, eu informo que não há corte de orçamento para 2024. |
| 2 | 116 | 0.762 | MINISTRO FLÁVIO DINO DE CASTRO E COSTA | Como não há ainda prazo para as emendas ao Orçamento de 2024, nós fizemos uma comparação, sem levar em conta as emendas parlamentares. |
| 3 | 112 | 0.757 | MINISTRO FLÁVIO DINO DE CASTRO E COSTA | Lembro que o Orçamento de 2024 ainda não foi votado, portanto não é possível aquilatar se haverá ou não redução em relação a um item fundamental, que são as emendas parlamentares. |
| 4 | 1575 | 0.718 | KIM KATAGUIRI | V.Exa. diz que não há corte no orçamento por parte da sua Pasta e diz que o orçamento ainda não foi votado e, portanto, não há que se falar em corte. |
| 5 | 113 | 0.668 | MINISTRO FLÁVIO DINO DE CASTRO E COSTA | As senhoras e os senhores ainda não apresentaram emendas parlamentares. |

**Contexto da melhor frase do orador** (frase 330)

- antes [MINISTRO FLÁVIO DINO DE CASTRO E COSTA]: O SR. MINISTRO FLÁVIO DINO DE CASTRO E COSTA- Então, a taxa é declinante.
- **frase [MINISTRO FLÁVIO DINO DE CASTRO E COSTA]: Em resumo à sua perquirição, eu informo que não há corte de orçamento para 2024.**
- depois [MINISTRO FLÁVIO DINO DE CASTRO E COSTA]: E eu espero que o senhor consulte os dados.

**Contexto da melhor frase global** (frase 330)

- antes [MINISTRO FLÁVIO DINO DE CASTRO E COSTA]: O SR. MINISTRO FLÁVIO DINO DE CASTRO E COSTA- Então, a taxa é declinante.
- **frase [MINISTRO FLÁVIO DINO DE CASTRO E COSTA]: Em resumo à sua perquirição, eu informo que não há corte de orçamento para 2024.**
- depois [MINISTRO FLÁVIO DINO DE CASTRO E COSTA]: E eu espero que o senhor consulte os dados.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 27 — `data_149#17`

- **Audiência (data_149):** Mudança demográfica exige reestruturação do Estado, afirmam especialistas
- **Participante atribuído:** Matheus Guerra Cotta — Secretário de Relações de Trabalho, Mobilização e Inserção Profissional, Federação Nacional dos Arquitetos e Urbanistas (FNA)
- **Orador casado na transcrição:** MATHEUS GUERRA COTTA (67 frases de 936; 11 oradores na audiência)
- **cos_s** = 0.763 · **best_other** = 0.797 · **Δ** = best_other − cos_s = +0.035 · cos_g = 0.797

**Opinião (PT original):**

> Sugeriu uma ação transversal envolvendo diferentes Ministérios e entidades para garantir políticas efetivas para a população idosa.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 291 | 0.763 | Dessa forma, pode ser estratégica, de novo, uma ação de Estado que pense uma forma de haver interlocução local, que identifique qual é essa população idosa que vai surgindo a cada ano, como ela se entende, como ela pretende participar e se é algum agente ativo, como o marco legal pressupõe, para essas políticas que são também destinatárias. |
| 2 | 265 | 0.743 | Nessa condição colocada, especialmente, essas políticas públicas devem chegar aonde essa população idosa se estabelece. |
| 3 | 271 | 0.722 | Inclusive, parece que a Política Nacional do Idoso e o Conselho Nacional dos Direitos da Pessoa Idosa têm uma representatividade bastante consistente, assim como há vários Ministérios e entidades da sociedade não governamental também. |
| 4 | 288 | 0.709 | Ao mesmo tempo, pelo visto, a política nacional de direitos humanos das pessoas idosas tem também como referência exatamente esses espaços de convivência, de socialização, que talvez sejam estratégicos até para outras políticas setoriais poderem acontecer, como a política de saúde, a política do cuidado de maneira geral. |
| 5 | 254 | 0.690 | Eu gostei de ouvir a fala dos colegas da Mesa, especialmente do Secretário Alexandre, porque verificamos que nos instrumentos que temos hoje direcionados para a questão da pessoa idosa — e eu fiz questão de verificar rapidamente o que está colocado na Política Nacional do Idoso — fica evidente o papel da família, da sociedade e do Estado no dever de assegurar os direitos e as condições necessárias para o bem-estar, incluindo a participação da comunidade. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 723 | 0.797 | MICHEL SAAD | Quais ações, em 2023, a Secretaria e o Ministério conseguiram pôr em prática no âmbito das políticas públicas para o idoso? |
| 2 | 291 | 0.763 | MATHEUS GUERRA COTTA | Dessa forma, pode ser estratégica, de novo, uma ação de Estado que pense uma forma de haver interlocução local, que identifique qual é essa população idosa que vai surgindo a cada ano, como ela se entende, como ela pretende participar e se é algum agente ativo, como o marco legal pressupõe, para essas políticas que são também destinatárias. |
| 3 | 203 | 0.756 | DANYEL IÓRIO DE LIMA | Então, a ideia é de que haja mais órgãos específicos de gestão da política de direitos humanos da pessoa idosa nos territórios, a partir da ação do Ministério dos Direitos Humanos. |
| 4 | 265 | 0.743 | MATHEUS GUERRA COTTA | Nessa condição colocada, especialmente, essas políticas públicas devem chegar aonde essa população idosa se estabelece. |
| 5 | 330 | 0.734 | ANDRÉA DOS SANTOS | E esse arranjo que precisamos organizar através da Câmara dos Deputados e desta Comissão é fundamental para que possamos, de fato, fazer um trabalho articulado de ações em defesa e para a população de pessoas idosas. |

**Contexto da melhor frase do orador** (frase 291)

- antes [MATHEUS GUERRA COTTA]: Frente à diversidade regional que temos no País, as diversas condições locais, que possam surgir formas específicas e peculiares em cada local do País de se organizar esses espaços de convivência, de socialização, de cuidado.
- **frase [MATHEUS GUERRA COTTA]: Dessa forma, pode ser estratégica, de novo, uma ação de Estado que pense uma forma de haver interlocução local, que identifique qual é essa população idosa que vai surgindo a cada ano, como ela se entende, como ela pretende participar e se é algum agente ativo, como o marco legal pressupõe, para essas políticas que são também destinatárias.**
- depois [MATHEUS GUERRA COTTA]: Esse é o nosso desafio.

**Contexto da melhor frase global** (frase 723)

- antes [MICHEL SAAD]: Queria deixar aqui também uma pergunta para o Secretário Nacional.
- **frase [MICHEL SAAD]: Quais ações, em 2023, a Secretaria e o Ministério conseguiram pôr em prática no âmbito das políticas públicas para o idoso?**
- depois [MICHEL SAAD]: Faço essa pergunta até para que nós da Comissão lá no Rio de Janeiro possamos divulgar a informação e levá-la até a ponta, o que é um desafio.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 28 — `data_151#22`

- **Audiência (data_151):** Especialistas defendem educação profissionalizante nos presídios
- **Participante atribuído:** Adauto Locatelli Taufer — Representante da Federação de Sindicatos de Professores e Professoras de Institutos Federais
- **Orador casado na transcrição:** ADAUTO LOCATELLI TAUFER (9 frases de 682; 12 oradores na audiência)
- **cos_s** = 0.560 · **best_other** = 0.739 · **Δ** = best_other − cos_s = +0.179 · cos_g = 0.739

**Opinião (PT original):**

> A leitura é um elemento essencial e deve ser promovida no sistema prisional.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 573 | 0.560 | Nós somos professores de universidades públicas e de institutos federais, e esta é uma pauta que certamente entrará no nosso planejamento, a da educação direcionada ao sistema prisional. |
| 2 | 578 | 0.526 | Fico muito contente, na condição de professor de literatura, porque a leitura aqui foi destacada e foi referendada várias vezes. |
| 3 | 577 | 0.470 | De novo reitero que o nosso GT e nós professores saímos daqui com o compromisso de promover ações direcionadas à população carcerária, também como uma alternativa de ressocialização e de reinserção desses sujeitos na sociedade. |
| 4 | 572 | 0.334 | Eu gostaria de ressaltar a importância de todas as discussões que foram feitas aqui, hoje de manhã, o quanto nós nos sentimos contemplados por todas as falas e o que levamos desta manhã, de aprendizado. |
| 5 | 575 | 0.326 | Temos como pautas, que defendemos com muita garra e muito afinco, ações direcionadas a uma educação antimachista, mais diversa e antirracista.Sobretudo neste ano nossas ações foram direcionadas à pauta das mulheres. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 34 | 0.739 | PETRA SILVIA PFALLER | A educação, a escola, a remissão por leitura é uma maneira de desencarcerar. |
| 2 | 353 | 0.732 | DIÓGENES FAUSTINO DO NASCIMENTO | A EJA é um instrumento que estimula a leitura e que consegue, através da educação, reintegrar à sociedade esse apenado, esse egresso do sistema penitenciário. |
| 3 | 358 | 0.706 | DIÓGENES FAUSTINO DO NASCIMENTO | Talvez exista esse grande medo porque a leitura liberta, a leitura ensina e forma cidadãos. |
| 4 | 355 | 0.633 | DIÓGENES FAUSTINO DO NASCIMENTO | Muitas bibliotecas no sistema prisional contêm livros plastificados, impossibilitando que quem está em cela e deseje ler tenha acesso à leitura. |
| 5 | 591 | 0.625 | MARIÂNGELA GRACIANO | Da mesma maneira, haverá o PNLD Literário, que também contemplará o sistema prisional. |

**Contexto da melhor frase do orador** (frase 573)

- antes [ADAUTO LOCATELLI TAUFER]: Eu gostaria de ressaltar a importância de todas as discussões que foram feitas aqui, hoje de manhã, o quanto nós nos sentimos contemplados por todas as falas e o que levamos desta manhã, de aprendizado.
- **frase [ADAUTO LOCATELLI TAUFER]: Nós somos professores de universidades públicas e de institutos federais, e esta é uma pauta que certamente entrará no nosso planejamento, a da educação direcionada ao sistema prisional.**
- depois [ADAUTO LOCATELLI TAUFER]: Além de professores universitários, nós também fazemos parte da ADUFRGS-Sindical, da PROIFES-Federação e do Grupo de Trabalho de Direitos Humanos.

**Contexto da melhor frase global** (frase 34)

- antes [PETRA SILVIA PFALLER]: Quando entramos no cárcere, percebemos que muitos querem estudar, sair desse mundo do cárcere e ter uma nova chance ao sair.
- **frase [PETRA SILVIA PFALLER]: A educação, a escola, a remissão por leitura é uma maneira de desencarcerar.**
- depois [PETRA SILVIA PFALLER]: Nós entendemos isso como uma medida de desencarceramento.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 29 — `data_152#8`

- **Audiência (data_152):** Debatedores alertam sobre extinção da lei que regulamenta o seguro obrigatório para vítimas do trânsito
- **Participante atribuído:** Patricia Menezes — Advogada e Diretora Jurídica do CDVT
- **Orador casado na transcrição:** PATRICIA MENEZES (65 frases de 725; 9 oradores na audiência)
- **cos_s** = 0.635 · **best_other** = 0.795 · **Δ** = best_other − cos_s = +0.160 · cos_g = 0.795

**Opinião (PT original):**

> Defende a importância do DPVAT para a manutenção das vítimas de trânsito.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 255 | 0.635 | E gostaria que esta audiência pública de fato surtisse um efeito prático, para que nós possamos ter a real noção e para que haja, de maneira urgente, a manutenção do seguro obrigatório DPVAT não só para 2024, mas para todo o sempre, porque é um seguro universal do qual necessitam a vítima de trânsito e a população. |
| 2 | 232 | 0.624 | Senhores, é sigiloso o direito das vítimas de trânsito de saber como é o DPVAT? |
| 3 | 203 | 0.623 | Gostaria também de deixar claro, pela minha fala, que estou aqui representando as vítimas de acidente de trânsito pelo CDVT. |
| 4 | 214 | 0.607 | Isso foi e é muito traumático até hoje pelas dificuldades que a vítima de trânsito tem de requerer o seu direito. |
| 5 | 204 | 0.584 | Eu represento aqui, como a nossa entidade, aquelas pessoas que precisam receber as suas indenizações para se manterem, porque, depois de um acidente de trânsito, como alguns já falaram, uns têm lesões leves, outros têm lesões médias e outros têm lesões graves, ficam deficientes, sofrem amputações. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 60 | 0.795 | CARLOS ROBERTO ALVES DE QUEIROZ | Eu entendo que é importante destacar aqui que a política pública do seguro DPVAT, tal como foi estabelecida na Lei 6.194, prevê apoio e reparação básicos e imediatos às vítimas de trânsito e seus beneficiários. |
| 2 | 618 | 0.740 | ERIKA KOKAY | Para além disso, deve-se fazer uma campanha para que as pessoas tenham consciência do próprio DPVAT, porque elas têm esse direito quando sofrem acidentes. |
| 3 | 647 | 0.740 | ERIKA KOKAY | Portanto, tudo isso faz com que tenhamos a necessidade de que a Caixa faça essa escuta.O DPVAT, penso eu, deveria ter um fórum permanente de discussão, com representantes das vítimas, com todas as pessoas que estão envolvidas no DPVAT, mas, em particular, com prioridade, porque ele funciona para atendimento das vítimas, seja por meio do financiamento ao SUS, seja por meio de indenização, seja por meio de campanhas, para que não haja outras vítimas da violência no trânsito, que tem índices tão cruéis e que devem nos levar a uma reflexão. |
| 4 | 474 | 0.720 | CARLOS ADEMIR VERAS PINHEIRO | O seguro DPVAT indeniza aquelas pessoas que sofreram acidente de trânsito e estão em estado de vulnerabilidade. |
| 5 | 125 | 0.718 | LÚCIO DEODATO MACHADO DE ALMEIDA | O DPVAT é o maior instrumento de redução de acidente de trânsito que existe. |

**Contexto da melhor frase do orador** (frase 255)

- antes [PATRICIA MENEZES]: Então, eu gostaria de finalizar — nem sei se já passou todo o meu tempo — agradecendo novamente a oportunidade.
- **frase [PATRICIA MENEZES]: E gostaria que esta audiência pública de fato surtisse um efeito prático, para que nós possamos ter a real noção e para que haja, de maneira urgente, a manutenção do seguro obrigatório DPVAT não só para 2024, mas para todo o sempre, porque é um seguro universal do qual necessitam a vítima de trânsito e a população.**
- depois [PATRICIA MENEZES]: Agradeço a todos.

**Contexto da melhor frase global** (frase 60)

- antes [CARLOS ROBERTO ALVES DE QUEIROZ]: As regras de responsabilização civil são basicamente as previstas no Código Civil, nos arts. 186 e 927.
- **frase [CARLOS ROBERTO ALVES DE QUEIROZ]: Eu entendo que é importante destacar aqui que a política pública do seguro DPVAT, tal como foi estabelecida na Lei 6.194, prevê apoio e reparação básicos e imediatos às vítimas de trânsito e seus beneficiários.**
- depois [CARLOS ROBERTO ALVES DE QUEIROZ]: É certo que o sistema de responsabilização civil do causador do acidente, do culpado pelo acidente, é o que, em tese, teria mais condições de promover a justiça em cada caso concreto, promovendo, assim, maiores e mais justas indenizações aos vitimados ou aos seus beneficiários.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 30 — `data_154#24`

- **Audiência (data_154):** Deputadas e especialistas cobram políticas públicas voltadas para mulheres no climatério
- **Participante atribuído:** Dra. Pérola Grinberg Plapler — Diretora da Divisão de Medicina Física do Instituto de Ortopedia e Traumatologia do Hospital das Clínicas da USP
- **Orador casado na transcrição:** PÉROLA GRINBERG PLAPLER (76 frases de 1172; 13 oradores na audiência)
- **cos_s** = 0.697 · **best_other** = 0.843 · **Δ** = best_other − cos_s = +0.146 · cos_g = 0.843

**Opinião (PT original):**

> Ressaltou a necessidade de apoio e informação para mulheres na menopausa.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 794 | 0.697 | Agradeço aos que me antecederam, agradeço por essa oportunidade de realmente poder falar sobre a importância dessas patologias na terceira idade e no climatério ou menopausa, exatamente pela falta do hormônio estrógeno. |
| 2 | 1123 | 0.659 | Eu realmente me senti acolhida, dentro dos nossos objetivos de trabalhar em prol das mulheres que estão entrando na menopausa. |
| 3 | 1126 | 0.572 | As mulheres estão vivendo mais tempo, e nós precisamos dar a elas qualidade de vida. |
| 4 | 752 | 0.548 | Eu, como médica fisiatra, lido exatamente com isso, com as repercussões da menopausa no aparelho locomotor. |
| 5 | 758 | 0.538 | As três patologias acabam sendo muito mais prevalentes em mulheres na pós-menopausa, exatamente pela falta do hormônio estrógeno. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 196 | 0.843 | ADRIANA FERREIRA | Nós nascemos da necessidade de informação e assistência integral à saúde da mulher na menopausa. |
| 2 | 115 | 0.789 | CARMEN HELENA FERREIRA FORO | O tema da informação sobre a menopausa, programas sobre menopausa é algo que tem que nos mover. |
| 3 | 914 | 0.762 | MARILDA DE CÁSSIA CASTRO | Por isso, estou trazendo para os cursos de doula a questão da menopausa.Nós temos contato, na rede de apoio das mulheres, com as avós, que geralmente estão na menopausa, no climatério e na menopausa. |
| 4 | 144 | 0.731 | CARMEN HELENA FERREIRA FORO | Portanto, a existência de um programa que reafirme que mulheres nesse ciclo precisam dessa atenção é fundamental. |
| 5 | 152 | 0.725 | CARMEN HELENA FERREIRA FORO | Eu comentava com a Deputada que, nesta mesa, há mulheres que estão na pré-menopausa, mulheres que estão na menopausa, mulheres que já passaram pela menopausa, mulheres que podem falar com propriedade sobre o tema. |

**Contexto da melhor frase do orador** (frase 794)

- antes [PÉROLA GRINBERG PLAPLER]: Não podemos deixar de estar muito felizes por isso ter sido assinado ainda nesta semana.
- **frase [PÉROLA GRINBERG PLAPLER]: Agradeço aos que me antecederam, agradeço por essa oportunidade de realmente poder falar sobre a importância dessas patologias na terceira idade e no climatério ou menopausa, exatamente pela falta do hormônio estrógeno.**
- depois [PÉROLA GRINBERG PLAPLER]: Agradeço muito poder falar com vocês.

**Contexto da melhor frase global** (frase 196)

- antes [ADRIANA FERREIRA]: Este é o nosso grupo que hoje compõe a nossa organização.
- **frase [ADRIANA FERREIRA]: Nós nascemos da necessidade de informação e assistência integral à saúde da mulher na menopausa.**
- depois [ADRIANA FERREIRA]: Hoje, como foi muito bem dito pelo Ministério da Saúde, há uma série de políticas públicas que perpassam várias faixas etárias, mas não há especificamente, em algum programa ou política, um trabalho diferenciado, uma ação efetiva com foco no público que está no climatério ou na menopausa.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 31 — `data_155#5`

- **Audiência (data_155):** Nos 20 anos do Estatuto do Idoso, especialistas pedem consolidação de políticas públicas
- **Participante atribuído:** Maria do Carmo Guido Di Lascio — Participante da audiência
- **Orador casado na transcrição:** MARIA DO CARMO GUIDO DI LASCIO (9 frases de 920; 11 oradores na audiência)
- **cos_s** = 0.344 · **best_other** = 0.734 · **Δ** = best_other − cos_s = +0.390 · cos_g = 0.734

**Opinião (PT original):**

> Apoiou a necessidade de revisão das políticas de pensão por morte.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 908 | 0.344 | E, através dessa Comissão do Idoso da Câmara Municipal de São Paulo, conseguimos levantar bandeiras, fazer pedidos de audiência pública. |
| 2 | 907 | 0.320 | Eu sou Conselheira do Conselho Municipal de Direitos da Pessoa Idosa de São Paulo e sou uma frequentadora assídua da nossa Comissão do Idoso. |
| 3 | 909 | 0.312 | Então, é uma saudação que eu trago de São Paulo para a Comissão do Idoso. |
| 4 | 904 | 0.216 | Eu queria saudar a Comissão aqui da Câmara. |
| 5 | 910 | 0.202 | Sempre acompanhamos esta Comissão pela televisão, quando há temas interessantes. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 866 | 0.734 | LUIZ LEGÑANI | Ele pede que a questão da pensão por morte seja revisto, Presidente Aliel. |
| 2 | 90 | 0.628 | ANTÔNIO FERNANDES TONINHO COSTA | Nós defendemos uma nova revisão na forma de financiamento das Instituições de Longa Permanência para Idosos — ILPIs filantrópicas. |
| 3 | 70 | 0.618 | ANTÔNIO FERNANDES TONINHO COSTA | Isso criou uma certa expectativa de sensibilidade e despertou, num certo ponto, um olhar para a política do idoso. |
| 4 | 811 | 0.613 | MARGÔ GOMES DE OLIVEIRA KARNIKOWSKI | Nós temos refletido muito sobre os avanços conquistados a partir do Estatuto do Idoso, que é uma lei federal e que, portanto, deve ser cumprida. |
| 5 | 202 | 0.599 | ALEXANDRE KALACHE | Ele foi indispensável para que essa proposta de uma política de Estado pudesse se tornar lei. |

**Contexto da melhor frase do orador** (frase 908)

- antes [MARIA DO CARMO GUIDO DI LASCIO]: Eu sou Conselheira do Conselho Municipal de Direitos da Pessoa Idosa de São Paulo e sou uma frequentadora assídua da nossa Comissão do Idoso.
- **frase [MARIA DO CARMO GUIDO DI LASCIO]: E, através dessa Comissão do Idoso da Câmara Municipal de São Paulo, conseguimos levantar bandeiras, fazer pedidos de audiência pública.**
- depois [MARIA DO CARMO GUIDO DI LASCIO]: Então, é uma saudação que eu trago de São Paulo para a Comissão do Idoso.

**Contexto da melhor frase global** (frase 866)

- antes [LUIZ LEGÑANI]: Essa mãe, que hoje tem 47 anos, já tentou suicídio, tem depressão, tem dificuldade de conseguir emprego e está pedindo socorro.
- **frase [LUIZ LEGÑANI]: Ele pede que a questão da pensão por morte seja revisto, Presidente Aliel.**
- depois [LUIZ LEGÑANI]: E essa questão é uma das bandeiras de luta da COBAP.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 32 — `data_155#14`

- **Audiência (data_155):** Nos 20 anos do Estatuto do Idoso, especialistas pedem consolidação de políticas públicas
- **Participante atribuído:** Alexandre Kalache — Presidente do Centro Internacional de Longevidade Brasil (ILC-BR)
- **Orador casado na transcrição:** ALEXANDRE KALACHE (87 frases de 920; 11 oradores na audiência)
- **cos_s** = 0.519 · **best_other** = 0.627 · **Δ** = best_other − cos_s = +0.108 · cos_g = 0.627

**Opinião (PT original):**

> Defendeu a participação ativa de universidades e entidades da sociedade civil na formulação de políticas públicas.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 202 | 0.519 | Ele foi indispensável para que essa proposta de uma política de Estado pudesse se tornar lei. |
| 2 | 227 | 0.446 | Da mesma forma, combater o idadismo é função de toda a sociedade e de todos os grupos etários. |
| 3 | 224 | 0.406 | Combater o idadismo é dever de todos. |
| 4 | 216 | 0.393 | O meu dileto amigo Alexandre da Silva esteve presente, em fevereiro, na reunião das Nações Unidas — uma reunião de composição aberta que trata de direitos humanos. |
| 5 | 173 | 0.380 | Ele se junta a dois outros marcos civilizatórios que nós conquistamos com determinação e continuaremos defendendo ardorosamente. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 570 | 0.627 | RAPHAEL FRANCO CASTELO BRANCO CARVALHO | E aí é necessário que as nossas políticas públicas, não só as políticas públicas construídas pelo Estado, até porque, para que nós tenhamos uma política pública, não existe política pública sem povo, então, é importante a participação da universidade, é importante a participação da ciência, da tecnologia, das entidades da sociedade civil, para que possamos, nesse grande esforço nacional, tornar de fato um País, um Brasil que seja humano, digno, não só para pessoas idosas, mas também para outros segmentos populacionais. |
| 2 | 477 | 0.600 | FLÁVIA MORAIS | Então, há várias ações que nós podemos fazer articuladas com as universidades — está aqui a UnB do meu ladinho —, e nós sabemos da importância de trabalharmos paralelamente à questão da Política Nacional de Cuidados. |
| 3 | 393 | 0.579 | ALEXANDRE DA SILVA | Isso é feito em uma articulação com o Município, com o Estado e com órgãos, conselhos, universidades, instituições de ensino superior, lideranças comunitárias, ONGs, etc. |
| 4 | 327 | 0.553 | ALEXANDRE DA SILVA | É importante que nós possamos gerar esse fortalecimento da participação social, que se dá tanto com o Conselho Nacional, com os Conselhos Estaduais, com os Conselhos Municipais e, como eu tenho dito, também com os fóruns — o Jairo está aqui para poder falar e representar esse local —, com as rodas de conversa, os quintais. |
| 5 | 350 | 0.548 | ALEXANDRE DA SILVA | Há também a importância de se discutir com lideranças comunitárias, discutir com conselhos e tantos outros órgãos que vão nos ajudar a pensar essa perspectiva. |

**Contexto da melhor frase do orador** (frase 202)

- antes [ALEXANDRE KALACHE]: Eu não sei, sinceramente, Deputado Aliel, se nós teríamos a sensibilidade política, hoje, no Congresso para esse espírito de humanismo, de solidariedade e de empatia que foi necessário para que o Estatuto fosse promulgado.
- **frase [ALEXANDRE KALACHE]: Ele foi indispensável para que essa proposta de uma política de Estado pudesse se tornar lei.**
- depois [ALEXANDRE KALACHE]: Eu digo isso porque, e o senhor citou, até hoje, até agora, o Brasil não promulgou, não assinou a Convenção Interamericana sobre os Direitos das Pessoas Idosas.

**Contexto da melhor frase global** (frase 570)

- antes [RAPHAEL FRANCO CASTELO BRANCO CARVALHO]: Ou seja, o processo de envelhecimento brasileiro, e não só brasileiro, mas dos países subdesenvolvidos, é amplamente diferente do que foi vivenciado em outros espaços do mundo.
- **frase [RAPHAEL FRANCO CASTELO BRANCO CARVALHO]: E aí é necessário que as nossas políticas públicas, não só as políticas públicas construídas pelo Estado, até porque, para que nós tenhamos uma política pública, não existe política pública sem povo, então, é importante a participação da universidade, é importante a participação da ciência, da tecnologia, das entidades da sociedade civil, para que possamos, nesse grande esforço nacional, tornar de fato um País, um Brasil que seja humano, digno, não só para pessoas idosas, mas também para outros segmentos populacionais.**
- depois [RAPHAEL FRANCO CASTELO BRANCO CARVALHO]: Outro desafio que sinalizamos é a ratificação.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 33 — `data_156#8`

- **Audiência (data_156):** Universidades comunitárias cobram ajustes na legislação para manter qualidade do ensino
- **Participante atribuído:** Ulysses Tavares Teixeira — Diretor de Avaliação da Educação Superior do INEP
- **Orador casado na transcrição:** ULYSSES TAVARES TEIXEIRA (178 frases de 764; 9 oradores na audiência)
- **cos_s** = 0.668 · **best_other** = 0.684 · **Δ** = best_other − cos_s = +0.016 · cos_g = 0.684

**Opinião (PT original):**

> A importância de diretrizes claras para a educação superior que contemplem as comunitárias.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 168 | 0.668 | Poderíamos, por exemplo, dentro do cenário da educação superior como um todo, discutir sobre o papel das universidades comunitárias, contextualizado num plano nacional da educação superior.Mas esse documento não existe. |
| 2 | 181 | 0.636 | Faço isso para nos dar a liberdade de pensar qual é o indicador, a estatística, o dado que nós precisamos para caracterizar a atuação de cada tipo de instituição e a especificidade de cada tipo de curso da melhor maneira possível. |
| 3 | 252 | 0.630 | Eu vou falar um pouco aqui também sobre as perspectivas de aperfeiçoamento que temos pensado para a política de avaliação da educação superior. |
| 4 | 158 | 0.630 | Esta é uma grande oportunidade para o INEP discutir a avaliação da educação superior e o papel específico das universidades comunitárias nesse sistema que temos hoje. |
| 5 | 275 | 0.630 | Isso aconteceu justamente pelo crescimento quantitativo das instituições, dos cursos e da necessidade de haver indicadores educacionais para tomar decisão das políticas públicas, da gestão universitária, do estudante e por aí vai. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 87 | 0.684 | PRESIDENTE | Como o Ministério da Educação pode colocar na sua agenda de prioridades as instituições federais, os institutos e as universidades, e as universidades comunitárias nos ajudando a fazer um novo marco legal? |
| 2 | 366 | 0.669 | LAERTE GUIMARÃES FERREIRA JUNIOR | Eu entendo que esta audiência pública é para discutirmos o cenário das instituições comunitárias de educação superior, os desafios, as perspectivas e o futuro. |
| 3 | 168 | 0.668 | ULYSSES TAVARES TEIXEIRA | Poderíamos, por exemplo, dentro do cenário da educação superior como um todo, discutir sobre o papel das universidades comunitárias, contextualizado num plano nacional da educação superior.Mas esse documento não existe. |
| 4 | 396 | 0.658 | LAERTE GUIMARÃES FERREIRA JUNIOR | Então, as comunitárias fazem parte da preocupação da CAPES, em termos de fomento, e da nossa preocupação, porque nós sabemos da qualidade do ensino ofertado. |
| 5 | 683 | 0.656 | GELSON LEONARDO RECH | Nós precisaríamos de sinalizações para 2024: a(ininteligível), a regulação, os sinais com as características peculiares para as universidades comunitárias, para os grupos, para o EAD. |

**Contexto da melhor frase do orador** (frase 168)

- antes [ULYSSES TAVARES TEIXEIRA]: Quando falamos de avaliação, estamos falando de um sistema que está muito bem consolidado.
- **frase [ULYSSES TAVARES TEIXEIRA]: Poderíamos, por exemplo, dentro do cenário da educação superior como um todo, discutir sobre o papel das universidades comunitárias, contextualizado num plano nacional da educação superior.Mas esse documento não existe.**
- depois [ULYSSES TAVARES TEIXEIRA]: Existe o PNE, com pouquíssimas metas relacionadas à educação superior.

**Contexto da melhor frase global** (frase 87)

- antes [PRESIDENTE]: A Dra. Denise esteve presente no lançamento da Frente, prestigiou o evento.
- **frase [PRESIDENTE]: Como o Ministério da Educação pode colocar na sua agenda de prioridades as instituições federais, os institutos e as universidades, e as universidades comunitárias nos ajudando a fazer um novo marco legal?**
- depois [PRESIDENTE]: Hoje, o Ministério da Educação, em parte, não nos reconhece.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 34 — `data_157#10`

- **Audiência (data_157):** Especialistas sugerem desoneração tributária para baratear custo de remédios para doenças raras
- **Participante atribuído:** Renato Porto — Presidente da Associação da Indústria Farmacêutica de Pesquisa — INTERFARMA
- **Orador casado na transcrição:** RENATO ALENCAR PORTO (157 frases de 1040; 9 oradores na audiência)
- **cos_s** = 0.679 · **best_other** = 0.701 · **Δ** = best_other − cos_s = +0.022 · cos_g = 0.701

**Opinião (PT original):**

> A importância de autorregulamentação no setor de precificação de medicamentos.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 317 | 0.679 | O que nós temos que fazer é tomar cuidado para não criar instrumentos regulatórios que inviabilizem a chegada rápida desse medicamento à população brasileira. |
| 2 | 355 | 0.616 | Não adianta haver medicamento nas prateleiras, nas fábricas, os medicamentos precisam chegar às pessoas e chegar no momento certo, na dose certa e, claro, por um valor adequado. |
| 3 | 892 | 0.607 | Nenhuma indústria farmacêutica inova pensando no preço, ela inova pensando em mudar a terapia e, depois, avalia o preço desse produto. |
| 4 | 354 | 0.582 | Em outras palavras, o pilar central da associação é ter um sistema sustentável de acesso a medicamentos. |
| 5 | 336 | 0.560 | O que acontece com medicamentos da categoria Caso Omisso? |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 46 | 0.701 | DANIELA MARRECO CERQUEIRA | Nossas competências estão ligadas principalmente à regulação econômica do mercado de medicamentos. |
| 2 | 99 | 0.681 | DANIELA MARRECO CERQUEIRA | Existem alguns critérios que foram estabelecidos pela Câmara de Regulação do Mercado de Medicamentos, que é o acompanhamento do preço internacional desses produtos e o acompanhamento dos dados de segurança e eficácia, até que possamos estabelecer o preço definitivo dessas terapias. |
| 3 | 317 | 0.679 | RENATO ALENCAR PORTO | O que nós temos que fazer é tomar cuidado para não criar instrumentos regulatórios que inviabilizem a chegada rápida desse medicamento à população brasileira. |
| 4 | 65 | 0.666 | DANIELA MARRECO CERQUEIRA | Aqui são os critérios utilizados novamente para a precificação de medicamentos. |
| 5 | 48 | 0.664 | DANIELA MARRECO CERQUEIRA | Então, além de definir os critérios para o estabelecimento de preços, que são os preços-teto dos medicamentos que são definidos em território nacional, nós também monitoramos esse mercado para que esses preços sejam realmente praticados e as infrações às normas da CMED possam ser devidamente apuradas. |

**Contexto da melhor frase do orador** (frase 317)

- antes [RENATO ALENCAR PORTO]: Então, quando surge um produto inovador e a população pode ter à disposição a cura de uma doença, ele chega aqui, Deputada.
- **frase [RENATO ALENCAR PORTO]: O que nós temos que fazer é tomar cuidado para não criar instrumentos regulatórios que inviabilizem a chegada rápida desse medicamento à população brasileira.**
- depois [RENATO ALENCAR PORTO]: Essa é a primeira base técnica que nós precisamos ter: dar acesso.

**Contexto da melhor frase global** (frase 46)

- antes [DANIELA MARRECO CERQUEIRA]: A Secretaria Executiva é exercida pela ANVISA.
- **frase [DANIELA MARRECO CERQUEIRA]: Nossas competências estão ligadas principalmente à regulação econômica do mercado de medicamentos.**
- depois [DANIELA MARRECO CERQUEIRA]: A CMED tem a competência de definir as diretrizes em relação à precificação de medicamentos no Brasil e também de monitorar o mercado de medicamentos.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 35 — `data_166#18`

- **Audiência (data_166):** Especialistas defendem uso de tecnologia blockchain no serviço público
- **Participante atribuído:** Caio Sanas — Advogado e Professor Convidado de Blockchain da Fundação Getulio Vargas do Rio de Janeiro
- **Orador casado na transcrição:** CAIO SANAS (93 frases de 1200; 11 oradores na audiência)
- **cos_s** = 0.680 · **best_other** = 0.810 · **Δ** = best_other − cos_s = +0.130 · cos_g = 0.810

**Opinião (PT original):**

> Contratos inteligentes podem reduzir custos de transação e melhorar a eficiência na execução de contratos.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 568 | 0.680 | Propriedade nas relações de execução imediata: é mais fácil a sua implementação, ao contrário de contratos de execução diferida, em que nós precisamos de inúmeros comportamentos dos agentes econômicos para monitorar dentro de um contrato inteligente.Imaginem um carro elétrico financiado em umsmart contract. |
| 2 | 581 | 0.675 | Num futuro não tão distante, as relações vão ser preferencialmente realizadas e instrumentalizadas por meio dos contratos inteligentes. |
| 3 | 577 | 0.653 | A tecnologiablockchain, combinada com ossmarts contracts,pode potencializar a redução de custos de transação até nessa área. |
| 4 | 534 | 0.632 | Em 2015, vieram os contratos inteligentes, ossmart contracts, e aí vem a economia tokenizada. |
| 5 | 517 | 0.577 | Ela de fato pode servir de meio para inovar, trazer novos modelos de negócio, eficiência, transparência e redução de custos de transação tanto na iniciativa privada quanto no setor público. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 63 | 0.810 | DIEGO OLIVEIRA FARIAS | A automação inteligente de contratos reduz riscos de erros e otimiza serviços. |
| 2 | 44 | 0.748 | DIEGO OLIVEIRA FARIAS | Com isso, você consegue reduzir o custo de transação de forma eficiente. |
| 3 | 568 | 0.680 | CAIO SANAS | Propriedade nas relações de execução imediata: é mais fácil a sua implementação, ao contrário de contratos de execução diferida, em que nós precisamos de inúmeros comportamentos dos agentes econômicos para monitorar dentro de um contrato inteligente.Imaginem um carro elétrico financiado em umsmart contract. |
| 4 | 581 | 0.675 | CAIO SANAS | Num futuro não tão distante, as relações vão ser preferencialmente realizadas e instrumentalizadas por meio dos contratos inteligentes. |
| 5 | 691 | 0.660 | DIEGO OLIVEIRA FARIAS | A tecnologia também apresenta diversas características para reduzir a burocracia na administração pública, o que acaba reduzindo os custos de transação, em razão de ela funcionar como uma máquina de confiança, em que se eliminam intermediários e se reduzem os custos de transação do seu processo de negócio. |

**Contexto da melhor frase do orador** (frase 568)

- antes [CAIO SANAS]: Todavia, se ele não for cumprido, esse contrato permanece da forma como se encontra.
- **frase [CAIO SANAS]: Propriedade nas relações de execução imediata: é mais fácil a sua implementação, ao contrário de contratos de execução diferida, em que nós precisamos de inúmeros comportamentos dos agentes econômicos para monitorar dentro de um contrato inteligente.Imaginem um carro elétrico financiado em umsmart contract.**
- depois [CAIO SANAS]: Nós sabemos que no custo do financiamento há um custo jurídico envolvido.

**Contexto da melhor frase global** (frase 63)

- antes [DIEGO OLIVEIRA FARIAS]: Isso aprimora o processo de registro e a troca de informações entre diferentes esferas, indústrias e sociedade.
- **frase [DIEGO OLIVEIRA FARIAS]: A automação inteligente de contratos reduz riscos de erros e otimiza serviços.**
- depois [DIEGO OLIVEIRA FARIAS]: Então, por meio desmart contracts, você consegue criar regras que reflitam o funcionamento do mundo real, e isso faz com que você automatize processos governamentais, reduzindo a burocracia.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 36 — `data_169#7`

- **Audiência (data_169):** Com apoio parcial do governo, movimentos sociais querem Cerrado e Caatinga como patrimônios nacionais
- **Participante atribuído:** Silvio Isoppo Porto — Representante da Campanha em Defesa do Cerrado
- **Orador casado na transcrição:** SÍLVIO ISOPPO PORTO (53 frases de 899; 15 oradores na audiência)
- **cos_s** = 0.587 · **best_other** = 0.668 · **Δ** = best_other − cos_s = +0.082 · cos_g = 0.668

**Opinião (PT original):**

> As políticas públicas para os biomas Cerrado e Caatinga foram orientadas por uma visão externa e colonizada, ignorando soluções locais e tradicionais.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 535 | 0.587 | Se nós pegarmos as duas concepções que orientaram as políticas públicas para esses biomas, vamos voltar à ideia do que o Paulo Pedro disse em relação à questão de que a Caatinga é um espaço não de convivência, mas em que se tem que combater a seca. |
| 2 | 538 | 0.556 | As soluções para a Caatinga passam por soluções que são de fora do próprio bioma. |
| 3 | 549 | 0.474 | Agora, é evidente que nós não podemos ter um pensamento colonizado, em que as coisas de fora sempre são melhores do que as soluções próprias. |
| 4 | 546 | 0.447 | Nessa questão, hoje, a grande solução seria não mandar 1.500 pesquisadores para fora, mas mandar 1.500 pesquisadores para os roçados de que a Deputada falou, onde as pessoas compreendem o bioma, têm sabedoria tradicional e popular.Efetivamente, é daqui de dentro que nós vamos ter soluções para esses dois biomas, assim como para a Amazônia, assim como para o Pantanal, assim como para o Pampa. |
| 5 | 536 | 0.432 | Essa ideia de combate à seca foi que fez com que os perímetros irrigados fossem desenvolvidos nessa região, a transposição do Rio São Francisco e tudo isso. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 360 | 0.668 | ALEXANDRE HENRIQUE BEZERRA PIRES | E foi construído nas nossas mentes que a Caatinga e o Cerrado seriam biomas impróprios, biomas onde não se reconhece o papel dos povos e das comunidades que vivem neles. |
| 2 | 255 | 0.616 | SAMANTHA RO'OTSITSINA JURUNA | Nesse processo, muito se fala também de problemas ambientais que são gerados no âmbito do Cerrado por não existirem políticas públicas eficazes. |
| 3 | 535 | 0.587 | SÍLVIO ISOPPO PORTO | Se nós pegarmos as duas concepções que orientaram as políticas públicas para esses biomas, vamos voltar à ideia do que o Paulo Pedro disse em relação à questão de que a Caatinga é um espaço não de convivência, mas em que se tem que combater a seca. |
| 4 | 538 | 0.556 | SÍLVIO ISOPPO PORTO | As soluções para a Caatinga passam por soluções que são de fora do próprio bioma. |
| 5 | 96 | 0.555 | LOURDES CARDOZO LAUREANO | O Brasil, que propôs metas ousadas para o enfrentamento à emergência climática, vive essa contradição de proteger apenas parte do seu patrimônio natural, não tendo o Cerrado e a Caatinga como biomas considerados patrimônio nacional. |

**Contexto da melhor frase do orador** (frase 535)

- antes [SÍLVIO ISOPPO PORTO]: Para mim, há aqui dois elementos muito relevantes, que colocaram em xeque, de certa forma, a conservação do Cerrado e da Caatinga.
- **frase [SÍLVIO ISOPPO PORTO]: Se nós pegarmos as duas concepções que orientaram as políticas públicas para esses biomas, vamos voltar à ideia do que o Paulo Pedro disse em relação à questão de que a Caatinga é um espaço não de convivência, mas em que se tem que combater a seca.**
- depois [SÍLVIO ISOPPO PORTO]: Essa ideia de combate à seca foi que fez com que os perímetros irrigados fossem desenvolvidos nessa região, a transposição do Rio São Francisco e tudo isso.

**Contexto da melhor frase global** (frase 360)

- antes [ALEXANDRE HENRIQUE BEZERRA PIRES]: Nós nos perguntamos: Certamente por esse ser um lugar de vida.
- **frase [ALEXANDRE HENRIQUE BEZERRA PIRES]: E foi construído nas nossas mentes que a Caatinga e o Cerrado seriam biomas impróprios, biomas onde não se reconhece o papel dos povos e das comunidades que vivem neles.**
- depois [ALEXANDRE HENRIQUE BEZERRA PIRES]: Então, reconhecer a importância e a aprovação dessa proposta de emenda constitucional — PEC é, sobretudo, reconhecer a importância dos povos que neles vivem, a importância da água, do solo, das florestas, da nossa mata branca, como nós chamamos a Caatinga, da biodiversidade para a sustentação e sobrevivência deste planeta.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 37 — `data_173#10`

- **Audiência (data_173):** País deve retomar projetos de hidrelétricas com reservatórios, apontam especialistas
- **Participante atribuído:** Cristiana Nepomuceno de Sousa Soares — Advogada especialista em Direito de Energia
- **Orador casado na transcrição:** CRISTIANA NEPOMUCENO DE SOUSA SOARES (45 frases de 682; 8 oradores na audiência)
- **cos_s** = 0.843 · **best_other** = 0.818 · **Δ** = best_other − cos_s = -0.025 · cos_g = 0.843

**Opinião (PT original):**

> Ressalta os benefícios sociais e econômicos das hidrelétricas, como o acesso à eletricidade em áreas rurais e o apoio aos Objetivos de Desenvolvimento Sustentável da ONU.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 119 | 0.843 | As hidrelétricas contribuem com os Objetivos de Desenvolvimento Sustentável da ONU, com aqueles que dizem respeito à energia para todos, água potável, a saneamento, ao trabalho decente e crescimento econômico, à indústria e à ação contra a mudança do clima. |
| 2 | 116 | 0.762 | Ela traz benefício para as comunidades em volta contribuindo para o melhor acesso à eletricidade nas áreas rurais e servindo como recurso de matéria limpa. |
| 3 | 120 | 0.743 | As hidrelétricas como padrão de sustentabilidade. |
| 4 | 101 | 0.676 | Sobre as hidrelétricas, é aproveitado o potencial hidrelétrico de um rio. |
| 5 | 123 | 0.673 | Temos também o padrão de sustentabilidade das hidrelétricas para qualidade de água; biodiversidade do local, que pode ser estudada; alocação dos povos indígenas; patrimônio cultural; governança; comunicações; mitigação das mudanças climáticas e resiliência; entre outros. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 119 | 0.843 | CRISTIANA NEPOMUCENO DE SOUSA SOARES | As hidrelétricas contribuem com os Objetivos de Desenvolvimento Sustentável da ONU, com aqueles que dizem respeito à energia para todos, água potável, a saneamento, ao trabalho decente e crescimento econômico, à indústria e à ação contra a mudança do clima. |
| 2 | 620 | 0.818 | LUDIMILA LIMA DA SILVA | A usina hidrelétrica é um importante vetor de desenvolvimento social e econômico. |
| 3 | 116 | 0.762 | CRISTIANA NEPOMUCENO DE SOUSA SOARES | Ela traz benefício para as comunidades em volta contribuindo para o melhor acesso à eletricidade nas áreas rurais e servindo como recurso de matéria limpa. |
| 4 | 260 | 0.752 | PRESIDENTE | Cabe salientar, mais uma vez, que as hidrelétricas são, sim, parceiras do desenvolvimento verdadeiro e sustentável, já que os reservatórios permitem o armazenamento de energia, o abastecimento de água, a(ininteligível),a irrigação, além de incentivar atividades relacionadas à aquicultura, à piscicultura, ao turismo, ao esporte e ao lazer. |
| 5 | 330 | 0.748 | CHARLES LENZI | A hidroeletricidade tem um valor imenso não só para a geração de energia, mas também para os serviços ancilares. |

**Contexto da melhor frase do orador** (frase 119)

- antes [CRISTIANA NEPOMUCENO DE SOUSA SOARES]: Reservatórios e barragens proveem outros benefícios para a sociedade, como regularização de vazões, irrigação, navegação e recreação também.
- **frase [CRISTIANA NEPOMUCENO DE SOUSA SOARES]: As hidrelétricas contribuem com os Objetivos de Desenvolvimento Sustentável da ONU, com aqueles que dizem respeito à energia para todos, água potável, a saneamento, ao trabalho decente e crescimento econômico, à indústria e à ação contra a mudança do clima.**
- depois [CRISTIANA NEPOMUCENO DE SOUSA SOARES]: As hidrelétricas como padrão de sustentabilidade.

**Contexto da melhor frase global** (frase 119)

- antes [CRISTIANA NEPOMUCENO DE SOUSA SOARES]: Reservatórios e barragens proveem outros benefícios para a sociedade, como regularização de vazões, irrigação, navegação e recreação também.
- **frase [CRISTIANA NEPOMUCENO DE SOUSA SOARES]: As hidrelétricas contribuem com os Objetivos de Desenvolvimento Sustentável da ONU, com aqueles que dizem respeito à energia para todos, água potável, a saneamento, ao trabalho decente e crescimento econômico, à indústria e à ação contra a mudança do clima.**
- depois [CRISTIANA NEPOMUCENO DE SOUSA SOARES]: As hidrelétricas como padrão de sustentabilidade.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 38 — `data_183#9`

- **Audiência (data_183):** Marina Silva: veto do Ibama à licença para Petrobras perfurar na Foz do Amazonas é técnico
- **Participante atribuído:** Ricardo Salles — Deputado
- **Orador casado na transcrição:** RICARDO SALLES (58 frases de 1634; 28 oradores na audiência)
- **cos_s** = 0.794 · **best_other** = 0.632 · **Δ** = best_other − cos_s = -0.161 · cos_g = 0.794

**Opinião (PT original):**

> A falta de licenciamento do Linhão Boa Vista-Manaus está causando mais danos ambientais devido ao uso de termelétricas a diesel.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 179 | 0.794 | Mas o fato é que o não avanço do linhão Boa Vista-Manaus tem causado uma consequência ambiental muito mais perniciosa do que a que o avanço do licenciamento traria. |
| 2 | 184 | 0.624 | É público e notório que o modal rodoviário, sob todos os aspectos, é muito mais lesivo ao meio ambiente, devido a emissões de gás carbônico, riscos, inclusive pessoais, etc., do que o modal ferroviário. |
| 3 | 182 | 0.619 | É claro que há interesses comerciais dos que vendem odiesel, nós sabemos bem disso, mas a não consecução desse licenciamento traz, sob o ponto de vista ambiental, consequências fartamente mais nocivas ao meio ambiente do que as que teríamos se tivéssemos avançado quanto a esse tema do licenciamento. |
| 4 | 185 | 0.549 | No entanto, muitas das ponderações acerca das dificuldades para o avanço do Ferrogrão acabam militando em desfavor da questão ambiental, e não o contrário. |
| 5 | 205 | 0.545 | Porque problemas de licenciamento, problemas de orçamento e problemas de execução de obra impedem que o Rio Bauru, ao final, tenha o tratamento, e a cidade de Bauru acaba sendo uma contribuinte de esgoto não tratado para toda aquela bacia naquela região. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 179 | 0.794 | RICARDO SALLES | Mas o fato é que o não avanço do linhão Boa Vista-Manaus tem causado uma consequência ambiental muito mais perniciosa do que a que o avanço do licenciamento traria. |
| 2 | 1288 | 0.632 | CORONEL CHRISÓSTOMO | Quanto à Hidrelétrica de Tabajara, o problema lá é ambiental. |
| 3 | 184 | 0.624 | RICARDO SALLES | É público e notório que o modal rodoviário, sob todos os aspectos, é muito mais lesivo ao meio ambiente, devido a emissões de gás carbônico, riscos, inclusive pessoais, etc., do que o modal ferroviário. |
| 4 | 182 | 0.619 | RICARDO SALLES | É claro que há interesses comerciais dos que vendem odiesel, nós sabemos bem disso, mas a não consecução desse licenciamento traz, sob o ponto de vista ambiental, consequências fartamente mais nocivas ao meio ambiente do que as que teríamos se tivéssemos avançado quanto a esse tema do licenciamento. |
| 5 | 1290 | 0.592 | CORONEL CHRISÓSTOMO | O problema lá é ambiental. |

**Contexto da melhor frase do orador** (frase 179)

- antes [RICARDO SALLES]: Isso tem a ver, obviamente, com a questão indígena, com a tradução das manifestações para diversos dialetos, enfim.
- **frase [RICARDO SALLES]: Mas o fato é que o não avanço do linhão Boa Vista-Manaus tem causado uma consequência ambiental muito mais perniciosa do que a que o avanço do licenciamento traria.**
- depois [RICARDO SALLES]: Devido à ausência de fornecimento de energia elétrica para Roraima — porque a Venezuela não tem feito manutenção no seu sistema, cai toda hora o fornecimento que vem da Venezuela; e Roraima, como a senhora sabe, está fora do sistema nacional de energia —, o que temos que fazer?

**Contexto da melhor frase global** (frase 179)

- antes [RICARDO SALLES]: Isso tem a ver, obviamente, com a questão indígena, com a tradução das manifestações para diversos dialetos, enfim.
- **frase [RICARDO SALLES]: Mas o fato é que o não avanço do linhão Boa Vista-Manaus tem causado uma consequência ambiental muito mais perniciosa do que a que o avanço do licenciamento traria.**
- depois [RICARDO SALLES]: Devido à ausência de fornecimento de energia elétrica para Roraima — porque a Venezuela não tem feito manutenção no seu sistema, cai toda hora o fornecimento que vem da Venezuela; e Roraima, como a senhora sabe, está fora do sistema nacional de energia —, o que temos que fazer?

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 39 — `data_183#10`

- **Audiência (data_183):** Marina Silva: veto do Ibama à licença para Petrobras perfurar na Foz do Amazonas é técnico
- **Participante atribuído:** Ricardo Salles — Deputado
- **Orador casado na transcrição:** RICARDO SALLES (58 frases de 1634; 28 oradores na audiência)
- **cos_s** = 0.565 · **best_other** = 0.771 · **Δ** = best_other − cos_s = +0.206 · cos_g = 0.771

**Opinião (PT original):**

> Preocupações com a exploração de petróleo na foz do Rio Amazonas precisam ser balanceadas com a realidade de que países vizinhos estão explorando na mesma região.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 168 | 0.565 | Com relação à foz do Amazonas, pelo que eu li na imprensa, e não tenho nenhuma informação mais técnica sobre isso, parece-me que a posição adotada pelo Ministério é adequada. |
| 2 | 177 | 0.549 | No caso, por exemplo, do linhão Boa Vista-Manaus, que a senhora conhece bem, na Região Amazônica — salvo engano da minha parte quanto à data —, nós estamos há cerca de 10 anos aguardando o avanço da liberalização, digamos assim, das medidas. |
| 3 | 217 | 0.530 | Portanto, a minha ponderação diz muito mais respeito ao cuidado em estabelecer quais são as áreas, do ponto de vista de conhecimento técnico, em que há efetivamente defasagem de pessoal em ambos os órgãos e fazer o concurso voltado para suprir essas vagas.Aquela dicotomia entre analista ambiental e técnico ambiental é muito importante de ser olhar, porque às vezes um não pode suprir o trabalho do outro; um não pode ir a campo no lugar do outro. |
| 4 | 185 | 0.530 | No entanto, muitas das ponderações acerca das dificuldades para o avanço do Ferrogrão acabam militando em desfavor da questão ambiental, e não o contrário. |
| 5 | 216 | 0.510 | Isso sobrecarrega muito aqueles que têm o efetivo conhecimento e que passam a ser, talvez, os únicos que têm capacidade técnica de analisar essas questões a fundo, a exemplo de questões relacionadas a temas hídricos, a emissões de gases de efeito estufa, enfim, todos os temas complexos que são levados ao escrutínio de qualquer um dos dois órgãos ambientais. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 1277 | 0.771 | CORONEL CHRISÓSTOMO | Ministra, a senhora também sabe como é importante a prospecção de petróleo lá na foz do Amazonas. |
| 2 | 960 | 0.764 | ODAIR CUNHA | É claro que a exploração do petróleo na margem equatorial que nós estamos discutindo agora é importante, e nós precisamos dar este tratamento. |
| 3 | 1054 | 0.752 | MINISTRA MARINA SILVA | Eu acho que a maioria das questões aqui levantadas tem a ver, de modo geral, com a exploração de petróleo na Foz do Amazonas e tem a ver com o processo de licenciamento. |
| 4 | 1381 | 0.751 | ZÉ HAROLDO CATHEDRAL | Nós, que já estivemos juntos na bancada de Roraima, conversando sobre as demarcações que estão em pauta no nosso Estado, hoje estamos aqui reunidos para tratar desse embate em torno do petrolífero na foz do Amazonas, dos possíveis prejuízos ambientais e dos benefícios que essa possibilidade traz consigo para toda a região. |
| 5 | 244 | 0.743 | LAFAYETTE DE ANDRADA | Além disso, temos que considerar que ali do lado a Guiana já está explorando petróleo. |

**Contexto da melhor frase do orador** (frase 168)

- antes [RICARDO SALLES]: Eu queria dar alguns exemplos aqui de casos em que o licenciamento teve, ou terá — porque ainda não estão concluídos —, impacto imediato.
- **frase [RICARDO SALLES]: Com relação à foz do Amazonas, pelo que eu li na imprensa, e não tenho nenhuma informação mais técnica sobre isso, parece-me que a posição adotada pelo Ministério é adequada.**
- depois [RICARDO SALLES]: Trata-se de uma discussão técnica, não comporta arbitramento jurídico de argumentos.

**Contexto da melhor frase global** (frase 1277)

- antes [CORONEL CHRISÓSTOMO]: Ajude este Deputado da Amazônia, filho da floresta!
- **frase [CORONEL CHRISÓSTOMO]: Ministra, a senhora também sabe como é importante a prospecção de petróleo lá na foz do Amazonas.**
- depois [CORONEL CHRISÓSTOMO]: Daqui a pouco, Ministra, o petróleo vai valer tanto quanto o dinheiro da Venezuela: nada!

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 40 — `data_185#14`

- **Audiência (data_185):** Cobertura do teste do pezinho é muito desigual no estados brasileiros, aponta levantamento
- **Participante atribuído:** Bruna Dornelas — Gestora de Regionalização da Secretaria de Saúde de Pernambuco
- **Orador casado na transcrição:** BRUNA RAFAELA DORNELAS MONTEIRO (35 frases de 1009; 10 oradores na audiência)
- **cos_s** = 0.472 · **best_other** = 0.636 · **Δ** = best_other − cos_s = +0.164 · cos_g = 0.636

**Opinião (PT original):**

> A redução do tempo de liberação dos resultados é essencial para a eficácia do programa.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 288 | 0.472 | E há mais: redução do tempo de liberação dos resultados, que é um dos nossos grandes trunfos, e nos deixa muitos honrosos a redução desse tempo, que antes era de 10 dias e agora passa para, em média, 3 dias, 4 dias a liberação do resultado pelo LACEN; descentralização dos pontos de coleta para todas as unidades básicas de saúde, oportunizando o alcance dos recém-nascidos no período ideal — essa é a nossa meta e estamos caminhando para isso; qualificação dos profissionais envolvidos na triagem neonatal por meio de cursos em parceria com a Escola de Governo em Saúde Pública de Pernambuco; institucionalização de rotina de monitoramento contínuo entre serviço de referência, rede complementar, Coordenação Estadual da Triagem Neonatal, regionais de saúde e Municípios; disseminação da temática nas consultas de pré-natal, uma das nossas grandes metas, assim como nos veículos de comunicação do Estado — nós precisamos conscientizar e empoderar cada vez mais essas gestantes e essas mulheres; implantação de um sistema próprio de monitoramento dos indicadores; pactuação nos espaços de governança do SUS de estratégias de captação precoce do recém-nascido no período ideal; perspectiva, é claro, de expansão do diagnóstico de toxoplasmose congênita, conforme a Lei nº 14.154, de 2021. |
| 2 | 286 | 0.380 | E Pernambuco, mais uma vez, assume um destaque e um protagonismo dentro do cenário nacional, dessa vez no processo de reestruturação dos fluxos assistenciais da Triagem Neonatal Biológica, que desencadeou uma série de ações estratégicas voltadas para esse fortalecimento, dentre elas: constituição de Grupo de Trabalho de Triagem Neonatal Biológica, publicado e instituído através da Portaria nº 315, de 2023, de forma a institucionalizar a política e torná-la cada vez mais sustentável; elaboração do plano de ação estadual com medidas estratégicas para o fortalecimento da política; publicação de edital para disseminação da temática nas instituições de ensino superior e programas de residência, porque nós acreditamos que essa temática precisa, sim, participar do processo formativo dos nossos futuros profissionais de saúde; lançamento da campanha Passos que Importam, ocorrido no dia 6 de junho, Dia Nacional do Teste do Pezinho; realização do diagnóstico situacional regional e municipal; realização de visitas técnicas aos Municípios com os indicadores fragilizados, não no intuito de apontar, mas no intuito de dizer que nós somos apoio, que nós estamos juntos para modificar essa realidade; construção conjunta do plano de ação entre as Gerências Regionais de Saúde, a Secretaria Estadual de Saúde e as Secretarias Municipais de Saúde, com um cronograma de acompanhamento, porque só há ação efetiva quando nós fazemos isso de forma tripartite. |
| 3 | 287 | 0.364 | Estamos em processo de viabilização dos agendamentos das consultas de maneira descentralizada e regionalizada, via CMCE, com acompanhamento e monitoramento realizado pelos apoiadores regionais dentro dos territórios. |
| 4 | 289 | 0.308 | Inclusive, neste exato momento, a nossa equipe técnica se encontra lá na Secretaria Estadual de Saúde discutindo esse processo de expansão. |
| 5 | 282 | 0.287 | No nosso Estado de Pernambuco, atualmente, nós ofertamos a triagem, a confirmação diagnóstica e a linha de cuidado para seis doenças contempladas no Programa Nacional de Triagem Neonatal, instituído através da Portaria nº 822, de 6 de junho de 2001. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 673 | 0.636 | DANIELA MACHADO MENDES | Isso mostra a efetividade do processo de triagem e a possibilidade de realização dessa experiência. |
| 2 | 652 | 0.607 | DANIELA MACHADO MENDES | Isso é muito importante para que, neste tempo, não haja nenhuma falha, nenhum erro na execução do teste, e que se possa prolongar esse tempo médio de execução. |
| 3 | 137 | 0.604 | CARLOS GOUVÊA | A efetividade, especialmente com a expansão das doenças triadas, vai depender dessaperformance, desse fluxo todo de ações que estão englobadas no programa. |
| 4 | 696 | 0.595 | DANIELA MACHADO MENDES | É necessário também auxiliar no custeio do envio de amostras, como já foi falado, principalmente uma parceria com os Correios, visando à diminuição do tempo da chegada da amostra, reduzindo custos. |
| 5 | 639 | 0.543 | DANIELA MACHADO MENDES | Ela promove esse tratamento adequado em tempo oportuno, isto é, antes que algum sinal ou sintoma apareça, reduzindo e evitando deficiências, sequelas e até mesmo óbitos. |

**Contexto da melhor frase do orador** (frase 288)

- antes [BRUNA RAFAELA DORNELAS MONTEIRO]: Estamos em processo de viabilização dos agendamentos das consultas de maneira descentralizada e regionalizada, via CMCE, com acompanhamento e monitoramento realizado pelos apoiadores regionais dentro dos territórios.
- **frase [BRUNA RAFAELA DORNELAS MONTEIRO]: E há mais: redução do tempo de liberação dos resultados, que é um dos nossos grandes trunfos, e nos deixa muitos honrosos a redução desse tempo, que antes era de 10 dias e agora passa para, em média, 3 dias, 4 dias a liberação do resultado pelo LACEN; descentralização dos pontos de coleta para todas as unidades básicas de saúde, oportunizando o alcance dos recém-nascidos no período ideal — essa é a nossa meta e estamos caminhando para isso; qualificação dos profissionais envolvidos na triagem neonatal por meio de cursos em parceria com a Escola de Governo em Saúde Pública de Pernambuco; institucionalização de rotina de monitoramento contínuo entre serviço de referência, rede complementar, Coordenação Estadual da Triagem Neonatal, regionais de saúde e Municípios; disseminação da temática nas consultas de pré-natal, uma das nossas grandes metas, assim como nos veículos de comunicação do Estado — nós precisamos conscientizar e empoderar cada vez mais essas gestantes e essas mulheres; implantação de um sistema próprio de monitoramento dos indicadores; pactuação nos espaços de governança do SUS de estratégias de captação precoce do recém-nascido no período ideal; perspectiva, é claro, de expansão do diagnóstico de toxoplasmose congênita, conforme a Lei nº 14.154, de 2021.**
- depois [BRUNA RAFAELA DORNELAS MONTEIRO]: Inclusive, neste exato momento, a nossa equipe técnica se encontra lá na Secretaria Estadual de Saúde discutindo esse processo de expansão.

**Contexto da melhor frase global** (frase 673)

- antes [DANIELA MACHADO MENDES]: Já nesse período, se pegarmos o ano inteiro de 2022, nós triamos mais de 185 mil crianças e fizemos o diagnóstico de 859 crianças com resultado laboratorial confirmado.
- **frase [DANIELA MACHADO MENDES]: Isso mostra a efetividade do processo de triagem e a possibilidade de realização dessa experiência.**
- depois [DANIELA MACHADO MENDES]: Também estamos realizando o piloto com relação à AME aqui no Município, por meio de um projeto de pesquisa.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 41 — `data_185#15`

- **Audiência (data_185):** Cobertura do teste do pezinho é muito desigual no estados brasileiros, aponta levantamento
- **Participante atribuído:** Bruna Dornelas — Gestora de Regionalização da Secretaria de Saúde de Pernambuco
- **Orador casado na transcrição:** BRUNA RAFAELA DORNELAS MONTEIRO (35 frases de 1009; 10 oradores na audiência)
- **cos_s** = 0.559 · **best_other** = 0.900 · **Δ** = best_other − cos_s = +0.342 · cos_g = 0.900

**Opinião (PT original):**

> A educação continuada dos profissionais de saúde é vital para o sucesso da triagem neonatal.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 902 | 0.559 | Quero enfatizar a importância desta audiência pública no fortalecimento da triagem neonatal como política pública de saúde, e dizer que o Estado de Pernambuco está aqui para partilhar, para trocar experiências e para construir junto com vocês, traçando uma linha de cuidado para as nossas futuras gerações. |
| 2 | 288 | 0.554 | E há mais: redução do tempo de liberação dos resultados, que é um dos nossos grandes trunfos, e nos deixa muitos honrosos a redução desse tempo, que antes era de 10 dias e agora passa para, em média, 3 dias, 4 dias a liberação do resultado pelo LACEN; descentralização dos pontos de coleta para todas as unidades básicas de saúde, oportunizando o alcance dos recém-nascidos no período ideal — essa é a nossa meta e estamos caminhando para isso; qualificação dos profissionais envolvidos na triagem neonatal por meio de cursos em parceria com a Escola de Governo em Saúde Pública de Pernambuco; institucionalização de rotina de monitoramento contínuo entre serviço de referência, rede complementar, Coordenação Estadual da Triagem Neonatal, regionais de saúde e Municípios; disseminação da temática nas consultas de pré-natal, uma das nossas grandes metas, assim como nos veículos de comunicação do Estado — nós precisamos conscientizar e empoderar cada vez mais essas gestantes e essas mulheres; implantação de um sistema próprio de monitoramento dos indicadores; pactuação nos espaços de governança do SUS de estratégias de captação precoce do recém-nascido no período ideal; perspectiva, é claro, de expansão do diagnóstico de toxoplasmose congênita, conforme a Lei nº 14.154, de 2021. |
| 3 | 278 | 0.504 | Eu gostaria de partilhar com vocês a alegria de estarmos hoje presentes nesta audiência pública tão importante para o fortalecimento da triagem neonatal como política pública de saúde. |
| 4 | 300 | 0.498 | Essa é uma das nossas reuniões na Escola de Saúde Pública, com o objetivo de lançarmos e implementarmos o nosso curso de qualificação para os nossos profissionais de saúde dentro do nosso Estado. |
| 5 | 284 | 0.485 | Com relação à nossa Rede Gestora do Programa de Triagem Neonatal de Pernambuco, atualmente, nós temos na nossa composição a Coordenação Estadual do Programa de Triagem Neonatal, que faz parte da Gerência de Atenção à Saúde da Criança, que compõe a Diretoria de Políticas e Estratégias; a presença de apoiadores regionais e municipais da triagem neonatal nas 12 regiões de saúde do Estado, pois acreditamos no processo de regionalização dentro dos territórios; a Coordenação da Triagem Neonatal no nosso laboratório de referência, o nosso LACEN, e a logística regional e municipal de transporte dessas amostras. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 88 | 0.900 | CARLOS GOUVÊA | Há necessidade de promover um aprimoramento daqueles que trabalham com triagem neonatal, e os profissionais precisam, sim, ter uma educação continuada. |
| 2 | 863 | 0.754 | CARLOS GOUVÊA | Esta é a importância da triagem neonatal. |
| 3 | 948 | 0.718 | SUHELLEN OLIVEIRA DA SILVA | A triagem neonatal tem extrema importância na vida dessas pessoas. |
| 4 | 480 | 0.696 | SUHELLEN OLIVEIRA DA SILVA | Para nós, sempre é muito importante e uma honra falar sobre a triagem neonatal. |
| 5 | 39 | 0.672 | CARLOS GOUVÊA | Como faz muito bem o programa, o monitoramento é feito pela vida toda, através dos Serviços de Referência em Triagem Neonatal. |

**Contexto da melhor frase do orador** (frase 902)

- antes [BRUNA RAFAELA DORNELAS MONTEIRO]: A SRA. BRUNA RAFAELA DORNELAS MONTEIRO- Eu gostaria, mais uma vez, de agradecer à Deputada Federal Iza Arruda o convite.
- **frase [BRUNA RAFAELA DORNELAS MONTEIRO]: Quero enfatizar a importância desta audiência pública no fortalecimento da triagem neonatal como política pública de saúde, e dizer que o Estado de Pernambuco está aqui para partilhar, para trocar experiências e para construir junto com vocês, traçando uma linha de cuidado para as nossas futuras gerações.**
- depois [BRUNA RAFAELA DORNELAS MONTEIRO]: Obrigada, mais uma vez, pelo convite, e nos colocamos à disposição.

**Contexto da melhor frase global** (frase 88)

- antes [CARLOS GOUVÊA]: As doenças têm sido incorporadas, como é o caso da deficiência de biotiniodase, em 2011.
- **frase [CARLOS GOUVÊA]: Há necessidade de promover um aprimoramento daqueles que trabalham com triagem neonatal, e os profissionais precisam, sim, ter uma educação continuada.**
- depois [CARLOS GOUVÊA]: Este é um esforço que deve ser feito pelos gestores públicos e também por parte da sociedade civil.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 42 — `data_190#22`

- **Audiência (data_190):** Entidades criticam falta de apoio a pesquisas clínicas sobre doenças raras no Brasil
- **Participante atribuído:** Rômulo Bezerra Marques — Diretor da Federação Brasileira das Associações de Doenças Raras
- **Orador casado na transcrição:** RÔMULO BEZERRA MARQUES (88 frases de 971; 13 oradores na audiência)
- **cos_s** = 0.584 · **best_other** = 0.607 · **Δ** = best_other − cos_s = +0.023 · cos_g = 0.607

**Opinião (PT original):**

> Defendeu a flexibilização de marcos regulatórios e incentivos fiscais para facilitar a produção de novos medicamentos.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 476 | 0.584 | Temos também que motivar pesquisadores, estimular investidores e entes públicos e privados, desenvolver a pesquisa em território nacional, aportar recursos orçamentários, inserir estímulos fiscais e revisar os marcos regulatórios para a entrada e produção de novos medicamentos no País. |
| 2 | 485 | 0.555 | Os aspectos econômicos da pauta em debate são tão oportunos e atuais que a melhor comprovação disso é a regulamentação pelo Governo dos limiares de custo-efetividade e seus efeitos indesejáveis para nós sobre as incorporações de tecnologias para as doenças raras. |
| 3 | 807 | 0.545 | Incentivo às pesquisas clínicas. |
| 4 | 488 | 0.512 | Ainda nessa lavra da economia, é bom destacar o Projeto de Lei nº 3.262, de 2020, que cria o Fundo Nacional para Custeio e Fornecimento de Medicações e Terapias destinadas ao Tratamento de Doenças Raras ou Negligenciadas. |
| 5 | 463 | 0.490 | Acrescento que a terapia gênica bate às portas, oferecendo tratamento mais adequado e já mencionado aqui. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 80 | 0.607 | MARINA DOMENECH | Os avanços nas pesquisas fazem com que ampliemos um arsenal terapêutico e a condição de fornecer novas tecnologias, inovação e, claramente, reduzir o custo e impactar essa cadeia de maneira muito positiva. |
| 2 | 476 | 0.584 | RÔMULO BEZERRA MARQUES | Temos também que motivar pesquisadores, estimular investidores e entes públicos e privados, desenvolver a pesquisa em território nacional, aportar recursos orçamentários, inserir estímulos fiscais e revisar os marcos regulatórios para a entrada e produção de novos medicamentos no País. |
| 3 | 485 | 0.555 | RÔMULO BEZERRA MARQUES | Os aspectos econômicos da pauta em debate são tão oportunos e atuais que a melhor comprovação disso é a regulamentação pelo Governo dos limiares de custo-efetividade e seus efeitos indesejáveis para nós sobre as incorporações de tecnologias para as doenças raras. |
| 4 | 807 | 0.545 | RÔMULO BEZERRA MARQUES | Incentivo às pesquisas clínicas. |
| 5 | 578 | 0.543 | FABRICIO CARNEIRO DE OLIVEIRA | Quando essa relação é favorável, isso já permite a autorização de registro do produto, com a continuação de alguns ensaios adicionais posteriormente. |

**Contexto da melhor frase do orador** (frase 476)

- antes [RÔMULO BEZERRA MARQUES]: Diante de todo o exposto, eu deduzo que o primeiro desafio a vencermos, sob o ponto de vista econômico, é trazer as pesquisas clínicas para o Brasil, o que fortemente já foi mencionado aqui.
- **frase [RÔMULO BEZERRA MARQUES]: Temos também que motivar pesquisadores, estimular investidores e entes públicos e privados, desenvolver a pesquisa em território nacional, aportar recursos orçamentários, inserir estímulos fiscais e revisar os marcos regulatórios para a entrada e produção de novos medicamentos no País.**
- depois [RÔMULO BEZERRA MARQUES]: Flexibilizar o número de pacientes também é algo relevante, como no exemplo dado aqui pela Lauda:"Dez pacientes são dez vidas".

**Contexto da melhor frase global** (frase 80)

- antes [MARINA DOMENECH]: A pesquisa tem esse poder, além de propiciar redução de gastos públicos muito grande, porque tira do vetor de saúde pública o contexto do oferecimento de tratamento.
- **frase [MARINA DOMENECH]: Os avanços nas pesquisas fazem com que ampliemos um arsenal terapêutico e a condição de fornecer novas tecnologias, inovação e, claramente, reduzir o custo e impactar essa cadeia de maneira muito positiva.**
- depois [MARINA DOMENECH]: Pesquisa clínica e ciência são a esperança desses pacientes.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 43 — `data_191#14`

- **Audiência (data_191):** Ações de bem-estar animal podem trazer múltiplos benefícios para o Brasil, dizem especialistas
- **Participante atribuído:** Cristina Mendonça — Diretora-Executiva da Mercy for Animals no Brasil
- **Orador casado na transcrição:** CRISTINA MENDONÇA (167 frases de 712; 11 oradores na audiência)
- **cos_s** = 0.720 · **best_other** = 0.672 · **Δ** = best_other − cos_s = -0.048 · cos_g = 0.720

**Opinião (PT original):**

> Mencionou a importância de uma alimentação mais sustentável e diversificada.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 246 | 0.720 | O relatório da ONU aponta para se atuar em uma mudança de demanda, inclusive em dieta, para utilizar um produto mais variado, nutritivo, reduzindo as perdas alimentares. |
| 2 | 302 | 0.691 | Como transformamos o sistema alimentar para que todos em um planeta possam se alimentar de forma sustentável? |
| 3 | 227 | 0.618 | Quanto aos sistemas alimentares, não é uma mudança incremental, é necessária uma transformação. |
| 4 | 235 | 0.616 | Este é um relatório também da ONU sobre sistemas alimentares. |
| 5 | 308 | 0.614 | Seria possível criar um sistema alimentar calcado nesses princípios? |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 246 | 0.720 | CRISTINA MENDONÇA | O relatório da ONU aponta para se atuar em uma mudança de demanda, inclusive em dieta, para utilizar um produto mais variado, nutritivo, reduzindo as perdas alimentares. |
| 2 | 302 | 0.691 | CRISTINA MENDONÇA | Como transformamos o sistema alimentar para que todos em um planeta possam se alimentar de forma sustentável? |
| 3 | 359 | 0.672 | KARINA ISHIDA | Para produzir todos esses alimentos — nem todos são saudáveis, há muitos embutidos — e para que toda essa produção seja possível, há uma mudança no uso da terra. |
| 4 | 330 | 0.671 | KARINA ISHIDA | Buscamos a implementação de práticas éticas e sustentáveis de produção de alimentos. |
| 5 | 521 | 0.639 | ALYSSON SOARES | É pensando nisto que o Programa Biomas surge, na busca de utilizar ingredientes cada vez mais sustentáveis, que melhorem os indicadores sociais, regionais e culturais das comunidades locais no seu entorno, e de transformar estas comunidades em fornecedores de ingredientes sustentáveis para fazer produtosplant-basedcada vez mais gostosos. |

**Contexto da melhor frase do orador** (frase 246)

- antes [CRISTINA MENDONÇA]: Isso é dado científico.
- **frase [CRISTINA MENDONÇA]: O relatório da ONU aponta para se atuar em uma mudança de demanda, inclusive em dieta, para utilizar um produto mais variado, nutritivo, reduzindo as perdas alimentares.**
- depois [CRISTINA MENDONÇA]: Isto aqui é um dado do IPCC.

**Contexto da melhor frase global** (frase 246)

- antes [CRISTINA MENDONÇA]: Isso é dado científico.
- **frase [CRISTINA MENDONÇA]: O relatório da ONU aponta para se atuar em uma mudança de demanda, inclusive em dieta, para utilizar um produto mais variado, nutritivo, reduzindo as perdas alimentares.**
- depois [CRISTINA MENDONÇA]: Isto aqui é um dado do IPCC.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 44 — `data_192#24`

- **Audiência (data_192):** Entidades de defesa do consumidor e representante da indústria divergem sobre redução da vida útil de celulares
- **Participante atribuído:** Igor Rodrigues Britto — Diretor de Relações Institucionais do IDEC
- **Orador casado na transcrição:** IGOR RODRIGUES BRITTO (121 frases de 694; 6 oradores na audiência)
- **cos_s** = 0.819 · **best_other** = 0.728 · **Δ** = best_other − cos_s = -0.091 · cos_g = 0.819

**Opinião (PT original):**

> É necessário garantir a durabilidade e a funcionalidade dos produtos e software por um tempo adequado, não apenas durante o período de garantia contratual.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 282 | 0.819 | Se nós aplicarmos, na realidade, que a parte mais funcional e relevante de um produto deste é osoftware, por equiparação nós devemos garantir, por lei, que os produtores ou fabricantes destes produtos garantam a durabilidade e a funcionalidade dosoftwarepor um tempo, não a cada ano, não a cada critério da lógica de evolução tecnológica. |
| 2 | 291 | 0.706 | Trata-se do critério da vida útil do produto. |
| 3 | 273 | 0.693 | Elas têm que funcionar e funcionar durante um tempo, ter uma durabilidade. |
| 4 | 324 | 0.608 | Existe um duplo nívelstandardde durabilidade e qualidade dos produtos. |
| 5 | 309 | 0.601 | As garantias contratuais da Apple e da Samsung estabelecem, basicamente para todos os produtos, dos mais baratos aos mais caros, que eles funcionam durante 1 ano. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 282 | 0.819 | IGOR RODRIGUES BRITTO | Se nós aplicarmos, na realidade, que a parte mais funcional e relevante de um produto deste é osoftware, por equiparação nós devemos garantir, por lei, que os produtores ou fabricantes destes produtos garantam a durabilidade e a funcionalidade dosoftwarepor um tempo, não a cada ano, não a cada critério da lógica de evolução tecnológica. |
| 2 | 107 | 0.728 | MARCELO DE SOUZA DO NASCIMENTO | Os Tribunais entenderam que a vida útil é a durabilidade esperada para aquele produto. |
| 3 | 439 | 0.722 | MARCELO DE SOUZA DO NASCIMENTO | Há a garantia contratual, que é essa que as empresas estabelecem para os seus produtos, de 6 meses, 1 ano ou pouco mais, mas também há a garantia legal, prevista pelo Código de Defesa do Consumidor, de 90 dias. |
| 4 | 291 | 0.706 | IGOR RODRIGUES BRITTO | Trata-se do critério da vida útil do produto. |
| 5 | 452 | 0.696 | PRESIDENTE | Mas, antes, já que falamos de garantias contratuais, vou fazer aqui uma pergunta que eu recepcionei e que vai também para o meu amigo Humberto Barbato, da ABINEE, sobre o tempo de vida útil dos aparelhos, que pode ser de 3 anos, 4 anos, 5 anos.Mas existe, às vezes, um contrassenso, que é a questão da validade do produto. |

**Contexto da melhor frase do orador** (frase 282)

- antes [IGOR RODRIGUES BRITTO]: Trata-se de uma determinação de 1990.
- **frase [IGOR RODRIGUES BRITTO]: Se nós aplicarmos, na realidade, que a parte mais funcional e relevante de um produto deste é osoftware, por equiparação nós devemos garantir, por lei, que os produtores ou fabricantes destes produtos garantam a durabilidade e a funcionalidade dosoftwarepor um tempo, não a cada ano, não a cada critério da lógica de evolução tecnológica.**
- depois [IGOR RODRIGUES BRITTO]: Como o Sr. Humberto bem falou, isso é algo que fica restrito ao conhecimento das fabricantes que aqui não se fazem presentes.

**Contexto da melhor frase global** (frase 282)

- antes [IGOR RODRIGUES BRITTO]: Trata-se de uma determinação de 1990.
- **frase [IGOR RODRIGUES BRITTO]: Se nós aplicarmos, na realidade, que a parte mais funcional e relevante de um produto deste é osoftware, por equiparação nós devemos garantir, por lei, que os produtores ou fabricantes destes produtos garantam a durabilidade e a funcionalidade dosoftwarepor um tempo, não a cada ano, não a cada critério da lógica de evolução tecnológica.**
- depois [IGOR RODRIGUES BRITTO]: Como o Sr. Humberto bem falou, isso é algo que fica restrito ao conhecimento das fabricantes que aqui não se fazem presentes.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 45 — `data_200#32`

- **Audiência (data_200):** Especialistas apoiam proposta que institui política de saúde funcional
- **Participante atribuído:** Djane da Silva Bento — Representante da Associação Nacional de Pessoas com Lúpus
- **Orador casado na transcrição:** DJANE DA SILVA BENTO (97 frases de 735; 10 oradores na audiência)
- **cos_s** = 0.499 · **best_other** = 0.537 · **Δ** = best_other − cos_s = +0.038 · cos_g = 0.537

**Opinião (PT original):**

> Enfatizou a importância de diagnósticos precoces e tratamentos contínuos.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 486 | 0.499 | A minha doença já vai estar muito avançada, como o doutor falou. |
| 2 | 499 | 0.494 | Aqui em Brasília foi criado um grupo de especialistas, que dão treinamento nas UBS, para que o lúpus e as doenças crônicas sejam diagnosticados com mais celeridade. |
| 3 | 462 | 0.427 | Infelizmente, o tratamento de lúpus é muito agressivo. |
| 4 | 481 | 0.419 | O diagnóstico do lúpus é tardio. |
| 5 | 708 | 0.414 | Reitero que as pautas que V.Exa. traz são importantíssimas. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 599 | 0.537 | PRESIDENTE | São muitos os elementos que vão apontar para o diagnóstico biopsicossocial como um avanço que tivemos, para a partir daí estabelecermos as condições que estão postas. |
| 2 | 27 | 0.521 | ARTHUR DE ALMEIDA MEDEIROS | Hoje a avaliação ainda é muito voltada para a questão biomédica, focada nos impedimentos, na CID — Classificação Internacional de Doenças. |
| 3 | 109 | 0.518 | GENILZA VALENTE | A partir de então, passou-se a pesquisar a CIF, entender que é necessário que ela seja utilizada em conjunto com a CID, visto que o diagnóstico precisa ser amplo, já que são classificações complementares, uma possa complementar a outra, e possamos ter um diagnóstico mais preciso, facilitando a abordagem de tratamentos mais específicos e direcionados. |
| 4 | 723 | 0.515 | PRESIDENTE | É fundamental que elas tenham também o diagnóstico biopsicossocial, como prevê a nossa própria legislação. |
| 5 | 169 | 0.513 | NADJA WALÉRIA VILELA CAMARA | Às vezes ele precisa de um olhar mais aprofundado, de uma reavaliação de todo o seu dia a dia, do desenvolvimento de um plano terapêutico singular para a especificidade que ele apresenta. |

**Contexto da melhor frase do orador** (frase 486)

- antes [DJANE DA SILVA BENTO]: Já era.
- **frase [DJANE DA SILVA BENTO]: A minha doença já vai estar muito avançada, como o doutor falou.**
- depois [DJANE DA SILVA BENTO]: O paciente já vai estar muito fragilizado, e vai ser impossível fazer o tratamento adequado, vai ser impossível reabilitá-lo.

**Contexto da melhor frase global** (frase 599)

- antes [PRESIDENTE]: Nenhum ser humano deve ter a sua maior atenção voltada a mitigar a própria dor ou a aprender a conviver com a dor, a tentar dizer, e essa dor ser ignorada pelos demais.
- **frase [PRESIDENTE]: São muitos os elementos que vão apontar para o diagnóstico biopsicossocial como um avanço que tivemos, para a partir daí estabelecermos as condições que estão postas.**
- depois [PRESIDENTE]: Não se restringe isso apenas a uma condição: se a pessoa tem um nível de funcionalidade ou não que vai ser impactada em outras formas, em outras relações da vida.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 46 — `data_201#21`

- **Audiência (data_201):** Familiares de presos em 8 de janeiro cobram individualização de condutas e negam tentativa de golpe
- **Participante atribuído:** Sargento Gonçalves — Deputado Federal (PL - RN)
- **Orador casado na transcrição:** SARGENTO GONÇALVES (42 frases de 4551; 49 oradores na audiência)
- **cos_s** = 0.464 · **best_other** = 0.849 · **Δ** = best_other − cos_s = +0.385 · cos_g = 0.849

**Opinião (PT original):**

> Relata a angústia e o sofrimento das famílias das pessoas presas.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 556 | 0.464 | É a de saber que existem homens e mulheres de bem pagando por um crime que não cometeram, passando por tão grande dificuldade. |
| 2 | 544 | 0.448 | Que dias difíceis nós temos vivido! |
| 3 | 551 | 0.415 | Quando eu vejo essas acusações, é como se fosse comigo, e digo:"Não consigo imaginar; não tem como ser aqueles homens e mulheres de bem, que não eram capazes de sujar a rua, de jogar um lixo numa via pública, cometerem atos tão graves". |
| 4 | 555 | 0.407 | E qual é a angústia, quando eu a busco no meu íntimo, no meu interior, na minha intimidade com Deus? |
| 5 | 547 | 0.387 | Eu combati, durante 18 anos, Dra. Gabriela, em uma guarnição de polícia e tantas vezes me senti desprestigiado ou desrespeitado ao ver criminosos, traficantes e homicidas saírem primeiro que eu de uma delegacia de polícia, tantas vezes estive em ocorrências que envolviam quadrilhas de dez, quinze bandidos que tinham feito a semana de arrastão nas praias do litoral norte do Rio Grande do Norte e, quando eu ia à delegacia e passava quase toda a noite lá, ao darem 5 horas da manhã, só tinha um menor lá apreendido e não era preso. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 2217 | 0.849 | MESSIAS DONATO | Eles sofrem junto com os familiares de quem se encontra preso. |
| 2 | 1170 | 0.765 | BIA KICIS | E vimos crianças que ficaram detidas, passando fome, passando sede e passando terror, como os filhos de pessoas que estão presas até hoje, com depressão, e tantas histórias terríveis. |
| 3 | 1406 | 0.762 | ADRIANA VENTURA | Eu queria dizer que é desesperador ver a cena do seu pai, de outros presos, da mãe com os filhos. |
| 4 | 3504 | 0.758 | SAMUEL FERNANDES CASTRO | É impossível não se comover com o que tem acontecido com todas as pessoas que estão presas. |
| 5 | 2069 | 0.726 | BRUNO JORDANO | Essas famílias aqui sofrem, e sofrem bastante. |

**Contexto da melhor frase do orador** (frase 556)

- antes [SARGENTO GONÇALVES]: E qual é a angústia, quando eu a busco no meu íntimo, no meu interior, na minha intimidade com Deus?
- **frase [SARGENTO GONÇALVES]: É a de saber que existem homens e mulheres de bem pagando por um crime que não cometeram, passando por tão grande dificuldade.**
- depois [SARGENTO GONÇALVES]: Nós tivemos a oportunidade de visitar um casal tornozelado, que estava usando tornozeleiras, o S.

**Contexto da melhor frase global** (frase 2217)

- antes [MESSIAS DONATO]: Quero saudar o Deputado Delegado Ramagem, que foi o autor do requerimento desta audiência pública que traz um alento, um conforto para as mães, para as esposas, para os maridos que aqui estão, para os advogados que acabamos de ouvir.
- **frase [MESSIAS DONATO]: Eles sofrem junto com os familiares de quem se encontra preso.**
- depois [MESSIAS DONATO]: Saúdo meu amigo e irmão, o Deputado Marcel van Hattem, por quem tenho um respeito muito grande.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 47 — `data_203#24`

- **Audiência (data_203):** Desmonte das políticas públicas levou a aumento da violência contra mulheres, afirmam debatedoras
- **Participante atribuído:** Lêda Borges — Deputada Federal (Bloco/PSDB - GO)
- **Orador casado na transcrição:** LÊDA BORGES (78 frases de 540; 8 oradores na audiência)
- **cos_s** = 0.672 · **best_other** = 0.770 · **Δ** = best_other − cos_s = +0.099 · cos_g = 0.770

**Opinião (PT original):**

> Ressaltou a importância da rede de proteção e da independência econômica para as mulheres.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 360 | 0.672 | Mas, na minha visão, se começamos a quebrar o ciclo da violência com a independência econômica dessa mulher, nós já estaremos contribuindo objetivamente. |
| 2 | 368 | 0.644 | Eu creio muito no MEI, na nossa legislação, que hoje não deu para passar, para as mulheres empreendedoras, para a capacitação e para uma renda que elas precisam ter. |
| 3 | 350 | 0.575 | Eu creio na rede de proteção. |
| 4 | 345 | 0.538 | Eu, como ex-Secretária de Estado da Mulher do Estado de Goiás, sei como essa rede de proteção precisa voltar a atuar e ser ampliada, e vou testemunhar como alguém que é do Judiciário. |
| 5 | 500 | 0.492 | A SRA. LÊDA BORGES(Bloco/PSDB - GO) - Deputada Ana, só quero dizer que a nossa Comissão de Defesa dos Direitos da Mulher destinou no Orçamento, para a Marcha das Margaridas, 1 milhão de reais, e nós ratificamos isso.(Palmas.) |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 333 | 0.770 | WILMA DOS REIS | É fundamental, principalmente, promovermos políticas de autonomia econômica para as mulheres, porque, quando a mulher tem o salário dela na conta ou tem como se sustentar, ela consegue romper esse ciclo e, a partir daí, ter uma vida melhor. |
| 2 | 280 | 0.744 | PRESIDENTE | A diferença que isso faz para proteger as mulheres do nosso País é fundamental. |
| 3 | 508 | 0.724 | DENISE MOTTA DAU | E as políticas de geração de emprego e renda para as mulheres, nesse contexto, têm sido fundamentais. |
| 4 | 360 | 0.672 | LÊDA BORGES | Mas, na minha visão, se começamos a quebrar o ciclo da violência com a independência econômica dessa mulher, nós já estaremos contribuindo objetivamente. |
| 5 | 334 | 0.670 | WILMA DOS REIS | Temos que promover políticas de fortalecimento da autonomia dos corpos e das vidas das mulheres. |

**Contexto da melhor frase do orador** (frase 360)

- antes [LÊDA BORGES]: Envolve sentimento, envolve dependência emocional e psicológica, que são os mais perigosos, porque são silenciosos.
- **frase [LÊDA BORGES]: Mas, na minha visão, se começamos a quebrar o ciclo da violência com a independência econômica dessa mulher, nós já estaremos contribuindo objetivamente.**
- depois [LÊDA BORGES]: Então, eu sou favorável, por exemplo, ao projeto.

**Contexto da melhor frase global** (frase 333)

- antes [WILMA DOS REIS]: Além disso, temos que fortalecer as legislações específicas, não só a Lei Maria da Penha, mas também a qualificação do feminicídio e várias outras leis que trazem direitos e a tentativa de coibir as várias formas de violência.
- **frase [WILMA DOS REIS]: É fundamental, principalmente, promovermos políticas de autonomia econômica para as mulheres, porque, quando a mulher tem o salário dela na conta ou tem como se sustentar, ela consegue romper esse ciclo e, a partir daí, ter uma vida melhor.**
- depois [WILMA DOS REIS]: Temos que promover políticas de fortalecimento da autonomia dos corpos e das vidas das mulheres.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 48 — `data_204#13`

- **Audiência (data_204):** Especialistas defendem melhorias no acesso ao diagnóstico e tratamento da distonia no SUS
- **Participante atribuído:** Maria Nilde Soares — Presidente do Instituto Distonia Saúde
- **Orador casado na transcrição:** MARIA NILDE SOARES (90 frases de 903; 8 oradores na audiência)
- **cos_s** = 0.745 · **best_other** = 0.748 · **Δ** = best_other − cos_s = +0.002 · cos_g = 0.748

**Opinião (PT original):**

> É importante divulgar e informar sobre a distonia para salvar vidas.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 862 | 0.745 | A informação salva vidas. |
| 2 | 863 | 0.638 | Precisamos divulgar, falar e repetir o que é distonia. |
| 3 | 654 | 0.605 | O mais importante é que se deve procurar se informar em fontes fidedignas, procurar médicos que tenham conhecimento da sua patologia. |
| 4 | 641 | 0.602 | Além disso, nós fazemos campanhas de conscientização, mobilização e até exposição de fotos no metrô, para que todas as pessoas tenham acesso à informação, uma vez que esta é uma das melhores opções para o diagnóstico precoce. |
| 5 | 642 | 0.582 | A informação deve ser compartilhada para chegar a quem dela, de fato, precisa. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 579 | 0.748 | ROSÂNGELA MORO | Acho que forças-tarefas como esta para divulgar a doença, divulgar o diagnóstico, ampliar a informação; audiências públicas; ter, sim, um dia — não sei se já existe — para a sensibilização da distonia são todos fatores que convergem para que a doença seja conhecida, o diagnóstico seja facilitado e, com isso, efetivamente, a vida do paciente melhore. |
| 2 | 862 | 0.745 | MARIA NILDE SOARES | A informação salva vidas. |
| 3 | 135 | 0.720 | SARA CASAGRANDE | É ampliar a informação sobre essa doença no País para leigos e para profissionais da saúde. |
| 4 | 128 | 0.647 | SARA CASAGRANDE | Poderíamos pensar em ações para ampliar o conhecimento — acho que se começa por aí — sobre essa doença para os profissionais da saúde. |
| 5 | 863 | 0.638 | MARIA NILDE SOARES | Precisamos divulgar, falar e repetir o que é distonia. |

**Contexto da melhor frase do orador** (frase 862)

- antes [MARIA NILDE SOARES]: E eu espero que você, sendo da equipe da Deputada Meire — assim como os demais —, consiga, assim como nós, voar, alçar voos, levando informação para todo o Brasil, porque este mundo é grande, este Brasil é grande, e nós precisamos de conhecimento, informação.
- **frase [MARIA NILDE SOARES]: A informação salva vidas.**
- depois [MARIA NILDE SOARES]: Precisamos divulgar, falar e repetir o que é distonia.

**Contexto da melhor frase global** (frase 579)

- antes [ROSÂNGELA MORO]: Para isso, reputo muito importante a capacitação da porta de entrada do SUS.
- **frase [ROSÂNGELA MORO]: Acho que forças-tarefas como esta para divulgar a doença, divulgar o diagnóstico, ampliar a informação; audiências públicas; ter, sim, um dia — não sei se já existe — para a sensibilização da distonia são todos fatores que convergem para que a doença seja conhecida, o diagnóstico seja facilitado e, com isso, efetivamente, a vida do paciente melhore.**
- depois [ROSÂNGELA MORO]: Com estas palavras, eu me despeço.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 49 — `data_204#16`

- **Audiência (data_204):** Especialistas defendem melhorias no acesso ao diagnóstico e tratamento da distonia no SUS
- **Participante atribuído:** Sara Casagrande — Neurologista
- **Orador casado na transcrição:** SARA CASAGRANDE (277 frases de 903; 8 oradores na audiência)
- **cos_s** = 0.586 · **best_other** = 0.747 · **Δ** = best_other − cos_s = +0.161 · cos_g = 0.747

**Opinião (PT original):**

> A atuação das associações é fundamental para o acolhimento e troca de experiências dos pacientes.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 112 | 0.586 | Estou diretamente envolvida, então, com pesquisas na área desses pacientes distônicos. |
| 2 | 109 | 0.566 | Para mim, é um grande prazer estar aqui, mais uma vez, representando os médicos, os neurologistas, os neurocirurgiões, os fisiatras, os neuropediatras e tantos profissionais envolvidos nessa causa, que é a causa dos pacientes com distonia. |
| 3 | 135 | 0.545 | É ampliar a informação sobre essa doença no País para leigos e para profissionais da saúde. |
| 4 | 231 | 0.528 | E ainda temos a reabilitação desses pacientes. |
| 5 | 869 | 0.524 | Agradeço, também, à Deputada Meire pelo espaço e por dar voz — não a nós — principalmente aos pacientes, que são realmente os protagonistas da história. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 555 | 0.747 | ROSÂNGELA MORO | Eu atribuo isso, doutora, à atuação das associações, que são muito importantes. |
| 2 | 639 | 0.713 | MARIA NILDE SOARES | Nós realizamos encontros anuais com pacientes para que se conheçam e possam ter amenizadas suas dores ao trocarem experiências. |
| 3 | 556 | 0.668 | ROSÂNGELA MORO | Nas associações, o acolhimento, a troca de experiências, o intercâmbio de informações importantes, sem atribuir todos os créditos à medicina e à ciência, eu acho que há uma combinação muito feliz. |
| 4 | 831 | 0.631 | AMIRA AWADA | Elas devem ser acompanhadas e tratadas para que esses pacientes tenham a qualidade de vida preservada e possam ser incluídos na sociedade de maneira integral. |
| 5 | 848 | 0.607 | PATRICIA DUMKE DA SILVA MÖLLER | E os nossos pacientes são a nossa força, quem traz o nosso conhecimento, quem traz ofeedback, quem nos dá energia. |

**Contexto da melhor frase do orador** (frase 112)

- antes [SARA CASAGRANDE]: Faço parte da equipe do Grupo de Transtornos de Movimento há 10 anos.
- **frase [SARA CASAGRANDE]: Estou diretamente envolvida, então, com pesquisas na área desses pacientes distônicos.**
- depois [SARA CASAGRANDE]: Vou reiterar o que o Dr. Heitor também falou.

**Contexto da melhor frase global** (frase 555)

- antes [ROSÂNGELA MORO]: Quero dizer que a Dra. Sara foi muito feliz quando disse que, às vezes, as pessoas ficam buscando o Google para saber o diagnóstico.
- **frase [ROSÂNGELA MORO]: Eu atribuo isso, doutora, à atuação das associações, que são muito importantes.**
- depois [ROSÂNGELA MORO]: Nas associações, o acolhimento, a troca de experiências, o intercâmbio de informações importantes, sem atribuir todos os créditos à medicina e à ciência, eu acho que há uma combinação muito feliz.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---

## Item 50 — `data_206#20`

- **Audiência (data_206):** Revisão deve servir para melhorar a Lei de Cotas, diz especialista
- **Participante atribuído:** Márcia Lima — Secretária de Políticas de Ações Afirmativas, Combate e Superação do Racismo do Ministério da Igualdade Racial
- **Orador casado na transcrição:** MÁRCIA REGINA DE LIMA SILVA (44 frases de 962; 17 oradores na audiência)
- **cos_s** = 0.743 · **best_other** = 0.795 · **Δ** = best_other − cos_s = +0.052 · cos_g = 0.795

**Opinião (PT original):**

> É importante institucionalizar as políticas de ações afirmativas nas universidades para garantir a inclusão e a diversidade.

**Top-5 nos turnos do orador atribuído**

| # | frase | cos | texto |
|---|---|---|---|
| 1 | 411 | 0.743 | Eu acho importante separar a questão da permanência da necessária mudança institucional para que tenhamos políticas de ações afirmativas, como pró-reitorias e secretarias nas universidades. |
| 2 | 412 | 0.709 | A universidade precisa institucionalizar a política, já que algumas universidades adotam essa prática e outras não. |
| 3 | 405 | 0.697 | A Lei de Cotas diversificou a universidade não apenas racialmente, mas também socialmente, o que eu acho que é importante. |
| 4 | 399 | 0.667 | E estamos muito preocupados, também, em discutir no âmbito desse GTI não somente o tema das questões afirmativas, mas também a questão das comissões de heteroidentificação, além de pensar boas práticas, ouvir histórias e conhecer como tem se dado no Brasil a questão das ações afirmativas nas universidades. |
| 5 | 417 | 0.642 | Eu acho que, nesta gestão, temos um acúmulo muito importante de pesquisadores, militantes, pessoas que dedicaram a sua vida a entender as ações afirmativas e a desigualdade racial. |

**Top-5 globais**

| # | frase | cos | orador | texto |
|---|---|---|---|---|
| 1 | 527 | 0.795 | PRESIDENTE | Temos que pensar em mecanismos de fomento e fortalecimento das corregedorias, das ouvidorias em cada universidade que trabalham institucionalmente a diversidade das pessoas e conseguem, em âmbito local, atuar em parceria com o Ministério Público, para investigação de casos de violência, de racismo, de capacitismo, de falta de acessibilidade, de LGBTfobia ocorridos em espaços universitários, que originalmente são espaços elitizados e perpetuam desigualdades e preconceitos. |
| 2 | 810 | 0.790 | MARIA PÁSCOA SARMENTO | O que se tem, dentro das políticas de ações afirmativas, para o nosso ingresso e permanência nas instituições de ensino superior? |
| 3 | 720 | 0.761 | LICINIA MARIA CORREA | As políticas afirmativas para nós assumem uma centralidade na discussão sobre a democratização do acesso às instituições de ensino superior e a consequente redução das desigualdades raciais no Brasil. |
| 4 | 735 | 0.756 | LICINIA MARIA CORREA | Além disso, propomos a construção da década das ações afirmativas e das políticas de reparação, produzindo estudos sobre o impacto da lei de cotas no acesso, permanência e pós-permanência, notadamente a formação de quadros de pesquisadores, pesquisadoras, docentes nas universidades, negros e negras, indígenas e pessoas com deficiência nas universidades, que nós sabemos que estão sub-representados nas universidades. |
| 5 | 411 | 0.743 | MÁRCIA REGINA DE LIMA SILVA | Eu acho importante separar a questão da permanência da necessária mudança institucional para que tenhamos políticas de ações afirmativas, como pró-reitorias e secretarias nas universidades. |

**Contexto da melhor frase do orador** (frase 411)

- antes [MÁRCIA REGINA DE LIMA SILVA]: Também identificamos gargalos que eu acho que são importantes, como a questão da permanência, que já foi tratada aqui.
- **frase [MÁRCIA REGINA DE LIMA SILVA]: Eu acho importante separar a questão da permanência da necessária mudança institucional para que tenhamos políticas de ações afirmativas, como pró-reitorias e secretarias nas universidades.**
- depois [MÁRCIA REGINA DE LIMA SILVA]: A universidade precisa institucionalizar a política, já que algumas universidades adotam essa prática e outras não.

**Contexto da melhor frase global** (frase 527)

- antes [PRESIDENTE]: Temos o direito de acessar esses espaços.
- **frase [PRESIDENTE]: Temos que pensar em mecanismos de fomento e fortalecimento das corregedorias, das ouvidorias em cada universidade que trabalham institucionalmente a diversidade das pessoas e conseguem, em âmbito local, atuar em parceria com o Ministério Público, para investigação de casos de violência, de racismo, de capacitismo, de falta de acessibilidade, de LGBTfobia ocorridos em espaços universitários, que originalmente são espaços elitizados e perpetuam desigualdades e preconceitos.**
- depois [PRESIDENTE]: O ambiente universitário precisa de pessoas jovens, diversas, com histórias e vivências que componham as discussões e a produção de conhecimentos e teorias.

**Auditor** — categoria: ______ · orador real: ______ · notas: ______

---
