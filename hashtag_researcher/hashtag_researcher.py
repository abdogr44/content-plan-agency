from agents import ModelSettings
from agency_swarm import Agent
from openai.types.shared import Reasoning

hashtag_researcher = Agent(
    name="Hashtag Researcher",
    description="Researches and recommends optimal hashtag strategies for each platform, combining popular and niche hashtags to maximize reach and engagement.",
    instructions="./instructions.md",
    tools_folder="./tools",
    files_folder="./files",
    model="gpt-5",
    model_settings=ModelSettings(
        reasoning=Reasoning(
            effort="medium",
            summary="auto",
        ),
    ),
)
