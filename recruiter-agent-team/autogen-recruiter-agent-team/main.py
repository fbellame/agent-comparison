"""
Example Refactor of ConversableAgent Recruiting Automation
=========================================================

This script demonstrates a more modular approach to setting up
and running a recruiting workflow with AI-driven tools.
"""

import os
import time
import json
import pandas as pd
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

# AutoGen / Conversable Agent imports
from autogen import ConversableAgent
from autogen import register_function
import autogen.runtime_logging

# Tool imports
from tools.zoom_meeting import schedule_zoom_meeting
from tools.gmail_email import send_email

# -------------------------------
# 1. Configuration & Environment
# -------------------------------
load_dotenv()  # Load environment variables if needed

JD_PATH = os.getenv("JD_PATH", "/media/farid/data1/projects/agent-comparison/recruiter-agent-team/autogen-recruiter-agent-team/data/jd")
RESUME_PATH = os.getenv("RESUME_PATH", "/media/farid/data1/projects/agent-comparison/recruiter-agent-team/autogen-recruiter-agent-team/data/resume")

RECRUITER_NAME = os.getenv("RECRUITER_NAME", "Franck Le Recruteur")
COMPANY = os.getenv("COMPANY", "The Best AI company")

LLM_CONFIG = {
    "model": os.getenv("MODEL_NAME", "gpt-4o-mini"),
    "cache_seed": None,
}

# -------------------------------
# 2. Utility Functions
# -------------------------------
def read_file(file_path: str) -> str:
    """Reads and returns the content of a file."""
    with open(file_path, "r") as file:
        return file.read()

def write_file(file_path: str, content: str) -> None:
    """Writes content to a file."""
    with open(file_path, "w") as file:
        file.write(content)

def get_file_list_from_path(path: str) -> list[str]:
    """Returns a list of full file paths from a directory."""
    return [
        os.path.join(path, f)
        for f in os.listdir(path)
        if os.path.isfile(os.path.join(path, f))
    ]

def start_logging(dbname: str = "logs.db") -> int:
    """
    Starts runtime logging using autogen.
    Returns the session ID.
    """
    config = {"dbname": dbname}
    session_id = autogen.runtime_logging.start(config=config)
    print(f"Logging session ID: {session_id}")
    return session_id

def stop_logging() -> None:
    """Stops runtime logging."""
    autogen.runtime_logging.stop()

def fetch_log_data(dbname="logs.db", table="chat_completions") -> list[dict]:
    """Fetches log data from the sqlite database and returns it as a list of dictionaries."""
    try:
        con = sqlite3.connect(dbname)
        query = f"SELECT * FROM {table}"
        cursor = con.execute(query)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        data = [dict(zip(column_names, row)) for row in rows]
        con.close()
        return data
    except sqlite3.Error as e:
        print("Error accessing the database:", e)
        return []

def str_to_dict(s: str) -> dict:
    """Helper function to safely convert JSON strings to Python dictionaries."""
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return {}

# -------------------------------
# 3. Tool Registration
# -------------------------------
def register_all_tools(assistant_agent: ConversableAgent, user_agent: ConversableAgent) -> None:
    """
    Registers all necessary tools (functions) with the assistant and user proxy agents.
    """
    # Zoom meeting
    schedule_zoom_description = """
        Schedule a Zoom meeting.
        Parameters:
        - topic (str): The topic/title of the meeting.
        - start_time (str): Start time in 'yyyy-MM-ddTHH:mm:ss' format (UTC).
        - duration (int): Duration of the meeting in minutes.
        Returns:
        - dict: Response from the Zoom API.
    """
    register_function(
        schedule_zoom_meeting,
        caller=assistant_agent,
        executor=user_agent,
        name="schedule_zoom_meeting",
        description=schedule_zoom_description
    )

    # File reading
    register_function(
        read_file,
        caller=assistant_agent,
        executor=user_agent,
        name="read_file",
        description="Read a file and return its content."
    )

    # File writing
    register_function(
        write_file,
        caller=assistant_agent,
        executor=user_agent,
        name="write_file",
        description="Write content to a specified file."
    )

    # Sending email
    register_function(
        send_email,
        caller=assistant_agent,
        executor=user_agent,
        name="send_email",
        description="Send an email."
    )

# -------------------------------
# 4. Agents Setup
# -------------------------------
def create_agents(llm_config: dict) -> tuple[ConversableAgent, ConversableAgent]:
    """
    Creates and returns the Assistant and User proxy agents configured with the given LLM settings.
    """
    assistant = ConversableAgent(
        name="Assistant",
        system_message=(
            "You are a helpful AI assistant. "
            "Return 'TERMINATE' when the task is done."
        ),
        llm_config=llm_config,
    )

    user_proxy = ConversableAgent(
        name="User",
        llm_config=llm_config,
        is_termination_msg=lambda x: x.get("content", "") and "TERMINATE" in x.get("content", ""),
        human_input_mode="NEVER",
    )

    return assistant, user_proxy

# -------------------------------
# 5. Main Flow
# -------------------------------
def main():
    start_time = time.time()

    # 1. Start logging
    session_id = start_logging(dbname="logs.db")

    # 2. Prepare Agents
    assistant, user_proxy = create_agents(LLM_CONFIG)

    # 3. Register Tools
    register_all_tools(assistant, user_proxy)

    # 4. Collect File Lists
    jd_files = get_file_list_from_path(JD_PATH)
    resume_files = get_file_list_from_path(RESUME_PATH)

    # 5. Build User Instruction (User->Assistant)
    current_date = datetime.now().date()
    user_message = f"""
    You are an expert technical recruiter with deep expertise in analyzing resumes and matching candidates to job descriptions.

    **Recruiting Company Information:**
    - Recruiter Name: {RECRUITER_NAME}
    - Company: {COMPANY}

    **Current Date:** {current_date}

    ### Task Instructions:

    1. **Resume Analysis:**
       - Analyze the provided resumes against the job descriptions in detail, adhering to the following guidelines:
         - Job Description Files: {jd_files}
         - Candidate Resume Files: {resume_files}
       - Use the `read_file` tool to read and extract relevant details from both resumes and job descriptions.
       - Maintain strict criteria for minimum experience, but:
         - Be lenient with AI/ML candidates demonstrating strong potential.
         - Consider project experience as valid professional experience.
         - Prioritize hands-on experience with key technologies.
       - Return a JSON response for each candidate with:
         - A selection decision (selected/rejected)
         - Detailed feedback justifying the decision.

    2. **Candidate Communication:**
       - **Rejected Candidates:**
         - Craft a professional rejection email in Markdown format using the `file_write` tool.
       - **Selected Candidates:**
         - Schedule a Zoom meeting for the following week using the `zoom_meeting` tool.
         - Craft a congratulatory email in Markdown format that includes Zoom meeting details.
         - Save the email using `file_write` and send it using `send_email`.

    3. **Activity Reporting:**
       - Summarize all actions taken (resume analysis, selection decisions, communications) in a concise report.
       - Save the report as `report.md` in Markdown format using the appropriate tool.
    """

    # 6. Begin Chat
    chat_result = user_proxy.initiate_chat(assistant, message=user_message)
    print("Chat cost info:", chat_result.cost)

    print(f"--- {time.time() - start_time} seconds ---")

    # 7. Stop Logging
    stop_logging()

    # 8. Retrieve and Process Logs
    log_data = fetch_log_data(dbname="logs.db")
    log_df = pd.DataFrame(log_data)

    if not log_df.empty:
        # Extract usage information
        log_df["total_tokens"] = log_df.apply(
            lambda row: str_to_dict(row["response"]).get("usage", {}).get("total_tokens", None),
            axis=1
        )

        # Extract the request content
        log_df["request"] = log_df.apply(
            lambda row: str_to_dict(row["request"])["messages"][0]["content"]
            if "messages" in str_to_dict(row["request"])
            else None,
            axis=1
        )

        # Extract the response content
        log_df["response"] = log_df.apply(
            lambda row: str_to_dict(row["response"]).get("choices", [{}])[0]
                        .get("message", {})
                        .get("content", None),
            axis=1
        )

        print("Requests:\n", log_df["request"])

if __name__ == "__main__":
    main()
