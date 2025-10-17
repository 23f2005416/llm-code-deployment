import hashlib
from app.utils import Config

# Simple in-memory store for development
# In production, this would query a database
SECRET_STORE = {}

def register_secret(email: str, secret: str):
    """Register a secret for a student (simulate Google Form submission)"""
    SECRET_STORE[email] = secret

def verify_secret(email: str, secret: str) -> bool:
    """
    Verify if the provided secret matches what was submitted
    """
    # For development, accept any secret if none registered
    if email not in SECRET_STORE:
        print(f"⚠️  No secret registered for {email}, accepting for development")
        SECRET_STORE[email] = "dev-secret"
    
    return secret == SECRET_STORE.get(email)

# Pre-register some test secrets
register_secret("student@example.com", "test123")
register_secret("test@test.com", "test123")