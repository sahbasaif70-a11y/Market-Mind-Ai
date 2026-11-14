import re
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse

# Domains that must be rejected for specific software/fintech B2B research claims
IRRELEVANT_DOMAINS = {
    "wikipedia.org", "en.wikipedia.org", "youtube.com", "m.youtube.com",
    "imdb.com", "zhihu.com", "hamariweb.com", "quran.com", "surah.pk",
    "tiktok.com", "facebook.com", "instagram.com", "reddit.com/r/funny",
    "pinterest.com", "quora.com", "manhattan-tourism.com"
}

# Official company domain mappings for targeted domain verification
OFFICIAL_DOMAINS = {
    "stripe": ["stripe.com"],
    "braintree": ["braintreepayments.com", "paypal.com"],
    "adyen": ["adyen.com"],
    "klaviyo": ["klaviyo.com", "help.klaviyo.com"],
    "omnisend": ["omnisend.com", "support.omnisend.com"],
    "zendesk": ["zendesk.com", "support.zendesk.com"],
    "intercom": ["intercom.com"],
    "github": ["github.com", "copilot.github.com"],
    "cursor": ["cursor.com", "cursor.sh"],
    "replit": ["replit.com"],
    "pinecone": ["pinecone.io"],
    "qdrant": ["qdrant.tech"],
    "weaviate": ["weaviate.io"]
}

class SourceValidator:
    """Evaluates web search results and local documents for entity, domain, topic, and criterion relevance."""

    @staticmethod
    def validate_source(
        target_entity: str,
        criterion: str,
        source_url: str,
        title: str,
        snippet: str,
        source_type: str = "live_web"
    ) -> Dict[str, Any]:
        """
        Validates whether a source result is genuine, relevant evidence for target_entity and criterion.
        """
        entity_clean = target_entity.strip().lower()
        title_clean = (title or "").lower()
        snippet_clean = (snippet or "").lower()
        url_clean = (source_url or "").lower()

        # Parse domain
        domain = ""
        if url_clean.startswith("http"):
            try:
                parsed = urlparse(url_clean)
                domain = parsed.netloc.lower()
                if domain.startswith("www."):
                    domain = domain[4:]
            except Exception:
                pass

        # 1. Reject Irrelevant/Spam Domains
        if domain in IRRELEVANT_DOMAINS or any(dom in domain for dom in ["wikipedia.org", "youtube.com", "imdb.com", "zhihu.com", "hamariweb", "quran", "surah", "manhattan-tourism"]):
            return {
                "is_valid": False,
                "confidence_score": 0.0,
                "rejection_reason": f"Irrelevant or low-credibility domain '{domain or url_clean}' rejected for B2B research."
            }

        # 2. Claim-Type vs Source-Content Validation
        crit_clean = criterion.lower()
        is_market_sizing_crit = any(kw in crit_clean for kw in ["cagr", "growth", "market size", "forecast", "automation"])
        
        if is_market_sizing_crit:
            has_metric_terms = any(kw in title_clean or kw in snippet_clean for kw in ["cagr", "billion", "market", "forecast", "growth", "2023", "2028", "usd", "size", "report"])
            is_pure_pricing_article = "pricing" in url_clean or "cost" in url_clean or "price" in title_clean
            if is_pure_pricing_article and not has_metric_terms:
                return {
                    "is_valid": False,
                    "confidence_score": 0.1,
                    "rejection_reason": f"Pricing article '{source_url}' cannot support market-sizing / CAGR claims for criterion '{criterion}'."
                }

        # 3. Check Cross-Entity Mismatch
        for other_ent, other_doms in OFFICIAL_DOMAINS.items():
            if other_ent != entity_clean and entity_clean not in other_ent:
                if any(dom in domain for dom in other_doms):
                    if not ("vs" in title_clean or "compare" in title_clean or "alternative" in title_clean):
                        return {
                            "is_valid": False,
                            "confidence_score": 0.0,
                            "rejection_reason": f"Competitor site '{domain}' cannot support claims for target entity '{target_entity}'."
                        }

        # 4. Entity Match Check
        entity_first_word = entity_clean.split()[0] if entity_clean else ""
        has_entity = (
            entity_clean in url_clean or entity_first_word in url_clean or
            entity_clean in title_clean or entity_first_word in title_clean or
            entity_clean in snippet_clean or entity_first_word in snippet_clean
        )

        if not has_entity and source_type != "local_corpus" and not is_market_sizing_crit:
            return {
                "is_valid": False,
                "confidence_score": 0.1,
                "rejection_reason": f"Entity mismatch: source title/snippet/URL does not mention target entity '{target_entity}'."
            }

        # 5. Official Domain Bonus
        is_official = False
        if entity_clean in OFFICIAL_DOMAINS:
            official_doms = OFFICIAL_DOMAINS[entity_clean]
            if any(dom in domain for dom in official_doms):
                is_official = True

        # 6. Criterion Relevance Check
        criterion_terms = [t.lower() for t in criterion.split() if len(t) > 2]
        criterion_matches = sum(1 for t in criterion_terms if t in title_clean or t in snippet_clean or t in url_clean)

        score = 0.5
        if is_official:
            score += 0.4
        if has_entity:
            score += 0.2
        if criterion_matches > 0:
            score += 0.2

        score = min(1.0, max(0.0, score))

        if score < 0.35:
            return {
                "is_valid": False,
                "confidence_score": score,
                "rejection_reason": f"Low topic/criterion relevance score ({score:.2f}) for criterion '{criterion}'."
            }

        return {
            "is_valid": True,
            "confidence_score": score,
            "is_official_domain": is_official,
            "rejection_reason": None
        }
