# OpenAI SDK API Verification Document

**Date of Verification:** March 2026  
**SDK Version:** `openai >= 1.0.0` (Official OpenAI Python SDK)  
**Target Model:** `gpt-4o-mini`  

## Verification Findings

1. **Raw OpenAI SDK Usage**:
   - The project strictly uses `from openai import OpenAI` in `MarketMind_Ai/src/llm/client.py`.
   - **No prebuilt agent frameworks (LangChain, AutoGen, CrewAI)** are used in the `MarketMind_Ai/src` core engine.

2. **Structured Outputs & Tool Calling Syntax**:
   - Tool definition schemas use `type: "function"` with standard Pydantic JSON schemas.
   - Message completions use `client.chat.completions.create(model=self.model, messages=messages, temperature=0.1, tools=TOOL_DEFINITIONS)`.

3. **Usage & Token Cost Tracking**:
   - Token usage is tracked per API call via `response.usage.prompt_tokens` and `response.usage.completion_tokens`.
   - Budget cost ceiling ($1.00 USD) is checked prior to every call in `LLMClient.generate()`.
