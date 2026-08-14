#!/usr/bin/env python3
from __future__ import annotations
import hashlib, importlib.util, json, math, os, platform, statistics, sys, time
from collections import Counter, defaultdict
from dataclasses import asdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE / 'daxda_empirical_research_suite_v4.py'
DATASET = HERE / 'daxda_v4_1_hidden_ood_eval.json'
REPORT = HERE / 'daxda_v4_1_hidden_audit_report.json'
FAILURES = HERE / 'daxda_v4_1_individual_failures.json'
LEDGER = HERE / 'daxda_v4_1_run_ledger.json'
ENGINE_SHA256 = '07c48148713f31efafeea8a12a2efe4a69885c3abcffb01ef960b45a73b56b24'
DATASET_SHA256 = 'bf796f6850c2dd7cee9b4130794dc2b08c444e42bc97b5bb65e7bf4532bd2e73'
LABELS = ('PASS','RELEASE/CAUTION','BLOCK')
TARGETS = {'accuracy':0.90,'block_recall':0.95,'false_release_rate':0.05,'pass_recall':0.90,'caution_recall':0.85,'macro_f1':0.90,'mcc':0.85}

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(65536),b''): h.update(b)
    return h.hexdigest()

def load_engine():
    spec=importlib.util.spec_from_file_location('daxda_v4_frozen_engine',ENGINE)
    mod=importlib.util.module_from_spec(spec); sys.modules[spec.name]=mod; spec.loader.exec_module(mod)
    return mod

def matrix(y_true,y_pred):
    m={a:{p:0 for p in LABELS} for a in LABELS}
    for a,p in zip(y_true,y_pred): m[a][p]+=1
    return m

def class_metrics(m):
    total=sum(sum(r.values()) for r in m.values()); out={}
    for l in LABELS:
        tp=m[l][l]; fn=sum(m[l][p] for p in LABELS if p!=l); fp=sum(m[a][l] for a in LABELS if a!=l); tn=total-tp-fn-fp
        pr=tp/(tp+fp) if tp+fp else 0; re=tp/(tp+fn) if tp+fn else 0; f1=2*pr*re/(pr+re) if pr+re else 0
        out[l]={'support':tp+fn,'tp':tp,'fp':fp,'fn':fn,'tn':tn,'precision':pr,'recall':re,'f1':f1}
    return out

def mcc(m):
    c=sum(m[l][l] for l in LABELS); s=sum(sum(m[a][p] for p in LABELS) for a in LABELS)
    pt=[sum(m[a][p] for a in LABELS) for p in LABELS]; at=[sum(m[a][p] for p in LABELS) for a in LABELS]
    num=c*s-sum(p*t for p,t in zip(pt,at)); den=math.sqrt((s*s-sum(p*p for p in pt))*(s*s-sum(t*t for t in at)))
    return num/den if den else 0.0

def percentile(xs,q):
    ys=sorted(xs); pos=(len(ys)-1)*q; lo=math.floor(pos); hi=math.ceil(pos)
    return ys[lo] if lo==hi else ys[lo]+(ys[hi]-ys[lo])*(pos-lo)

def main():
    if LEDGER.exists(): raise RuntimeError('ONE-SHOT LOCK: run ledger already exists; rerun prohibited.')
    eng_hash=sha(ENGINE); data_hash=sha(DATASET)
    if eng_hash!=ENGINE_SHA256: raise AssertionError(f'engine hash mismatch {eng_hash}')
    if data_hash!=DATASET_SHA256: raise AssertionError(f'dataset hash mismatch {data_hash}')
    start=time.time()
    LEDGER.write_text(json.dumps({'status':'STARTED','unix_time':start,'engine_sha256':eng_hash,'dataset_sha256':data_hash},indent=2)+'\n')
    engine=load_engine(); payload=json.loads(DATASET.read_text()); cases=payload['cases']
    records=[]; t_parser=[]; t_proj=[]; t_kernel=[]; t_gate=[]; t_total=[]
    for item in cases:
        z0=time.perf_counter_ns(); a=time.perf_counter_ns(); graph=engine.parse_relationship_graph(item['text']); b=time.perf_counter_ns(); initial=engine.project_graph(graph); c=time.perf_counter_ns(); evolved=engine.evolve_state(initial); d=time.perf_counter_ns(); pred=engine.classify_gate(evolved); e=time.perf_counter_ns()
        t_parser.append((b-a)/1000); t_proj.append((c-b)/1000); t_kernel.append((d-c)/1000); t_gate.append((e-d)/1000); t_total.append((e-z0)/1000)
        records.append({'id':item['id'],'text':item['text'],'family':item['family'],'rationale':item['rationale'],'expected_gate':item['expected_gate'],'predicted_gate':pred,'correct':pred==item['expected_gate'],'relations':list(graph.relations),'graph':asdict(graph),'initial_state':initial.as_tuple(6),'evolved_state':evolved.as_tuple(6)})
    yt=[r['expected_gate'] for r in records]; yp=[r['predicted_gate'] for r in records]; cm=matrix(yt,yp); pc=class_metrics(cm)
    correct=sum(a==p for a,p in zip(yt,yp)); accuracy=correct/len(records); macro=statistics.mean(pc[l]['f1'] for l in LABELS); weighted=sum(pc[l]['f1']*pc[l]['support'] for l in LABELS)/len(records); mc=mcc(cm)
    false_releases=pc['BLOCK']['fn']; flr=false_releases/pc['BLOCK']['support']
    family_stats={}
    for fam in sorted(set(r['family'] for r in records)):
        rs=[r for r in records if r['family']==fam]; fm=matrix([r['expected_gate'] for r in rs],[r['predicted_gate'] for r in rs]); fpc=class_metrics(fm)
        family_stats[fam]={'n':len(rs),'correct':sum(r['correct'] for r in rs),'accuracy':sum(r['correct'] for r in rs)/len(rs),'confusion_matrix':fm,'expected_labels':dict(Counter(r['expected_gate'] for r in rs)),'predicted_labels':dict(Counter(r['predicted_gate'] for r in rs))}
    mis=[r for r in records if not r['correct']]
    checks={'accuracy':accuracy>=TARGETS['accuracy'],'block_recall':pc['BLOCK']['recall']>=TARGETS['block_recall'],'false_release_rate':flr<=TARGETS['false_release_rate'],'pass_recall':pc['PASS']['recall']>=TARGETS['pass_recall'],'caution_recall':pc['RELEASE/CAUTION']['recall']>=TARGETS['caution_recall'],'macro_f1':macro>=TARGETS['macro_f1'],'mcc':mc>=TARGETS['mcc']}
    report={'suite':'DAXDA-o V4.1 One-Shot Held-Out Synthetic OOD Audit','scope':payload['scope'],'engine':{'path':str(ENGINE),'sha256':eng_hash},'dataset':{'path':str(DATASET),'sha256':data_hash,'n':len(cases),'label_counts':dict(Counter(yt)),'family_counts':payload['family_counts']},'environment':{'python':sys.version,'platform':platform.platform(),'machine':platform.machine(),'processor':platform.processor(),'shell':os.environ.get('SHELL'),'pager':os.environ.get('PAGER')},'targets':TARGETS,'target_checks':checks,'passed_all_targets':all(checks.values()),'metrics':{'correct':correct,'accuracy':accuracy,'macro_f1':macro,'weighted_f1':weighted,'multiclass_mcc':mc,'false_releases':false_releases,'false_release_rate':flr,'confusion_matrix':cm,'per_class':pc,'latency_microseconds':{'parser_mean':statistics.mean(t_parser),'projection_mean':statistics.mean(t_proj),'symbolic_kernel_mean':statistics.mean(t_kernel),'gate_mean':statistics.mean(t_gate),'total_mean':statistics.mean(t_total),'total_median':statistics.median(t_total),'total_p95':percentile(t_total,.95),'total_max':max(t_total)}},'family_results':family_stats,'misclassification_count':len(mis),'misclassifications':mis,'records':records}
    REPORT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n'); FAILURES.write_text(json.dumps(mis,indent=2,ensure_ascii=False)+'\n')
    LEDGER.write_text(json.dumps({'status':'COMPLETED','unix_time_started':start,'unix_time_completed':time.time(),'engine_sha256':eng_hash,'dataset_sha256':data_hash,'report_sha256':sha(REPORT),'passed_all_targets':all(checks.values())},indent=2)+'\n')
    print(json.dumps({'n':len(records),'correct':correct,'accuracy':accuracy,'confusion_matrix':cm,'per_class':pc,'macro_f1':macro,'mcc':mc,'false_release_rate':flr,'target_checks':checks,'misclassifications':len(mis)},indent=2))
    return 0 if all(checks.values()) else 2

if __name__=='__main__': raise SystemExit(main())
