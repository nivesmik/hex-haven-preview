import json,sys,time,urllib.request
base=sys.argv[1].rstrip('/')+'/'
paths=['','preview-entry.js','preview.json','style.css','src/main.js','src/engine.js','src/renderer.js','src/ecosystem.js','src/experiment.js']
for attempt in range(12):
    try:
        bodies={}
        for path in paths:
            with urllib.request.urlopen(base+path,timeout=15) as r:
                if r.status!=200:raise RuntimeError(f'{path}: HTTP {r.status}')
                bodies[path]=r.read().decode()
        manifest=json.loads(bodies['preview.json'])
        assert 'preview-entry.js' in bodies['']
        assert manifest['default_difficulty']=='standard' and manifest['default_seed']==202607
        for key in ['hexhaven-save-v3','hexhaven-experiment-v07','hexhaven-view-v07']:
            assert "'"+manifest['storage_prefix']+key+"'" in bodies['src/main.js']
            assert "'"+key+"'" not in bodies['src/main.js']
        print(json.dumps({'url':base,'verified_assets':len(paths),'source_sha':manifest['source_sha'],'storage_prefix':manifest['storage_prefix']}));break
    except Exception:
        if attempt==11:raise
        time.sleep(5)
