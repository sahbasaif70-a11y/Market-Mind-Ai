import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
from src.config import Config
from src.llm.usage import UsageTracker

class LLMClient:
    """Wrapper around OpenAI API client with usage tracking and budget checking."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or Config.OPENAI_API_KEY
        self.model = model or Config.MODEL_NAME
        self.usage_tracker = UsageTracker(model=self.model)
        
        # Initialize standard OpenAI client
        self.client = OpenAI(api_key=self.api_key)

    def generate(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Any] = "auto",
        temperature: float = 0.2,
        response_format: Optional[Any] = None
    ) -> Any:
        """
        Send a completion request to OpenAI API and record token usage.
        """
        # Check cost budget ceiling before making call
        if self.usage_tracker.total_cost_usd >= Config.MAX_COST_USD:
            raise RuntimeError(
                f"Cost limit exceeded! Used ${self.usage_tracker.total_cost_usd:.4f}, limit is ${Config.MAX_COST_USD:.2f}"
            )

        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = tool_choice
            
        if response_format:
            kwargs["response_format"] = response_format

        try:
            response = self.client.chat.completions.create(**kwargs)
            
            # Record token usage
            if hasattr(response, "usage") and response.usage:
                self.usage_tracker.record_usage(
                    prompt_tokens=response.usage.prompt_tokens,
                    completion_tokens=response.usage.completion_tokens,
                    model=self.model
                )
                
            return response.choices[0].message
        except Exception as e:
            raise RuntimeError(f"OpenAI API Call Failed: {str(e)}") from e
