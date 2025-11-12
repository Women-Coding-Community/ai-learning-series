"""
Security Guardrails
"""

import re
from typing import List, Dict, Tuple
from datetime import datetime


class SecurityGuardrails:
    """Multi-layered security system"""
    
    INJECTION_PATTERNS = [
        r'ignore\s+(previous|all|above|prior)\s+instructions?',
        r'disregard\s+(previous|all|above)\s+instructions?',
        r'forget\s+(everything|all|previous)',
        r'you\s+are\s+now\s+(a|an)',
        r'act\s+as\s+(a|an)',
        r'pretend\s+(you\s+are|to\s+be)',
        r'roleplay\s+as',
        r'system\s+prompt',
        r'show\s+(me\s+)?your\s+(instructions|prompt)',
        r'reveal\s+your\s+(prompt|instructions)',
        r'developer\s+mode',
        r'debug\s+mode',
        r'jailbreak',
        r'\[SYSTEM\]',
        r'\[ADMIN\]',
    ]
    
    PII_PATTERNS = [
        (r'\b\d{3}-\d{2}-\d{4}\b', '[REDACTED_SSN]', 'NI'),
        (r'\b\d{3}[\s-]?\d{3}[\s-]?\d{4}\b', '[REDACTED_PHONE]', 'Phone'),
        (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[REDACTED_EMAIL]', 'Email'),
        (r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', '[REDACTED_CC]', 'Credit Card'),
        (r'\b\d{5}(?:-\d{4})?\b', '[REDACTED_ZIP]', 'ZIP Code'),
    ]
    
    INAPPROPRIATE_KEYWORDS = [
        'hate', 'racist', 'violence', 'suicide', 'bomb', 'weapon',
        'drugs', 'hack', 'exploit', 'scam', 'fraud'
    ]
    
    CRISIS_KEYWORDS = [
        'suicide', 'kill myself', 'end my life', 'want to die',
        'self harm', 'cut myself'
    ]
    
    @classmethod
    def detect_prompt_injection(cls, text: str) -> Tuple[bool, List[str]]:
        """Detect prompt injection attempts"""
        detected = []
        text_lower = text.lower()
        
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                detected.append(pattern)
                print(f"  🚨 Detected pattern: {pattern}")
        
        is_malicious = len(detected) > 0
        if is_malicious:
            print(f"  ⚠️ ALERT: {len(detected)} injection pattern(s) detected!")
        
        return is_malicious, detected
    
    @classmethod
    def redact_pii(cls, text: str) -> Tuple[str, List[Dict]]:
        """Redact personally identifiable information"""
        redacted_text = text
        detected_pii = []
        
        for pattern, replacement, pii_type in cls.PII_PATTERNS:
            matches = re.findall(pattern, text)
            if matches:
                detected_pii.append({
                    'type': pii_type,
                    'count': len(matches)
                })
                redacted_text = re.sub(pattern, replacement, redacted_text)
                print(f"  🔒 Redacted {len(matches)} {pii_type}(s)")
        
        return redacted_text, detected_pii
    
    @classmethod
    def moderate_content(cls, text: str) -> Tuple[bool, List[str], bool]:
        """Check for inappropriate content"""
        text_lower = text.lower()
        
        flagged = [word for word in cls.INAPPROPRIATE_KEYWORDS 
                   if word in text_lower]
        
        crisis_detected = any(keyword in text_lower 
                            for keyword in cls.CRISIS_KEYWORDS)
        
        if flagged:
            print(f"  ⚠️ Content flagged: {', '.join(flagged)}")
        
        if crisis_detected:
            print(f"  🚨 CRISIS DETECTED - Human intervention needed!")
        
        is_inappropriate = len(flagged) > 0
        
        return is_inappropriate, flagged, crisis_detected
    
    @classmethod
    def validate_output(cls, response: str) -> Tuple[bool, List[str]]:
        """Validate AI response is safe and on-topic"""
        issues = []
        response_lower = response.lower()
        
        leakage_indicators = [
            'system prompt',
            'my instructions',
            'i was told to',
            'my guidelines state'
        ]
        
        for indicator in leakage_indicators:
            if indicator in response_lower:
                issues.append(f'Prompt leakage: "{indicator}"')
                print(f"  🚨 Output validation failed: {indicator}")
        
        wcc_keywords = [
            'wcc', 'washtenaw', 'college', 'program', 'course', 
            'degree', 'admission', 'enroll', 'student', 'tuition',
            'financial aid', 'apply', 'transfer', 'campus'
        ]
        
        has_topic = any(keyword in response_lower for keyword in wcc_keywords)
        
        if not has_topic and len(response) > 100:
            issues.append('Response may be off-topic')
            print(f"  ⚠️ Response appears off-topic")
        
        is_safe = len(issues) == 0
        return is_safe, issues
    
    @staticmethod
    def log_security_event(event_type: str, message: str, severity: str = "INFO"):
        """Log security events"""
        timestamp = datetime.now().isoformat()
        
        severity_emoji = {
            'INFO': 'ℹ️',
            'WARNING': '⚠️',
            'CRITICAL': '🚨'
        }
        
        emoji = severity_emoji.get(severity, '📝')
        print(f"[SECURITY] {emoji} {severity}: {event_type} - {message}")
