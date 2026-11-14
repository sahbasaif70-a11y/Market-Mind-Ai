from enum import Enum
from src.schemas.report import MarketReport
from src.agents.report_generator import ReportGenerator

class ApprovalDecision(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    RETURN_FOR_REVISION = "return_for_revision"
    EXPORT = "export"

class HumanApprovalGate:
    """CLI Gate requiring explicit human review before publishing final research report."""

    @staticmethod
    def review_report(report: MarketReport, interactive: bool = True) -> ApprovalDecision:
        """Display report summary and prompt human reviewer for approval decision."""
        print("\n" + "="*60)
        print("          HUMAN APPROVAL GATE - REPORT REVIEW")
        print("="*60)
        
        md_content = ReportGenerator.render_markdown(report)
        print("\n" + md_content + "\n")
        print("="*60)

        if not interactive:
            print("[Auto-Approval Mode]: Explicit non-interactive flag set.")
            return ApprovalDecision.APPROVE

        while True:
            print("\nPlease select an approval action:")
            print(" [1] APPROVE - Publish report and save final outputs.")
            print(" [2] REJECT - Reject report.")
            print(" [3] REVISION - Return for further research.")
            print(" [4] EXPORT - Export state log and pause.")

            try:
                choice = input("\nEnter choice (1-4): ").strip()
                if choice == "1":
                    return ApprovalDecision.APPROVE
                elif choice == "2":
                    return ApprovalDecision.REJECT
                elif choice == "3":
                    return ApprovalDecision.RETURN_FOR_REVISION
                elif choice == "4":
                    return ApprovalDecision.EXPORT
                else:
                    print("[🔴] Invalid choice. Please enter 1, 2, 3, or 4.")
            except Exception:
                return ApprovalDecision.RETURN_FOR_REVISION
