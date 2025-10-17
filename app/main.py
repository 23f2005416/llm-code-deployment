from fastapi import FastAPI, BackgroundTasks, HTTPException
import requests
import asyncio
import time
from app.auth import verify_secret
from app.utils import Config

app = FastAPI(title="LLM Code Deployment API")

# Initialize configuration
Config.validate()

async def submit_to_evaluation(evaluation_url: str, payload: dict, max_retries: int = 5):
    """Submit results to evaluation URL with exponential backoff"""
    for attempt in range(max_retries):
        try:
            print(f"📤 Attempt {attempt + 1} to submit to evaluation URL...")
            response = requests.post(
                evaluation_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✅ Successfully submitted to evaluation URL")
                return True
            else:
                print(f"❌ Evaluation URL returned {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"⚠️  Error submitting to evaluation URL (attempt {attempt + 1}): {e}")
        
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt
            print(f"⏳ Retrying in {wait_time} seconds...")
            await asyncio.sleep(wait_time)
    
    print(f"💥 Failed to submit to evaluation URL after {max_retries} attempts")
    return False

async def process_build_request(request_data: dict):
    """Background task to process the build request"""
    try:
        print(f"🚀 Processing request for task: {request_data['task']} (Round {request_data['round']})")
        
        # TODO: Add actual LLM code generation here
        # TODO: Add actual GitHub repo creation here
        
        # Mock response for now
        mock_response = {
            "email": request_data["email"],
            "task": request_data["task"],
            "round": request_data["round"],
            "nonce": request_data["nonce"],
            "repo_url": f"https://github.com/user/repo-{request_data['task']}",
            "commit_sha": "mock_commit_123",
            "pages_url": f"https://user.github.io/repo-{request_data['task']}/"
        }
        
        # Submit to evaluation URL
        success = await submit_to_evaluation(request_data["evaluation_url"], mock_response)
        
        if success:
            print(f"🎉 Successfully processed task: {request_data['task']}")
        else:
            print(f"⚠️  Task processed but evaluation submission failed: {request_data['task']}")
            
    except Exception as e:
        print(f"💥 Error processing build request: {e}")

@app.post("/api/build")
async def build_endpoint(request: dict, background_tasks: BackgroundTasks):
    """Main build endpoint - accepts both round 1 and round 2 requests"""
    
    # Verify secret
    if not verify_secret(request.get("email", ""), request.get("secret", "")):
        raise HTTPException(status_code=403, detail="Invalid secret")
    
    # Validate required fields
    required_fields = ["email", "task", "round", "nonce", "brief", "evaluation_url"]
    for field in required_fields:
        if field not in request:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    print(f"📥 Received request: {request['task']} (Round {request['round']})")
    
    # Start background processing
    background_tasks.add_task(process_build_request, request)
    
    return {
        "status": "accepted",
        "message": f"Build request for round {request['round']} is being processed",
        "task": request["task"],
        "round": request["round"]
    }

@app.get("/health")
async def health_check():
    config_status = "configured" if Config.GITHUB_TOKEN and Config.OPENAI_API_KEY else "missing_keys"
    return {
        "status": "healthy", 
        "service": "student-build-api",
        "environment": "WSL + Windows Desktop",
        "config": config_status
    }

@app.get("/")
async def root():
    return {
        "message": "LLM Code Deployment API is running!",
        "endpoints": {
            "POST /api/build": "Accept build/revise requests",
            "GET /health": "Health check",
            "GET /docs": "API documentation"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)