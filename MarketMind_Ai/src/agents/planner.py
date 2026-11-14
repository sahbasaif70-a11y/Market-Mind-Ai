import json
import re
from typing import List, Dict, Any, Optional
from src.llm.client import LLMClient
from src.schemas.plan import ResearchPlan, SubQuestion, RequestAnalysis, QuestionStatus

PLANNER_SYSTEM_PROMPT = """You are the Senior Research Planner for MarketMind AI.
Your job is to parse market research prompts and extract a structured research plan.

CRITICAL PARSING RULES:
1. 'topic': Extract ONLY the core market/product category as a clean noun phrase (e.g., "Digital Payment Gateway Software", "E-Commerce Retention Marketing Software", "AI Customer Support Software"). NEVER include prompt instructions, verbs, dots, or competitor names in 'topic'!
2. 'competitors': Extract ALL specific company, brand, or product names explicitly mentioned in the query (e.g. ["Stripe", "Braintree", "Adyen"], ["Klaviyo", "Omnisend"], ["Zendesk AI", "Intercom Fin AI"]).
3. 'criteria': Extract ALL comparison criteria explicitly or implicitly requested (e.g. ["pricing models", "transaction fees", "key features"], ["pricing plans", "free plan limits", "SMS automation features", "target audience"]).
4. NEVER invent fake brand names or merge competitor names or sentences into the topic!

Respond ONLY in valid JSON matching this schema:
{
  "analysis": {
    "topic": "Digital Payment Gateway Software",
    "competitors": ["Stripe", "Braintree", "Adyen"],
    "criteria": ["pricing models", "transaction fees", "key features"],
    "geographic_scope": "Global",
    "time_sensitive": true,
    "industry_segment": "Digital Payment Gateway Software",
    "clarified_objective": "Research and compare Stripe, Braintree, and Adyen on pricing models, transaction fees, and key features."
  },
  "sub_questions": [
    {
      "id": "SQ1",
      "question": "What are Stripe's pricing models, transaction fees, and pricing tiers?",
      "target_entity": "Stripe",
      "target_metric": "pricing models",
      "status": "open"
    },
    {
      "id": "SQ2",
      "question": "What are Stripe's domestic and international card processing transaction fees?",
      "target_entity": "Stripe",
      "target_metric": "transaction fees",
      "status": "open"
    },
    {
      "id": "SQ3",
      "question": "What are Stripe's key payment features and integration capabilities?",
      "target_entity": "Stripe",
      "target_metric": "key features",
      "status": "open"
    },
    {
      "id": "SQ4",
      "question": "What are Braintree's pricing models, transaction fees, and pricing tiers?",
      "target_entity": "Braintree",
      "target_metric": "pricing models",
      "status": "open"
    },
    {
      "id": "SQ5",
      "question": "What are Braintree's domestic and international card processing transaction fees?",
      "target_entity": "Braintree",
      "target_metric": "transaction fees",
      "status": "open"
    },
    {
      "id": "SQ6",
      "question": "What are Braintree's key payment features and integration capabilities?",
      "target_entity": "Braintree",
      "target_metric": "key features",
      "status": "open"
    },
    {
      "id": "SQ7",
      "question": "What are Adyen's pricing models, transaction fees, and pricing tiers?",
      "target_entity": "Adyen",
      "target_metric": "pricing models",
      "status": "open"
    },
    {
      "id": "SQ8",
      "question": "What are Adyen's domestic and international card processing transaction fees?",
      "target_entity": "Adyen",
      "target_metric": "transaction fees",
      "status": "open"
    },
    {
      "id": "SQ9",
      "question": "What are Adyen's key payment features and integration capabilities?",
      "target_entity": "Adyen",
      "target_metric": "key features",
      "status": "open"
    }
  ],
  "estimated_iterations": 9
}
"""

STOP_VERBS = {"research", "compare", "analyze", "identify", "calculate", "evaluate", "global", "digital", "payment", "gateway", "market", "software", "platform", "tool", "tools", "features", "pricing", "fees"}

KNOWN_BRANDS = [
    "GitHub Copilot", "Copilot", "Cursor AI", "Cursor", "Claude Code", "Claude",
    "ChatGPT", "Gemini", "Perplexity", "Stripe", "Braintree", "Adyen",
    "Klaviyo", "Omnisend", "Zendesk", "Intercom", "Gorgias", "Freshworks"
]

def clean_topic_phrase(text: str) -> str:
    """Sanitize raw prompt string to produce a clean, concise market topic phrase."""
    if not text:
        return "Market Analysis"

    text_lower = text.lower()
    if "payment" in text_lower or "gateway" in text_lower or "stripe" in text_lower or "braintree" in text_lower or "adyen" in text_lower:
        return "Digital Payment Gateway Software"
    if "retention" in text_lower or "klaviyo" in text_lower or "omnisend" in text_lower:
        return "E-Commerce Retention Marketing Software"
    if "support" in text_lower or "chat" in text_lower or "zendesk" in text_lower or "intercom" in text_lower:
        return "AI Customer Support Software"
    if "code" in text_lower or "copilot" in text_lower or "cursor" in text_lower or "claude" in text_lower:
        return "AI Code Assistant Software"
    if "skincare" in text_lower or "grooming" in text_lower:
        return "Organic Men's Skincare & Grooming"

    clean = text.replace('\n', ' ').strip().strip('.').strip('?').strip('"').strip("'")
    if '.' in clean:
        clean = clean.split('.')[0].strip()

    clean = re.sub(r'^(research|compare|analyze|identify|find|calculate|get|show|what are|how to)\s+(the\s+)?', '', clean, flags=re.IGNORECASE)

    if ',' in clean and ("pricing" in clean.lower() or "compare" in clean.lower()):
        clean = clean.split(',')[0].strip()

    clean = re.sub(r'^(global\s+)?(digital\s+)?', '', clean, flags=re.IGNORECASE)
    clean = re.sub(r'\s+market$', '', clean, flags=re.IGNORECASE)
    clean = clean.strip()

    if not clean or len(clean) < 3 or len(clean) > 50:
        return "Market Analysis"

    return clean.title()

def validate_competitors(competitors: List[str], user_request: str) -> List[str]:
    """Ensure every extracted competitor actually exists in the user request and is not an action verb."""
    validated = []
    req_lower = user_request.lower()

    # First check LLM suggested competitors
    if competitors:
        for comp in competitors:
            comp_clean = comp.strip().strip('.').strip(',').strip('?')
            if not comp_clean or comp_clean.lower() in STOP_VERBS:
                continue
            comp_first_word = comp_clean.split()[0].lower()
            if comp_first_word in STOP_VERBS:
                continue
            if comp_clean.lower() in req_lower or comp_first_word in req_lower:
                if comp_clean not in validated:
                    validated.append(comp_clean)

    # Check known brands in user prompt
    for brand in KNOWN_BRANDS:
        if brand.lower() in req_lower:
            if not any(brand.lower() in v.lower() or v.lower() in brand.lower() for v in validated):
                validated.append(brand)

    return validated

def extract_entities_from_text(prompt: str) -> List[str]:
    """Legacy helper to extract requested entities/companies from user prompt."""
    potential_comps = re.findall(r'\b[A-Z][a-zA-B0-9]+\b', prompt)
    valid = validate_competitors(potential_comps, prompt)
    if valid:
        return valid

    # Regex fallback for company names
    words = re.findall(r'\b[A-[#0-9a-zA-Z_-]+\b', prompt)
    return [w for w in ["ChatGPT", "Gemini", "Claude", "Copilot", "Perplexity", "Zendesk", "Intercom"] if w.lower() in prompt.lower()]

def extract_criteria_fallback(user_request: str) -> List[str]:
    """Extract requested comparison criteria deterministically if LLM misses them."""
    criteria = []
    req_lower = user_request.lower()

    standard_metrics = [
        ("pricing models", ["pricing models", "pricing", "pricing plans", "price", "cost"]),
        ("transaction fees", ["transaction fees", "processing fees", "card fees", "fees"]),
        ("free plan limits", ["free plan", "free tier", "freemium", "trial", "free limits"]),
        ("SMS automation features", ["sms", "text messaging", "sms automation"]),
        ("key features", ["features", "capabilities", "functionality"]),
        ("target audience", ["target audience", "ideal customer", "users", "audience"]),
        ("limitations", ["limitations", "limits", "drawbacks", "cons"])
    ]

    for metric_name, keywords in standard_metrics:
        if any(kw in req_lower for kw in keywords):
            if metric_name not in criteria:
                criteria.append(metric_name)

    if not criteria:
        criteria = ["pricing models", "key features", "limitations"]

    return criteria

class ResearchPlanner:
    """Agent responsible for analyzing user request and creating a ResearchPlan."""

    def __init__(self, llm_client: LLMClient):
        self.client = llm_client

    def create_plan(self, user_request: str) -> ResearchPlan:
        """Analyze user request and return structured ResearchPlan object."""
        messages = [
            {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
            {"role": "user", "content": f"Parse and create a structured research plan for this query:\n'{user_request}'"}
        ]

        try:
            response_msg = self.client.generate(messages=messages, temperature=0.1)
            content = response_msg.content.strip()

            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            plan_dict = json.loads(content)
            analysis_dict = plan_dict.get("analysis", {})

            # Deterministic validations
            topic = clean_topic_phrase(analysis_dict.get("topic") or user_request)
            raw_comps = analysis_dict.get("competitors", [])
            valid_comps = validate_competitors(raw_comps, user_request)

            raw_criteria = analysis_dict.get("criteria", [])
            if not raw_criteria:
                raw_criteria = extract_criteria_fallback(user_request)

            # Build sanitized Analysis object
            analysis = RequestAnalysis(
                topic=topic,
                competitors=valid_comps,
                criteria=raw_criteria,
                geographic_scope=analysis_dict.get("geographic_scope", "Global"),
                time_sensitive=analysis_dict.get("time_sensitive", True),
                industry_segment=topic,
                clarified_objective=f"Research and analyze {topic}" + (f" comparing {', '.join(valid_comps)}" if valid_comps else "")
            )

            # Ensure subquestions cover every competitor and criterion
            sub_qs = []
            sq_id_counter = 1

            if valid_comps:
                for comp in valid_comps:
                    for crit in raw_criteria:
                        sub_qs.append(
                            SubQuestion(
                                id=f"SQ{sq_id_counter}",
                                question=f"What are {comp}'s {crit}?",
                                target_entity=comp,
                                target_metric=crit,
                                status=QuestionStatus.OPEN
                            )
                        )
                        sq_id_counter += 1
            else:
                for crit in raw_criteria:
                    sub_qs.append(
                        SubQuestion(
                            id=f"SQ{sq_id_counter}",
                            question=f"What are the {crit} for {topic}?",
                            target_entity=topic,
                            target_metric=crit,
                            status=QuestionStatus.OPEN
                        )
                    )
                    sq_id_counter += 1

            return ResearchPlan(
                analysis=analysis,
                sub_questions=sub_qs,
                estimated_iterations=len(sub_qs) + 1
            )
        except Exception:
            # Deterministic Fallback Plan
            topic = clean_topic_phrase(user_request)
            criteria = extract_criteria_fallback(user_request)

            # Extract potential brand names using regex
            potential_comps = re.findall(r'\b[A-Z][a-zA-B0-9]+\b', user_request)
            valid_comps = validate_competitors(potential_comps, user_request)

            sub_qs = []
            sq_counter = 1

            if valid_comps:
                for comp in valid_comps:
                    for crit in criteria:
                        sub_qs.append(
                            SubQuestion(
                                id=f"SQ{sq_counter}",
                                question=f"What are {comp}'s {crit}?",
                                target_entity=comp,
                                target_metric=crit,
                                status=QuestionStatus.OPEN
                            )
                        )
                        sq_counter += 1
            else:
                for crit in criteria:
                    sub_qs.append(
                        SubQuestion(
                            id=f"SQ{sq_counter}",
                            question=f"What are the {crit} for {topic}?",
                            target_entity=topic,
                            target_metric=crit,
                            status=QuestionStatus.OPEN
                        )
                    )
                    sq_counter += 1

            analysis = RequestAnalysis(
                topic=topic,
                competitors=valid_comps,
                criteria=criteria,
                geographic_scope="Global",
                time_sensitive=True,
                industry_segment=topic,
                clarified_objective=f"Research and analyze {topic}"
            )

            return ResearchPlan(
                analysis=analysis,
                sub_questions=sub_qs,
                estimated_iterations=len(sub_qs) + 1
            )
