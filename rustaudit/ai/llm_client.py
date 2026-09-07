"""
Modular LLM Client for RustAuditAI.
Supports Google Gemini API and Groq API via direct REST HTTP requests.
Loads API keys automatically from .env file.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import httpx
from dotenv import load_dotenv

# Load environment variables from root .env file if available
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class LLMClient:
    """
    Modular client interface for Google Gemini API and Groq API.
    """

    GEMINI_MODELS = ["gemini-3.7-flash", "gemini-3.5-flash", "gemma-4-26b-a4b-it"]
    GROQ_MODELS = ["openai/gpt-oss-120b", "groq/compound", "qwen/qwen3.6-27b", "openai/gpt-oss-20b"]

    def __init__(
        self,
        provider: Optional[str] = None,
        gemini_key: Optional[str] = None,
        groq_key: Optional[str] = None,
    ):
        self.provider = (provider or os.getenv("LLM_PROVIDER", "gemini")).lower()
        self.gemini_key = gemini_key or os.getenv("GEMINI_API_KEY")
        self.groq_key = groq_key or os.getenv("GROQ_API_KEY")

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generates text completion using the selected LLM provider.
        """
        if self.provider == "gemini" or (self.gemini_key and not self.groq_key):
            return self._call_gemini(prompt, system_prompt)
        elif self.provider == "groq" or self.groq_key:
            return self._call_groq(prompt, system_prompt)
        else:
            raise ValueError("No valid LLM API keys found. Please set GEMINI_API_KEY or GROQ_API_KEY in your .env file.")

    def _call_gemini(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if not self.gemini_key:
            if self.groq_key:
                return self._call_groq(prompt, system_prompt)
            raise ValueError("GEMINI_API_KEY is missing in .env file")

        contents = []
        if system_prompt:
            contents.append({"role": "user", "parts": [{"text": f"System Instructions:\n{system_prompt}"}]})
            contents.append({"role": "model", "parts": [{"text": "Understood. I will strictly follow the provided graph facts and RQI optimization rules."}]})
        
        contents.append({"role": "user", "parts": [{"text": prompt}]})

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 2500,
            },
        }

        # Try user-specified model or fallback list
        env_model = os.getenv("GEMINI_MODEL")
        models_to_try = [env_model] if env_model else self.GEMINI_MODELS

        last_err = None
        for model in models_to_try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.gemini_key}"
            try:
                with httpx.Client(timeout=30.0) as client:
                    res = client.post(url, json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        candidates = data.get("candidates", [])
                        if candidates:
                            parts = candidates[0].get("content", {}).get("parts", [])
                            if parts:
                                return parts[0].get("text", "").strip()
                    else:
                        last_err = f"Gemini API ({model}) returned {res.status_code}: {res.text[:200]}"
            except Exception as e:
                last_err = str(e)

        # Fallback to Groq if Gemini failed
        if self.groq_key:
            return self._call_groq(prompt, system_prompt)

        raise RuntimeError(f"Failed to communicate with Gemini API: {last_err}")

    def _call_groq(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if not self.groq_key:
            raise ValueError("GROQ_API_KEY is missing in .env file")

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_key}",
            "Content-Type": "application/json",
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        env_model = os.getenv("GROQ_MODEL")
        models_to_try = [env_model] if env_model else self.GROQ_MODELS

        last_err = None
        for model in models_to_try:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": 0.2,
                "max_tokens": 2500,
            }
            try:
                with httpx.Client(timeout=30.0) as client:
                    res = client.post(url, headers=headers, json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        choices = data.get("choices", [])
                        if choices:
                            return choices[0].get("message", {}).get("content", "").strip()
                    else:
                        last_err = f"Groq API ({model}) returned {res.status_code}: {res.text[:200]}"
            except Exception as e:
                last_err = str(e)

        raise RuntimeError(f"Failed to communicate with Groq API: {last_err}")

