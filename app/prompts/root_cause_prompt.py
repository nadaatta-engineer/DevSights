def build_root_cause_prompt(build_id, error_log, recent_commit):
    return f"""
    You are an expert AI DevOps investigator. Your task is to perform Root Cause Correlation AND provide an actionable fix.

    Analyze the following failure log data:

    Build ID: {build_id}
    Error Log: {error_log}

    Recent Commit Info:
    Commit ID: {recent_commit.commit_id}
    Author: {recent_commit.author}
    Commit Message: {recent_commit.commit_message}
    Changed Lines: {",".join(recent_commit.changed_lines)}

    CRITICAL: you must return the response as a valid JSON object only, strictly following this scheme:
    {{
        "responsible_commit": {{
            "commit_id": "string",
            "author": "string",
            "commit_message": "string",
            "changed_lines": ["list of strings"]
        }},
        "suspected_line": "string",
        "reason": "string",
        "solution": "string",
        "is_code_fix": "boolean, to show whether the error will be solved by some code or not",
        "recommended_code": "string or null"
    }}

    Do not include any additional text, explanations, or markdown formatting like ```json.
    """