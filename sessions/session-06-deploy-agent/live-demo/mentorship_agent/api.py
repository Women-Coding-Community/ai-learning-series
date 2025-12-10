from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import asyncio
# Check that these ADK imports are correct
from google.adk.runners import InMemoryRunner
from google.genai import types
import google.generativeai as genai

# Import your existing agent
from agent import root_agent

app = FastAPI(title="Mentorship Agent API")

# Initialize Runner
runner = InMemoryRunner(agent=root_agent, app_name="mentorship_app")

class ChatRequest(BaseModel):
    session_id: str
    user_input: str
    user_id: str = "default_user"

class ChatResponse(BaseModel):
    response: str

@app.on_event("startup")
async def startup_event():
    print("Initializing Agent Runner...")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # Raise a clear error if the key is missing
        raise ValueError("GEMINI_API_KEY environment variable is not set. Cannot start agent.")
    
    # Configure the client globally for the application
    genai.configure(api_key=api_key)
    print("✅ Gemini client configured successfully.")
    # --------------------------------------------------------------------


# Optional: Add a health check endpoint for testing/Cloud Run
@app.get("/")
async def root():
    return {"message": "Mentorship Agent API is running! Go to /docs to test it."}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):

    try:
        await runner.session_service.create_session(
            app_name="mentorship_app",
            user_id=request.user_id,
            session_id=request.session_id
        )

        # --- 2. Prepare ADK content ---
        user_content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=request.user_input)]
        )

        full_response_text = ""
        
        # --- 3. Run the agent loop (The crucial fix is here) ---
        # The 'await' is correct, but sometimes the environment needs a simple 
        # structure to ensure the generator's __aiter__ is correctly recognized.
        
        # runner.run() is an async generator, we must use 'async for'
        async for event in runner.run_async(
            user_id=request.user_id,
            session_id=request.session_id,
            new_message=user_content
        ):
            if event.content and event.content.parts:
                part = event.content.parts[0]
                if part.text:
                    full_response_text += part.text

        if not full_response_text:
             return ChatResponse(response="I received your request, but the agent did not return a text response.")
             
        return ChatResponse(response=full_response_text)

    except Exception as e:
        # Print the detailed error for debugging in the server console
        print(f"FATAL ERROR IN CHAT ENDPOINT: {e}") 
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    # Cloud Run requires listening on 0.0.0.0 and the PORT env var
    import os
    port = int(os.environ.get("PORT", 8080))
    # Note: host='0.0.0.0' is necessary for Docker/Cloud Run
    uvicorn.run(app, host="0.0.0.0", port=port)