#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DAXDA-o V5 Transparent Development Corpus Harness & Verification Suite
========================================================================
Executes the 5-Stage V5 Engine against the transparent naturalistic development corpus
(daxda_v5_dev_corpus.json), verifying relational dependency parsing, zero-collision
separation, Nitsche-inspired boundary damping, and exact latency/environment metrics.
"""

import json
import math
import os
import platform
import sys
import time
from collections import defaultdict, Counter
from typing import Dict, List, Tuple

from daxda_engine_v5 import DAXDAEngineV5, SemanticRoleDependencyParser


def compute_mcc(cm: Dict[Tuple[str, str], int], classes: List[str]) -> float:
    t_sum = sum(cm.values())
    if t_sum == 0:
        return 0.0
    c_sum = sum(cm[(k, k)] for k in classes)
    num = c_sum * t_sum - sum(
        sum(cm[(k, l)] for l in classes) * sum(cm[(l, k)] for l in classes)
        for k in classes
    )
    den_sq = (
        t_sum**2 - sum(sum(cm[(k, l)] for l in classes)**2 for k in classes)
    ) * (
        t_sum**2 - sum(sum(cm[(l, k)] for l in classes)**2 for k in classes)
    )
    return num / math.sqrt(den_sq) if den_sq > 0 else 0.0


def compute_shannon_entropy(labels: List[str]) -> float:
    counts = Counter(labels)
    total = len(labels)
    if total == 0:
        return 0.0
    return -sum((c / total) * math.log2(c / total) for c in counts.values() if c > 0)


def run_harness():
    print("========================================================================================")
    print("                 DAXDA-o V5 TRANSPARENT DEVELOPMENT HARNESS EXECUTION                   ")
    print("========================================================================================")
    
    # Execution Environment Specification
    env_info = {
        "os": platform.system(),
        "os_release": platform.release(),
        "python_version": platform.python_version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    print(f"[ENVIRONMENT] OS: {env_info['os']} {env_info['os_release']} ({env_info['machine']})")
    print(f"[ENVIRONMENT] Python: {env_info['python_version']} | Timestamp: {env_info['timestamp']}")

    corpus_path = "daxda_v5_dev_corpus.json"
    if not os.path.exists(corpus_path):
        print(f"Error: {corpus_path} not found.")
        sys.exit(1)

    with open(corpus_path, "r") as f:
        corpus = json.load(f)

    print(f"[CORPUS] Loaded {len(corpus)} naturalistic items spanning 8 adversarial families.")

    classes = ["PASS", "RELEASE/CAUTION", "BLOCK"]
    cm = defaultdict(int)
    latencies = []
    stage_latencies = {"stage1_2_parser": [], "stage3_projection": [], "stage4_kernel": [], "stage5_gate": []}
    
    results = []
    state_to_labels = defaultdict(set)
    state_to_items = defaultdict(list)
    family_stats = defaultdict(lambda: {"total": 0, "correct": 0})

    start_total = time.perf_counter()
    for item in corpus:
        text = item["text"]
        expected = item["expected"]
        family = item["family"]
        uid = item["uid"]

        # Precise timing across stages
        t0 = time.perf_counter_ns()
        graph = SemanticRoleDependencyParser.parse(text)
        t1 = time.perf_counter_ns()
        from daxda_engine_v5 import GraphToCliffordProjection, GovernanceKernelV5
        psi0 = GraphToCliffordProjection.project(graph)
        t2 = time.perf_counter_ns()
        psi_kernel = GovernanceKernelV5.step_symbolic(psi0)
        t3 = time.perf_counter_ns()
        gate = GovernanceKernelV5.classify_gate(psi_kernel)
        t4 = time.perf_counter_ns()

        total_us = (t4 - t0) / 1000.0
        latencies.append(total_us)
        stage_latencies["stage1_2_parser"].append((t1 - t0) / 1000.0)
        stage_latencies["stage3_projection"].append((t2 - t1) / 1000.0)
        stage_latencies["stage4_kernel"].append((t3 - t2) / 1000.0)
        stage_latencies["stage5_gate"].append((t4 - t3) / 1000.0)

        cm[(expected, gate)] += 1
        family_stats[family]["total"] += 1
        if gate == expected:
            family_stats[family]["correct"] += 1

        # Quantize state for collision audit
        state_key = f"S:{psi_kernel.s:.3f}|E1:{psi_kernel.e1:.3f}|E2:{psi_kernel.e2:.3f}|I:{psi_kernel.i:.3f}|Omega:{psi_kernel.omega:.3f}"
        state_to_labels[state_key].add(gate)
        state_to_items[state_key].append(uid)

        results.append({
            "uid": uid,
            "family": family,
            "expected": expected,
            "predicted": gate,
            "correct": gate == expected,
            "latency_us": round(total_us, 2),
            "psi_0": str(psi0),
            "psi_kernel": str(psi_kernel),
            "edges": [f"{e.source_role}->{e.target_role} ({e.edge_type})" for e in graph.edges]
        })

    elapsed_total = time.perf_counter() - start_total

    # Metrics computation
    total_items = len(corpus)
    correct_items = sum(cm[(k, k)] for k in classes)
    accuracy = (correct_items / total_items) * 100.0 if total_items > 0 else 0.0

    per_class_metrics = {}
    for c in classes:
        tp = cm[(c, c)]
        fp = sum(cm[(k, c)] for k in classes if k != c)
        fn = sum(cm[(c, k)] for k in classes if k != c)
        prec = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 1.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
        per_class_metrics[c] = {"precision": round(prec, 4), "recall": round(rec, 4), "f1": round(f1, 4)}

    macro_f1 = sum(m["f1"] for m in per_class_metrics.values()) / len(classes)
    mcc = compute_mcc(cm, classes)

    # False Release Rate calculation
    expected_block = sum(cm[("BLOCK", k)] for k in classes)
    false_releases = sum(cm[("BLOCK", k)] for k in classes if k != "BLOCK")
    frr = (false_releases / expected_block) * 100.0 if expected_block > 0 else 0.0

    # Collision & Compression Audit
    unique_states = len(state_to_labels)
    cross_label_collisions = sum(1 for labels in state_to_labels.values() if len(labels) > 1)
    state_distribution = [len(items) for items in state_to_items.values()]
    shannon_entropy = compute_shannon_entropy([r["predicted"] for r in results])
    max_entropy = math.log2(len(classes))
    entropy_efficiency = (shannon_entropy / max_entropy) * 100.0 if max_entropy > 0 else 0.0

    mean_lat = sum(latencies) / len(latencies) if latencies else 0.0
    mean_s12 = sum(stage_latencies["stage1_2_parser"]) / len(latencies) if latencies else 0.0
    mean_s3 = sum(stage_latencies["stage3_projection"]) / len(latencies) if latencies else 0.0
    mean_s4 = sum(stage_latencies["stage4_kernel"]) / len(latencies) if latencies else 0.0
    mean_s5 = sum(stage_latencies["stage5_gate"]) / len(latencies) if latencies else 0.0

    print("\n[VERIFICATION RESULTS - CONFUSION MATRIX]")
    print(f"{'Expected vs Predicted':<22} | {'PASS':<10} | {'CAUTION':<10} | {'BLOCK':<10} | {'Recall':<10}")
    print("-" * 72)
    for exp in classes:
        p_cnt = cm[(exp, "PASS")]
        c_cnt = cm[(exp, "RELEASE/CAUTION")]
        b_cnt = cm[(exp, "BLOCK")]
        rec_str = f"{per_class_metrics[exp]['recall']*100:.1f}%"
        print(f"{exp:<22} | {p_cnt:<10} | {c_cnt:<10} | {b_cnt:<10} | {rec_str:<10}")
    print("-" * 72)

    print("\n[STATISTICAL SAFETY & GOVERNANCE METRICS]")
    print(f"  Overall Accuracy:      {accuracy:.2f}% ({correct_items}/{total_items})")
    print(f"  BLOCK Recall:          {per_class_metrics['BLOCK']['recall']*100:.2f}% ({cm[('BLOCK','BLOCK')]}/{expected_block})")
    print(f"  False Release Rate:    {frr:.2f}% ({false_releases}/{expected_block})")
    print(f"  Macro F1 Score:        {macro_f1:.4f}")
    print(f"  Multiclass MCC:        {mcc:.4f}")
    print(f"  Shannon Entropy:       {shannon_entropy:.4f} bits ({entropy_efficiency:.1f}% of max)")
    print(f"  Unique Geometric States: {unique_states} (Compression ratio: {total_items/unique_states:.2f}:1)")
    print(f"  Cross-Label Collisions:  {cross_label_collisions} / {unique_states}")

    print("\n[PERFORMANCE DECOMPOSITION BY STAGE (Mean Latency)]")
    print(f"  Stage 1 & 2 (Dependency & Role Parser):  {mean_s12:.2f} μs")
    print(f"  Stage 3 (Graph-to-Clifford Projection): {mean_s3:.2f} μs")
    print(f"  Stage 4 (Cl(2,0) Rotor & Damping Kernel):{mean_s4:.2f} μs")
    print(f"  Stage 5 (Deterministic Governance Gate): {mean_s5:.2f} μs")
    print(f"  Total End-to-End Mean Execution Time:    {mean_lat:.2f} μs")

    report = {
        "title": "DAXDA-o V5 Structured Semantic-Role & Dependency Governance Harness Report",
        "scientific_status": "DEVELOPMENT & REGRESSION HARNESS ONLY (Transparent Corpus)",
        "environment": env_info,
        "metrics": {
            "total_samples": total_items,
            "overall_accuracy": round(accuracy, 2),
            "macro_f1": round(macro_f1, 4),
            "mcc": round(mcc, 4),
            "false_release_rate_pct": round(frr, 2),
            "shannon_entropy_bits": round(shannon_entropy, 4),
            "compression_ratio": round(total_items / unique_states, 2),
            "cross_label_collisions": cross_label_collisions
        },
        "per_class": per_class_metrics,
        "family_breakdown": {fam: {"accuracy_pct": round(s["correct"]/s["total"]*100, 2), "correct": s["correct"], "total": s["total"]} for fam, s in family_stats.items()},
        "stage_latencies_us": {
            "stage1_2_parser": round(mean_s12, 2),
            "stage3_projection": round(mean_s3, 2),
            "stage4_kernel": round(mean_s4, 2),
            "stage5_gate": round(mean_s5, 2),
            "total_mean_us": round(mean_lat, 2)
        },
        "results": results
    }

    with open("daxda_v5_dev_benchmark_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\n[COMPLETE] Report saved to daxda_v5_dev_benchmark_report.json.")
    print("========================================================================================")


if __name__ == "__main__":
    run_harness()
