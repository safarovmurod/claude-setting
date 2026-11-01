"""Small, ownership-aware Claude Code profile installer (Python 3.11+)."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile

ROOT=Path(__file__).resolve().parent
PRODUCT='claude-setting'

def sha(data):return hashlib.sha256(data).hexdigest()

def plain(path):
    for p in (path,*path.parents):
        if p.is_symlink() or (hasattr(p,'is_junction') and p.is_junction()):raise ValueError('LINK_REFUSED:'+str(p))
        if p.is_file() and p.stat().st_nlink>1:raise ValueError('HARDLINK_REFUSED:'+str(p))

def write(path,data):
    plain(path);path.parent.mkdir(parents=True,exist_ok=True)
    handle,name=tempfile.mkstemp(dir=path.parent,prefix='.claude-setting-')
    try:
        with os.fdopen(handle,'wb') as f:f.write(data)
        os.replace(name,path)
    finally:
        if os.path.exists(name):os.unlink(name)

def load(path):return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}

def run(action,home,source=ROOT):
    if action=='doctor':return operate(action,home,source)
    lock=home.resolve()/'.claude/.claude-setting.lock';plain(lock)
    lock.parent.mkdir(parents=True,exist_ok=True)
    descriptor=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    try:return operate(action,home,source)
    finally:os.close(descriptor);lock.unlink()

def operate(action,home,source=ROOT):
    home=home.resolve();state=home/'.claude/claude-setting';receipt=state/'receipt.json'
    plain(receipt);record=load(receipt)
    if record and record.get('product')!=PRODUCT:raise ValueError('FOREIGN_RECEIPT')
    allowed=load(source/'manifest.json')['files']
    if any(rel not in allowed for rel in record.get('files',{})):raise ValueError('UNOWNED_RECEIPT_PATH')
    if action=='doctor':
        issues=[rel for rel,item in record.get('files',{}).items() if not (home/rel).is_file() or sha((home/rel).read_bytes())!=item['sha256']]
        return {'installed':bool(record),'files_ok':bool(record) and not issues,'issues':issues,'claude_cli_found':shutil.which('claude') is not None,'runtime_discovery_verified':False}
    if action=='install':
        manifest=load(source/'manifest.json');files={}
        for rel,expected in manifest['files'].items():
            if Path(rel).is_absolute() or '..' in Path(rel).parts:raise ValueError('INVALID_PATH')
            data=(source/'profile'/rel).read_bytes()
            if sha(data)!=expected:raise ValueError('SOURCE_HASH_MISMATCH:'+rel)
            target=home/rel;plain(target)
            old=record.get('files',{}).get(rel)
            if old and target.exists() and sha(target.read_bytes())!=old['sha256']:raise ValueError('OWNER_EDIT_REVIEW_REQUIRED:'+rel)
            if rel=='.claude/CLAUDE.md' and target.exists() and not old:
                data=target.read_bytes()+b'\n\n'+data
            elif rel!='.claude/CLAUDE.md' and target.exists() and not old:
                raise ValueError('EXISTING_SKILL_REVIEW_REQUIRED:'+rel)
            files[rel]=data
        record=record or {'product':PRODUCT,'files':{}}
        for rel,data in files.items():
            if rel not in record['files']:
                target=home/rel;backup=sha(rel.encode())+'.bak'
                if target.exists():write(state/'backups'/backup,target.read_bytes())
                record['files'][rel]={'existed':target.exists(),'backup':backup}
            # Preserve the previously merged personal instruction bytes on repeat installs.
            if rel=='.claude/CLAUDE.md' and 'sha256' in record['files'][rel] and (home/rel).exists():files[rel]=(home/rel).read_bytes()
            record['files'][rel]['sha256']=sha(files[rel])
        write(receipt,(json.dumps(record,indent=2)+'\n').encode())
        for rel,data in files.items():write(home/rel,data)
        return run('doctor',home,source)
    if action=='uninstall':
        if not record:raise ValueError('NOT_INSTALLED')
        conflicts=[]
        for rel,item in record['files'].items():
            target=home/rel;plain(target)
            if target.exists() and sha(target.read_bytes())!=item['sha256']:conflicts.append(rel);continue
            if item['existed']:write(target,(state/'backups'/item['backup']).read_bytes())
            elif target.exists():target.unlink()
        if not conflicts:write(receipt,b'{}\n')
        return {'conflicts':conflicts,'backups_retained':True}
    raise ValueError('UNKNOWN_ACTION')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['install','doctor','uninstall']);parser.add_argument('--home',type=Path,default=Path.home())
    args=parser.parse_args()
    try:print(json.dumps(run(args.action,args.home),ensure_ascii=True,indent=2))
    except (ValueError,OSError) as e:parser.exit(1,str(e)+'\n')
