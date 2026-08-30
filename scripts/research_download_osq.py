import json, os, shutil, subprocess, time, zipfile
from pathlib import Path
ROOT=Path('.').resolve()
LIST=ROOT/'Download code osquestador auditor memoria'/'REPOS.json'
MANIFEST=ROOT/'Download code osquestador auditor memoria'/'RESEARCH_DOWNLOAD_MANIFEST.jsonl'
WORK=ROOT/'_work/osq'; SRC=WORK/'src'; PACK=WORK/'pack'
SPLIT_TARGET=12000000; BATCH_LIMIT=90*1024*1024; CHUNK=8*1024*1024
def run(c,cwd=None):
    subprocess.run(c,cwd=cwd,check=True)
def done(slug):
    if not MANIFEST.exists(): return False
    return any(json.loads(x).get('slug')==slug and json.loads(x).get('status')=='COMPLETE' for x in MANIFEST.read_text().splitlines() if x.strip())
def chunk_big(root):
    for p in list(root.rglob('*')):
        if not p.is_file(): continue
        if p.stat().st_size<=CHUNK: continue
        d=p.parent/(p.name+'.chunks'); d.mkdir(exist_ok=True)
        with p.open('rb') as f:
            i=0
            while True:
                data=f.read(CHUNK)
                if not data: break
                (d/f'{p.name}.part-{i:04d}').write_bytes(data); i+=1
        p.unlink()
