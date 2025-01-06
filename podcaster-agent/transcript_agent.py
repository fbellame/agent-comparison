from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from VideoSurfer import VideoSurfer
from dotenv import load_dotenv
import asyncio
from autogen_agentchat.agents import AssistantAgent
from tools import read_file, write_file

load_dotenv()

async def main() -> None:

    # Define an agent for blog writing
    transcript_agent = AssistantAgent(
        name="Planner",
        system_message="You are the transcripter of a team, a video surfer agents and a file system agent. Please plan carefully in order to generate a high quality english transcript file from the provided video",
        description="A helpful assistant that can transcript a video.",
        model_client=OpenAIChatCompletionClient(model="gpt-4o-mini"),
        tools=[read_file, write_file]
        )    

    # Define an agent for video access
    video_agent = VideoSurfer(
        name="VideoSurfer",
        model_client=OpenAIChatCompletionClient(model="gpt-4o-mini")
        )


    # Define termination condition
    termination = TextMentionTermination("TERMINATE")

    # Define a team
    agent_team = RoundRobinGroupChat([transcript_agent, video_agent], termination_condition=termination)

    # Run the team and stream messages to the console
    prompt = """
        Fait une transcription complete et traduit en anglais 
        Audio: /media/farid/data1/projects/agent-comparison/podcaster-agent/video/agent-final-comp.mp3
    """

    stream = agent_team.run_stream(task=prompt)
    await Console(stream)

if __name__ == "__main__":
    asyncio.run(main())