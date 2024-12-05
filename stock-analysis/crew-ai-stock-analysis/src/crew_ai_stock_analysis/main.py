#!/usr/bin/env python
import sys
from crew_ai_stock_analysis.crew import CrewAiStockAnalysisCrew
from dotenv import load_dotenv
import agentops
import os

# Load environment variables from .env file
load_dotenv()

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"), default_tags=["stock_research"])

    inputs = {
        'ticker': 'NVDA'
    }
    CrewAiStockAnalysisCrew().crew().kickoff(inputs=inputs)

    agentops.end_session("Success")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "ticker": "NVDA"
    }
    try:
        CrewAiStockAnalysisCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CrewAiStockAnalysisCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "ticker": "NVDA"
    }
    try:
        CrewAiStockAnalysisCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
