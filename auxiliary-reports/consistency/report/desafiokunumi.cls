%==============================================================================
%  desafiokunumi.cls
%  Classe de documento para o artigo cientifico do
%  1o Desafio de Dados do Instituto Kunumi - 2026
%
%  NAO ALTERE este arquivo: ele concentra toda a formatacao (margens, fontes,
%  espacamentos, cabecalho/rodape) exigida pelo desafio. Escreva o seu artigo
%  em main.tex, preenchendo apenas os comandos de metadados e o conteudo.
%
%  Uso:
%    \documentclass{desafiokunumi}            % portugues (padrao)
%    \documentclass[english]{desafiokunumi}   % ingles
%==============================================================================
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{desafiokunumi}[2026/06/26 Template de artigo - Desafio de Dados Kunumi]

% ----- Opcoes da classe ------------------------------------------------------
% Idioma do babel: brazil (padrao) ou english via a opcao [english].
% Demais opcoes sao repassadas a classe article.
\newcommand{\kunumi@lang}{brazil}
\DeclareOption{english}{\renewcommand{\kunumi@lang}{english}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass[10pt,a4paper,twoside]{article}

% ----- Codificacao e idioma --------------------------------------------------
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\expandafter\RequirePackage\expandafter[\kunumi@lang]{babel}

% ----- Tipografia ------------------------------------------------------------
\RequirePackage{newtxtext,newtxmath}  % fonte serifada tipo Times (padrao de conferencia)
\RequirePackage{microtype}            % ajuste fino de espacamento

% ----- Geometria da pagina ---------------------------------------------------
% Coluna unica com largura ~14,6cm: medida confortavel para corpo em 10pt
% (aprox. 70-80 caracteres por linha, padrao de legibilidade academica).
\RequirePackage[a4paper,top=2.6cm,bottom=2.6cm,left=3.2cm,right=3.2cm,
            headheight=15pt,headsep=12pt,footskip=24pt]{geometry}
\RequirePackage{setspace}
\setstretch{1.03}

% ----- Prevencao de quebras de pagina indesejadas ----------------------------
% Penalidades maximas para linhas orfas (primeira de paragrafo no final da pagina)
% e viuvas (ultima de paragrafo sozinha no inicio da pagina).
\widowpenalty=10000
\clubpenalty=10000
\displaywidowpenalty=10000

% Espacamento ao redor de floats (figuras/tabelas): valores mais controlados
% para evitar buracos verticais excessivos na pagina.
\setlength{\textfloatsep}{14pt plus 2pt minus 4pt}
\setlength{\floatsep}{10pt plus 2pt minus 2pt}
\setlength{\intextsep}{10pt plus 2pt minus 2pt}


% ----- Recursos matematicos e graficos ---------------------------------------
\RequirePackage{amsmath,amssymb}
\RequirePackage{graphicx}
\graphicspath{{figures/}}
\RequirePackage{float}                % permite a posicao fixa [H] em tabelas/figuras
\RequirePackage{booktabs}             % tabelas elegantes (\toprule \midrule \bottomrule)
\RequirePackage{multirow}
\RequirePackage{caption}
\captionsetup{font=small,labelfont=bf,labelsep=period}
\RequirePackage{subcaption}
\RequirePackage{xcolor}

% ----- Codigo-fonte ----------------------------------------------------------
\RequirePackage{listings}
\definecolor{codebg}{RGB}{248,248,248}
\definecolor{codekw}{RGB}{20,40,110}
\definecolor{codecm}{RGB}{110,110,110}
\lstset{
  basicstyle=\ttfamily\footnotesize,
  backgroundcolor=\color{codebg},
  keywordstyle=\color{codekw}\bfseries,
  commentstyle=\color{codecm}\itshape,
  frame=single, framesep=5pt, rulecolor=\color{black!15},
  numbers=left, numberstyle=\tiny\color{codecm}, numbersep=8pt,
  breaklines=true, showstringspaces=false, captionpos=b,
  xleftmargin=14pt
}

% ----- Hiperlinks e citacoes -------------------------------------------------
\RequirePackage[hidelinks]{hyperref}
\RequirePackage{url}
\RequirePackage[numbers,sort&compress]{natbib}
\bibliographystyle{plainnat}

% ----- Cabecalho e rodape (sobrio) ------------------------------------------
\RequirePackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\footnotesize\itshape 1\textsuperscript{o} Desafio de Dados do Instituto Kunumi}
\fancyhead[R]{\raisebox{-1.5pt}{\includegraphics[height=0.34cm]{kunumi-icon.png}}}
% Rodape: numero de pagina alinhado a direita, precedido por uma fina faixa de identidade.
\fancyfoot[R]{\raisebox{0.3pt}{\includegraphics[width=1.3cm,height=0.1cm]{banner.png}}\hspace{7pt}\footnotesize\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0pt}

% ----- Espacamento dos titulos de secao --------------------------------------
\RequirePackage[explicit]{titlesec}
\titlespacing*{\section}{0pt}{12pt}{4pt}
\titlespacing*{\subsection}{0pt}{8pt}{3pt}

%==============================================================================
%  METADADOS DO ARTIGO
%  Defina estes comandos no preambulo do seu main.tex; \maketitle os utiliza
%  para montar o cabecalho do artigo.
%==============================================================================
\newcommand{\kunumi@title}{}
\renewcommand{\title}[1]{\renewcommand{\kunumi@title}{#1}}

\newcommand{\kunumi@subtitle}{}
\newif\ifkunumi@hassubtitle
\newcommand{\subtitle}[1]{\renewcommand{\kunumi@subtitle}{#1}\kunumi@hassubtitletrue}

\newcommand{\kunumi@authors}{}
\newcommand{\authors}[1]{\renewcommand{\kunumi@authors}{#1}}

\newcommand{\kunumi@affiliations}{}
\newcommand{\affiliations}[1]{\renewcommand{\kunumi@affiliations}{#1}}

\newcommand{\kunumi@keywords}{}
\newcommand{\keywords}[1]{\renewcommand{\kunumi@keywords}{#1}}

\newcommand{\kunumi@abstract}{}
\newcommand{\abstracttext}[1]{\renewcommand{\kunumi@abstract}{#1}}

% Logo do Colab do grupo (opcional). Se nao definido, um placeholder e exibido.
%\newcommand{\kunumi@colablogo}{}
%\newif\ifkunumi@haslogo
%{#1}\kunumi@haslogotrue
%\newcommand{\colablogo}[1]{\renewcommand{\kunumi@colablogo}{#1}\kunumi@haslogotrue}


%==============================================================================
%  CABECALHO DO ARTIGO (\maketitle)
%==============================================================================
\renewcommand{\maketitle}{%
  % ----- Faixa decorativa (identidade visual do desafio) -----
  \noindent\includegraphics[width=\textwidth,height=0.45cm]{banner.png}
  \vspace{12pt}

  \begin{center}
    % ----- Linha de logos: desafio (esquerda) + Colab do autor (direita) -----
    \makebox[\textwidth]{%
      \begin{minipage}[c]{0.48\textwidth}\raggedright
        \includegraphics[height=0.95cm]{kunumi-logo.png}
      \end{minipage}\hfill
      %\begin{minipage}[c]{0.48\textwidth}\raggedleft
        %\ifkunumi@haslogo
         % \includegraphics[height=0.95cm]{\kunumi@colablogo}%
        %\else
         % \fbox{\parbox[c][0.95cm][c]{4.4cm}{\centering\ttfamily\scriptsize logo do seu Colab\\(adapte a partir do kunuminst)}}%
        %\fi
      %\end{minipage}%
    }\\[12pt]
    {\footnotesize\itshape 1\textsuperscript{o} Desafio de Dados do Instituto Kunumi --- IA e a Esfera P\'ublica}\\[12pt]

    % ----- TITULO -----
    {\LARGE\bfseries \kunumi@title
     \ifkunumi@hassubtitle \\[2pt] \kunumi@subtitle\fi}\\[14pt]

    % ----- AUTORES -----
    {\large \kunumi@authors}\\[8pt]

    % ----- AFILIACOES (Colabs / Instituicoes) -----
    {\small \kunumi@affiliations}
  \end{center}

  \vspace{6pt}

  % ----- RESUMO -----
  \begin{abstract}
  \noindent
  \textbf{Resumo.} \kunumi@abstract

  \smallskip
  \noindent\textbf{Palavras-chave:} \kunumi@keywords
  \end{abstract}

  \vspace{4pt}
  \hrule
  \vspace{8pt}
}

\endinput
