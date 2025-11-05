from google.cloud import dlp_v2
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
import openai
from typing import Dict, List, Tuple

class ProductionSafetyPipeline:
    """
    Complete safety pipeline for LLM inputs
    Combines multiple detection methods for robust protection
    """
    
    def __init__(
        self,
        gcp_project_id: str,
        openai_api_key: str,
        use_google_dlp: bool = True,
        use_presidio: bool = True,
        use_openai_moderation: bool = True
    ):
        # Initialize services
        self.use_google_dlp = use_google_dlp
        self.use_presidio = use_presidio
        self.use_openai_moderation = use_openai_moderation
        
        if use_google_dlp:
            self.dlp_client = dlp_v2.DlpServiceClient()
            self.gcp_parent = f"projects/{gcp_project_id}"
        
        if use_presidio:
            self.presidio_analyzer = AnalyzerEngine()
            self.presidio_anonymizer = AnonymizerEngine()
        
        if use_openai_moderation:
            self.openai_client = openai.OpenAI(api_key=openai_api_key)
    
    def validate_input(
        self,
        text: str,
        max_length: int = 10000,
        block_on_pii: bool = True,
        block_on_harmful: bool = True
    ) -> Tuple[bool, str, Dict]:
        """
        Complete input validation pipeline
        
        Returns:
            (is_safe, processed_text, details)
        """
        
        details = {
            "pii_detected": False,
            "harmful_content": False,
            "length_exceeded": False,
            "pii_findings": [],
            "moderation_flags": {},
            "redacted_text": text
        }
        
        # Layer 1: Length Check
        if len(text) > max_length:
            details["length_exceeded"] = True
            if block_on_pii:
                return False, text, details
        
        # Layer 2: PII Detection (Google DLP)
        if self.use_google_dlp:
            pii_result = self._detect_pii_dlp(text)
            details["pii_detected"] = pii_result["has_pii"]
            details["pii_findings"].extend(pii_result["findings"])
            
            if block_on_pii and pii_result["has_pii"]:
                # Redact PII
                details["redacted_text"] = self._redact_pii_dlp(text)
                return False, details["redacted_text"], details
        
        # Layer 3: PII Detection (Presidio - backup/validation)
        if self.use_presidio:
            presidio_result = self._detect_pii_presidio(text)
            if presidio_result["has_pii"]:
                details["pii_detected"] = True
                details["pii_findings"].extend(presidio_result["findings"])
                
                if block_on_pii:
                    details["redacted_text"] = self._redact_pii_presidio(text)
                    return False, details["redacted_text"], details
        
        # Layer 4: Content Moderation (OpenAI)
        if self.use_openai_moderation:
            moderation_result = self._moderate_content(text)
            details["harmful_content"] = moderation_result["flagged"]
            details["moderation_flags"] = moderation_result["categories"]
            
            if block_on_harmful and moderation_result["flagged"]:
                return False, text, details
        
        # All checks passed
        return True, text, details
    
    def _detect_pii_dlp(self, text: str) -> Dict:
        """Detect PII using Google Cloud DLP"""
        
        info_types = [
            "EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD_NUMBER",
            "US_SOCIAL_SECURITY_NUMBER", "PERSON_NAME", "STREET_ADDRESS",
            "DATE_OF_BIRTH", "IP_ADDRESS", "PASSPORT", "DRIVER_LICENSE_NUMBER"
        ]
        
        inspect_config = {
            "info_types": [{"name": t} for t in info_types],
            "min_likelihood": "POSSIBLE",
        }
        
        response = self.dlp_client.inspect_content(
            request={
                "parent": self.gcp_parent,
                "inspect_config": inspect_config,
                "item": {"value": text},
            }
        )
        
        findings = [
            {
                "type": f.info_type.name,
                "quote": f.quote,
                "likelihood": f.likelihood.name
            }
            for f in response.result.findings
        ]
        
        return {
            "has_pii": len(findings) > 0,
            "findings": findings
        }
    
    def _redact_pii_dlp(self, text: str) -> str:
        """Redact PII using Google Cloud DLP"""
        
        info_types = [
            "EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD_NUMBER",
            "US_SOCIAL_SECURITY_NUMBER", "PERSON_NAME", "STREET_ADDRESS"
        ]
        
        inspect_config = {
            "info_types": [{"name": t} for t in info_types],
        }
        
        deidentify_config = {
            "info_type_transformations": {
                "transformations": [{
                    "primitive_transformation": {
                        "replace_config": {
                            "new_value": {"string_value": "[REDACTED]"}
                        }
                    }
                }]
            }
        }
        
        response = self.dlp_client.deidentify_content(
            request={
                "parent": self.gcp_parent,
                "deidentify_config": deidentify_config,
                "inspect_config": inspect_config,
                "item": {"value": text},
            }
        )
        
        return response.item.value
    
    def _detect_pii_presidio(self, text: str) -> Dict:
        """Detect PII using Presidio (backup validation)"""
        
        results = self.presidio_analyzer.analyze(
            text=text,
            language="en",
            score_threshold=0.5
        )
        
        findings = [
            {
                "type": r.entity_type,
                "text": text[r.start:r.end],
                "score": r.score
            }
            for r in results
        ]
        
        return {
            "has_pii": len(findings) > 0,
            "findings": findings
        }
    
    def _redact_pii_presidio(self, text: str) -> str:
        """Redact PII using Presidio"""
        
        analyzer_results = self.presidio_analyzer.analyze(
            text=text,
            language="en"
        )
        
        anonymized = self.presidio_anonymizer.anonymize(
            text=text,
            analyzer_results=analyzer_results
        )
        
        return anonymized.text
    
    def _moderate_content(self, text: str) -> Dict:
        """Check for harmful content using OpenAI Moderation"""
        
        response = self.openai_client.moderations.create(input=text)
        result = response.results[0]
        
        return {
            "flagged": result.flagged,
            "categories": {
                cat: score 
                for cat, score in result.category_scores.model_dump().items()
                if score > 0.5
            }
        }

# Usage Example
pipeline = ProductionSafetyPipeline(
    gcp_project_id="your-project",
    openai_api_key="your-key",
    use_google_dlp=True,
    use_presidio=True,
    use_openai_moderation=True
)

# Test with problematic input
test_input = """
Hi, I'm John Smith. Email me at john@company.com or call 555-123-4567.
My SSN is 123-45-6789. Also, I hate [harmful content here].
"""

is_safe, processed_text, details = pipeline.validate_input(
    test_input,
    block_on_pii=True,
    block_on_harmful=True
)

if not is_safe:
    print("❌ Input blocked!")
    print(f"  PII detected: {details['pii_detected']}")
    print(f"  Harmful content: {details['harmful_content']}")
    print(f"  Redacted text: {details['redacted_text']}")
else:
    print("✅ Input is safe")
    # Proceed to LLM