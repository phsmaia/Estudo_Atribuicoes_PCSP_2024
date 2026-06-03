# Changelog

Todas as modificações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado no [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

## [Unreleased] - 2026-06-03

### Added
- **Auditoria de Segurança (SAST/SCA)**: Realizada verificação contra SQL Injection, XSS e vazamento de dependências.
- **Segurança de Dados Locais**: Criação de regras de exclusão no `.gitignore` impedindo versionamento indevido de logs, caches e bancos de dados locais.

### Changed
- **Migração de Banco de Dados**: Refatoração estrutural da aplicação (arquivos `logger.py`, `contact_manager.py` e novo `db.py`) de **SQLite para PostgreSQL**. A arquitetura agora utiliza `psycopg2-binary` e suporta conexões em nuvem para eliminar bloqueios de banco de dados (`database is locked`) sob alta concorrência de usuários no painel interativo.

## [Unreleased] - 2026-06-02

### Added
- **Módulo Explorador Dinâmico**: Nova seção em abas com cruzamentos interativos "Por Cargo" e "Por Atribuição", automatizando verificações do Jupyter Notebook original e provendo selos visuais de status (ex: Exclusiva de 1 cargo).
- **Botões de Ajuda Metodológica**: Adição do parâmetro `help` aos subtítulos gerando pop-ups integrados para explicar como interpretar e os cálculos de cada gráfico.
- **Animações Premium CSS**: Implementação de efeito *Fade & Focus* nas renderizações.
- **Logger LGPD (`logger.py`)**: Desenvolvimento de banco de dados SQLite furtivo no backend focado em métricas e visitações, protegendo a privacidade por meio de Hash unidirecional (SHA-256) aplicado sobre os IPs.
- **Mídia Social e Repositórios**: Inserção de Badges com formatação shields.io nativa apontando para Artigo, Github, Zenodo e LinkedIn na barra lateral.
- **Formulário de Contato Nativo**: Implementação de sistema direto de comunicação na barra lateral, com persistência segura em banco de dados SQLite (`contacts.db`).
- **Engine SMTP para E-mails**: Disparo assíncrono de notificações de contato para o autor alimentado pelo provedor de *secrets* do Streamlit (`secrets.toml`).

### Changed
- **Arquitetura Visual**: Layout do Streamlit transformado em Dashboard Vertical 100% (*wide*), sobrepondo componentes na totalidade do eixo Y.
- **Painel de Controle Central**: Deslocamento da seleção de cenários (Matrizes, Originais) e KPIs de redução dimensional diretamente para a `sidebar`.
- **UX em Matrizes**: Encurtamento do título "Investigador de Polícia (+ Agente de Telecomunicações policial + Agente Policial + Carcereiro Policial)" para "Investigador de Polícia (+ Apoio)" afim de viabilizar leitura ótica das colunas.
- **Ordenação Lógica**: O eixo Y das Matrizes (Atribuição e Adjacência) foi invertido (`autorange="reversed"`) garantindo o topo com o escopo de Delegado de Polícia.
- **UX Dendograma e Gower**: Adicionadas as marcações de Médias, além de caixas numéricas semi-transparentes em cada braço hierárquico informando o peso gravitacional da junção de carreiras.
- **Micro-interações CSS na Barra Lateral**: Achatamento completo de margens, *paddings* e uso intensivo de *Flexbox* e componentes flutuantes (`absolute`) para aniquilar as barras de rolagem nativas e manter os KPIs de Redução (Originais, Condensadas, Redução e Eficácia) em uma malha horizontal perfeita.

### Fixed
- **Erro de Memória de Matriz**: Corrigido `ValueError: underlying array is read-only` decorrente de manipulação matemática de vetores Numpy 2.0+ no Plotly;
- **Refatoração Gráfica**: Corrigido bug grave na ausência do `NetworkX` via injeção direta dos cálculos matemáticos de arestas (Edges) exclusivamente dentro da camada de processamento `data_processing.py`.
- **KeyError do Explorador Dinâmico**: Corrigida a indexação reversa onde a aplicação tentava rastrear siglas (A_01) em um DataFrame já re-composto pelas longas orações normativas originárias.
- **Bug do Iframe (Barras de rolagem artificiais)**: Removidos parâmetros restritivos `width=800` do Python e `transform: rotate` do CSS Global do aplicativo que induziam falha no motor de *Resize Observer* do próprio Streamlit.
- **Índice Nulo no Gower**: Corrigido bug de injeção da pseudo-carreira genérica onde colunas preenchidas com strings (ao invés de números) quebravam a nomeação do Pandas, fazendo a Matriz de Gower cuspir rótulos "0" na renderização visual do Plotly.

## [Unreleased] - 2026-06-01

### Added
- Inicialização do arquivo `CHANGELOG.md` para gerenciamento de continuidade e rastreamento das sessões do projeto, adotando a diretriz do "technical-change-skill".
- Início da Etapa 2: Planejamento arquitetural para conversão dos scripts analíticos em um painel interativo com Streamlit.

### Changed
- Adição de nota explicativa no `README.md` indicando a branch [`scientific-publication`](https://github.com/phsmaia/Estudo_Atribuicoes_PCSP_2024/tree/scientific-publication) (versão estática do artigo) e a branch `main` (atualizações contínuas), em linguagem acessível para leigos.
- Reestruturação completa do arquivo `README.md`:
  - Criação da seção de **Visão Geral** para introdução do projeto a leigos.
  - Separação clara da seção do **Artigo Científico e Scripts Analíticos**, incluindo orientações de execução local.
  - Adição da seção sobre a futura **Aplicação Web Interativa**, sinalizada para implementação posterior.
  - Movimentação e destaque para a **Citação do Zenodo** na área de Referências.
