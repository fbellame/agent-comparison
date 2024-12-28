from datetime import datetime
from autogen import ConversableAgent
from autogen import register_function
import pprint

from dotenv import load_dotenv
load_dotenv()
from autogen import ConversableAgent
from tools.zoom_meeting import schedule_zoom_meeting
from tools.gmail_email import send_email
import time
import autogen
import json
import pandas as pd
import os

llm_config = {
    "model": "gpt-4o-mini",
    "cache_seed": None,
    }

start_time = time.time()
logging_session_id = autogen.runtime_logging.start(config={"dbname": "logs.db"})

def read_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()

def write_file(file_path: str, content: str) -> None:
    with open(file_path, "w") as file:
        file.write(content)

# Let's first define the assistant agent that suggests tool calls.
assistant = ConversableAgent(
    name="Assistant",
    system_message="You are a helpful AI assistant. "
    "Return 'TERMINATE' when the task is done.",
    llm_config=llm_config,
)

# The user proxy agent is used for interacting with the assistant agent
# and executes tool calls.
user_proxy = ConversableAgent(
    name="User",
    llm_config=llm_config,
    #is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    is_termination_msg=lambda x: x.get("content", "") and "TERMINATE" in x.get("content", ""),
    human_input_mode="NEVER",
)

# Register the calculator function to the two agents.

description = """
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
    caller=assistant,  
    executor=user_proxy, 
    name="schedule_zoom_meeting",  # By default, the function name is used as the tool name.
    description=description
)

# Register the read_file function to the two agents.
register_function(
    read_file,
    caller=assistant,  # The assistant agent can suggest calls to the read_file function.
    executor=user_proxy,  # The user proxy agent can execute the read_file calls.
    name="read_file",  # By default, the function name is used as the tool name.
    description="Read a file",  # A description of the tool.
)

# Register the write_file function to the two agents.
register_function(
    write_file,
    caller=assistant,  # The assistant agent can suggest calls to the write_file function.
    executor=user_proxy,  # The user proxy agent can execute the write_file calls.
    name="write_file",  # By default, the function name is used as the tool name.
    description="Write to a file",  # A description of the tool.
)

# Register the write_file function to the two agents.
register_function(
    send_email,
    caller=assistant,  # The assistant agent can suggest calls to the write_file function.
    executor=user_proxy,  # The user proxy agent can execute the write_file calls.
    name="send_email",  # By default, the function name is used as the tool name.
    description="Send an email",  # A description of the tool.
)

jd_path = "/media/farid/data1/projects/agent-comparison/recruiter-agent-team/autogen-recruiter-agent-team/data/jd"
jd_files = [os.path.join(jd_path, f) for f in os.listdir(jd_path)]

resume_path = "/media/farid/data1/projects/agent-comparison/recruiter-agent-team/autogen-recruiter-agent-team/data/resume"
resumes_files = [os.path.join(resume_path, f) for f in os.listdir(resume_path)]

# Get the current date
current_date = datetime.now().date()

recruiter_name = "Franck Le Recruteur"
company = "The Best AI company"

user_message = f"""
You are an expert technical recruiter with deep expertise in analyzing resumes and matching candidates to job descriptions.

**Recruiting Company Information:**
- Recruiter Name: {recruiter_name}
- Company: {company}

**Current Date:** {current_date}

### Task Instructions:

1. **Resume Analysis:**
   - Analyze the provided resumes against the job descriptions in detail, adhering to the following guidelines:
     - Job Description Files: {jd_files}
     - Candidate Resume Files: {resumes_files}
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

# Start logging
print("Logging session ID: " + str(logging_session_id))

chat_result = user_proxy.initiate_chat(assistant, message=user_message)

pprint.pprint(chat_result.cost)
#print needed time
print("--- %s seconds ---" % (time.time() - start_time))

autogen.runtime_logging.stop()

def get_log(dbname="logs.db", table="chat_completions"):
    import sqlite3

    con = sqlite3.connect(dbname)
    query = f"SELECT * from {table}"
    cursor = con.execute(query)
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    data = [dict(zip(column_names, row)) for row in rows]
    con.close()
    return data

def str_to_dict(s):
    return json.loads(s)


log_data = get_log()
log_data_df = pd.DataFrame(log_data)

log_data_df["total_tokens"] = log_data_df.apply(
    lambda row: str_to_dict(row["response"])["usage"]["total_tokens"], axis=1
)

log_data_df["request"] = log_data_df.apply(lambda row: str_to_dict(row["request"])["messages"][0]["content"], axis=1)

log_data_df["response"] = log_data_df.apply(
    lambda row: str_to_dict(row["response"])["choices"][0]["message"]["content"], axis=1
)

print(log_data_df["request"])