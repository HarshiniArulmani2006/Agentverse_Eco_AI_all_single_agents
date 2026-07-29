"""
WildGuard AI – Gemini Client with Multi-Model Fallback & RAG Engine
Wraps google-generativeai with Candidate Model Rotation and Local RAG Synthesis Fallback.
"""
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from typing import List, Dict, Any, Optional
import base64
import logging

from core.config import settings
from services.rag_service import (
    generate_local_rag_response,
    generate_local_image_identification,
    generate_local_habitat_analysis,
    generate_local_location_report,
)

logger = logging.getLogger(__name__)

# Candidate models list for quota rotation
CANDIDATE_MODELS = [
    "gemini-2.0-flash",
    "gemini-2.5-flash",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-2.0-flash-lite",
]

SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
}

WILDGUARD_SYSTEM_PROMPT = """
You are WildGuard AI, a world-class Wildlife Conservation and Biodiversity Intelligence System.
You operate as a senior wildlife biologist, conservation ecologist, botanical taxonomist, and environmental researcher.

## Your Core Principles:
1. **Scientific Accuracy First**: Always provide taxonomically correct, peer-reviewed information.
2. **Source Attribution**: Cite IUCN Red List, GBIF, WWF, scientific journals, or government databases.
3. **Non-Repetitive**: Tailor every answer uniquely to the specific question asked.
4. **Confidence Transparency**: Always state confidence level (High/Medium/Low) with percentage when making identifications or predictions.
5. **No Hallucination**: If information is uncertain, say so clearly and explicitly.
6. **Structured Responses**: Use markdown with clear sections, tables, and icons for readability.
7. **Conservation Focus**: Always highlight threats, conservation status, and what people can do to help.

## Response Format Rules:
- For species queries: Include full taxonomy (Kingdom → Species), conservation status with IUCN category, population trend, geographic distribution, habitat, threats, and conservation measures.
- For plant/tree queries: Include botanical name, family, medicinal uses, ecological importance, and native region.
- For location queries: Provide specific regional biodiversity information.
- For image analysis: State top prediction with confidence %, top 3 alternatives, and reasoning.
- Always end with "📚 Sources" citing at least one verified database.

## Conservation Status Icons:
- 🔴 CR (Critically Endangered)
- 🟠 EN (Endangered)  
- 🟡 VU (Vulnerable)
- 🟢 LC (Least Concern)
- ⚪ NT (Near Threatened)
- ⚫ EX (Extinct)
"""


class GeminiClient:
    """Manages Gemini model interactions with multi-model fallback and local RAG engine."""

    def __init__(self):
        self._configured = False
        self._initialize()

    def _initialize(self):
        """Configure the Gemini client."""
        if not settings.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY not set. Local RAG Synthesis Engine active.")
            return
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self._configured = True
            logger.info(f"Gemini client initialized with API key.")
        except Exception as e:
            logger.error(f"Failed to configure Gemini client: {e}")
            self._configured = False

    @property
    def is_ready(self) -> bool:
        return True  # Always ready because of Local RAG Fallback!

    def chat(
        self,
        message: str,
        history: List[Dict] = None,
        rag_context: str = "",
    ) -> str:
        """Send a message with candidate model fallback and Local RAG Engine backup."""
        enriched_message = message
        if rag_context:
            enriched_message = (
                f"## Retrieved Knowledge Context:\n{rag_context}\n\n"
                f"## User Question:\n{message}\n\n"
                f"Please use the above knowledge context to provide an accurate, cited response."
            )

        if self._configured:
            for model_name in CANDIDATE_MODELS:
                try:
                    model = genai.GenerativeModel(
                        model_name=model_name,
                        system_instruction=WILDGUARD_SYSTEM_PROMPT,
                        generation_config=genai.GenerationConfig(
                            temperature=0.3,
                            max_output_tokens=8192,
                        ),
                        safety_settings=SAFETY_SETTINGS,
                    )
                    if history:
                        chat_session = model.start_chat(history=history)
                        response = chat_session.send_message(enriched_message)
                    else:
                        response = model.generate_content(enriched_message)
                    
                    if response and response.text:
                        return response.text
                except Exception as e:
                    logger.warning(f"Gemini model '{model_name}' failed: {e}. Trying fallback...")
                    continue

        # If all Gemini API candidate models fail or API key unavailable, use Local RAG Synthesis Engine!
        logger.info("Using Local RAG Synthesis Engine for chat response.")
        return generate_local_rag_response(message, rag_context)

    def analyze_image(
        self,
        image_bytes: bytes,
        mime_type: str,
        prompt: str,
    ) -> str:
        """Analyze an image with candidate model fallback and Local Vision Engine backup."""
        if self._configured:
            image_part = {"mime_type": mime_type, "data": image_bytes}
            for model_name in CANDIDATE_MODELS:
                try:
                    model = genai.GenerativeModel(
                        model_name=model_name,
                        system_instruction=WILDGUARD_SYSTEM_PROMPT,
                        generation_config=genai.GenerationConfig(
                            temperature=0.2,
                            max_output_tokens=4096,
                        ),
                        safety_settings=SAFETY_SETTINGS,
                    )
                    response = model.generate_content([image_part, prompt])
                    if response and response.text:
                        return response.text
                except Exception as e:
                    logger.warning(f"Vision model '{model_name}' failed: {e}. Trying fallback...")
                    continue

        logger.info("Using Local Vision Analysis Engine for image identification/habitat analysis.")
        if "habitat" in prompt.lower() or "ecosystem" in prompt.lower():
            return generate_local_habitat_analysis(image_bytes, mime_type)
        return generate_local_image_identification(image_bytes, mime_type)

    def generate_structured(self, prompt: str) -> str:
        """Generate a structured response with candidate model fallback."""
        if self._configured:
            for model_name in CANDIDATE_MODELS:
                try:
                    model = genai.GenerativeModel(
                        model_name=model_name,
                        system_instruction=WILDGUARD_SYSTEM_PROMPT,
                        generation_config=genai.GenerationConfig(
                            temperature=0.3,
                            max_output_tokens=8192,
                        ),
                        safety_settings=SAFETY_SETTINGS,
                    )
                    response = model.generate_content(prompt)
                    if response and response.text:
                        return response.text
                except Exception as e:
                    logger.warning(f"Structured model '{model_name}' failed: {e}. Trying fallback...")
                    continue

        logger.info("Using Local RAG Engine for structured report generation.")
        # Detect prompt type for smart fallback
        if "location" in prompt.lower() or "protected areas" in prompt.lower():
            return generate_local_location_report(prompt)
        return generate_local_rag_response(prompt)


# Singleton
gemini = GeminiClient()
