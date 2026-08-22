from fastapi import FastAPI
from app.models.failure import FailureLog
from app.prompts.root_cause_prompt import build_root_cause_prompt
from app.services.ai_analyzer import AIAnalyzer
import json 

app = FastAPI()

ai_analyzer = AIAnalyzer()

@app.post("/errorAnalyze")
def analyze_error_logs(data: FailureLog):

    prompt = build_root_cause_prompt(
        data.build_id,
        data.error_log,
        data.recent_commit
    )

    response = ai_analyzer.analyze(prompt)

    clean_text = response.replace("```json", "").replace("```", "").strip()

    data_dict = json.loads(clean_text)

    responsible_commit_obj = data_dict.get("responsible_commit")

    cause = RootCause(
        responsible_commit=CommitInfo(
            commit_id=responsible_commit_obj.get("commit_id"),
            author=responsible_commit_obj.get("author"),
            commit_message=responsible_commit_obj.get("commit_message"),
            changed_lines=responsible_commit_obj.get("changed_lines")
        ),
        suspected_line=data_dict.get("suspected_line"),
        reason=data_dict.get("reason"),
        solution=data_dict.get("solution"),
        is_code_fix=data_dict.get("is_code_fix"),
        recommended_code=data_dict.get("recommended_code")
    )

    return cause