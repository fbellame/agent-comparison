import os
from datetime import datetime
from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Tool imports
from tools.zoom_meeting import schedule_zoom_meeting
from tools.gmail_email import send_email
from tools.file_system_tools import read_file, write_file, get_file_list_from_path
from utils import format_prompt, load_prompt, load_vars

# -------------------------------
# 1. Configuration & Environment
# -------------------------------
load_dotenv()  # Load environment variables if needed

async def main() -> None:
    
    # 0. Get tools
    tools = [read_file, write_file, get_file_list_from_path, send_email, schedule_zoom_meeting]
    
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
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of this script
    prompt_dir = os.path.join(script_dir, '..', 'prompt')  # Prompt folder is one level up

    prompt_path = os.path.join(prompt_dir, "user_message.txt")
    vars_path = os.path.join(prompt_dir, "variables.json")

    raw_prompt = load_prompt(prompt_path)
    variables = load_vars(vars_path)

    # 4. Add dynamic variables
    variables.update({
        "current_date": datetime.now().date(),
        "location": "Montreal"
    })

    # 5. Generate prompt with variables
    task_message = format_prompt(raw_prompt, variables)    

    # 6. Run the team and stream messages
    stream = agent_team.run_stream(task=task_message)
    await Console(stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
