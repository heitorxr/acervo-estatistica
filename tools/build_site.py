"""Build static HTML and printable project sheets from one canonical catalog."""
from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1]
projects=json.loads((ROOT/'projetos.json').read_text(encoding='utf-8'))
assert len(projects)==6 and len({p['id'] for p in projects})==6
escape=html.escape
cards=[]
for i,p in enumerate(projects):
 category='Análise ambiental' if p['category']=='ambiental' else 'Visualização de dados'
 cards.append(f'''<article class="project{' featured' if i==0 else ''}" data-category="{p['category']}" id="card-{p['id']}">
<button type="button" class="preview" data-project="{p['id']}" aria-label="Ver estudo: {escape(p['title'])}"><img src="{p['image']}" alt="{escape(p['imageAlt'])}" {'loading="lazy"' if i else 'fetchpriority="high"'} width="1200" height="650"></button>
<div class="project-body"><p class="category">{category} · {escape(p['label'])}</p><h3>{escape(p['title'])}</h3><p class="summary">{escape(p['summary'])}</p><ul class="tags" aria-label="Métodos e ferramentas">{''.join('<li>'+escape(t)+'</li>' for t in p['tags'])}</ul><button class="read-study" type="button" data-project="{p['id']}">Ver estudo <span aria-hidden="true">↗</span></button><noscript><a href="trabalhos/ficha-{p['id']}.pdf">Ver ficha em PDF</a></noscript></div></article>''')
serialized=json.dumps(projects,ensure_ascii=False).replace('<','\\u003c')
template=(ROOT/'index.template.html').read_text(encoding='utf-8')
index=template.replace('__CARDS__','\n'.join(cards)).replace('__PROJECTS__',serialized)
assert '__CARDS__' not in index and '__PROJECTS__' not in index
(ROOT/'index.html').write_text(index,encoding='utf-8')
(ROOT/'.nojekyll').write_text('',encoding='utf-8')
BUILD=ROOT/'_build';BUILD.mkdir(exist_ok=True)
for p in projects:
 methods=''.join('<li>'+escape(m)+'</li>' for m in p['methods'])
 work=f'<a href="{escape(p["workUrl"] if p["workUrl"].startswith("https:") else "https://heitorxr.github.io/acervo-estatistica/"+p["workUrl"])}">{escape(p["workLabel"])}</a> · ' if p.get('workUrl') else ''
 page=f'''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>{escape(p['label'])} — Heitor Cardoso Fernandes</title><style>
@page{{size:A4;margin:16mm 18mm}}*{{box-sizing:border-box}}body{{font:12pt/1.35 Arial,sans-serif;color:#293c35;margin:0}}.byline{{font-size:10pt;color:#567065;border-bottom:1px solid #cad7cd;padding-bottom:8pt;margin-bottom:14pt}}h1{{font:24pt/1.12 Georgia,serif;color:#193b32;margin:0 0 12pt}}h2{{font-size:12pt;color:#193b32;margin:12pt 0 5pt}}p{{margin:0 0 8pt}}.question{{font-size:12pt}}img{{display:block;width:100%;height:170px;object-fit:contain;background:#faf9f5;margin:10pt 0 4pt}}.caption{{font-size:9pt;color:#567065}}ul{{padding-left:15pt;margin:0}}li{{margin-bottom:3pt}}.scope{{background:#f1f3ed;padding:8pt 10pt;margin-top:12pt;break-inside:avoid}}.scope h2{{margin-top:0}}.links{{font-size:10pt;margin-top:12pt}}a{{color:#286250}}.tags{{font-size:10pt;color:#567065;margin-bottom:8pt}}
</style><body><div class="byline">HEITOR CARDOSO FERNANDES · ACERVO DE PROJETOS</div><h1>{escape(p['title'])}</h1><p class="tags">{escape(' · '.join(p['tags']))}</p><p class="question">{escape(p['question'])}</p><img src="{(ROOT/p['image']).as_uri()}" alt="{escape(p['imageAlt'])}"><p class="caption">{escape(p['caption'])}</p><h2>Como o estudo foi conduzido</h2><ul>{methods}</ul><h2>Leitura dos resultados</h2><p>{escape(p['finding'])}</p><div class="scope"><h2>Escopo e interpretação</h2><p>{escape(p['limit'])}</p></div><p class="links">{work}<a href="{escape(p['sourceUrl'])}">Materiais de origem e documentação</a></p></body></html>'''
 (BUILD/('ficha-'+p['id']+'.html')).write_text(page,encoding='utf-8')
print('CATALOGO_GERADO',len(projects),'fichas HTML e index.html')
