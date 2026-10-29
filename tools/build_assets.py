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
def finish(fig,name,rect=(0,0,1,1)):
 fig.set_facecolor('#faf9f5');fig.tight_layout(pad=1.8,rect=rect);fig.savefig(ASSETS/(name+'.png'),dpi=160,facecolor=fig.get_facecolor());plt.close(fig)
repo='acervo-de-contribuicoes-Heitor-Fernandes-Simepar'
# Forest plot: uncertainty and signed error, not only a fit-on-sample score.
fig,axes=plt.subplots(1,2,figsize=(12,6.2))
for ax,folder,title,unit,color in zip(axes,['temperatura','umidade'],['Temperatura do ar','Umidade relativa'],['°C','pontos percentuais'],[GREEN,OCHRE]):
 path='01_estacao_et/resultados/'+folder+'/tabelas/intervalos_confianca_'+folder+'_bootstrap_blocos.csv'
 r=rows(repo,path,';');ax.set_facecolor('#faf9f5')
 for y,metric in enumerate(['vies','mae','rmse']):
  row=next(x for x in r if x['metrica']==metric)
  v,lo,hi=[value(row,k) for k in ['estimativa','limite_inferior_95','limite_superior_95']]
  ax.errorbar(v,y,xerr=[[v-lo],[hi-v]],fmt='o',color=color,ecolor=color,markersize=9,elinewidth=3,capsize=6,zorder=3)
  text=f'{v:.2f}  [{lo:.2f}; {hi:.2f}]'.replace('.',',')
  ax.annotate(text,(v,y),xytext=(0,20),textcoords='offset points',ha='center',color=color,fontsize=12,fontweight='bold')
 ax.set_yticks([0,1,2],['Viés','MAE','RMSE']);ax.set_ylim(2.6,-.8);ax.axvline(0,color='#b8c3b9',lw=1,ls='--');ax.set_title(title,loc='left',fontweight='bold',fontsize=15,pad=14);ax.set_xlabel(unit);ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
 ax.set_xlim((-.12,.76) if folder=='temperatura' else (-2.5,5.2))
fig.suptitle('Quanto a estação difere da verificação?',fontsize=18,fontweight='bold',x=.04,ha='left',color='#193b32')
fig.text(.04,.045,'Ponto = estimativa  ·  Haste = IC de 95% por bootstrap em blocos de 96 observações',fontsize=11,color='#53685c')
fig.text(.04,.012,'Viés: desvio médio  |  MAE: erro absoluto médio  |  RMSE: maior peso para desvios grandes',fontsize=10.5,color='#53685c')
finish(fig,'estacao-et',rect=(0,.085,1,.96))

r=rows(repo,'02_umidade_solo/contribuicoes/validacao_pc01_pc03_cs_20261002_a_20261007/resultados/tabelas/validacao_temporal_70_30.csv')
fig,axes=plt.subplots(1,2,figsize=(12,6.2))
for ax,key,title in zip(axes,['rmse_pp','bias_pp'],['Tamanho do erro · RMSE','Direção do desvio · viés']):
 ax.set_facecolor('#faf9f5')
 for sensor,label,color,marker,offset in [('plugfild','PC01 / plugfild',GREEN,'o',-21),('PC03/azul','PC03 / azul',OCHRE,'D',12)]:
  vals=[value(next(x for x in r if x['sensor']==sensor and x['modelo']==m),key) for m in ['original','linear_treino70','quadratico_treino70']]
  ax.plot([0,1,2],vals,color=color,marker=marker,ms=7,lw=2.3,label=label,zorder=3)
  for x,v in enumerate(vals):ax.annotate(f'{v:.2f}'.replace('.',','),(x,v),xytext=(0,offset),textcoords='offset points',ha='center',color=color,fontweight='bold',fontsize=12)
 ax.set_xticks([0,1,2],['Original','Linear','Quadrático']);ax.set_xlim(-.3,2.3);ax.set_ylim((-2,17) if key=='rmse_pp' else (-9,17));ax.set_ylabel('pontos percentuais');ax.set_title(title,loc='left',fontweight='bold',fontsize=14,pad=18);ax.axhline(0,color='#a8b9a9',ls='--',lw=1);ax.grid(axis='y',alpha=.14);ax.set_axisbelow(True)
fig.suptitle('O que muda depois do ajuste?',fontsize=18,fontweight='bold',x=.04,ha='left',color='#193b32')
handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='upper right',bbox_to_anchor=(.97,.99),frameon=False,ncol=2,fontsize=11)
fig.text(.04,.045,'Validação nos 30% finais · 450 pares por sensor · modelos ajustados apenas nos 70% iniciais',fontsize=11,color='#53685c')
fig.text(.04,.012,'Menor RMSE e viés próximo de zero são desejáveis. As linhas comparam versões da leitura, não horários.',fontsize=10.5,color='#53685c')
finish(fig,'umidade-solo',rect=(0,.085,1,.93))

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
