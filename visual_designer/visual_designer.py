from agents import ModelSettings
from agency_swarm import Agent
from openai.types.shared import Reasoning

visual_designer = Agent(
    name="Visual Designer",
    description="Creates specific design suggestions and visual concepts for each content post, ensuring visual elements align with brand identity and platform best practices.",
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
