"""
Career Counsellor Chatbot - NOT SECURE VERSION
"""

import json
import google.generativeai as genai
from typing import Dict
from config import MODEL_CONFIG, MODEL_ID, initialize_api
from prompt_patterns import (
    create_career_coach_prompt,
    create_action_plan_prompt,
    PromptPatterns
)


class NoSecureCareerCoachBot:
    """Career coach chatbot WITHOUT security guardrails"""
    
    def __init__(self, pattern_type: str = "advanced"):
        # Initialize API
        initialize_api()
        
        self.pattern_type = pattern_type
        self.model = genai.GenerativeModel(
            model_name=MODEL_ID,
            generation_config=MODEL_CONFIG
            # NOTE: No safety_settings - this is the insecure version
        )
        print(f"⚠️ NoSecureCareerCoachBot initialized (NO SECURITY)")
        print(f"   Pattern type: '{pattern_type}'")
        print(f"   WARNING: This version has no security features!\n")

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
    
    def process_message(self, user_message: str, mode: str = "coach") -> Dict:
        """
        Process message WITHOUT any security checks
        ⚠️ WARNING: This version does NOT:
        - Detect prompt injection
        - Redact PII
        - Moderate content
        - Detect crisis situations
        - Validate output
        - Block resume PII
        """
        print(f"Processing message (NO SECURITY CHECKS): {user_message[:50]}...")
        
        try:
            prompt = self._select_prompt_pattern(user_message, mode)
            response = self.model.generate_content(prompt)
            ai_response = response.text
            
            # Parse JSON if action plan mode
            parsed_json = None
            if mode == "action_plan":
                try:
                    json_start = ai_response.find('{')
                    json_end = ai_response.rfind('}') + 1
                    if json_start >= 0 and json_end > json_start:
                        json_str = ai_response[json_start:json_end]
                        parsed_json = json.loads(json_str)
                except json.JSONDecodeError:
                    pass
            
            result = {
                "response": ai_response,
                "blocked": False
            }
            
            if parsed_json:
                result["action_plan"] = parsed_json
            
            print("✓ Response generated (no validation)\n")
            return result
            
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")
            return {
                "response": f"Error occurred: {str(e)}",
                "blocked": False
            }
    
    def chat(self, user_message: str, mode: str = "coach") -> str:
        """Simple chat wrapper"""
        result = self.process_message(user_message, mode)
        return result["response"]

