from fastapi import FastAPI
from google import genai
import json
import os
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class CodeChange(BaseModel):
    repo_name : str
    branch : str
    modified_files : list[str]
    commit_message : str

class CommitInfo(BaseModel):
    commit_id : str
    author : str
    commit_message : str
    changed_lines : list[str]
    
class FailureLog(BaseModel):
    build_id : str
    error_log : str
    recent_commit : CommitInfo
    
class RemediationRequest(BaseModel):
    build_id : str
    proposed_code : str
    commit_message : str = "Fix error log"

class TestResponse(BaseModel):
    recommended_tests : list[str]
    skippes_tests_count : int
    time_saved : float

class RootCause(BaseModel):
    responsible_commit : CommitInfo
    suspected_line : str
    reason : str
    solution : str
    is_code_fix : bool
    recommended_code : Optional[str] = None #it may not exist

class RedemiationResponse(BaseModel):
    success : bool
    pr_url : Optional[str] = None #it may not exist
    message : str

##prepare the LLM we use:

key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key = key)

##prepare the end points:

#1.
@app.post("/errorAnalyze")

def analyze_error_logs(data : FailureLog):
    response = client.models.generate_content(
        model = "gemini-3.5-flash",
        contents = f"""
        You are an expert AI DevOps investigator. Your task is to perform Root Cause Correlation AND provide an actionable fix.
        
        Analyze the following failure log data:
        
        Build ID: {data.build_id}
        Error Log: {data.error_log}
        
        Recent Commit Info :
        Commit ID : {data.recent_commit.commit_id}
        Author : {data.recent_commit.author}
        Commit Message : {data.recent_commit.commit_message}
        Changed Lines : {','.join(data.recent_commit.changed_lines)}
        
        CRITICAL : you must return the response as a valid JSON object only , strictly following this scheme :
        {{
        "responsible_commit": {{
            "commit_id": "string",
            "author": "string",
            "commit_message": "string",
            "changed_lines": ["list of strings"]
        }},
        "suspected_line": "string"
        "reason": "string",
        "solution": "string",
        "is_code_fix": boolean, to show wether the error will be solved by some code or not
        "recommended_code": "string or null"
        }}
        Do not include any additional text, explanations, or markdown formatting like ```json.
        
        """
        )
    # to clean the text 
    clean_text = response.text.replace("```json", "").replace("```", "").strip()
    #invert the text to direction
    data_dict = json.loads(clean_text)
    
    responsible_commit_obj = data_dict.get("responsible_commit")
    
    cause = RootCause(
        responsible_commit = CommitInfo(
            commit_id = responsible_commit_obj.get("commit_id"),
            author = responsible_commit_obj.get("author"),
            commit_message = responsible_commit_obj.get("commit_message"),
            changed_lines = responsible_commit_obj.get("changed_lines"),
            ),
        suspected_line = data_dict.get("suspected_line"),
        reason = data_dict.get("reason"),
        solution = data_dict.get("solution"),
        is_code_fix = data_dict.get("is_code_fix"),
        recommended_code = data_dict.get("recommended_code")
        )
    return cause
    

