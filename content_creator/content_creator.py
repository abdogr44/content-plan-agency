from agents import ModelSettings
from agency_swarm import Agent
from openai.types.shared import Reasoning

content_creator = Agent(
    name="Content Creator",
    description="Generates detailed daily content posts including titles, captions, and coordinates with Visual Designer and Hashtag Researcher for complete content creation.",
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
