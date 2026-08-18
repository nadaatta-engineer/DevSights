from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from config import Config



key = Config["API_KEY"]
client = genai.Client(api_key = key)

app = FastAPI()

class log (BaseModel):
        error_log : str
        recent_commits : str

@app.post("/analyze")

def error_analysis(data : log):
    response = client.models.generate_content(
        model = "gemini-3.5-flash",
        contents=f"""
    You are an expert AI DevOps investigator. Your task is to perform Root Cause Correlation AND provide an actionable fix.
    
    Here is the Error Log:
    {data.error_log}
    
    Here are the recent GitHub/GitLab Commits and changes:
    {data.recent_commits}
    
    Analyze both together and return the response in this exact structured format (keep it brief and straight to the point):
    
    ### 🔍 Root Cause Analysis
    - **Responsible Commit:** [Commit Hash / ID]
    - **Developer / Author:** [Who made the change]
    - **Exact File & Line:** [File path and line number causing the issue]
    - **Root Cause Explanation:** [Why this specific code change triggered this error log]
    
    ### 🛠️ Proposed Fix
    - **Solution:** [Brief explanation of how to fix it]
    - **Fixed Code Snippet:** [The corrected code or git fix if applicable]
    
    Keep it precise and actionable.
    """
        )
    return {"analysis": response.text}


    
    
