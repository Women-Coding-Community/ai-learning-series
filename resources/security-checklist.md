# Security Checklist for AI Applications

## API Key Management

### ✅ DO

- Store API keys in environment variables
- Use `.env` files for local development (add to `.gitignore`)
- Rotate keys regularly
- Use service accounts with minimal permissions
- Enable key restrictions (IP, API, etc.)

### ❌ DON'T

- Hardcode API keys in source code
- Commit `.env` files to Git
- Share API keys in messages or emails
- Use personal API keys for production
- Expose keys in logs or error messages

### Implementation

```python
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not API_KEY:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS not set")
```

## Input Validation

### Sanitize User Input

```python
def sanitize_input(user_input: str) -> str:
    """Remove potentially harmful content"""
    # Remove suspicious patterns
    suspicious_patterns = [
        "Ignore previous instructions",
        "System prompt",
        "Admin",
        "DELETE",
        "DROP"
    ]
    
    for pattern in suspicious_patterns:
        user_input = user_input.replace(pattern, "")
    
    return user_input.strip()
```

### Validate Input Length

```python
MAX_INPUT_LENGTH = 5000

def validate_input(user_input: str) -> bool:
    if len(user_input) > MAX_INPUT_LENGTH:
        raise ValueError(f"Input too long (max {MAX_INPUT_LENGTH})")
    if len(user_input) < 1:
        raise ValueError("Input cannot be empty")
    return True
```

## Rate Limiting

### Prevent Abuse

```python
from datetime import datetime, timedelta
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests=10, window_seconds=60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, user_id: str) -> bool:
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.window_seconds)
        
        # Remove old requests
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if req_time > cutoff
        ]
        
        if len(self.requests[user_id]) >= self.max_requests:
            return False
        
        self.requests[user_id].append(now)
        return True

# Usage
limiter = RateLimiter(max_requests=10, window_seconds=60)

if not limiter.is_allowed(user_id):
    raise Exception("Rate limit exceeded")
```

## Error Handling

### Don't Expose Sensitive Info

```python
# ❌ BAD - Exposes internal details
except Exception as e:
    print(f"Error: {e}")  # Might expose API keys or paths

# ✅ GOOD - Generic error message
except Exception as e:
    logger.error(f"API Error: {str(e)}")
    return "An error occurred. Please try again."
```

### Log Securely

```python
import logging

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_safely(message: str):
    """Log without exposing sensitive data"""
    # Remove API keys from message
    safe_message = message.replace(API_KEY, "[REDACTED]")
    logging.info(safe_message)
```

## Data Privacy

### Encrypt Sensitive Data

```python
from cryptography.fernet import Fernet

def encrypt_data(data: str, key: bytes) -> str:
    cipher = Fernet(key)
    encrypted = cipher.encrypt(data.encode())
    return encrypted.decode()

def decrypt_data(encrypted_data: str, key: bytes) -> str:
    cipher = Fernet(key)
    decrypted = cipher.decrypt(encrypted_data.encode())
    return decrypted.decode()
```

### Handle User Data Responsibly

```python
# ✅ DO
- Ask for consent before storing user data
- Store only necessary information
- Delete data when no longer needed
- Comply with GDPR/CCPA

# ❌ DON'T
- Store passwords in plain text
- Share user data with third parties
- Keep data longer than necessary
- Ignore privacy regulations
```

## Dependency Security

### Keep Dependencies Updated

```bash
# Check for vulnerabilities
pip install safety
safety check

# Update packages
pip install --upgrade -r requirements.txt
```

### Use Specific Versions

```bash
# requirements.txt
google-cloud-aiplatform==1.26.0  # ✅ Specific version
vertexai>=0.1.0,<1.0.0           # ✅ Version range
streamlit                         # ❌ No version specified
```

## Authentication

### Implement User Authentication

```python
import hashlib

def hash_password(password: str) -> str:
    """Hash password securely"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hash: str) -> bool:
    """Verify password"""
    return hash_password(password) == hash
```

### Use OAuth for Web Apps

```python
# Example with Google OAuth
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    'service-account-key.json',
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)
```

## Monitoring & Logging

### Track API Usage

```python
import json
from datetime import datetime

def log_api_call(user_id: str, prompt: str, response: str):
    """Log API calls for monitoring"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "prompt_length": len(prompt),
        "response_length": len(response),
        "cost_estimate": calculate_cost(prompt, response)
    }
    
    with open("api_usage.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
```

### Set Up Alerts

```python
def check_usage_limits(user_id: str):
    """Alert if usage exceeds limits"""
    daily_limit = 1000  # API calls per day
    current_usage = get_user_usage(user_id)
    
    if current_usage > daily_limit * 0.8:
        send_alert(f"User {user_id} approaching limit")
    
    if current_usage > daily_limit:
        raise Exception("Daily limit exceeded")
```

## Deployment Security

### Environment Variables

```bash
# .env (local development only)
GCP_PROJECT_ID=my-project
GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json

# Production (use Cloud Secret Manager)
gcloud secrets create api-key --data-file=key.json
```

### HTTPS Only

```python
# Streamlit config
[server]
sslMode = "auto"
```

### CORS Configuration

```python
# For web APIs
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["https://yourdomain.com"]}})
```

## Compliance Checklist

- ✅ GDPR compliant (if serving EU users)
- ✅ CCPA compliant (if serving California users)
- ✅ Data retention policy defined
- ✅ User consent collected
- ✅ Privacy policy published
- ✅ Security policy documented
- ✅ Incident response plan ready

## Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Google Cloud Security Best Practices](https://cloud.google.com/docs/security)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

## Quick Security Audit

```bash
# Check for exposed secrets
git log -p | grep -i "password\|api_key\|secret"

# Check dependencies
pip install safety
safety check

# Check code quality
pip install pylint
pylint your_code.py
```

---

**Remember:** Security is ongoing, not one-time. Review and update regularly!
