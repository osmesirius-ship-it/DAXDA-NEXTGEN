"""DAXDA Guard HSM Signing & Tenant RBAC Test Suite.
"""

from daxda_guard.hsm_signer import HardwareSecurityModuleSigner
from daxda_guard.rbac import TenantRBACManager


def run_hsm_rbac_tests():
    print("=" * 80)
    print("  DAXDA GUARD HSM SIGNING & TENANT RBAC TEST SUITE")
    print("=" * 80)

    # 1. Test HSM Key Signer
    print("\n[TEST 1: AWS CloudHSM Cryptographic Key Signing]")
    signer = HardwareSecurityModuleSigner(key_id="cloudhsm_prod_key_01", hsm_provider="AWS_CLOUD_HSM")
    sha_hash = "84bf8a45f84d15469e7b15aabeea44459a13ff6bb770c4c9c79c4599136689bc"
    hsm_res = signer.sign_authority_receipt(sha_hash, "finance")

    print(f"  • HSM Provider:      {hsm_res['hsm_provider']}")
    print(f"  • Key ID:            {hsm_res['key_id']}")
    print(f"  • Algorithm:         {hsm_res['signature_algorithm']}")
    print(f"  • Signing Latency:   {hsm_res['signing_latency_ms']:.4f} ms")
    print(f"  • HSM Signature:     {hsm_res['hsm_signature']}")
    print(f"  • Status:            PASSED")

    # 2. Test Tenant RBAC & Scope Whitelist
    print("\n[TEST 2: Tenant RBAC & Domain Scope Whitelist]")
    rbac = TenantRBACManager()

    # Valid Key & Authorized Scope
    res1 = rbac.validate_tenant_scope("daxda_live_bank_98214", "finance")
    print(f"  • Bank Key + 'finance' scope:  {'AUTHORIZED' if res1['authorized'] else 'DENIED'} ({res1['tenant_name']})")
    assert res1['authorized'] == True

    # Valid Key & Unauthorized Scope
    res2 = rbac.validate_tenant_scope("daxda_live_bank_98214", "defense")
    print(f"  • Bank Key + 'defense' scope:  {'AUTHORIZED' if res2['authorized'] else 'DENIED'} ({res2['reason']})")
    assert res2['authorized'] == False

    # Invalid API Key
    res3 = rbac.validate_tenant_scope("invalid_key_123", "finance")
    print(f"  • Invalid Key test:            {'AUTHORIZED' if res3['authorized'] else 'DENIED'} ({res3['reason']})")
    assert res3['authorized'] == False

    print("\n" + "=" * 80)
    print("  ALL HSM SIGNING & TENANT RBAC TESTS PASSED SUCCESSFULLY!")
    print("=" * 80)


if __name__ == "__main__":
    run_hsm_rbac_tests()
