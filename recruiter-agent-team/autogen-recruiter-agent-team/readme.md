# Recruitment Automation with AI Agents

## Overview

This project automates the process of analyzing resumes, scheduling interviews, and managing candidate communication using Conversable AI agents and tools like Zoom and Gmail. It streamlines the recruiting workflow, offering efficient and personalized interactions.

## Features

1. **Resume Analysis:**
   - Reads resumes and job descriptions using `read_file`.
   - Evaluates candidates strictly against the job requirements, while being lenient for AI/ML roles with strong potential.
   - Considers project experience as valid experience and prioritizes hands-on expertise with key technologies.

2. **Candidate Decision Workflow:**
   - If a candidate is not selected:
     - Generates a rejection email in Markdown format using `write_file`.
     - Sends the rejection email using `send_email`.
   - If a candidate is selected:
     - Schedules a Zoom meeting for the following week using `schedule_zoom_meeting`.
     - Crafts a congratulatory email including Zoom details in Markdown format.
     - Sends the email using `send_email`.

3. **Report Generation:**
   - Generates a brief report of the recruitment process in Markdown format and saves it to `report.md`.

4. **Logging and Cost Tracking:**
   - Logs all interactions for auditing and performance analysis.
   - Tracks usage tokens for cost estimation.

## Prerequisites

- Python 3.10+
- Required Python packages:
  - `pandas`
  - `autogen`
  - `dotenv`
  - `sqlite3`
- API credentials for Zoom and Gmail, configured in a `.env` file.
- A SQLite database (`logs.db`) for logging interaction data.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/fbellame/agent-comparison.git
   cd agent-comparison/recruiter-agent-team/autogen-recruiter-agent-team

2. Install the libs:
   ```bash
   pip install -r requirements.txt
   ```

3. Setup .env for OpenAI, Zoom and Gmail:
   ```bash
   OPENAI_API_KEY=
    ZOOM_ACCOUNT_ID=
    ZOOM_CLIENT_ID=
    ZOOM_CLIENT_SECRET=
    GMAIL_PASS_CODE=
   ```

4. Run the agent:
   ```bash
   python main.py
   ```
