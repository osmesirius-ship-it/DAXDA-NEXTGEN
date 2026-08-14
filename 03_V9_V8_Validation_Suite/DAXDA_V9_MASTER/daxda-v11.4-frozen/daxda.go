/*
 * DAXDA Guard Go Binding (daxda.go)
 * cgo wrapper connecting Go enterprise microservices to libdaxda_core.so.
 */

package daxda

/*
#cgo LDFLAGS: -L. -ldaxda_core
#include "libdaxda.h"
#include <stdlib.h>
*/
import "C"
import (
	"unsafe"
)

type GovernanceReceipt struct {
	Verdict             string  `json:"verdict"`
	DecisionRule        string  `json:"decision_rule"`
	ReconstructionLoss float64 `json:"reconstruction_loss"`
	Grade0Scalar        float64 `json:"grade0_scalar"`
	CalibratedCertainty float64 `json:"calibrated_certainty"`
	AuthoritySHA256     string  `json:"authority_sha256"`
	PublicationPermitted bool   `json:"publication_permitted"`
}

func InitCore() {
	C.daxda_init_core()
}

func EvaluateGovernance(domain string, inputText string) GovernanceReceipt {
	cDomain := C.CString(domain)
	cInput := C.CString(inputText)
	defer C.free(unsafe.Pointer(cDomain))
	defer C.free(unsafe.Pointer(cInput))

	var receipt C.daxda_receipt_t
	C.daxda_evaluate_governance(cDomain, cInput, nil, &receipt)

	vCode := int(receipt.verdict_code)
	verdictMap := map[int]string{0: "PASS", 1: "CAUTION", 2: "SEVERE_BLOCK", 3: "FAIL_CLOSED"}
	verdictStr := verdictMap[vCode]
	if verdictStr == "" {
		verdictStr = "UNKNOWN"
	}

	pubPermitted := (vCode == 0)
	sha := C.GoString(&receipt.authority_sha256[0])

	return GovernanceReceipt{
		Verdict:             verdictStr,
		DecisionRule:        "WITHIN_GOVERNANCE_TOLERANCE",
		ReconstructionLoss: float64(receipt.reconstruction_loss),
		Grade0Scalar:        float64(receipt.grade0_scalar),
		CalibratedCertainty: float64(receipt.calibrated_certainty),
		AuthoritySHA256:     sha,
		PublicationPermitted: pubPermitted,
	}
}
