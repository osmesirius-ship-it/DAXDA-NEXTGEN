/*
 * DAXDA Guard Core C++ Engine - Header (daxda_core.h)
 * Cl(7,0) 128-Blade Multivector Algebra & Synchronous Authority Gate
 * High-performance, zero-dependency C++ shared library for DAXDA Guard.
 */

#ifndef DAXDA_CORE_H
#define DAXDA_CORE_H

#include <vector>
#include <string>
#include <array>
#include <cmath>
#include <chrono>

#ifdef __cplusplus
extern "C" {
#endif

// Constants for Cl(7,0)
#define DAXDA_CL70_DIM 128
#define DAXDA_CL70_P 7
#define DAXDA_CL70_Q 0

typedef struct {
    double coeffs[DAXDA_CL70_DIM];
} daxda_multivector_t;

typedef struct {
    int verdict_code;           // 0: PASS, 1: CAUTION, 2: SEVERE_BLOCK, 3: FAIL_CLOSED
    double reconstruction_loss; // Residual epsilon
    double grade0_scalar;       // Baseline scalar s
    double calibrated_certainty; // C(s)
    char authority_sha256[65];  // Cryptographic receipt hash
} daxda_governance_receipt_t;

// C API Exports
void daxda_init_core();
void daxda_multivector_init(daxda_multivector_t* mv);
void daxda_multivector_set_scalar(daxda_multivector_t* mv, double s);
void daxda_multivector_multiply(const daxda_multivector_t* a, const daxda_multivector_t* b, daxda_multivector_t* out);
void daxda_multivector_revert(const daxda_multivector_t* in, daxda_multivector_t* out);
double daxda_multivector_norm2(const daxda_multivector_t* in);
void daxda_multivector_normalize(daxda_multivector_t* mv);

// Single blade multiplication lookup (< 50ns)
int daxda_blade_mul_lookup(int a, int b, double* out_sign);
double daxda_benchmark_blade_lookup(int iterations);

// Governance evaluation API (< 2.0ms)
void daxda_evaluate_governance(
    const char* domain,
    const char* input_text,
    const daxda_multivector_t* mv,
    daxda_governance_receipt_t* receipt
);

#ifdef __cplusplus
}
#endif

#endif // DAXDA_CORE_H
