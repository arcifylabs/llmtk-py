"""
LLMTK (LLM Tool Kit) - Type-safe function registration and validation for LLM function calls.
"""

from .core import call_function, get_openai_tools, register_function

__version__ = "0.1.0"
__all__ = ["register_function", "call_function", "get_openai_tools"]
