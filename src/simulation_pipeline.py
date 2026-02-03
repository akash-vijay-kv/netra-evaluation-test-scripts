import asyncio
import os
from netra import Netra
from dotenv import load_dotenv
load_dotenv()


async def main():


    headers = f"x-api-key={os.getenv('NETRA_API_KEY')}"
    Netra.init(app_name="Simulation Pipeline", headers=headers, debug_mode=True)

    """
    Simulation Based Evaluation
    --------------------------------------------------
    """

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # 1. Milestone Agent
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    from milestone_agent_wrapper import MilestoneAgent

    Netra.simulation.run_simulation(
        name="Milestone Agent v1",
        dataset_id="06f94894-0a1f-4062-a978-a739866f9b16",
        context={"Metadata": "Customer Support"},
        task=MilestoneAgent(),
    )


    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # 2. Customer Service Agent (Refund)
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    # from customer_service_agent import CustomerServiceBot

    # Netra.simulation.run_simulation(
    #     name="Customer Service Agent (Refund) v1",
    #     dataset_id="06f94894-0a1f-4062-a978-a739866f9b16",
    #     context={"Metadata": "Customer Support"},
    #     task=CustomerServiceBot(),
    # )


if __name__ == "__main__":
    asyncio.run(main())
