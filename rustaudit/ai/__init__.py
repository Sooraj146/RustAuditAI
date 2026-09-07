"""
Explainable AI (XAI) and Patch Synthesis package for RustAuditAI.
"""

from .llm_client import LLMClient
from .prompt_builder import XAIPromptBuilder
from .xai_engine import XAIEngine, XAIReport

__all__ = ["LLMClient", "XAIPromptBuilder", "XAIEngine", "XAIReport"]
