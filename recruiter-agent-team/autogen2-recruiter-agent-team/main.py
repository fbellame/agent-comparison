import os
from datetime import datetime
from dotenv import load_dotenv
import json

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Tool imports
from tools.zoom_meeting import schedule_zoom_meeting
from tools.gmail_email import send_email
from tools.file_system_tools import read_file, write_file

# -------------------------------
# 1. Configuration & Environment
# -------------------------------
load_dotenv()  # Load environment variables if needed

LLM_CONFIG = {
    "model": os.getenv("MODEL_NAME", "gpt-4o-mini"),
    "cache_seed": None,
}

def get_file_list_from_path(path: str) -> list[str]:
    return [
        os.path.join(path, f)
        for f in os.listdir(path)
        if os.path.isfile(os.path.join(path, f))
    ]

def load_prompt(file_path: str) -> str:
    """Loads a text prompt from a file."""
    with open(file_path, 'r') as file:
        return file.read()

def load_vars(file_path: str) -> dict:
    """Loads variables from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def format_prompt(prompt: str, variables: dict) -> str:
    """Formats a prompt by replacing placeholders with variable values."""
    return prompt.format(**variables)

async def main() -> None:
    
    # 0. Get tools
    tools = [read_file, write_file, send_email, schedule_zoom_meeting]
    
    # 1. Create the recruiter agent
    recruiter_agent = AssistantAgent(
        name="recruiter_agent",
        model_client=OpenAIChatCompletionClient(
            model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
        ),
        system_message=(
            "You are an expert technical recruiter with deep expertise in analyzing "
            "resumes and matching candidates to job descriptions. Return 'TERMINATE' "
            "when the task is done."
        ),
        tools=tools,
    )

    # 2. Create the agent team
    agent_team = RoundRobinGroupChat([recruiter_agent], max_turns=10)

    # 3. Load and Format Prompt
    prompt_path = "/media/farid/data1/projects/agent-comparison/recruiter-agent-team/prompt/user_message.txt"
    vars_path = "/media/farid/data1/projects/agent-comparison/recruiter-agent-team/prompt/variables.json"

    raw_prompt = load_prompt(prompt_path)
    variables = load_vars(vars_path)

    # 4. Collect File Lists
    jd_files = get_file_list_from_path(variables["JD_PATH"])
    resume_files = get_file_list_from_path(variables["RESUME_PATH"])

    # 5. Add dynamic variables
    variables.update({
        "jd_files": jd_files,
        "resume_files": resume_files,
        "current_date": datetime.now().date(),
    })

    # 5. Generate prompt with variables
    task_message = format_prompt(raw_prompt, variables)    

    # 6. Run the team and stream messages
    stream = agent_team.run_stream(task=task_message)
    await Console(stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())