#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json, os, pathlib, shutil, tempfile

BASE=pathlib.Path('➡️📂 Shack imput/➡️📂 shart imput code Run')
HELPER=BASE/'repair_ignored_publication.py'
REPORT=pathlib.Path('➡️📂 Shack imput/📂 Craxy wall bitácora stated JSON/FIRECRAWL-EXACT-ONE-REPAIR.json')
spec=importlib.util.spec_from_file_location('repair_ignored_publication', HELPER)
if spec is None or spec.loader is None: raise SystemExit('HELPER_IMPORT_GAP')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
TARGET=mod.COMPONENTS/'search'/'firecrawl'
REL='examples/o1_web_crawler/o1_web_crawler.py'
EXPECTED_SOURCE_BLOB='ebe4bcbf7a5d8a2df5a6c1e8c9257de691152a4e'
EXPECTED_CURRENT_BLOB='45bbd1eeae6e9be5684e7efdd86b637517759023'

def blob(p:pathlib.Path)->str:
    return mod.run(['git','hash-object','--',p.as_posix()]).stdout.strip()

def main()->int:
    manifest=json.loads((TARGET/'DOWNLOAD_EXTRACT_MANIFEST.json').read_text())
    source_repo=str(manifest['source_repo']).removeprefix('https://github.com/')
    source_commit=str(manifest['source_commit'])
    expected=mod.source_blobs(source_repo, source_commit)
    if expected.get(REL)!=EXPECTED_SOURCE_BLOB: raise RuntimeError('UPSTREAM_BLOB_PRECONDITION_GAP')
    current=TARGET/'code'/pathlib.PurePosixPath(REL)
    if not current.is_file() or blob(current)!=EXPECTED_CURRENT_BLOB: raise RuntimeError('DESTINATION_BLOB_PRECONDITION_GAP')
    mod.verify_archive_parts(TARGET, manifest)
    with tempfile.TemporaryDirectory(prefix='shark-firecrawl-exact-one-') as td:
        temp=pathlib.Path(td); extracted=temp/'extracted'; source=temp/'source'
        env1=dict(os.environ); env1.update({'ARCHIVE_INPUT':str(TARGET/'_archives'),'DEST_DIR':str(extracted),'STATE_FILE':str(temp/'extract-state.json'),'BATCH_SIZE':'100'})
        p1=mod.run(['python3',str(mod.MOTOR1)],env=env1,check=False); v1=mod.json_from_last_line(p1.stdout)
        if p1.returncode or v1.get('verdict')!='VERIFIED_CLOSED': raise RuntimeError('MOTOR1_NOT_CLOSED:'+json.dumps(v1,ensure_ascii=False))
        src=extracted/pathlib.PurePosixPath(REL)
        if not src.is_file() or blob(src)!=EXPECTED_SOURCE_BLOB: raise RuntimeError('EXTRACTED_SOURCE_BLOB_MISMATCH')
        staged=source/pathlib.PurePosixPath(REL); staged.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,staged)
        env3=dict(os.environ); env3.update({'SOURCE_DIR':str(source),'DEST_DIR':str(TARGET/'code'),'STATE_FILE':str(temp/'copy-state.json'),'BATCH_SIZE':'1','COLLISION_POLICY':'replace'})
        p3=mod.run(['python3',str(mod.MOTOR3)],env=env3,check=False); v3=mod.json_from_last_line(p3.stdout)
        if p3.returncode or v3.get('verdict')!='VERIFIED_CLOSED': raise RuntimeError('MOTOR3_NOT_CLOSED:'+json.dumps(v3,ensure_ascii=False))
    if blob(current)!=EXPECTED_SOURCE_BLOB: raise RuntimeError('POST_REPLACE_BLOB_MISMATCH')
    mod.run(['git','add','-f','--',current.as_posix()])
    changed=mod.staged_paths(TARGET/'code','MRTUXB')
    expected_path=current.as_posix()
    if changed!=[expected_path]: raise RuntimeError('STAGED_PATH_SET_MISMATCH:'+json.dumps(changed,ensure_ascii=False))
    payload={'schema':'wanted-shark.firecrawl-exact-one-repair.v1','path':REL,'previous_blob':EXPECTED_CURRENT_BLOB,'source_blob':EXPECTED_SOURCE_BLOB,'source_commit':source_commit,'motor_1':'VERIFIED_CLOSED','motor_3':'VERIFIED_CLOSED','collision_policy':'replace','overwrite_scope':'ONE_EXPLICIT_VERIFIED_PATH','verdict':'READY_FOR_PUBLISH'}
    REPORT.write_text(json.dumps(payload,indent=2,ensure_ascii=False,sort_keys=True)+'\n'); mod.run(['git','add','-f','--',REPORT.as_posix()])
    print(json.dumps(payload,ensure_ascii=False,sort_keys=True)); return 0

if __name__=='__main__':
    try: raise SystemExit(main())
    except Exception as exc:
        mod.rollback_target(TARGET)
        payload={'schema':'wanted-shark.firecrawl-exact-one-repair.v1','error':str(exc),'verdict':'REPAIR_FAILED_CLOSED'}
        REPORT.write_text(json.dumps(payload,indent=2,ensure_ascii=False,sort_keys=True)+'\n'); mod.run(['git','add','-f','--',REPORT.as_posix()])
        print(json.dumps(payload,ensure_ascii=False,sort_keys=True)); raise SystemExit(2)
