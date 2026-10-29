# Acervo de projetos — Heitor Cardoso Fernandes

Acervo visual de cinco estudos de estatística aplicada e visualização de dados.

Site: https://heitorxr.github.io/acervo-estatistica/

## Experiência de leitura

- Cinco estudos reunidos em uma página, com filtros por área.
- Pergunta, métodos, leitura dos resultados e limitações em cada estudo.
- Gráficos ampliáveis, cinco fichas em PDF (as duas de sensores com contexto técnico ampliado), relatório meteorológico e apresentação histórica.
- Link direto para o painel Faces do voto.
- Os materiais de origem e os códigos continuam nos repositórios originais, sem alteração.
- O site funciona sem servidor de aplicação e não utiliza rastreadores nem formulário de coleta.

## Conteúdo

1. Estação ambiental ET.
2. Comparação e ajuste de sensores de umidade do solo, incluindo a etapa laboratorial do CS625.
3. Faces do voto.
4. Análise e visualização meteorológica do SIMEPAR.
5. Releitura de visualizações históricas.

`projetos.json` é o catálogo canônico. `fontes.json` fixa as revisões consultadas. `proveniencia.json` identifica os arquivos públicos usados nas prévias e documentos, com seus hashes.

## Privacidade e atribuição

Foram usados apenas materiais já públicos. Os gráficos ambientais do acervo são reconstruídos de tabelas agregadas; este repositório não distribui entradas confidenciais, pares individuais nem séries brutas de sensores. As limitações de ajuste, extrapolação, validação interna e interpretação constam nas fichas e nas páginas dos estudos.

O desenvolvimento do acervo teve apoio de IA na organização, redação, implementação e verificação. Os estudos e materiais de referência mantêm os créditos e as ressalvas documentados em seus repositórios. A apresentação histórica e o relatório meteorológico são preservados como documentos de origem; publicar este índice não cria uma nova licença para esses materiais.

## Atualizar

1. Edite `projetos.json` para atualizar as descrições.
2. Para atualizar as fontes, revise explicitamente as revisões em `fontes.json`.
3. Execute `python tools/build_assets.py` em um ambiente com Matplotlib; esse passo só acessa arquivos públicos fixados e recompõe as duas prévias ambientais.
4. Execute `python tools/build_site.py`.
5. Execute `python tools/verify_site.py` em um ambiente com Playwright e Chrome. Isso também recompõe as cinco fichas PDF e testa os filtros e os detalhes em desktop e celular.
6. Revise os resultados, faça commit e push. GitHub Pages publica a raiz da branch `main`.

A captura do painel eleitoral é uma prévia; o trabalho interativo permanece no endereço público original. Para trocá-la, capture o painel real e substitua `assets/faces-voto.png`.

## Verificação

A verificação atual cobre cinco trabalhos, três categorias de filtro (todos e duas áreas), abertura e fechamento dos detalhes, imagens, links das fichas, link direto por projeto e ausência de rolagem horizontal em desktop e celular. As fontes e dados das análises não foram modificados por esta publicação.
