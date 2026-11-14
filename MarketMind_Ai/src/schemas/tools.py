# OpenAI Tool Definitions for MarketMind AI

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Perform live web search across internet sources for current company pricing, features, market size, or news.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Targeted search query (e.g., 'ChatGPT Plus monthly pricing', 'Claude Pro features 2026')."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_webpage",
            "description": "Fetch and extract text content from a specific web URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The target webpage URL to fetch."
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_information",
            "description": "Search local approved corpus documents and live web for market, company, pricing, or feature information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query terms or keywords."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "retrieve_document",
            "description": "Retrieve the full text content of a specific document from the corpus by filename.",
            "parameters": {
                "type": "object",
                "properties": {
                    "document_id": {
                        "type": "string",
                        "description": "The exact document filename (e.g., 'vendor_zendesk.txt')."
                    }
                },
                "required": ["document_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_metric",
            "description": "Perform financial or statistical metric calculations (growth rate, average, CAGR).",
            "parameters": {
                "type": "object",
                "properties": {
                    "metric_type": {
                        "type": "string",
                        "enum": ["average", "growth_rate", "cagr", "sum"],
                        "description": "Type of calculation to perform."
                    },
                    "values": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "List of numbers required for calculation."
                    }
                },
                "required": ["metric_type", "values"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_research",
            "description": "Record a verified evidence claim with source provenance into the evidence store.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sub_question_id": {
                        "type": "string",
                        "description": "ID of subquestion being answered (e.g., 'SQ1')."
                    },
                    "source_id": {
                        "type": "string",
                        "description": "Filename or ID of source document."
                    },
                    "claim_text": {
                        "type": "string",
                        "description": "Extracted factual statement supported by source."
                    },
                    "claim_type": {
                        "type": "string",
                        "enum": ["pricing", "feature", "metric", "limitation", "general_trend"],
                        "description": "Classification of claim."
                    },
                    "verbatim_quote": {
                        "type": "string",
                        "description": "Exact text quote from source backing this claim."
                    }
                },
                "required": ["sub_question_id", "source_id", "claim_text", "claim_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compare_companies",
            "description": "Generate or retrieve structured comparison matrix for target companies from evidence store.",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of company names to compare."
                    }
                },
                "required": ["company_names"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_report",
            "description": "Assemble and synthesize all recorded evidence into the final market research report structure.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]
