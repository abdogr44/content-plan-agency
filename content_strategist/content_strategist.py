from agents import ModelSettings
from agency_swarm import Agent
from openai.types.shared import Reasoning

content_strategist = Agent(
    name="Content Strategist",
    description="Primary interface for content planning agency. Collects business information, analyzes requirements, and coordinates comprehensive content strategy development.",
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
