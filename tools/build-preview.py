"""Build a static, namespaced preview without changing source game files."""
import argparse,json,re,shutil,urllib.request
from pathlib import Path

SOURCE_REPO='nivesmik/hex-haven'
ASSETS=['index.html','style.css','src/main.js','src/engine.js','src/renderer.js','src/ecosystem.js','src/experiment.js']
KEYS=['hexhaven-save-v3','hexhaven-experiment-v07','hexhaven-view-v07']

def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'hex-haven-preview','Accept':'application/vnd.github+json'})
    with urllib.request.urlopen(req,timeout=30) as response:return response.read().decode()

def build(source,output,pr,sha):
    if pr<1 or not re.fullmatch('[a-f0-9]{40}',sha):raise ValueError('Invalid PR or SHA')
    dest=output/f'pr-{pr}';dest.mkdir(parents=True,exist_ok=True)
    prefix=f'hexhaven-preview:pr-{pr}:'
    for name in ASSETS:
        content=source(name)
        if name=='src/main.js':
            for key in KEYS:
                if content.count("'"+key+"'")!=1:raise ValueError('Review new game storage keys before publishing')
                content=content.replace("'"+key+"'", "'"+prefix+key+"'")
        if name=='index.html':
            if content.count('src="src/main.js"')!=1:raise ValueError('Unsupported entrypoint')
            content=content.replace('src="src/main.js"','src="preview-entry.js"')
            content=content.replace('<title>HEX HAVEN v0.7</title>',f'<title>HEX HAVEN PR #{pr} 테스트</title>')
            content=content.replace('HEX HAVEN <span>v0.7</span>',f'HEX HAVEN <span>PR #{pr} 테스트 · {sha[:7]}</span>')
        path=dest/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
    entry="""import {createExperiment,serialize} from './src/engine.js';
const prefix=PREFIX;
const params=new URLSearchParams(window.location.search);
// Only an explicit fresh link resets this PR's own save; reload then resumes it.
if(params.get('fresh')==='1'){
  try{
    localStorage.setItem(prefix+'hexhaven-experiment-v07',JSON.stringify(serialize(createExperiment('standard',202607))));
    localStorage.setItem(prefix+'hexhaven-view-v07','experiment');
  }catch{}
  params.delete('fresh');
  window.history.replaceState(null,'',window.location.pathname+(params.size?'?'+params.toString():'')+window.location.hash);
}
await import('./src/main.js');
""".replace('PREFIX',json.dumps(prefix))
    (dest/'preview-entry.js').write_text(entry)
    manifest={'source_repository':SOURCE_REPO,'source_pr':pr,'source_sha':sha,'default_difficulty':'standard','default_seed':202607,'storage_prefix':prefix}
    (dest/'preview.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    (output/'index.html').write_text(f'<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>HEX HAVEN PR 테스트</title><h1>HEX HAVEN PR #{pr} 테스트</h1><p>정식 게임과 저장 데이터가 분리됩니다.</p><a href="pr-{pr}/?fresh=1">기본 난이도 · 시드 202607로 새 테스트 시작</a><p><a href="pr-{pr}/">저장한 테스트 계속하기</a></p></html>\n')
    (output/'.nojekyll').touch()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--pr',type=int,default=3);parser.add_argument('--source-dir',type=Path);parser.add_argument('--sha');parser.add_argument('--output',type=Path,default=Path('_site'));args=parser.parse_args()
    if args.source_dir:
        source=lambda name:(args.source_dir/name).read_text();sha=args.sha
    else:
        info=json.loads(get(f'https://api.github.com/repos/{SOURCE_REPO}/pulls/{args.pr}'))
        sha=info['head']['sha'];repo=info['head']['repo']['full_name']
        source=lambda name:get(f'https://raw.githubusercontent.com/{repo}/{sha}/{name}')
    build(source,args.output,args.pr,sha)
