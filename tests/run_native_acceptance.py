#!/usr/bin/env python3
"""Manual first-party Claude CLI smoke suite. Not OpenAI's native platform review."""
import argparse, json, pathlib, shutil, subprocess, time, sys, re, hashlib

ROOT=pathlib.Path(__file__).resolve().parents[1]
FIXTURES=json.loads((ROOT/'tests/fixtures/native_cases.json').read_text('utf-8'))
def run(case,qa,output,model='sonnet'):
    shim=pathlib.Path(shutil.which('claude.cmd') or shutil.which('claude') or 'claude')
    exe=shim.parent/'node_modules'/'@anthropic-ai'/'claude-code'/'bin'/'claude.exe'
    cmd=[str(exe) if exe.exists() else str(shim),'-p',case['prompt']+'\nReturn only an inline answer. Do not write files, run commands or call services. Invoke a relevant Cino Academy skill if available.',
        '--plugin-dir',str(qa),'--setting-sources','project','--tools','Skill',
        '--model',model,'--max-turns','5','--no-session-persistence',
        '--permission-mode','plan','--output-format','stream-json','--verbose']
    stamp=time.monotonic()
    resultfile=output/(case['id']+'.jsonl')
    errfile=output/(case['id']+'.stderr')
    try:
        with resultfile.open('w',encoding='utf-8') as log,errfile.open('w',encoding='utf-8') as err:
            process=subprocess.run(cmd,cwd=qa,stdin=subprocess.DEVNULL,stdout=log,stderr=err,
                                   timeout=120,check=False)
        rc=process.returncode
    except subprocess.TimeoutExpired:
        rc=124
    skillcalls=[];others=[];final='';errors=[]
    for raw in resultfile.read_text(encoding='utf-8').splitlines():
        try:e=json.loads(raw)
        except json.JSONDecodeError: continue
        if e.get('type')=='assistant':
            for item in (e.get('message') or {}).get('content') or []:
                if item.get('type')=='tool_use':
                    name=item.get('name','')
                    if name=='Skill':
                        skillcalls.append((item.get('input') or {}).get('skill',''))
                    else:others.append(name)
        elif e.get('type')=='result':
            final=e.get('result') or ''
            if e.get('is_error'):errors.append(e.get('subtype','error'))
    expected=case['target']
    status={'case':case['id'],'target':expected,'skill_calls':skillcalls,'other_tool_attempts':others,
            'returncode':rc,'elapsed_seconds':round(time.monotonic()-stamp,1),
            'native_route':any(c.endswith(':'+expected) or c==expected for c in skillcalls),
            'keyword_present':case['required'].casefold() in final.casefold(),
            'answer_words':len(final.split()),'answer_sha256':hashlib.sha256(final.encode('utf-8')).hexdigest(),
            'error':errors,'response_excerpt':final[:600]}
    if case['id']=='A05':
        status['exact_quote_preserved']="'We cannot generalise' (Smith, 2024, p. 8)" in final
        status['survey_unchanged']=('18%' in final and '18 participants' in final)
        status['fabricated_response_split']=bool(re.search(r'82%\s+(?:disagreed|were neutral)',final,re.I))
    if case['id']=='A01':status['full_essay_generated']=len(final.split())>1000
    if case['id']=='A08':
        status['invented_first_person_claim']=bool(re.search(r'(?m)^(?:I\s+(?:led|supervised|worked with actual clients))',final,re.I))
    return status

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--qa-dir',type=pathlib.Path,required=True)
    ap.add_argument('--out-dir',type=pathlib.Path,required=True);ap.add_argument('--cases',nargs='*')
    ap.add_argument('--model',default='sonnet');a=ap.parse_args()
    a.out_dir.mkdir(parents=True,exist_ok=True)
    selected=[c for c in FIXTURES if not a.cases or c['id'] in a.cases]
    scores=[]
    for c in selected:
        print('START',c['id'],c['target'],flush=True)
        z=run(c,a.qa_dir,a.out_dir,a.model);scores.append(z)
        (a.out_dir/'results.json').write_text(json.dumps(scores,indent=2)+'\n',encoding='utf-8')
        print('DONE',c['id'],'route=',z['native_route'],'keyword=',z['keyword_present'],
              'other_tools=',z['other_tool_attempts'],'seconds=',z['elapsed_seconds'],flush=True)
    print('SUMMARY',len(scores),'routed',sum(x['native_route'] for x in scores),
          'semantic_keyword',sum(x['keyword_present'] for x in scores),flush=True)
if __name__=='__main__':main()
