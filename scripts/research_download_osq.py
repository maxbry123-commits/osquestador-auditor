import json, shutil, subprocess, time, zipfile
from pathlib import Path
ROOT=Path('.').resolve()
LIST=ROOT/'Download code osquestador auditor memoria'/'REPOS.json'
MANIFEST=ROOT/'Download code osquestador auditor memoria'/'RESEARCH_DOWNLOAD_MANIFEST.jsonl'
WORK=ROOT/'_work/osq'; SRC=WORK/'src'; PACK=WORK/'pack'
SPLIT_TARGET=12000000; BATCH_LIMIT=90*1024*1024
def run(c,cwd=None): subprocess.run(c,cwd=cwd,check=True)
def done(slug):
    if not MANIFEST.exists(): return False
    return any(json.loads(x).get('slug')==slug and json.loads(x).get('status')=='COMPLETE' for x in MANIFEST.read_text().splitlines() if x.strip())
def push(label):
    for attempt in range(1,8):
        try:
            run(['git','fetch','origin','main']); run(['git','rebase','origin/main']); run(['git','push','origin','HEAD:main']); print('PUSH PASS',label,attempt); return
        except subprocess.CalledProcessError:
            if attempt==7: raise
            time.sleep(attempt*3)
def commit(n,label):
    if not n: return
    run(['git','add','-A'])
    if subprocess.run(['git','diff','--cached','--quiet']).returncode==0: return
    run(['git','config','user.name','github-actions[bot]']); run(['git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com']); run(['git','commit','-m',f'build(osq): {label} ({n} bytes)']); push(label)
REPOS=json.loads(LIST.read_text()); MANIFEST.parent.mkdir(parents=True, exist_ok=True); SRC.mkdir(parents=True, exist_ok=True); PACK.mkdir(parents=True, exist_ok=True)
batch=batch_no=0
for item in REPOS:
    number,slug,url=item['n'],item['slug'],item['url']
    print(f'===== QUEUE {number}: {slug} =====')
    if done(slug): print(slug,'COMPLETE'); continue
    root=SRC/slug; shutil.rmtree(root,ignore_errors=True)
    run(['git','clone','--depth','1','--no-tags',url,str(root)])
    sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(); shutil.rmtree(root/'.git',ignore_errors=True)
    full=PACK/f'{slug}_full.zip'; full.unlink(missing_ok=True)
    run(['zip','-q','-r','-9','-y',str(full.resolve()),'.'],cwd=root)
    parts=[]
    if full.stat().st_size<=SPLIT_TARGET:
        out=PACK/f'{slug}_0001.zip'; full.replace(out); parts=[(out,out.stat().st_size)]
    else:
        before=set(PACK.glob('*.zip')); run(['zipsplit','-n',str(SPLIT_TARGET),'-b',str(PACK.resolve()),str(full.resolve())]); full.unlink(missing_ok=True)
        made=[p for p in PACK.glob('*.zip') if p not in before]
        for i,p in enumerate(sorted(made,key=lambda p:(p.stat().st_mtime,p.name)),1):
            q=PACK/f'{slug}_{i:04d}.zip'; p.replace(q); parts.append((q,q.stat().st_size))
    dest=ROOT/slug; dest.mkdir(parents=True, exist_ok=True)
    for z,sz in parts:
        shutil.copy2(z, dest/z.name)
        with zipfile.ZipFile(z) as zf: zf.extractall(dest)
    size=sum(s for _,s in parts)
    if batch and batch+size>BATCH_LIMIT: commit(batch,f'{batch_no:03d}'); batch=0; batch_no+=1
    batch+=size
    with MANIFEST.open('a') as f: f.write(json.dumps({'number':int(number),'slug':slug,'source':url,'source_commit':sha,'parts':len(parts),'status':'COMPLETE'})+'\n')
    shutil.rmtree(root,ignore_errors=True); shutil.rmtree(PACK,ignore_errors=True); PACK.mkdir(parents=True, exist_ok=True)
commit(batch,f'{batch_no:03d}-final'); print('===== QUEUE OSQ 96 COMPLETE =====')
