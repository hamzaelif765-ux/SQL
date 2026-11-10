"""Builds dist/index.html (single file, lessons + datasets embedded). Usage: python3 build.py"""
import json, glob, os
L = [json.load(open(f)) for f in sorted(glob.glob('lessons/m[0-9]*.json'))]
D = {os.path.basename(f)[:-4]: open(f).read() for f in glob.glob('data/sqlite/*.sql')}
h = open('index.template.html').read()
h = h.replace('/*@LESSONS@*/[]', json.dumps(L, ensure_ascii=False).replace('</', '<\\/')).replace('/*@DATASETS@*/{}', json.dumps(D).replace('</', '<\\/'))
os.makedirs('dist', exist_ok=True); open('dist/index.html', 'w').write(h); print('built dist/index.html', len(h), 'bytes')
