from dotenv import load_dotenv
from agency_swarm import Agency
from content_strategist import content_strategist
from content_creator import content_creator
from visual_designer import visual_designer
from hashtag_researcher import hashtag_researcher

import asyncio

load_dotenv()

# do not remove this method, it is used in the main.py file to deploy the agency (it has to be a method)
def create_agency(load_threads_callback=None):
    agency = Agency(
        content_strategist,  # Entry point for user communication
        communication_flows=[
            (content_strategist, content_creator),
            (content_creator, visual_designer),
            (content_creator, hashtag_researcher),
            (visual_designer, content_creator),
            (hashtag_researcher, content_creator),
        ],
        name="ContentPlanningAgency",
        shared_instructions="shared_instructions.md",
        load_threads_callback=load_threads_callback,
    )

    return agency

if __name__ == "__main__":
    agency = create_agency()

    # test 1 message
    # async def main():
    #     response = await agency.get_response("Hello, how are you?")
    #     print(response)
    # asyncio.run(main())

    # run in terminal
    agency.terminal_demo()