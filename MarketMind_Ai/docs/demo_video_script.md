# MarketMind AI — Demo Video Script & Outline (8–12 Minutes)

## Timeline & Scene Outline

1. **0:00 - 1:30 | Introduction & Problem Statement**
   - Introduce MarketMind AI as an autonomous, evidence-grounded research agent.
   - Explain why ground truth, evidence validation, and provenance matter over plain LLM guessing.

2. **1:30 - 3:30 | Architecture & Tool Dispatcher Overview**
   - Show the Architecture Diagram.
   - Explain the trust boundaries: Model -> Code (Tool Dispatcher) & Search Results -> Prompt (Source Validator).

3. **3:30 - 6:00 | Live Agent Loop & Real-Time Research Run**
   - Submit prompt: *"Research the e-commerce retention marketing software market. Compare Klaviyo and Omnisend on pricing plans, free plan limits, SMS automation features, and target audience."*
   - Show live search calls, evidence saving, and cost tracking.

4. **6:00 - 8:30 | Report Inspection, Provenance & Quality Audit**
   - Inspect the generated report, competitor matrix, and Source Provenance Table.
   - Show the 10-check Quality Audit breakdown.

5. **8:30 - 10:30 | Human Approval Gate & Deliverables**
   - Demonstrate the Human Approval Gate choices (Approve, Reject, Revision, Export).
   - Show saved run artifacts in `runs/<run_id>.json`.

6. **10:30 - 12:00 | Conclusion & Evaluation Results**
   - Review pass rates on the 18 automated regression test cases.
