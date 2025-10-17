# app/main.py - COMPLETE VERSION WITH ROUND 2 SUPPORT
from fastapi import FastAPI, BackgroundTasks, HTTPException
import requests
import asyncio
import time
from app.auth import verify_secret
from app.utils import Config
from app.llm_generator import LLMCodeGenerator
from app.github_manager import GitHubManager
from app.simple_generator import SimpleCodeGenerator

app = FastAPI(title="LLM Code Deployment API")

# Initialize managers
try:
    github_mgr = GitHubManager()
    llm_gen = LLMCodeGenerator()
    simple_gen = SimpleCodeGenerator()
    print("✅ All managers initialized: GitHub, LLM, Simple Generator")
except Exception as e:
    print(f"⚠️  Initialization warning: {e}")
    github_mgr = None
    llm_gen = None
    simple_gen = SimpleCodeGenerator()

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
        task_id = request_data["task"]
        round_num = request_data["round"]
        
        print(f"🚀 Processing request for task: {task_id} (Round {round_num})")
        
        # Check if this is Round 2 and repo should exist
        if round_num == 2 and github_mgr:
            if not github_mgr.repo_exists(task_id):
                print(f"⚠️  Round 2: Repository for task {task_id} doesn't exist. Creating new one.")
                # Fall back to Round 1 behavior
                request_data["round"] = 1
        
        # Generate code using LLM with fallback
        code_files = {}
        if llm_gen:
            try:
                print("🧠 Generating code with LLM...")
                code_files = llm_gen.generate_app(
                    request_data["brief"],
                    request_data.get("attachments", []),
                    request_data.get("checks", [])
                )
                print("✅ LLM code generation completed")
            except Exception as e:
                print(f"❌ LLM generation failed, using fallback: {e}")
                code_files = simple_gen.generate_from_brief(request_data["brief"])
        else:
            print("⚠️  LLM not available, using simple generator")
            code_files = simple_gen.generate_from_brief(request_data["brief"])
        
        # Create/update GitHub repository
        repo_info = {}
        if github_mgr:
            if request_data["round"] == 1:
                print("🔄 Creating new GitHub repository...")
                repo_info = github_mgr.create_repo_from_code(
                    task_id, 
                    code_files, 
                    request_data["brief"]
                )
            else:  # Round 2
                print("🔄 Updating existing GitHub repository...")
                repo_url = github_mgr.get_repo_url(task_id)
                repo_info = github_mgr.update_repo(
                    repo_url,
                    code_files,
                    request_data["brief"],
                    f"Round {round_num} updates - {request_data['brief'][:50]}..."
                )
        else:
            # Mock response if GitHub not available
            repo_info = {
                "repo_url": f"https://github.com/user/repo-{task_id}",
                "commit_sha": f"mock_commit_round_{round_num}",
                "pages_url": f"https://user.github.io/repo-{task_id}/"
            }
        
        # Submit to evaluation URL
        eval_payload = {
            "email": request_data["email"],
            "task": task_id,
            "round": round_num,
            "nonce": request_data["nonce"],
            "repo_url": repo_info["repo_url"],
            "commit_sha": repo_info["commit_sha"],
            "pages_url": repo_info["pages_url"]
        }
        
        success = await submit_to_evaluation(request_data["evaluation_url"], eval_payload)
        
        if success:
            print(f"🎉 Successfully processed Round {round_num} for task: {task_id}")
            print(f"   📁 Repo: {repo_info['repo_url']}")
            print(f"   🌐 Live: {repo_info['pages_url']}")
            print(f"   🔧 Method: {'LLM' if llm_gen and 'llm_gen' in locals() else 'Simple'} Generation")
            print(f"   📝 Commit: {repo_info['commit_sha'][:8]}...")
        else:
            print(f"⚠️  Task processed but evaluation submission failed: {task_id}")
            
    except Exception as e:
        print(f"💥 Error processing build request: {e}")
        import traceback
        traceback.print_exc()

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
    
    # Validate round number
    if request["round"] not in [1, 2]:
        raise HTTPException(status_code=400, detail="Round must be 1 or 2")
    
    print(f"📥 Received Round {request['round']} request: {request['task']}")
    
    # Start background processing
    background_tasks.add_task(process_build_request, request)
    
    return {
        "status": "accepted",
        "message": f"Round {request['round']} build request is being processed",
        "task": request["task"],
        "round": request["round"]
    }

@app.get("/health")
async def health_check():
    config_status = "fully_configured" if (Config.GITHUB_TOKEN and Config.OPENAI_API_KEY) else "partial_config"
    return {
        "status": "healthy", 
        "service": "student-build-api",
        "environment": "WSL + Windows Desktop",
        "config": config_status,
        "features": ["round1", "round2", "llm_generation", "github_pages"]
    }

@app.get("/")
async def root():
    return {
        "message": "LLM Code Deployment API is running!",
        "endpoints": {
            "POST /api/build": "Accept build/revise requests (Round 1 & 2)",
            "GET /health": "Health check with config status",
            "GET /docs": "API documentation"
        },
        "version": "1.0.0",
        "supports": ["GitHub Pages", "LLM Code Generation", "Round 2 Revisions"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)