"""Runs every exercise's reference solution on SQLite. Usage: python3 validate.py  (exit 1 on any failure)"""
import json, glob, sqlite3, sys
bad = 0
def fail(m):
    global bad; bad += 1; print('FAIL', m)
def fresh(ds):
    c = sqlite3.connect(':memory:'); c.executescript(open('data/sqlite/%s.sql' % ds).read()); return c
for f in sorted(glob.glob('lessons/m[0-9]*.json')):
    L = json.load(open(f))
    for k in ('id','module','title','order','level','estimatedMinutes','prerequisites','engines','dataset','theory','examples','exercises'):
        if k not in L: fail('%s missing %s' % (f, k))
    for ex in L['examples']:
        try: fresh(L['dataset']).execute(ex['sql']).fetchall()
        except Exception as e: fail('%s example error: %s' % (L['id'], e))
    for e in L['exercises']:
        ds = e.get('dataset', L['dataset']); eid = e['id']
        for k in ('task','starter','hint1','hint2','solution','explain','compare'):
            if not e.get(k): fail('%s missing %s' % (eid, k))
        try:
            c = fresh(ds); st = e.get('check', {}).get('type') == 'state'
            if st: c.executescript(e['solution']); rows = c.execute(e['check']['verify']).fetchall()
            else: rows = c.execute(e['solution']).fetchall()
            if not rows: fail('%s solution returns no rows' % eid)
            else: print('ok  ', eid, len(rows), 'rows')
        except Exception as ex: fail('%s solution error: %s' % (eid, ex))
print('FAILED: %d' % bad if bad else 'ALL OK'); sys.exit(1 if bad else 0)
