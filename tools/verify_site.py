"""Build project PDF sheets and exercise the real static portfolio in Chromium."""
from pathlib import Path
import json,sys,re,urllib.parse
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=Path('C:/Users/heito/AppData/Local/hermes/cache/scratch/portfolio-qa')
OUT.mkdir(exist_ok=True)
projects=json.loads((ROOT/'projetos.json').read_text(encoding='utf-8'))
url=sys.argv[1] if len(sys.argv)>1 else (ROOT/'index.html').as_uri()
live=url.startswith('https:')
report={'live':live,'projects':len(projects),'checks':[]}
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
 if not live and '--skip-pdfs' not in sys.argv:
  page=browser.new_page()
  for p in projects:
   page.goto((ROOT/'_build'/('ficha-'+p['id']+'.html')).as_uri(),wait_until='load')
   page.pdf(path=str(ROOT/'trabalhos'/('ficha-'+p['id']+'.pdf')),format='A4',print_background=True,prefer_css_page_size=True)
  page.close()
 for width,height,label in [(1440,1000,'desktop'),(390,844,'mobile')]:
  page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
  errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
  page.goto(url,wait_until='load',timeout=60000)
  assert len(projects)==5
  assert page.locator('#card-calibracao-cs625').count()==0
  assert page.locator('article.project').count()==len(projects)
  assert page.locator('article.project:visible').count()==len(projects)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),label+' overflow'
  page.screenshot(path=str(OUT/(('live-' if live else '')+label+'.png')),full_page=True)
  for category in ['ambiental','visualizacao']:
   page.locator('[data-filter="'+category+'"]').click()
   expected=sum(p['category']==category for p in projects)
   assert page.locator('article.project:visible').count()==expected
   assert page.locator('[data-filter="'+category+'"]').get_attribute('aria-pressed')=='true'
  page.locator('[data-filter="todos"]').click()
  for p in projects:
   page.locator('#card-'+p['id']+' .read-study').click()
   assert page.locator('#project-dialog').is_visible()
   assert page.locator('#detail-title').inner_text()==p['title']
   page.wait_for_function("document.querySelector('.detail-figure img').complete && document.querySelector('.detail-figure img').naturalWidth>0")
   assert page.locator('.brief-link').get_attribute('href')=='trabalhos/ficha-'+p['id']+'.pdf'
   assert page.locator('.source-link').get_attribute('href')==p['sourceUrl']
   if p.get('background'):
    assert page.locator('.project-context').is_visible()
    assert p['contribution'] in page.locator('.project-context').inner_text()
    assert page.locator('.related-source').evaluate_all('(nodes)=>nodes.map(n=>n.getAttribute("href"))')==[s['url'] for s in p['relatedSources']]
   assert page.evaluate("document.querySelector('dialog').scrollWidth<=document.querySelector('dialog').clientWidth+1")
   if p['id']=='estacao-et':
    page.screenshot(path=str(OUT/(('live-' if live else '')+label+'-detail.png')),full_page=False)
   page.keyboard.press('Escape')
   assert not page.locator('#project-dialog').is_visible()
   report['checks'].append(label+': '+p['id']+' opens, image, links, Escape')
  assert not errors,errors
  page.evaluate('window.scrollTo(0,0)')
  page.wait_for_timeout(150)
  page.screenshot(path=str(OUT/(('live-' if live else '')+label+'.png')),full_page=True)
  page.close()
 # Direct links must open the selected work without requiring another click.
 page=browser.new_page(viewport={'width':390,'height':844})
 page.goto(url.split('#')[0]+'#projeto-umidade-solo',wait_until='load')
 assert page.locator('#project-dialog').is_visible()
 assert page.locator('#detail-title').inner_text()==projects[1]['title']
 page.close();browser.close()
report['checks'].append('deep link to soil-moisture project')
(OUT/('live-report.json' if live else 'report.json')).write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True,indent=2))
