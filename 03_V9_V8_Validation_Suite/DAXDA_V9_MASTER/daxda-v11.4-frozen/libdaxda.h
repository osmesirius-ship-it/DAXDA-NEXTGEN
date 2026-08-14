/*
 * DAXDA Guard C ABI Enterprise Header (libdaxda.h)
 * Native C ABI exports for Go, C#, C++, and Node.js enterprise microservices.
 */

#ifndef LIBDAXDA_H
#define LIBDAXDA_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define DAXDA_DIM 128

typedef struct {
    double coeffs[DAXDA_DIM];
} daxda_mv_t;

typedef struct {
    int verdict_code;           // 0: PASS, 1: CAUTION, 2: SEVERE_BLOCK, 3: FAIL_CLOSED
    double reconstruction_loss; // Residual epsilon
    double grade0_scalar;       // Baseline scalar s
    double calibrated_certainty; // C(s)
    char authority_sha256[65];  // Cryptographic receipt hash
} daxda_receipt_t;

// Core C ABI Functions
void daxda_init_core(void);
void daxda_multivector_init(daxda_mv_t* mv);
void daxda_multivector_set_scalar(daxda_mv_t* mv, double s);
void daxda_multivector_multiply(const daxda_mv_t* a, const daxda_mv_t* b, daxda_mv_t* out);
void daxda_multivector_revert(const daxda_mv_t* in, daxda_mv_t* out);
double daxda_multivector_norm2(const daxda_mv_t* in);
int daxda_blade_mul_lookup(int a, int b, double* out_sign);

void daxda_evaluate_governance(
    const char* domain,
    const char* input_text,
    const daxda_mv_t* mv,
    daxda_receipt_t* receipt
);

#ifdef __cplusplus
}
#endif

#endif // LIBDAXDA_H
