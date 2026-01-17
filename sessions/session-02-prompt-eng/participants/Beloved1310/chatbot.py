"""
Career Counsellor Chatbot
Production-ready chatbot with prompt patterns and security guardrails
"""

import json
import google.generativeai as genai
from typing import Dict, Optional
from config import MODEL_CONFIG, SAFETY_SETTINGS, MODEL_ID, initialize_api
from prompt_patterns import (
    create_career_coach_prompt,
    create_action_plan_prompt,
    PromptPatterns
)
from security import SecurityGuardrails


CAREER_CRISIS_KEYWORDS = [
    "giving up on life",
    "not worth living",
    "failed at everything",
    "want to disappear"
]

RESUME_PII_KEYWORDS = [
    "ssn",
    "national insurance",
    "@",
    "phone number",
    "address"
]

RESUME_WRITING_REQUESTS = [
    "write my resume",
    "create my resume",
    "make a resume for me",
    "generate my cv"
]


class CareerCoachBot:
    """AI-powered career counsellor with layered security"""

    def __init__(self, pattern_type: str = "advanced"):
        # Initialize API
        initialize_api()
        
        self.pattern_type = pattern_type
        self.model = genai.GenerativeModel(
            model_name=MODEL_ID,
            generation_config=MODEL_CONFIG,
            safety_settings=SAFETY_SETTINGS
        )
        self.conversation_history = []
        self.security_log = []

        print(f"✓ CareerCoachBot initialised with '{pattern_type}' prompt pattern")

    # ------------------------------------------------------------------
    # Detection helpers
    # ------------------------------------------------------------------

    def detect_crisis(self, message: str) -> bool:
        return any(keyword in message.lower() for keyword in CAREER_CRISIS_KEYWORDS)

    def detect_resume_pii(self, message: str) -> bool:
        return "resume" in message.lower() and any(
            keyword in message.lower() for keyword in RESUME_PII_KEYWORDS
        )

    def detect_resume_writing_attempt(self, message: str) -> bool:
        return any(req in message.lower() for req in RESUME_WRITING_REQUESTS)

    # ------------------------------------------------------------------
    # Prompt selection
    # ------------------------------------------------------------------

    def _select_prompt_pattern(self, user_query: str, mode: str) -> str:
        """Select appropriate prompt based on mode and pattern type"""

        if mode == "action_plan":
            return create_action_plan_prompt(user_query)

        patterns = {
            "few_shot": PromptPatterns.few_shot_prompt,
            "role_based": PromptPatterns.role_based_prompt,
            "structured": PromptPatterns.structured_output_prompt
        }

        pattern_func = patterns.get(
            self.pattern_type,
            PromptPatterns.advanced_prompt_with_guardrails
        )

        return pattern_func(user_query)

    # ------------------------------------------------------------------
    # Main processing pipeline
    # ------------------------------------------------------------------

    def process_message(self, user_message: str, mode: str = "coach") -> Dict:
        """Process message through full security and prompt pipeline"""

        processing_steps = []
        security_events = []

        # STEP 1: Prompt injection detection
        is_injection, injection_patterns = SecurityGuardrails.detect_prompt_injection(user_message)
        if is_injection:
            SecurityGuardrails.log_security_event(
                "PROMPT_INJECTION",
                f"Detected {len(injection_patterns)} patterns",
                "CRITICAL"
            )
            return {
                "response": (
                    "I’m here to help with career-related questions only. "
                    "Please let me know what you’d like support with."
                ),
                "blocked": True,
                "security_events": [{"type": "prompt_injection"}],
                "processing_steps": ["❌ Blocked: prompt injection detected"]
            }

        processing_steps.append("✓ Prompt injection check passed")

        # STEP 2: Crisis handling
        if self.detect_crisis(user_message):
            SecurityGuardrails.log_security_event(
                "CRISIS_DETECTED",
                "Career anxiety escalated to crisis language",
                "CRITICAL"
            )
            return {
                "response": (
                    "I’m really concerned about what you’ve shared. "
                    "Career setbacks can feel overwhelming, but you don’t have to go through this alone.\n\n"
                    "Please consider reaching out to a trusted person or a local crisis support service."
                ),
                "blocked": True,
                "security_events": [{"type": "crisis"}],
                "processing_steps": processing_steps + ["🚨 Crisis response triggered"]
            }

        # STEP 3: Resume protections
        if self.detect_resume_pii(user_message):
            return {
                "response": (
                    "I’m happy to help improve your resume, but please don’t share personal information here. "
                    "Instead, describe your experience and goals, and I’ll give you targeted advice."
                ),
                "blocked": True,
                "security_events": [{"type": "resume_pii"}],
                "processing_steps": processing_steps + ["🔒 Resume PII blocked"]
            }

        if self.detect_resume_writing_attempt(user_message):
            return {
                "response": (
                    "I can’t write your entire resume for you, but I *can* help you improve it.\n\n"
                    "Tell me:\n"
                    "1) The role you’re targeting\n"
                    "2) Your main experiences\n"
                    "3) Where you feel stuck\n\n"
                    "I’ll help you shape it effectively."
                ),
                "blocked": True,
                "security_events": [{"type": "resume_generation_blocked"}],
                "processing_steps": processing_steps + ["✋ Full resume generation blocked"]
            }

        # STEP 4: PII redaction
        redacted_message, detected_pii = SecurityGuardrails.redact_pii(user_message)
        if detected_pii:
            SecurityGuardrails.log_security_event(
                "PII_REDACTED",
                f"{len(detected_pii)} PII items removed",
                "WARNING"
            )
            security_events.append({"type": "pii_redacted", "details": detected_pii})
            processing_steps.append("🔒 PII redacted")

        # STEP 5: Content moderation
        is_inappropriate, flagged_words, _ = SecurityGuardrails.moderate_content(redacted_message)
        if is_inappropriate:
            return {
                "response": (
                    "I’m here to provide helpful, respectful career guidance. "
                    "Please rephrase your question and I’ll be glad to help."
                ),
                "blocked": True,
                "security_events": [{"type": "content_flagged", "words": flagged_words}],
                "processing_steps": processing_steps + ["⚠️ Content moderation failed"]
            }

        processing_steps.append("✓ Content moderation passed")

        # STEP 6: Generate response
        parsed_json = None
        try:
            prompt = self._select_prompt_pattern(redacted_message, mode)
            response = self.model.generate_content(prompt)
            ai_response = response.text
            processing_steps.append("✓ AI response generated")
            
            # Parse JSON if action plan mode
            if mode == "action_plan":
                try:
                    # Try to extract JSON from response (in case there's extra text)
                    json_start = ai_response.find('{')
                    json_end = ai_response.rfind('}') + 1
                    if json_start >= 0 and json_end > json_start:
                        json_str = ai_response[json_start:json_end]
                        parsed_json = json.loads(json_str)
                        processing_steps.append("✓ JSON parsed successfully")
                except json.JSONDecodeError:
                    processing_steps.append("⚠️ JSON parsing failed, returning raw response")
        except Exception as e:
            SecurityGuardrails.log_security_event(
                "GENERATION_ERROR",
                str(e),
                "CRITICAL"
            )
            return {
                "response": "I'm having trouble responding right now. Please try again shortly.",
                "blocked": True,
                "security_events": security_events,
                "processing_steps": processing_steps + ["❌ Generation error"]
            }

        # STEP 7: Output validation
        is_safe, issues = SecurityGuardrails.validate_output(ai_response)
        if not is_safe:
            SecurityGuardrails.log_security_event(
                "OUTPUT_BLOCKED",
                f"{len(issues)} validation issues",
                "WARNING"
            )
            return {
                "response": (
                    "I’m sorry — my response didn’t meet quality standards. "
                    "Could you rephrase your question?"
                ),
                "blocked": True,
                "security_events": [{"type": "unsafe_output", "issues": issues}],
                "processing_steps": processing_steps + ["✗ Output validation failed"]
            }

        processing_steps.append("✓ Output validated")

        result = {
            "response": ai_response,
            "blocked": False,
            "security_events": security_events,
            "processing_steps": processing_steps
        }
        
        # Add parsed JSON if available
        if mode == "action_plan" and parsed_json:
            result["action_plan"] = parsed_json
        
        return result

    # ------------------------------------------------------------------
    # Simple chat interface
    # ------------------------------------------------------------------

    def chat(self, user_message: str, mode: str = "coach") -> str:
        """Simple chat wrapper"""
        result = self.process_message(user_message, mode)
        return result["response"]
