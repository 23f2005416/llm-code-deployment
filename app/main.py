from fastapi import FastAPI, BackgroundTasks
import requests
import asyncio

app = FastAPI(title="LLM Code Deployment API")

async def process_build_request(request_data: dict):
    """Background task to process the build request"""
    print(f"🚀 Processing request for task: {request_data['task']}")
    
    # Mock response for testing
    mock_response = {
        "email": request_data["email"],
        "task": request_data["task"],
        "round": request_data["round"],
        "nonce": request_data["nonce"],
        "repo_url": "https://github.com/user/mock-repo",
        "commit_sha": "mock123",
        "pages_url": "https://user.github.io/mock-repo/"
    }
    
    # Try to call evaluation URL
    try:
        response = requests.post(
            request_data["evaluation_url"],
            json=mock_response,
            timeout=10
        )
        print(f"✅ Evaluation response: {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to call evaluation URL: {e}")

@app.post("/api/build")
async def build_endpoint(request: dict, background_tasks: BackgroundTasks):
    """Main build endpoint - accepts both round 1 and round 2 requests"""
    print(f"📥 Received request: {request.get('task')} (Round {request.get('round', 1)})")
    
    background_tasks.add_task(process_build_request, request)
    
    return {
        "status": "accepted",
        "message": f"Build request for round {request.get('round', 1)} is being processed",
        "task": request.get("task", "unknown"),
        "round": request.get("round", 1)
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "student-build-api",
        "environment": "WSL + Windows Desktop"
    }

@app.get("/")
async def root():
    return {"message": "LLM Code Deployment API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
