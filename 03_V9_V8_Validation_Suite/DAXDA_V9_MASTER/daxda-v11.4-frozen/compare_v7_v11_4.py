#!/usr/bin/env python3
"""Evaluator-controlled JSONL comparison. Labels are never generated here."""
from __future__ import annotations
import argparse, csv, hashlib, importlib.util, json, pathlib, sys

ROOT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from daxda_engine_v11 import DAXDAEngineV11

def load_v7(path):
    spec=importlib.util.spec_from_file_location("frozen_v7",path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod.DAXDAEngineV7()

def sha(path):
    h=hashlib.sha256(); h.update(pathlib.Path(path).read_bytes()); return h.hexdigest()

def main():
    p=argparse.ArgumentParser(); p.add_argument("corpus"); p.add_argument("--v7",required=True); p.add_argument("--out",default="comparison_results.json")
    a=p.parse_args(); v7=load_v7(a.v7); v11=DAXDAEngineV11(); rows=[]
    with open(a.corpus,encoding="utf-8") as f:
      for line in f:
        if not line.strip(): continue
        case=json.loads(line); expected=case["expected_verdict"]
        r7=v7.evaluate(case["prompt_text"]); r11=v11.evaluate(case["prompt_text"],case.get("sources"))
        rows.append({"case_id":case["case_id"],"domain":case.get("domain","UNSPECIFIED"),"expected":expected,"v7":r7["verdict"],"v7_rule":r7["decision_rule"],"v11":r11["verdict"],"v11_rule":r11["decision_rule"],"v7_correct":r7["verdict"]==expected,"v11_correct":r11["verdict"]==expected,"v11_audit_sha256":r11["audit_sha256"]})
    def summary(key):
      n=len(rows); c=sum(x[key] for x in rows); return {"correct":c,"total":n,"accuracy":c/n if n else None}
    out={"scope":"evaluator-controlled only if corpus custody is external","corpus_sha256":sha(a.corpus),"v7_sha256":sha(a.v7),"v11_sha256":sha(ROOT/"daxda_engine_v11.py"),"v7":summary("v7_correct"),"v11":summary("v11_correct"),"rows":rows}
    pathlib.Path(a.out).write_text(json.dumps(out,indent=2),encoding="utf-8"); print(json.dumps({k:v for k,v in out.items() if k!="rows"},indent=2))
if __name__=="__main__": main()

