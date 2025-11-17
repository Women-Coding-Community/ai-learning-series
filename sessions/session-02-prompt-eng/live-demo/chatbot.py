"""
WCC Alexa Secure Chatbot
"""

import google.generativeai as genai
from typing import Dict
from config import MODEL_CONFIG, SAFETY_SETTINGS, MODEL_ID
from prompt_patterns import PromptPatterns
from security import SecurityGuardrails


class SecureWCCChatbot:
    """Production-ready chatbot with security"""
    
    def __init__(self, pattern_type: str = "advanced"):
        self.pattern_type = pattern_type
        self.model = genai.GenerativeModel(
            model_name=MODEL_ID,
            generation_config=MODEL_CONFIG,
            safety_settings=SAFETY_SETTINGS
        )
        self.conversation_history = []
        self.security_log = []
        
        print(f"✓ Chatbot initialized with '{pattern_type}' pattern")
    
    def _select_prompt_pattern(self, user_query: str) -> str:
        """Select prompt pattern"""
        patterns = {
            'zero_shot': PromptPatterns.zero_shot_prompt,
            'few_shot': PromptPatterns.few_shot_prompt,
            'cot': PromptPatterns.chain_of_thought_prompt,
            'role_based': PromptPatterns.role_based_prompt,
            'structured': PromptPatterns.structured_output_prompt
        }
        
        pattern_func = patterns.get(self.pattern_type, PromptPatterns.advanced_prompt_with_guardrails)
        return pattern_func(user_query)
    
    def process_message(self, user_message: str) -> Dict:
        """Process message through security pipeline"""
        processing_steps = []
        security_events = []
        
        print(f"\n{'='*70}")
        print(f"PROCESSING USER MESSAGE")
        print(f"{'='*70}")
        print(f"Original: {user_message}\n")
        
        # STEP 1: Detect Prompt Injection
        print("STEP 1: Prompt Injection Detection")
        print("-" * 70)
        
        is_injection, injection_patterns = SecurityGuardrails.detect_prompt_injection(user_message)
        
        if is_injection:
            SecurityGuardrails.log_security_event(
                'PROMPT_INJECTION',
                f'Detected {len(injection_patterns)} patterns',
                'CRITICAL'
            )
            security_events.append({
                'type': 'prompt_injection',
                'patterns': injection_patterns
            })
            
            return {
                'response': "I noticed your message might be trying to change how I work. I'm here to help with WCC-related questions only! What would you like to know?",
                'blocked': True,
                'security_events': security_events,
                'processing_steps': ['❌ Blocked at injection detection']
            }
        
        processing_steps.append('✓ No injection detected')
        print("✓ No injection detected\n")
        
        # STEP 2: Redact PII
        print("STEP 2: PII Redaction")
        print("-" * 70)
        
        redacted_message, detected_pii = SecurityGuardrails.redact_pii(user_message)
        
        if detected_pii:
            pii_summary = ', '.join([f"{p['count']} {p['type']}" for p in detected_pii])
            SecurityGuardrails.log_security_event('PII_REDACTED', pii_summary, 'WARNING')
            security_events.append({'type': 'pii_redacted', 'details': detected_pii})
            processing_steps.append(f'🔒 PII redacted: {pii_summary}')
            print(f"Redacted message: {redacted_message}\n")
        else:
            processing_steps.append('✓ No PII detected')
            print("✓ No PII detected\n")
        
        # STEP 3: Content Moderation
        print("STEP 3: Content Moderation")
        print("-" * 70)
        
        is_inappropriate, flagged_words, is_crisis = SecurityGuardrails.moderate_content(redacted_message)
        
        if is_crisis:
            SecurityGuardrails.log_security_event('CRISIS_DETECTED', 'Immediate intervention needed', 'CRITICAL')
            return {
                'response': "I'm concerned about what you've shared. Please reach out to:\n\n• National Suicide Prevention Lifeline: 988\n• Crisis Text Line: Text HOME to 741741\n and help is available 24/7.",
                'blocked': True,
                'security_events': [{'type': 'crisis', 'severity': 'critical'}],
                'processing_steps': processing_steps + ['🚨 Crisis intervention triggered']
            }
        
        if is_inappropriate:
            SecurityGuardrails.log_security_event('CONTENT_FLAGGED', f'{len(flagged_words)} keywords', 'WARNING')
            security_events.append({'type': 'inappropriate_content', 'flagged': flagged_words})
            processing_steps.append(f'⚠️ Content flagged: {len(flagged_words)} keywords')
            
            return {
                'response': "I'm here to provide helpful information about WCC in a respectful manner. Please rephrase your question, and I'll be happy to assist!",
                'blocked': True,
                'security_events': security_events,
                'processing_steps': processing_steps
            }
        
        processing_steps.append('✓ Content moderation passed')
        print("✓ Content appropriate\n")
        
        # STEP 4: Generate AI Response
        print("STEP 4: Generating AI Response")
        print("-" * 70)
        
        try:
            prompt = self._select_prompt_pattern(redacted_message)
            response = self.model.generate_content(prompt)
            ai_response = response.text
            processing_steps.append('✓ AI response generated')
            print("✓ Response generated\n")
        except Exception as e:
            SecurityGuardrails.log_security_event('ERROR', f'Generation failed: {str(e)}', 'CRITICAL')
            return {
                'response': "I'm having trouble right now. Please try again later.",
                'blocked': True,
                'security_events': security_events,
                'processing_steps': processing_steps + [f'✗ Error: {str(e)}']
            }
        
        # STEP 5: Validate Output
        print("STEP 5: Output Validation")
        print("-" * 70)
        
        is_safe, issues = SecurityGuardrails.validate_output(ai_response)
        
        if not is_safe:
            SecurityGuardrails.log_security_event('OUTPUT_BLOCKED', f'{len(issues)} issues', 'WARNING')
            security_events.append({'type': 'unsafe_output', 'issues': issues})
            processing_steps.append(f'✗ Output validation failed: {len(issues)} issues')
            
            return {
                'response': "I apologize, my response didn't meet quality standards. Could you rephrase your question?",
                'blocked': True,
                'security_events': security_events,
                'processing_steps': processing_steps
            }
        
        processing_steps.append('✓ Output validation passed')
        print("✓ Output safe\n")
        
        print(f"✅ MESSAGE PROCESSED SUCCESSFULLY")
        print(f"{'='*70}\n")
        
        return {
            'response': ai_response,
            'blocked': False,
            'security_events': security_events,
            'processing_steps': processing_steps
        }
    
    def chat(self, user_message: str) -> str:
        """Simple chat interface"""
        result = self.process_message(user_message)
        return result['response']