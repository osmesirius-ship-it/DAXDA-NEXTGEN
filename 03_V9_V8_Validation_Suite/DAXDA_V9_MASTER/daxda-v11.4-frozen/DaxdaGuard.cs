/*
 * DAXDA Guard C# / .NET Binding (DaxdaGuard.cs)
 * P/Invoke interop wrapper connecting .NET enterprise microservices to libdaxda_core.so.
 */

using System;
using System.Runtime.InteropServices;
using System.Text;

namespace Daxda.Guard
{
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]
    public struct DaxdaReceiptNative
    {
        public int VerdictCode;
        public double ReconstructionLoss;
        public double Grade0Scalar;
        public double CalibratedCertainty;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 65)]
        public string AuthoritySha256;
    }

    public class GovernanceReceipt
    {
        public string Verdict { get; set; }
        public string DecisionRule { get; set; }
        public double ReconstructionLoss { get; set; }
        public double Grade0Scalar { get; set; }
        public double CalibratedCertainty { get; set; }
        public string AuthoritySha256 { get; set; }
        public bool PublicationPermitted { get; set; }
    }

    public static class DaxdaGuardEngine
    {
        private const string DllName = "daxda_core";

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl)]
        public static extern void daxda_init_core();

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void daxda_evaluate_governance(
            string domain,
            string inputText,
            IntPtr mv,
            out DaxdaReceiptNative receipt
        );

        static DaxdaGuardEngine()
        {
            try
            {
                daxda_init_core();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"DAXDA Guard C# Engine Init Warning: {ex.Message}");
            }
        }

        public static GovernanceReceipt Evaluate(string domain, string inputText)
        {
            daxda_evaluate_governance(domain, inputText, IntPtr.Zero, out DaxdaReceiptNative nativeReceipt);

            string verdict = nativeReceipt.VerdictCode == 0 ? "PASS" : "FAIL_CLOSED";
            bool pubPermitted = nativeReceipt.VerdictCode == 0;

            return new GovernanceReceipt
            {
                Verdict = verdict,
                DecisionRule = pubPermitted ? "WITHIN_GOVERNANCE_TOLERANCE" : "GOV_FAIL_05",
                ReconstructionLoss = nativeReceipt.ReconstructionLoss,
                Grade0Scalar = nativeReceipt.Grade0Scalar,
                CalibratedCertainty = nativeReceipt.CalibratedCertainty,
                AuthoritySha256 = nativeReceipt.AuthoritySha256,
                PublicationPermitted = pubPermitted
            };
        }
    }
}
