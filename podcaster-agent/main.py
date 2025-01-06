from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from VideoSurfer import VideoSurfer
from dotenv import load_dotenv
import asyncio
from autogen_agentchat.agents import AssistantAgent

load_dotenv()

async def main() -> None:

    # Define an agent for blog writing
    planner_agent = AssistantAgent(
        name="Planner",
        system_message="You are the planner of a team of a blogger and a video surfer agents. Please plan carefully in order to generate a high quality blog post from the provided video",
        description="A helpful assistant that can plan the writing of a blog.",
        model_client=OpenAIChatCompletionClient(model="gpt-4o-mini")
        )    

    # Define an agent for video access
    video_agent = VideoSurfer(
        name="VideoSurfer",
        model_client=OpenAIChatCompletionClient(model="gpt-4o-mini")
        )


    # Define an agent for blog writing
    blogger_agent = AssistantAgent(
        name="Blogger",
        system_message="You are an English blogger, you will use VideoSurfer if required to extract information for the blog you will write",
        description="A helpful assistant that can write a blog post.",
        model_client=OpenAIChatCompletionClient(model="gpt-4o-mini")
        )

    # Define termination condition
    termination = TextMentionTermination("TERMINATE")

    # Define a team
    agent_team = RoundRobinGroupChat([planner_agent, blogger_agent, video_agent], termination_condition=termination)

    # Run the team and stream messages to the console
    prompt = """
        Fait une transcription complete et traduit en anglais la vidéo
        Vidéo: /media/farid/data1/projects/agent-comparison/podcaster-agent/video/Agent-Comp - CrewAI.mp4
    """

    stream = agent_team.run_stream(task=prompt)
    await Console(stream)

if __name__ == "__main__":
    asyncio.run(main())