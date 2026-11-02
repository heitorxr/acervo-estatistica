# Acervo de projetos — Heitor Cardoso Fernandes

Acervo visual de sete trabalhos: cinco estudos de análise de dados e duas iniciações científicas em Física e Matemática.

Site: https://heitorxr.github.io/acervo-estatistica/

## Experiência de leitura

- Sete trabalhos reunidos em uma página, com filtros de análise ambiental, visualização de dados e iniciação científica.
- Pergunta, métodos, leitura dos resultados e limitações em cada estudo.
- Prévias reais ampliáveis, sete fichas-resumo em PDF, documentos completos das duas ICs, relatório meteorológico e apresentação histórica.
- Link direto para o painel Faces do voto.
- Os materiais de origem e os códigos continuam nos repositórios originais, sem alteração.
- O site funciona sem servidor de aplicação e não utiliza rastreadores nem formulário de coleta.

## Conteúdo

1. Estação ambiental ET.
2. Comparação e ajuste de sensores de umidade do solo, incluindo a etapa laboratorial do CS625.
3. Faces do voto.
4. Análise e visualização meteorológica do SIMEPAR.
5. Releitura de visualizações históricas.
6. Rotações e simetria: IC em Matemática orientada por Carlos Eduardo Durán Fernández; apresentação de 30 de julho de 2024.
7. Modelos hierárquicos para turbulência em fluidos e sistemas complexos: IC em Física estatística na UFPR, orientada por Giovani L. Vasconcelos; relatório final de 2025. Bolsa CNPq confirmada pelo autor.

As duas ICs integram o mesmo acervo por solicitação do autor. A apresentação de Matemática é pesquisa, não uma aula. Suas 102 páginas incluem quadros intermediários de animações, não trabalhos independentes. O relatório de Física tem 26 páginas e inclui simulações e análise estatística de vento do ATTO. As medições ATTO não são apresentadas como coleta própria.

`projetos.json` é o catálogo canônico e determina os totais exibidos. `fontes.json` fixa as revisões consultadas. `proveniencia.json` identifica os arquivos públicos usados anteriormente. `proveniencia-ics.json` registra os documentos de IC autorizados, hashes e páginas das prévias, sem caminhos locais dos originais.

## Privacidade e atribuição

Os cinco estudos anteriores usam materiais já públicos. As cópias integrais das ICs foram autorizadas pelo autor, com orientação, figuras e bibliografia preservadas. Os gráficos ambientais são reconstruídos de tabelas agregadas; este repositório não distribui entradas confidenciais, pares individuais nem séries brutas dos sensores. As limitações dos estudos constam nas fichas e nos detalhes.

A preparação das ICs verifica possíveis identificadores pessoais, anexos, anotações e ações de abertura de arquivos externos. Os originais locais permanecem intactos. As prévias são renderizações reais; a de Física recorta as figuras 24 e 25 da página 24 do PDF. A publicação não executa novamente simulações ou ajustes, nem afirma revisão matemática integral. A ficha de Física distingue concordância visual de validação quantitativa e registra limitações de parâmetros, incertezas, normalização, simetria e tratamento das caudas.

O desenvolvimento do acervo teve apoio de IA na organização, redação, implementação e verificação. Os estudos e materiais de referência mantêm os créditos e as ressalvas documentados em seus repositórios. A apresentação histórica e o relatório meteorológico são preservados como documentos de origem; publicar este índice não cria uma nova licença para esses materiais.

## Atualizar

1. Edite `projetos.json` para atualizar as descrições.
2. Para atualizar as fontes, revise explicitamente as revisões em `fontes.json`.
3. Execute `python tools/build_assets.py` em um ambiente com Matplotlib; esse passo só acessa arquivos públicos fixados e recompõe as duas prévias ambientais.
4. Execute `python tools/build_site.py`.
5. Execute `python tools/verify_site.py` em um ambiente com Playwright e Chrome. Isso recompõe as fichas PDF e testa todo o catálogo em desktop e celular. Para preservar fichas não alteradas, gere somente as afetadas e execute `python tools/verify_site.py URL_LOCAL --skip-pdfs`.
6. Revise os resultados, faça commit e push. GitHub Pages publica a raiz da branch `main`.

A captura do painel eleitoral é uma prévia; o trabalho interativo permanece no endereço público original. Para trocá-la, capture o painel real e substitua `assets/faces-voto.png`.

Para preparar versões autorizadas das ICs com PyMuPDF, use `python tools/prepare_ic.py --slides CAMINHO_DOS_SLIDES --report CAMINHO_DO_RELATORIO --report-preview-page 24`. Os caminhos são argumentos locais e não entram no manifesto público. A preparação não modifica os originais.

## Verificação

A verificação percorre todos os trabalhos do catálogo, quatro filtros (todos e três áreas), abertura e fechamento dos detalhes, imagens, destinos dos documentos e fichas, link direto e ausência de rolagem horizontal em desktop e celular. Os cinco registros anteriores e seus documentos são preservados ao acrescentar as ICs. Após publicar, execute novamente o teste na URL pública e compare os arquivos com as cópias locais.
