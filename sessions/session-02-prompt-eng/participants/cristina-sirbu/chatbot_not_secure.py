"""
WCC Alexa Not So Secure Chatbot
"""

import google.generativeai as genai
from typing import Dict
from prompt_patterns import PromptPatterns
from config import MODEL_CONFIG, MODEL_ID

class NoSecureWCCChatbot:
    """Chatbot without security"""
    
    def __init__(self, pattern_type: str = "advanced"):
        self.pattern_type = pattern_type
        self.model = genai.GenerativeModel(
            model_name=MODEL_ID,
            generation_config=MODEL_CONFIG
        )

    def _select_prompt_pattern(self, user_query: str) -> str:
        """Select prompt pattern"""
        patterns = {
            'few_shot': PromptPatterns.few_shot_prompt,
            'cot': PromptPatterns.chain_of_thought_prompt,
            'role_based': PromptPatterns.role_based_prompt,
        }
        
        pattern_func = patterns.get(self.pattern_type, PromptPatterns.few_shot_prompt)
        return pattern_func(user_query) 
       
    
    def process_message(self, user_message: str) -> Dict:
        """Process message without security"""
        prompt = self._select_prompt_pattern(user_message)
        response = self.model.generate_content(prompt)
        ai_response = response.text
        print("✓ Response generated\n")
    
        return {
        'response': ai_response
        }