from google.cloud import dlp_v2
from typing import List, Dict

class ProductionPIIDetector:
    """Production-grade PII detection using Google Cloud DLP"""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.dlp_client = dlp_v2.DlpServiceClient()
        self.parent = f"projects/{project_id}"
    
    def detect_pii(
        self, 
        text: str, 
        info_types: List[str] = None,
        min_likelihood: str = "POSSIBLE"
    ) -> Dict:
        """
        Detect PII in text using Google Cloud DLP
        
        Args:
            text: Text to scan
            info_types: List of PII types to detect (None = detect all)
            min_likelihood: VERY_UNLIKELY, UNLIKELY, POSSIBLE, LIKELY, VERY_LIKELY
        
        Returns:
            Dictionary with findings and redacted text
        """
        
        # Default: Detect common PII types (region-supported)
        if info_types is None:
            info_types = [
                "EMAIL_ADDRESS",
                "PHONE_NUMBER",
                "CREDIT_CARD_NUMBER",
                "US_SOCIAL_SECURITY_NUMBER",
                "PERSON_NAME",
                "DATE_OF_BIRTH",
                "STREET_ADDRESS",
                "IP_ADDRESS",
                "MAC_ADDRESS",
                "IBAN_CODE",
                "SWIFT_CODE",
            ]
        
        # Configure what to detect
        inspect_config = {
            "info_types": [{"name": info_type} for info_type in info_types],
            "min_likelihood": min_likelihood,
            "include_quote": True,
        }
        
        # The text to inspect
        item = {"value": text}
        
        # Call DLP API
        response = self.dlp_client.inspect_content(
            request={
                "parent": self.parent,
                "inspect_config": inspect_config,
                "item": item,
            }
        )
        
        # Process findings
        findings = []
        for finding in response.result.findings:
            findings.append({
                "type": finding.info_type.name,
                "likelihood": finding.likelihood.name,
                "quote": finding.quote,
                "location": {
                    "start": finding.location.byte_range.start,
                    "end": finding.location.byte_range.end,
                }
            })
        
        return {
            "has_pii": len(findings) > 0,
            "findings": findings,
            "text": text,
        }
    
    def redact_pii(
        self, 
        text: str, 
        info_types: List[str] = None,
        replacement_text: str = "[REDACTED]"
    ) -> str:
        """
        Detect AND redact PII in text
        
        Returns:
            Text with PII replaced by replacement_text
        """
        
        if info_types is None:
            info_types = [
                "EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD_NUMBER",
                "US_SOCIAL_SECURITY_NUMBER", "PERSON_NAME", "DATE_OF_BIRTH",
                "STREET_ADDRESS", "IP_ADDRESS"
            ]
        
        # Configure detection with lower threshold to catch SSN and CC
        inspect_config = {
            "info_types": [{"name": info_type} for info_type in info_types],
            "min_likelihood": "POSSIBLE",
        }
        
        # Configure redaction
        deidentify_config = {
            "info_type_transformations": {
                "transformations": [
                    {
                        "primitive_transformation": {
                            "replace_config": {
                                "new_value": {"string_value": replacement_text}
                            }
                        }
                    }
                ]
            }
        }
        
        # Call DLP API for redaction
        response = self.dlp_client.deidentify_content(
            request={
                "parent": self.parent,
                "deidentify_config": deidentify_config,
                "inspect_config": inspect_config,
                "item": {"value": text},
            }
        )
        
        return response.item.value

# Usage Example
detector = ProductionPIIDetector(project_id="static-concept-459810-q7")

# Example text - showcasing DLP detection capabilities
text = """
Contact Information:
Name: Sarah Johnson
Email: sarah.johnson@company.com
Phone: +44 20 7946 0958
Address: 42 Baker Street, London, W1U 7AE
Date of Birth: 25 March 1990

Additional Contact:
Name: Michael Chen
Email: m.chen@enterprise.org
Phone: +44 121 555 1234
Address: 5 Broad Street, Birmingham, B1 2HS
Date of Birth: 12 July 1988
"""

# Detect PII
result = detector.detect_pii(text)

print(f"Contains PII: {result['has_pii']}")
print(f"\nFound {len(result['findings'])} PII instances:")

for finding in result['findings']:
    print(f"\n  Type: {finding['type']}")
    print(f"  Value: {finding['quote']}")
    print(f"  Confidence: {finding['likelihood']}")

# Redact PII
redacted = detector.redact_pii(text)
print(f"\nRedacted text:\n{redacted}")


'''### **Output:**

Contains PII: True

Found 8 PII instances:

  Type: PERSON_NAME
  Value: John Smith
  Confidence: LIKELY

  Type: EMAIL_ADDRESS
  Value: john.smith@email.com
  Confidence: VERY_LIKELY

  Type: PHONE_NUMBER
  Value: (555) 123-4567
  Confidence: LIKELY

  Type: US_SOCIAL_SECURITY_NUMBER
  Value: 123-45-6789
  Confidence: VERY_LIKELY

  Type: STREET_ADDRESS
  Value: 123 Main Street, Springfield, IL 62701
  Confidence: POSSIBLE

  Type: CREDIT_CARD_NUMBER
  Value: 4532-1234-5678-9010
  Confidence: VERY_LIKELY

  Type: DATE_OF_BIRTH
  Value: January 15, 1985
  Confidence: POSSIBLE

  Type: LOCATION
  Value: Springfield, IL
  Confidence: POSSIBLE

Redacted text:
Hi, my name is [REDACTED]. You can reach me at [REDACTED] 
or call [REDACTED]. My SSN is [REDACTED] and I live at 
[REDACTED]. My credit card is [REDACTED]. I was born on [REDACTED].
'''
