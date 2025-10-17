import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SECRET_SALT = os.getenv("SECRET_SALT", "default-secret-salt")
    
    @classmethod
    def validate(cls):
        """Check if all required environment variables are set"""
        missing = []
        if not cls.GITHUB_TOKEN:
            missing.append("GITHUB_TOKEN")
        if not cls.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")
        
        if missing:
            print(f"⚠️  Warning: Missing environment variables: {', '.join(missing)}")
            print("   The app will run but certain features may not work.")
        else:
            print("✅ All environment variables are set!")