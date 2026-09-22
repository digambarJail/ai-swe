# TYPE: PROJECT
# PATH: src/llm.py

from dataclasses import dataclass
from typing import Protocol, Optional
import json


@dataclass
class LLMResponse:
    content: str
    input_tokens: int
    output_tokens: int
    model_name: str


class LLMProvider(Protocol):
    """Abstract interface enforcing provider agnosticism across the SSD Platform."""
    
    def complete(self, prompt: str, system_prompt: str = "", temperature: float = 0.0) -> LLMResponse:
        ...


class MockLLMProvider:
    """
    A deterministic Mock LLM provider for offline development, local testing,
    and predictable verification without requiring live API keys.
    """
    
    def __init__(self, model_name: str = "mock-ssd-analyzer-v1"):
        self.model_name = model_name

    def complete(self, prompt: str, system_prompt: str = "", temperature: float = 0.0) -> LLMResponse:
        # Simulate basic token estimation (rough heuristic: 1 token ~ 4 chars)
        input_tokens = len(prompt) // 4 + len(system_prompt) // 4
        
        # Standard mock response simulating an SSD telemetry analysis
        if "CRITICAL" in prompt or "high_temp" in prompt:
            content = json.dumps({
                "status": "ANOMALY_DETECTED",
                "severity": "CRITICAL",
                "reason": "Drive temperature or bad block count exceeds operational thresholds."
            })
        else:
            content = json.dumps({
                "status": "NORMAL",
                "severity": "INFO",
                "reason": "All operational metrics within standard tolerances."
            })
            
        output_tokens = len(content) // 4
        
        return LLMResponse(
            content=content,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            model_name=self.model_name
        )


if __name__ == "__main__":
    # Quick sanity test of our model abstraction
    provider: LLMProvider = MockLLMProvider()
    
    test_prompt = "Analyze telemetry: drive_temp=85, smart_status=CRITICAL"
    response = provider.complete(prompt=test_prompt, temperature=0.0)
    
    print(f"Model: {response.model_name}")
    print(f"Input Tokens: {response.input_tokens} | Output Tokens: {response.output_tokens}")
    print(f"Response Content:\n{response.content}")