import json
from typing import Dict, Any, Optional
from models.task import Task, Result
from agent.llm import openai_client

async def verify_task(task: Task) -> Optional[Result]:
    # Check if any action failed
    failed_actions = [a for a in task.actions if a.status == "failed"]
    if failed_actions:
        return None # Task fails if there are unrecovered failed actions
        
    # Aggregate summaries from all completed actions
    summaries = []
    for i, action in enumerate(task.actions):
        if action.status == "completed":
            summaries.append(f"Step {i+1} ({action.tool}): {action.summary}")
            
    final_summary_log = "\n".join(summaries)
    if not final_summary_log:
        return Result(
            type="generic",
            status="verified",
            title="Task Completed",
            summary="Task completed successfully with no output.",
            evidence=["0 tools executed"]
        )
        
    system_prompt = """
    You are ALFRED, an advanced AI assistant. Your task is to summarize the results of your execution.
    The user asked you to achieve a GOAL. You executed several tools.
    Here is the log of your executed steps:
    {log}
    
    Write a concise, natural, and helpful response to the user summarizing what you accomplished.
    If you found information (like 5 emails), state it directly (e.g., "Yes, you received 5 new mails").
    If you created a file or modified a file, mention it clearly.
    
    Output JSON format ONLY:
    {{
      "summary": "Your conversational response here",
      "file_name": "filename if a file was created or edited, otherwise null"
    }}
    """
    
    prompt = system_prompt.format(log=final_summary_log)
    
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"GOAL: {task.goal}"}
            ],
            response_format={ "type": "json_object" },
            temperature=0.0
        )
        
        result_json = json.loads(response.choices[0].message.content)
        final_summary = result_json.get("summary", "Task completed.")
        file_name = result_json.get("file_name")
        
        return Result(
            type="generic",
            status="verified",
            title="Task Completed",
            summary=final_summary,
            file_name=file_name,
            evidence=[f"{len(task.actions)} tools executed"]
        )
    except Exception as e:
        print(f"Verifier LLM failed: {e}")
        return Result(
            type="generic",
            status="verified",
            title="Task Completed",
            summary="Task completed, but could not generate a conversational summary.",
            evidence=[f"{len(task.actions)} tools executed"]
        )
