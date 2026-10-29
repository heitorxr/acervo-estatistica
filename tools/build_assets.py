"""Generate portfolio previews from public, pinned aggregate results only."""
from pathlib import Path
import json,csv,io,urllib.request,urllib.parse,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'; DOCS=ROOT/'trabalhos'
ASSETS.mkdir(exist_ok=True);DOCS.mkdir(exist_ok=True)
PINS=json.loads((ROOT/'fontes.json').read_text(encoding='utf-8'))
provenance=[]
def download(repo,path,destination=None):
 url='https://raw.githubusercontent.com/heitorxr/'+repo+'/'+PINS[repo]+'/'+urllib.parse.quote(path,safe='/')
 with urllib.request.urlopen(url,timeout=60) as r:data=r.read()
 if destination: destination.write_bytes(data)
 provenance.append({'repo':repo,'revision':PINS[repo],'path':path,'url':url,'sha256':hashlib.sha256(data).hexdigest()})
 return data

def rows(repo,path,delimiter=','):
 text=download(repo,path).decode('utf-8-sig')
 return list(csv.DictReader(io.StringIO(text),delimiter=delimiter))
def value(row,key):return float(row[key].replace(',','.'))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.grid':False})
GREEN='#286250'; OCHRE='#c16a3f'; MUTED='#91a89c'
def finish(fig,name):
 fig.set_facecolor('#faf9f5');fig.tight_layout(pad=1.8);fig.savefig(ASSETS/(name+'.png'),dpi=160,facecolor=fig.get_facecolor());plt.close(fig)
repo='acervo-de-contribuicoes-Heitor-Fernandes-Simepar'
r=rows(repo,'01_estacao_et/resultados/calibracao_empirica/tabelas/metricas_calibracao_empirica.csv',';')
fig,axes=plt.subplots(1,2,figsize=(10,4.7))
for ax,var,title,unit in zip(axes,['temperatura_bulbo_seco','umidade_relativa'],['Temperatura','Umidade relativa'],['°C','pontos percentuais']):
 sel=[next(x for x in r if x['variavel']==var and x['metodo']==m) for m in ['bruto','ajuste_linear_global']]
 vals=[value(x,'rmse') for x in sel]
 ax.set_facecolor('#faf9f5');ax.barh(['Original','Ajuste na campanha'],vals,color=[MUTED,GREEN],height=.5);ax.invert_yaxis();ax.set_xlim(0,max(vals)*1.28);ax.set_title(title,loc='left',fontweight='bold',pad=18);ax.set_xlabel('RMSE · '+unit);ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
 for i,v in enumerate(vals):ax.text(v+max(vals)*.035,i,f'{v:.3f}'.replace('.',','),va='center',fontsize=12)
finish(fig,'estacao-et')

r=rows(repo,'02_umidade_solo/contribuicoes/validacao_pc01_pc03_cs_20261002_a_20261007/resultados/tabelas/validacao_temporal_70_30.csv')
fig,ax=plt.subplots(figsize=(10,4.7));ax.set_facecolor('#faf9f5')
for i,(model,label,color) in enumerate([('linear_treino70','Linear',GREEN),('quadratico_treino70','Quadrático',OCHRE)]):
 vals=[value(next(x for x in r if x['sensor']==sensor and x['modelo']==model),'rmse_pp') for sensor in ['plugfild','PC03/azul']]
 pos=[j+(i-.5)*.32 for j in range(2)];ax.bar(pos,vals,width=.29,label=label,color=color)
 for x,v in zip(pos,vals):ax.text(x,v+.035,f'{v:.2f}'.replace('.',','),ha='center',fontsize=12)
ax.set_xticks([0,1],['PC01 / plugfild','PC03 / azul']);ax.set_ylim(0,2);ax.set_ylabel('RMSE · pontos percentuais');ax.set_title('Validação nos 30% finais da campanha',loc='left',fontweight='bold',pad=20);ax.legend(frameon=False,loc='upper left');ax.grid(axis='y',alpha=.13);ax.set_axisbelow(True);finish(fig,'umidade-solo')

r=rows(repo,'02_umidade_solo/resultados/calibracao_laboratorial_cs625/tabelas/metricas_comparacao_curvas_cs625.csv')
fig,ax=plt.subplots(figsize=(10,4.7));ax.set_facecolor('#faf9f5')
for i,(key,label,color) in enumerate([('rmse_ajuste_ponto_percentual','No ajuste',GREEN),('rmse_loocv_ponto_percentual','LOOCV',OCHRE)]):
 vals=[value(next(x for x in r if x['modelo']==model),key) for model in ['linear_especifica_diagnostica','quadratica_especifica']]
 pos=[j+(i-.5)*.32 for j in range(2)];ax.bar(pos,vals,width=.29,label=label,color=color)
 for x,v in zip(pos,vals):ax.text(x,v+.13,f'{v:.2f}'.replace('.',','),ha='center',fontsize=12)
ax.set_xticks([0,1],['Linear diagnóstica','Quadrática específica']);ax.set_ylim(0,10);ax.set_ylabel('RMSE · pontos percentuais');ax.set_title('Ajustar bem não é o mesmo que validar',loc='left',fontweight='bold',pad=20);ax.legend(frameon=False,loc='upper left');ax.grid(axis='y',alpha=.13);ax.set_axisbelow(True);finish(fig,'calibracao-cs625')

download('av1-visualizacao-simepar','resultados/AV1_frente.png',ASSETS/'meteorologia.png')
download('av1-visualizacao-simepar','resultados/AV1_frente_verso_A4.pdf',DOCS/'visualizacao-simepar.pdf')
download('viazualisa-o-de-graficos-de-maneira-moderna','imagens/van_langren_moderno.png',ASSETS/'historico.png')
download('viazualisa-o-de-graficos-de-maneira-moderna','viazualisação_de_graficos_de_maneira_moderna.pdf',DOCS/'visualizacoes-historicas.pdf')
(ROOT/'proveniencia.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2),encoding='utf-8')
print('ASSETS',len(list(ASSETS.glob('*.png'))),'DOCUMENTOS_ORIGINAIS',len(list(DOCS.glob('*.pdf'))),'FONTES',len(provenance))
